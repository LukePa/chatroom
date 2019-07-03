import socket, threading, servercommands

#port the chatroom runs on
PORT = 6789
TIMEOUTTIME = 0.5


class Client(object):
    """Represents clients connecting to the server"""
    def __init__(self, sock, address, username, server):
        """sock is socket object for specific client, username is string"""
        self._sock = sock
        self._address = address
        self._username = username
        self._recieverThread = threading.Thread(target=self.recieverThreadMethod,
                                                args=(server,))
        self._killThread = False

    def getUsername(self):
        return self._username

    def getAddress(self):
        return self._address

    def disconnect(self):
        self._killThread = True
        self._sock.close()

    def startThread(self):
        self._recieverThread.start()

    def sendMessage(self, message):
        """message is a string to be sent to client"""
        if type(message) == str:
            message = message.encode()
        if type(message) == bytes:
            self._sock.sendall(message)

    def recieveMessage(self):
        try:
            message = self._sock.recv(4096)
            while not message:
                message += self._sock.recv(4096)
            return message
        except ConnectionResetError:
            return "/leave"

    def recieverThreadMethod(self, server):
        while not self._killThread:
            message = self.recieveMessage()
            server.messageHandler(self, message)
            
            
        
class Server(object):
    """Represents server"""
    def __init__(self):
        self._clientList = []
        self._CommandStructure = servercommands.CommandStructure()
        self._serversock = socket.socket()
        self._serversock.bind(("", PORT))
        self._serversock.listen(10)
        self._serversock.settimeout(TIMEOUTTIME)
        print("Server has started...")

    def broadcast(self, message):
        """Send a message to all clients"""
        if type(message) != bytes:
            message = message.encode()
        print("Broadcasting: ", message)
        for client in self._clientList:
            client.sendMessage(message)

    def addNewClients(self):
        """Check if client wants to join and adds them to clientList"""
        while True:
            try:
                conn, addr = self._serversock.accept()
                usernameBytes = conn.recv(1024)
                username = usernameBytes.decode()
                print(addr, " has connected, username: ", username)
                client = Client(conn, addr, username, self)
                introMessage = """
################################
# Welcome to the chatroom!     #
# Type to talk and enter /help #
# for command list             #
################################
"""
                client.sendMessage(introMessage.encode())
                joinMessage = username + " has joined the server!"
                self._clientList.append(client)
                self.broadcast(joinMessage)
                client.startThread()
            except socket.timeout:
                continue

    def disconnectClient(self, client):
        client.disconnect()
        self._clientList.remove(client)
        message = client.getUsername() + " has disconnected."
        self.broadcast(message.encode())


    def messageHandler(self, client, message):
        if type(message) == bytes:
            message = message.decode()
        if message[0] == "\\" or message[0] == "/":
            self._CommandStructure.processMessage(self, client, message)
        else:
            username = client.getUsername()
            formattedName = username + "> "
            formattedMessage = formattedName + message
            self.broadcast(formattedMessage.encode())
            
            
            
def main():
    server = Server()
    server.addNewClients()
    

if __name__ == "__main__":
    main()
