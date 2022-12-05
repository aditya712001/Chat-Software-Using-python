# server 
# client.send() -> server sends message to a specific client 
# client.recv(1024) -> server requests message from a specific client 
# broadcast -> server sends message to all connected  clients

import socket
import threading 
import sqlite3
import os

# HOST = socket.gethostbyname(socket.gethostname())
HOST = "127.0.0.1"
PORT = 9000

SEPARATOR = '<SEPARATOR>'
ENDTAG = '<ENDTAG>'
MSG_DELIMITER = '\!?^'
# ALL_USERS = '<%All%>'

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
    
            # if message[0]=='#':
            #     filedata=message
            #     while len(filedata)>1 and filedata[-1]!='#':
            #         filedata+=str(client.recv(1024).decode('ascii'))
            #     print(filedata)
            #     broadcast(filedata.encode('ascii'))
            if SEPARATOR in message: # File transfer
                print("Received a file")
                # message contains filename and filesize separated by separator
                filename, from_user = message.split(SEPARATOR, 1)
                # to_user_name = 'ALL'
                # server data storage:
                server_data = 'server_data'
                if not os.path.exists(server_data):
                    os.makedirs(server_data)
                # for file in list(os.listdir(server_data)):
                #     os.remove(os.path.join(server_data, file))
                file_byte_info = from_user.split(MSG_DELIMITER)
                filepath = os.path.join(server_data, file_byte_info[0]+ '@' +  filename)
                f = open(filepath, 'wb')
                print(file_byte_info)
                file_bytes = b''
                if len(file_byte_info) > 1:
                    file_bytes += (file_byte_info[1].encode('utf-8'))#ascii

                while 1:
                    if file_bytes.endswith(ENDTAG.encode('utf-8')):#ascii
                        break
                    data = client.recv(1024)
                    file_bytes += data

                f.write(file_bytes[:-len(ENDTAG)])
                f.close()

                print('Saved a file to server')
                # File transfer:
                send_msg =  file_byte_info[0]+ ': Sent file - ' + os.path.basename(filename)+'\n'
                rec_msg =   file_byte_info[0] + ': You received a file -' + os.path.basename(filename)+'\n' 
                
                for tou in nicknames:
                    if tou.decode('utf-8') == file_byte_info[0]:
                        continue
                    
                    index=nicknames.index(tou)
                    message = rec_msg
                    clients[index].sendall(message.encode('utf-8'))#nothing
                    
                    # message = from_user + '~' + rec_msg
                    # client_id[tou].sendall(message.encode())  # message format: "sender~message"

                    # File transfer:
                    clients[index].sendall(f"{os.path.basename(filename)}{SEPARATOR}{file_byte_info[0]}{MSG_DELIMITER}".encode('utf-8'))#nothing

                    f = open(filepath, 'rb')
                    data = f.read()
                    clients[index].sendall(data)
                    clients[index].sendall(ENDTAG.encode('utf-8'))#ascii
                    f.close()
                            
                message = send_msg
                index=nicknames.index(file_byte_info[0].encode('utf-8'))
                clients[index].sendall(message.encode('utf-8'))#nothing
                
            elif(message[0] == '~'):
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
