from socket import *
import threading
from datetime import datetime

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"{GREEN}[{datetime.now().strftime('%H:%M:%S')}] Server listening on {HOST}:{PORT}{RESET}\n")

def handle_client(client_sock, client_addr):
    print(f"{YELLOW}[{datetime.now().strftime('%H:%M:%S')}] New connection from {client_addr}{RESET}")
    while True:
        try:
            message_bytes = client_sock.recv(2048)
            if not message_bytes:
                break
            message = message_bytes.decode("utf-8")
            print(f"{GREEN}[{datetime.now().strftime('%H:%M:%S')}] {client_addr} says: {message}{RESET}")

            reply = input(f"{YELLOW}Reply to {client_addr}: {RESET}")
            client_sock.send(reply.encode("utf-8"))
        except ConnectionResetError:
            print(f"{RED}[{datetime.now().strftime('%H:%M:%S')}] {client_addr} disconnected abruptly.{RESET}")
            break
    client_sock.close()
    print(f"{RED}[{datetime.now().strftime('%H:%M:%S')}] {client_addr} disconnected.{RESET}\n")

while True:
    client_sock, client_addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_sock, client_addr), daemon=True).start()
