import socket
import threading
import paramiko

# Host key for the SSH server
HOST_KEY = paramiko.RSAKey.generate(2048)

class SimpleSSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        if username == "testuser" and password == "testpass":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

# Function to start the SSH server
def start_ssh_server(host="0.0.0.0", port=2222):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Listening for connections on {host}:{port}...")

        while True:
            client_socket, client_addr = server_socket.accept()
            print(f"Connection from {client_addr}")

            transport = paramiko.Transport(client_socket)
            transport.add_server_key(HOST_KEY)
            server = SimpleSSHServer()
            transport.start_server(server=server)

            channel = transport.accept(20)
            if channel is None:
                print("Client did not request a channel.")
                continue

            print("Shell opened. Waiting for commands...")
            server.event.wait(10)

            if server.event.is_set():
                channel.send("Welcome to Simple SSH Server!\n")
                while True:
                    try:
                        command = channel.recv(1024).decode("utf-8").strip()
                        if command.lower() == "exit":
                            channel.send("Goodbye!\n")
                            break
                        response = f"Received: {command}\n"
                        channel.send(response)
                    except Exception as e:
                        print(f"Error: {e}")
                        break

            channel.close()
            transport.close()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()

# Example usage
if __name__ == "__main__":
    start_ssh_server()
