from header_utilsA2 import format_message, LENGTH_HEADER_SIZE, USER_HEADER_SIZE, ADDRESSING_HEADER_SIZE, TYPE_HEADER_SIZE
import select
import socket

IP = '127.0.0.1'
PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(10)

print (f'Listeing on {IP}:{PORT}')
all_sockets = [server_socket]
all_addresses = []

def arrive(address):
    for sockets in all_sockets:
        message = f'ONL{address}'
        sockets.send(message.encode('utf-8'))

def offline(address):
    for sockets in all_sockets:
        message = f'OFF{address}'

def routing():
    addressierung = client_socket.recv(ADDRESSING_HEADER_SIZE)
    addressierung = addressierung.decode('utf-8').strip()
    if addressierung == "Gruppe":
        return 'group'
    else:
        return addressierung
    
    
def receive(client_socket, mes_type, empfaenger):
    size_header = client_socket.recv(LENGTH_HEADER_SIZE)
    if not size_header:
        return None
    size_header = size_header.decode('utf-8')
    message_size = int(size_header.strip())

    user_header = client_socket.recv(USER_HEADER_SIZE).decode('utf-8')
    user = user_header.strip()        
    message = client_socket.recv(message_size).decode('utf-8')

    print (f'{user} > {message} an {empfaenger}')    
    return f'{mes_type}{size_header}{user_header}{message}'

def broadcast(sender, message):
    for socket in all_sockets:                
        if socket != sender and socket != server_socket:            
            socket.send(message.encode('utf-8'))

def weiterleiten(empfaenger, nachricht, sender):
    if empfaenger == "group":
        broadcast(sender, nachricht)
    else:
        empfaenger.send(nachricht.encode('utf-8'))

while True:
    read_sockets, _, error_sockets = select.select(all_sockets, [], all_sockets)        
    for socket in read_sockets:
        if socket == server_socket:            
            client_socket, client_address = server_socket.accept()            
            all_sockets.append(client_socket)
            all_addresses.append(client_address) 
            arrive(client_address)
            #broadcast an alle clients mit bestimmter flag beinhaltet client socket und
            #client address dass der neue client online ist
            print(f'Established connection to {client_address[0]}:{client_address[1]}')

        else:
            try:
                message_type = socket.recv(TYPE_HEADER_SIZE)
                if message_type == 'MES':
                    index_socket = all_sockets.index(socket)-1
                    sender = all_addresses[index_socket]
                    address = routing()
                    message = receive(socket, message_type, address)
                    if not message or address:
                        print(f'{client_socket.getpeername()[0]}:{client_socket.getpeername()[1]} closed the connection')
                        all_sockets.remove(socket)
                        offline(socket)
                        #braodcast an alle dass dieser client offline ist
                        continue
                    weiterleiten(address, message, sender)
                    
                elif message_type == 'USR':
                    message = receive(socket, message_type)
                    broadcast(socket, message)

            except ConnectionResetError as e:
                all_sockets.remove(socket)
                #braodcast an alle dass dieser client offline ist
                offline(socket)
                print('Client forcefully closed the connection')

    for error_socket in error_sockets:
        all_sockets.remove(error_socket)


