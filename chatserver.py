import socket

#port the chatroom runs on
PORT = 6789
TIMEOUTTIME = 0.5


class Client(object):
    """Represents clients connecting to the server"""
    def __init__(self, sock, address, username):
        """sock is socket object for specific client, username is string"""
        self._sock = sock
        self._address = address
        self._sock.settimeout(TIMEOUTTIME)
        self._username = username

    def getUsername(self):
        return self._username

    def getAddress(self):
        return self._address

    def disconnect(self):
        self._sock.close()

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
        except socket.timeout:
            return None
        except ConnectionResetError:
            return "leave"
            


class Server(object):
    """Represents server"""
    def __init__(self):
        self._clientList = []
        self._serversock = socket.socket()
        self._serversock.bind((socket.gethostname(), PORT))
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
        try:
            conn, addr = self._serversock.accept()
            usernameBytes = conn.recv(1024)
            username = usernameBytes.decode()
            print(addr, " has connected, username: ", username)
            client = Client(conn, addr, username)
            introMessage = """
################################
# Welcome to the chatroom!     #
# Type to talk and enter /help #
# for command list (WIP)       #
################################
"""
            client.sendMessage(introMessage.encode())
            joinMessage = username + " has joined the server!"
            self._clientList.append(client)
            self.broadcast(joinMessage)
        except socket.timeout:
            return None

    def disconnectClient(self, client):
        if client in self._clientList:
            client.disconnect()
            self._clientList.remove(client)
            message = client.getUsername() + " has disconnected."
            self.broadcast(message.encode())

    def checkNewMessages(self):
        """Checks if anyone has entered a message and broadcasts it"""
        for client in self._clientList:
            messageBytes = client.recieveMessage()
            if messageBytes == "leave":
                self.disconnectClient(client)
            elif messageBytes != None:
                print("Message recieved from ", client.getAddress())
                message = messageBytes.decode()
                formatted = client.getUsername() + "> " + message
                formattedBytes = formatted.encode()
                self.broadcast(formattedBytes)


def main():
    server = Server()
    while True:
        server.addNewClients()
        server.checkNewMessages()
    

if __name__ == "__main__":
    main()
