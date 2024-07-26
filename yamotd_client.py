import socket

SERVER_PORT = 8319  # Should match the server's port

def main(server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, SERVER_PORT))

    while True:
        command = input("Enter command (MSGGET, MSGSTORE, QUIT, SHUTDOWN): ").strip()

        if command == "MSGGET":
            client_socket.send("MSGGET\n".encode())
            response = client_socket.recv(1024).decode()
            print("Server response:\n" + response)

        elif command == "MSGSTORE":
            client_socket.send("MSGSTORE\n".encode())
            response = client_socket.recv(1024).decode()
            if "200 OK" in response:
                new_message = input("Enter new message of the day: ").strip()
                client_socket.send((new_message + "\n").encode())
                response = client_socket.recv(1024).decode()
                print("Server response:\n" + response)

        elif command == "QUIT":
            client_socket.send("QUIT\n".encode())
            response = client_socket.recv(1024).decode()
            print("Server response:\n" + response)
            break

        elif command == "SHUTDOWN":
            client_socket.send("SHUTDOWN\n".encode())
            response = client_socket.recv(1024).decode()
            print("Server response:\n" + response)
            if "300 PASSWORD REQUIRED" in response:
                password = input("Enter password: ").strip()
                client_socket.send((password + "\n").encode())
                response = client_socket.recv(1024).decode()
                print("Server response:\n" + response)
                if "200 OKAY" in response:
                    break

    client_socket.close()

if __name__ == "__main__":
    server_ip = input("Enter server IP address: ").strip()
    main(server_ip)
