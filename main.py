from asyncio import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

import subprocess
from os import environ

class Terminal_Runner(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, RunCommand())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):

        command = event.get_argument()

        if command == None: 

            command = ""


        data = { "command": command }

        return RenderResultListAction([ExtensionResultItem(icon="images/icon.png",
                                                           name="Run %s" %command,
                                                           on_enter=ExtensionCustomAction(data))])


class RunCommand(EventListener):

    def on_event(self, event, extension):

        data = event.get_data()
        
        terminal = extension.preferences["term"]
        exec = extension.preferences["exec"]
        command = data["command"]

        userShell = environ["SHELL"]


        subprocess.run( [f'{terminal} {exec} {userShell} -c "{command}; {userShell}"'], shell=True )

        return HideWindowAction()



if __name__ == '__main__':
    Terminal_Runner().run()