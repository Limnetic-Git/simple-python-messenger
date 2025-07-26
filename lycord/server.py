import socket, os
from _thread import *

accounts = []
chats = [[]]

ServerSocket = socket.socket()
host, port = '127.0.0.2', 1234 
ThreadCount = -1 
try:
    ServerSocket.bind((host, port))
    print('Сервер в сети!')
except socket.error as e:
    print(str(e))


ServerSocket.listen(100) 
def threaded_client(connection):
    connection.send(str.encode(str(ThreadCount))) 
    nick = str(connection.recv(20480).decode('utf-8'))

    accounts.append([ThreadCount, nick]) 
     
    this_client_id = ThreadCount
    this_client_account = accounts[this_client_id]
    
    connection.send(str.encode(str(chats[0]))) 
    while True: 

        log = eval(connection.recv(20480).decode('utf-8'))
        if log != None:
            log['id'] = len(chats[0])
            chats[0].append(log)

            
        connection.send(str.encode(str(chats[0][-3:]))) 

while True:
    Client, address = ServerSocket.accept() 
    print('Connected to: ' + address[0] + ':' + str(address[1])) 
    print(type(Client))
    ThreadCount += 1
    start_new_thread(threaded_client, (Client,))
    
    print('Thread Number: ' + str(ThreadCount)) 
ServerSocket.close()
