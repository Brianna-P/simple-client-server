from socket import *
import threading
from datetime import datetime

CYAN = "\033[96m"
MAGENTA = "\033[95m"
RED = "\033[91m"
RESET = "\033[0m"

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

client_socket = socket(AF_INET, SOCK_STREAM)
print(f"{CYAN}[{datetime.now().strftime('%H:%M:%S')}] Connecting to {SERVER_HOST}:{SERVER_PORT}...{RESET}")
client_socket.connect((SERVER_HOST, SERVER_PORT))
print(f"{CYAN}[{datetime.now().strftime('%H:%M:%S')}] Connected! Type 'exit' to quit.{RESET}\n")

def receive_messages(sock):
    while True:
        try:
            message_bytes = sock.recv(2048)
            if not message_bytes:
                print(f"{RED}[{datetime.now().strftime('%H:%M:%S')}] Server closed the connection.{RESET}")
                break
            message = message_bytes.decode("utf-8")
            print(f"\n{MAGENTA}[{datetime.now().strftime('%H:%M:%S')}] Server says: {message}{RESET}")
        except ConnectionResetError:
            print(f"{RED}[{datetime.now().strftime('%H:%M:%S')}] Server disconnected abruptly.{RESET}")
            break

threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

while True:
    msg = input(f"{CYAN}You: {RESET}")
    if msg.lower() == "exit":
        print(f"{RED}Disconnecting... Bye!{RESET}")
        break
    client_socket.send(msg.encode("utf-8"))

client_socket.close()
