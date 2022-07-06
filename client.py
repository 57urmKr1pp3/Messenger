import socket
import errno
import sys


from threading import Thread

from header_utilsA2 import LENGTH_HEADER_SIZE, USER_HEADER_SIZE, ADDRESSING_HEADER_SIZE, TYPE_HEADER_SIZE, format_message
       
IP = '127.0.0.1'
PORT = 5555
chat_anzahl = 0
chat_partner = {}

def verbinden():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT)) 
    client_socket.setblocking(False)

def clientexit(message, username):
    message = format_message('MES',username, 'Signing out')
    client_socket.send(message.encode('utf-8'))
    client_socket.close
    sys.exit

def clientsend(message, username):
    formatted_message = format_message('MES',username, message).encode('utf-8')
    client_socket.send(formatted_message)

def clientusername(username):
    #lokale IP
    address = client_socket
    message = f'USR{address}{username}'
    client_socket.send(message.encode('utf-8'))

def receive():
    #erweiterung je nach flag
    try:
        message_type = client_socket.recv(TYPE_HEADER_SIZE)

        if message_type == 'MES':            
            message_size = client_socket.recv(LENGTH_HEADER_SIZE)
            message_size = int(message_size.decode('utf-8').strip())
            sender = client_socket.recv(USER_HEADER_SIZE).decode('utf-8').strip()
            message = client_socket.recv(message_size).decode('utf-8')
            return f'{sender} > {message}'

        elif message_type == 'ONL':
            ip = client_socket.recv(ADDRESSING_HEADER_SIZE)
            ip = ip.decode('utf-8')
            print(f'Client{ip} ist online')

        elif message_type == 'OFF':
            ip = client_socket.recv(ADDRESSING_HEADER_SIZE)
            ip = ip.decode('utf-8')
            print(f'Client{ip} ist offline')
            chat_partner.pop(ip)

        elif message_type == 'USR':
            ip = client_socket.recv(ADDRESSING_HEADER_SIZE)
            usr = client_socket.recv(USER_HEADER_SIZE)
            usr = usr.decode('utf-8')
            ip = ip.decode('utf-8')
            #dictionary hinzufügen
            chat_partner[ip]=usr

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Encountered error while reading', e)
            client_socket.close()
            sys.exit()

    except Exception as e:
        client_socket.close()
        sys.exit()
        

#Müll
#_________________________________________________________________
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#|
client_socket.connect((IP, PORT))                                #|
client_socket.setblocking(False)                                 #|
#_________________________________________________________________|

