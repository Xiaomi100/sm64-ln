from PySimpleGUI import *
import os
import subprocess

mainwin = [[Text('SM64-LN - A modern launcher.')],
           [Text('Welcome to SM64-LN - new launcher!')],
           [Button('Ok', key=('procid1'))]]
select = [[Text('1. Write information about Port')],
          [Text('Name of port(need to be same as name of port):'), Input()],
          [Text('Link to port:'), Input()],
          [Text('Branch(leave blank to default)'), Input()],
          [Button('Ok', key='procid2')]]
build = [[Text("BUILDING! DON'T CLOSE THE APPEARED WINDOWS!")]]
fail = [[Text('Build failed! Try again later...')]]

msys2 = popup_get_folder('To proceed, select MSYS2 folder.')
msys2folder = msys2
window = Window('SM64-LN', mainwin)

def run(command):
        return subprocess.run(
            [
                msys2folder+"/usr/bin/bash.exe",
                "--login",
                "-c",
                command,
            ],
            encoding="utf-8",
            env={**os.environ, "MSYSTEM": "MINGW64", "CHERE_INVOKING": "yes"},
        ).returncode

while True:
    event, values = window.read()
    
    if event == WINDOW_CLOSED or event == 'procid1':
        window.close()
        window = Window('SM64-LN', select)
        while True:
            event, values = window.read()
            if event == 'procid2':
                name = values[0]
                link = values[1]
                branch = values[2]
                if name != '' or link != '':
                    window.close()
                    rom = popup_get_file('Select ROM(ONLY US)')
                    romn = rom
                    window = Window('SM64-LN: Building...', build)
                    if branch == '':
                        run('git clone ' + link)
                    else:
                        run('git clone ' + link + '-b=' + branch)
                    slash = chr(92)
                    dirf = '$PWD'
                    dirfw = '%cd%'
                    run('cp ' + romn + " "+ dirf + '/' + name + '/baserom.us.z64')
                    run('cd ' + name + ' && make')
                    if os.path.exists(dirfw + '/' + name + '/build/us_pc/sm64.us.f3dex2e.exe') == False:
                        fl = Window('BUILD FAILED', fail)
                    else:
                        os.system(dirfw + '/' + name + '/build/us_pc/sm64.us.f3dex2e.exe')