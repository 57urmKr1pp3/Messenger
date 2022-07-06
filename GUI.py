import sys
import tkinter as tk
from threading import Thread
from tkinter import messagebox
from tkinter.font import NORMAL
from client import client_socket, verbinden, clientexit, clientsend, receive, clientusername
from datetime import datetime
from header_utilsA2 import format_message

def name_get():
#    print(user_input.get())
    return user_input.get()

def message_input_get():
    return message_input

def print_message(message):
    chat_log.configure(state=NORMAL)
    chat_log.insert(tk.END, message)
    chat_log.configure(state=tk.DISABLED)

def lock_username():
    if user_input.get():
#       print(user_input.get())
        message_input.configure(state=NORMAL)
        send_button.configure(state=NORMAL)
        user_input.configure(state=tk.DISABLED)
        user_input_button.configure(state=tk.DISABLED)
        clientusername(user_input.get())
    else:
        messagebox.showinfo('Error', 'Please enter a username!')

def send():
    username = name_get()
    message = message_input.get()
    if message == '[exit]':
        print_message('\nSigned out')
        clientexit(message, username)
        
    elif message:
        print_message(f'\n<{current_time}> {username} > {message}')
        clientsend(message, username)
        message_input.delete(0, tk.END)

def loop_receive():
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        message = receive()
        if message: 
            print_message(f'<{current_time}> {message}')

#erstellen aller fenster
#Receive
receive_thread = Thread(target = loop_receive)


#Zeit
#https://www.stackvidhya.com/how-to-get-current-time-in-python/#:~:text=You%20can%20use%20the%20below,get%20only%20the%20time%20information.&text=When%20you%20print%20the%20current_time,24H%20format%20as%20shown%20below.
now = datetime.now()
current_time = now.strftime("%H:%M")
#Fenster
window = tk.Tk()
window.title("Messenger")
window.geometry("950x550")

#Transparenz
window.attributes('-alpha', 1)

chats = tk.Listbox(window, width = 20, height = 29)
chats.place(x = 0, y = 30)


#Username

user_label = tk.Label(window, text='Username')
user_label.place(x = 30, y = 3)
user_input = tk.Entry(window, width = 110)
user_input.place(x = 129, y = 5)

user_input_button = tk.Button(window, width = 18, text = 'Confirm', bg='lightgrey', command=lock_username)
user_input_button.place(x = 799, y = 2)


#chat fenster
chat_log = tk.Text(window, width=100, height=29, state = tk.DISABLED)
chat_log.place(x=130, y=30)


#message teil

message_label = tk.Label(window, text='Message')
message_label.place(x=30, y=505)
message_input = tk.Entry(window, width=110, state=tk.DISABLED)
message_input.place(x=130, y=505)

#sendebutton


send_button = tk.Button(window, width=19, text='Send', bg='white', state=tk.DISABLED, command=send)
send_button.place(x=799, y=503)

#print(message_input)

#Ausfuehrung
verbinden()
receive_thread.start()
window.mainloop()