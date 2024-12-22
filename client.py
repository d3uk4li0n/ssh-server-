import paramiko

def ssh_client(host, username, password, command):
    client = paramiko.SSHClient()
    # Automatically add the server's host key (not recommended for production)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        print("Output:")
        print(stdout.read().decode())
        print("Errors:")
        print(stderr.read().decode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

# Example usage
ssh_client("127.0.0.1", "testuser", "testpass", "uname -a")
