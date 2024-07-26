import socket

SERVER_PORT = 8319  # Replace with the last 4-5 digits of your UM-ID
DEFAULT_MOTD = "An apple a day keeps the doctor away."
DEFAULT_PASSWORD = "123!abc"

def handle_client(client_socket):
    global message_of_the_day
    message_of_the_day = DEFAULT_MOTD

    while True:
        request = client_socket.recv(1024).decode().strip()

        if request == "MSGGET":
            response = "200 OK\n" + message_of_the_day + "\n"
            client_socket.send(response.encode())

        elif request == "MSGSTORE":
            client_socket.send("200 OK\n".encode())
            new_message = client_socket.recv(1024).decode().strip()
            message_of_the_day = new_message
            client_socket.send("200 OK\n".encode())

        elif request == "QUIT":
            client_socket.send("200 OK\n".encode())
            break

        elif request == "SHUTDOWN":
            client_socket.send("300 PASSWORD REQUIRED\n".encode())
            password = client_socket.recv(1024).decode().strip()
            if password == DEFAULT_PASSWORD:
                client_socket.send("200 OKAY\n".encode())
                client_socket.close()
                return True
            else:
                client_socket.send("301 WRONG PASSWORD\n".encode())

    client_socket.close()
    return False

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', SERVER_PORT))
    server_socket.listen(5)

    print(f"Server listening on port {SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        if handle_client(client_socket):
            break

    server_socket.close()
    print("Server shutdown.")

if __name__ == "__main__":
    main()