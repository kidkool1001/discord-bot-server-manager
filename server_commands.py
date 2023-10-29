import subprocess
import os
from pywinauto import application


def start_server(game):
    """Starts server when given a game object"""
    script_name = game.start_script
    game.server_process = os.startfile(script_name)
    print(f'Starting {game.title} server process')
    
    


def stop_server(game):
    """Communicates with server process to stop server when given a game object"""
    app = application.Application()
    app.connect(title=game.window)
    dlg = app.top_window()
    dlg.type_keys(game.exit_command)
    
    # print(f'Attempting to stop {game.title} server process')
    # game.server_process.communicate(str.encode(game.exit_command))


