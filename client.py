import socket
import threading
import tkinter as tk

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 12345

# connect to the server
client_socket.connect((host, port))

# function to send a message to the server
def send_message(event=None):
    message = message_entry.get()
    message_entry.delete(0, tk.END)
    client_socket.send(message.encode('utf-8'))

# function to handle incoming messages
def handle_messages():
    while True:
        try:
            # receive data from the server
            data = client_socket.recv(1024)
            # display the received data in the message list
            message_list.insert(tk.END, data.decode('utf-8'))
        except:
            break

# create the user interface
root = tk.Tk()
root.title("Chat Client")

# message list
message_list = tk.Listbox(root)
message_list.pack()
message_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# message entry
message_entry = tk.Entry(root)
message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
message_entry.focus_set()

# send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

# bind the message entry to the "Return" key to send the message
root.bind('<Return>', send_message)

# create a new thread to handle incoming messages from the server
message_thread = threading.Thread(target=handle_messages)
message_thread.start()

# start the GUI main loop
root.mainloop()

# close the socket connection when the GUI is closed
client_socket.close()
