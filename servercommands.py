


class Command(object):
    """This is intended to be used as an abstract class"""
    def __init__(self):
        self._trigger = ""
        self._helpInfo = """
Placeholder Info
"""

    def getTrigger(self):
        return self._trigger

    def getHelpInfo(self):
        return self._helpInfo

    def action(self, server, client, args):
        return None

    
class Leave(Command):
    def __init__(self):
        self._trigger = "leave"
        self._helpInfo = """
Makes you leave the server
"""

    def action(self, server, client, args):
        client.sendMessage(b"You are disconnected")
        server.disconnectClient(client)



class CommandStructure(object):
    """Keeps track of commands"""
    def __init__(self):
        #Add commands to command list to add them to chat service,
        #must be subclasses of Command obj
        self._commandList = [Leave()]
        self._commandDict = {}
        for command in self._commandList:
            self._commandDict[command.getTrigger()] = command


    def processMessage(self, server, client, message):
        if message[0] == "/" or message[0] == "\\":
            message = message[1:]
        args = message.split(" ")
        if args[0].lower() == "help":
            self.helpMessage(client, args)
        else:
            for trigger in self._commandDict.keys():
                if trigger == args[0]:
                    self._commandDict[trigger].action(server,client,args)
                    return None
            client.sendMessage(b"Sorry, command is invalid")


    def helpMessage(self, client, args):
        helpResponce = ""
        if len(args) == 1:
            helpResponce += "Type /{command} to execute command.\n"
            helpResponce += "Type '/help {command}' for help with specific command.\n"
            helpResponce += "The following is a command list.\n"
            for trigger in self._commandDict.keys():
                helpResponce += "+ " + trigger + "\n"
        else:
            if args[1].lower() in self._commandDict.keys():
                helpResponce = self._commandDict[args[1]].getHelpInfo()
            else:
                helpResponce = "Sorry, command is invalid"
        client.sendMessage(helpResponce.encode())
        
        
        
