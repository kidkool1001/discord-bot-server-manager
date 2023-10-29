import discord
from discord.ext import tasks
from discord.ext import commands
import subprocess
import asyncio
import json
from pywinauto import application
import server_commands as server_command
#Defines discord client, can change command prefix here
intents = discord.Intents.all()
client = discord.Bot(help_command=commands.DefaultHelpCommand(), intents=intents)
#Loads user config and defines variabels
with open('bot_config.json') as f:
    config = json.load(f)

class Game:
    def __init__(self, title, port, window, query, exit_command):
        self.port = port
        self.title = title
        self.window = window
        self.active = False
        self.has_query = query
        self.exit_command = exit_command
        self.start_script = '.\\servers\\' + self.title + '.lnk'
    
    def start_server(self):
        print(f'Starting {self.title} server')
        server_command.start_server(self)

    def stop_server(self):
        print(f'Stopping {self.title} server')
        server_command.stop_server(self)

game_library = {}
for title, info in config['game_library'].items():
    port = info [0]
    window = info [1]
    if info[2]:
        query_enabled = True
    else:
        query_enabled = False
    exit_command = info[3]
    game_library[title] = Game(title, port, window, query_enabled, exit_command)

bot_token = config['bot_token']
public_ip = config['public_ip']

#Sends message to console upon loading in and sets listening status for bot
@client.event
async def on_ready():
    """Sends ready message and sets listening status"""
    print(f'Logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/serverhelp"))
    restart_active.start()
    
async def game_starters(ctx: discord.AutocompleteContext):
    active_games = []
    for title, game in game_library.items():
            active_games.append(game.title)
    return active_games
    
async def game_stoppers(ctx: discord.AutocompleteContext):
    active_games = []
    for title, game in game_library.items():
        if game.active:
            active_games.append(game.title)
    return active_games
   
@tasks.loop(seconds=10)  
async def restart_active():
    try:
        for title, game in game_library.items():
            if game.active:
                app = application.Application()
                app.connect(title=game.window)
      #DEBUG    print(f' {game.title} Server is running...')
            else:
                await asyncio.sleep(10)
    except:
            print(f'ERROR! {game.title} Server crashed restarting...')
            restart_error()
            game.start_server()
    
@client.command(name="start", description="Starts server for the given game")
async def start(ctx: discord.ApplicationContext, game_title: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(game_starters))):
    try:
        game = game_library[game_title]
        if game.active:
            await ctx.respond(f'ERROR! {game.title} server already running')
        else:
            await ctx.respond(f'Starting {game.title} server')
            game.start_server()
            game.active = True
    except KeyError:
        await ctx.respond(f'ERROR! {game_title} is not supported or mistyped')

@client.command(description="Stops currently running server if there is one running")
async def stop(ctx: discord.ApplicationContext, game_title: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(game_stoppers))):
    try:
        game = game_library[game_title]
        if game.active:
            await ctx.respond(f'Stopping {game.title} Server!')
            game.stop_server()
            game.active = False
        else:
            await ctx.respond(f'ERROR! {game.title} is not currently running')
    except KeyError:
        await ctx.respond(f'ERROR! {game_title} is not supported or mistyped')

@client.command(description="How to use bot")
async def serverhelp(ctx: discord.ApplicationContext):
        help_embed = discord.Embed(title="Server Manager Help")
        command_names_list = [x.name for x in client.commands]
        game_names_list = [game.title for title, game in game_library.items]
        help_embed.add_field(name="Available Commands:", value="\n".join(x.name for i, x in enumerate(client.commands)), inline=False)
        help_embed.add_field(name="How to use", value="Type `/start or /stop <servername> to start or stop a server.", inline=False)
        await ctx.send(embed=help_embed)


@client.command(description="Checks the status of the currently running servers")
async def status(ctx):
    output = ''
    for title, game in game_library.items():
        if game.active:
            app = application.Application()
            app.connect(title=game.window)
            status = '**online**'
            if game.has_query:
                await ctx.respond(server_command.query_server(game))
        else:
            status = '**offline**'
        output = output + f'{game.title} server is currently {status} \n'
    await ctx.respond(output)

client.run(bot_token)
