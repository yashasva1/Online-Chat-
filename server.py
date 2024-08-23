import socket
import threading

# Connection Data
host = socket.gethostbyname(socket.gethostname())
port = 5050

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
            if message != '':
                print(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('sys : {} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        client.send('sys ` Connected to server!'.encode('ascii'))
        broadcast("sys ` {} joined!".format(nickname).encode('ascii'))

        # updating nickname and client list
        nicknames.append(nickname)
        clients.append(client)

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('The server is running.... ')
print('HOST : ', host)
print('PORT : ', port)
receive()
