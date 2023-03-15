import socket
import threading
import tkinter as tk

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 12345

# bind the socket to a public host, and a port
server_socket.bind((host, port))

# set the server to listen for incoming connections
server_socket.listen(5)

# list to hold all client connections
clients = []

# function to handle incoming messages from a client
def handle_client(client_socket):
    while True:
        try:
            # receive data from the client
            data = client_socket.recv(1024)
            # send the received data to all other connected clients
            for client in clients:
                if client != client_socket:
                    client.send(data)
            # display the received data in the message list
            message_list.insert(tk.END, data.decode('utf-8'))
        except:
            # if there is an error, remove the client from the list of clients
            clients.remove(client_socket)
            break

# function to continuously accept incoming connections
def accept_connections():
    while True:
        # accept a new connection
        client_socket, addr = server_socket.accept()
        # add the new client to the list of clients
        clients.append(client_socket)
        # notify the server that a new client has connected
        message_list.insert(tk.END, f"{addr} has connected")
        # create a new thread to handle incoming messages from the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# create the user interface
root = tk.Tk()
root.title("Chat Server")


# message list
message_list = tk.Listbox(root)
message_list.pack()
message_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# message entry
message_entry = tk.Entry(root)
message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
message_entry.focus_set()


# send button
send_button = tk.Button(root, text="Send", command=lambda: send_message(message_entry.get()))
send_button.pack(side=tk.RIGHT)

# function to send a message to all clients
def send_message(message):
    # send the message to all clients
    for client in clients:
        client.send(message.encode('utf-8'))
    # display the message in the message list
    message_list.insert(tk.END, f"You: {message}")
    # clear the message entry
    message_entry.delete(0, tk.END)

# start accepting connections
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

# start the GUI main loop
root.mainloop()
