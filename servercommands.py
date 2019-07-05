


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
        """All subclasses must override this and create their own"""
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


class BecomeAdmin(Command):
    def __init__(self):
        self._trigger = "becomeadmin"
        self._helpInfo = """
Become a server admin, must provide password like so '/becomeadmin {password}'
"""

    def action(self, server, client, args):
        if len(args) != 2:
            client.sendMessage(b"Incorrect format, must be /becomeadmin {password}")
            return None
        password = args[1]
        if password != server.getAdminPassword():
            client.sendMessage(b"Password is incorrect")
        elif password == server.getAdminPassword():
            if client.getAdmin() == True:
                client.sendMessage(b"You are already an admin")
            elif client.getAdmin() == False:
                client.setAdmin(True)
                client.sendMessage(b"You are now an admin")


class Kick(Command):
    def __init__(self):
        self._trigger = "kick"
        self._helpInfo = """
Kick user from chat service, must be an admin to use.
Type '/kick {username} to kick a user
"""

    def action(self, server, client, args):
        if client.getAdmin() != True:
            client.sendMessage(b"You must have admin permissions for this command")
            return None
        if len(args) != 2:
            client.sendMessage(b"Incorrect format, muse be '/kick {username}'")
            return None
        username = args[1]
        for user in server.getClientList():
            if user.getUsername() == username:
                kickMessage = username + " was kicked from the server!"
                server.broadcast(kickMessage.encode())
                server.disconnectClient(user)
                return None
        client.sendMessage(b"None in server with that username")
            


class CommandStructure(object):
    """Keeps track of commands"""
    def __init__(self):
        #Add commands to command list to add them to chat service,
        #must be subclasses of Command obj
        self._commandList = [Leave(), BecomeAdmin(), Kick()]
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
        
        
        
