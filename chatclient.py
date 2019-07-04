import socket, threading, sys

def connector(address, port, username):
    """Creates connection between client and server"""
    try:
        print("Connecting...")
        sock = socket.socket()
        sock.connect((address, port))
        sock.sendall(username.encode())
        sock.settimeout(10)
        print("Connected.")
        return sock
    except socket.timeout:
        input("Connection failed")
        sys.exit()


def sendMessage(message, sock):
    """Send message to serverm, message is a string"""
    try:
        sock.sendall(message.encode())
    except:
        return None


def reciever(sock):
    """Runs as thread, retrives message from server and  prints it"""
    while True:
        try:
            message = sock.recv(4096)
            while not message:
                message += sock.recv(4096)
            print(message.decode())
        except socket.timeout:
            continue
        except ConnectionResetError:
            sys.exit()


def sender(sock):
    """Retrieves message entered by client and sends it to server"""
    while True:
        try:
            message = input()
            sock.sendall(message.encode())
        except:
            continue

def enterDetails():
    address = input("Enter server address: ")
    port = input("Enter port: ")
    while not port.isdigit():
        port = input("Enter a valid port: ")
    port = int(port)
    username = input("Enter desired username: ")
    return address, port, username
            
        
def main():
    address, port, username = enterDetails()
    sock = connector(address, port, username)
    thread = threading.Thread(target = reciever, args = (sock,))
    thread.setDaemon(True)
    thread.start()
    sender(sock)

if __name__ == "__main__":
    main()
    
