import socket

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)

    # potrebuješ zariadiť abý správa obsahujúca dĺžku správy bola dlhá 64
    send_lenght += b" " * (HEADER - len(send_lenght))

    # poslanie psráv
    client.send(send_lenght)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

# start, klient môže posielať správy
while True:
    user_input = input("Writte your message: ")

    if user_input == "DISCONNECT":
        send(DISCONNECT_MESSAGE)
        break
    else:
        send(user_input)