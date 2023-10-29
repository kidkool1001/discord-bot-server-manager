# discord-bot-server-manager
This is a discord bot that enables users in a discord server to easily start and stop various game servers such as minecraft and terraria.

ORIGINAL REPO : https://github.com/Phreakester/discord-bot-server-manager

Big thanks to @Phreakester
 
THIS IS WINDOWS ONLY IF YOU ARE LOOKING FOR LINUX VER GO HERE

https://github.com/Phreakester/discord-bot-server-manager

Requirements:
Windows computer

Ability to install requirements.txt
  
Knowledge of how to set up game servers & discord bots (view tutorials online)


Installation & Setup:
Create a new directory, place main_bot.py, server_commands.py, run.bat, bot_config_sample.json inside

Create a new discord project and corresponding bot, copy the bot key into the corresponding spot in bot_config.json(Keep the "")

Finish filling out bot_config.json, you may delete or add port items to fit what you need (game library uses python list synatx EX: ["No One Survived", "Zomboid"]

Download and setup the game servers in a different directory, and test to ensure that they work

Create the necessary shortcut files. They should be named with simply the game title EX: create a shortcut of however you launch the server, rename it whatever, put in server/ folder, 

Run main_bot.py and you should be up and running! Use the "/serverhelp" command in discord to see how to use the bot


NOTE:
this is still a wip 
