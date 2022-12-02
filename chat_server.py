# Problem The address is the local host address of the client, we want 
        # IPv4 Address. . . . . . . . . . . : 172.16.177.213
        # Subnet Mask . . . . . . . . . . . : 255.255.240.0
        # So we should assure that the ip addresses conected over LAN are unique ( Checking leave for later )

# Accounts

# sudeeprnp@gmail.com 
# pass -> 1234

# s@gmail.com 
# pass-> 1234

# a@gmail.com 
# pass-> 1234

# 1 
# pass-> 1

# server 
# client.send() -> server sends message to a specific client 
# client.recv(1024) -> server requests message from a specific client 
# broadcast -> server sends message to all connected  clients

# Client side 
# client.sock.send() -> a specific client sends message  to server ant then server broadcasts the message
# client.sock.recv() -> a specific client receives message from the server

import socket
import threading 
import sqlite3

# HOST = socket.gethostbyname(socket.gethostname())
HOST = "127.0.0.1"
PORT = 9000

sqlite3.connect('1.db')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen(100)

clients = []
nicknames = []
typing_users = []
# For broadcasting messages 
def broadcast(message):
    for client in clients:
        client.send(message)
    
def handle(client):
    while True:
        try:
            message = str(client.recv(1024).decode('utf-8'))
    
                
            if(message[0] == '~'):
                # message = ~nickname
                temp_list = message.split('~') 
                nontyping_user = '$' + temp_list[1] #$1
                temp_typing_users = set(typing_users)
                temp_typing_users.remove(nontyping_user)
                
                while nontyping_user in typing_users:
                    try:
                        typing_users.remove(nontyping_user)
                    except:
                        pass
                    
                type_string = ""
                for user_name in temp_typing_users:
                    type_string += user_name
                    
                if(type_string == ""):
                    type_string = '$' 
                broadcast(type_string.encode('utf-8'))
            elif(message[0] == '$'):
                typing_users.append(str(message))  #$1 
                temp_typing_users = set(typing_users)
                type_string = ""
                for user_name in temp_typing_users:
                    type_string += user_name
                print(type_string,'*****')
                
                broadcast(str(type_string).encode('utf-8'))    
            else:
                print(f"{nicknames[clients.index(client)]} says {message}")
                broadcast(message.encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            online_users= '@'
            
            for name in nicknames:
                online_users = online_users + str(name) + '@'
            # print(online_users)    
            broadcast(f"{online_users}".encode('utf-8'))

            break
    
    
# For receivng meessages 
def receive():
    while True:
        client,  address = server.accept()
        # Problem The address is the local host address of the client, we want 
        # IPv4 Address. . . . . . . . . . . : 172.16.177.213
        # Subnet Mask . . . . . . . . . . . : 255.255.240.0
        
        print(f"connected with {address}")
        
        # client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        
        nicknames.append(nickname)
        clients.append(client)
        
        print(f"nickname of the client is {nickname}")
        # broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
        online_users= '@'
        
        for name in nicknames:
            online_users = online_users + str(name) + '@'
        # print(online_users)    
        broadcast(f"{online_users}".encode('utf-8'))
        
        # client.send("Connected to the server".encode('utf-8'))
        thread = threading.Thread(target =handle , args = (client,))
        thread.start()

print("Server Running")
receive()
