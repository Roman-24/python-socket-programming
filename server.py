import socket
import threading

# to bude vždy prvá správa kt. budeme zisťovať aké dlhá správa príde
# môže sa však aj stať že údaj o veľkosti správy sa do headru nezmestí
HEADER = 64

# portov je veľa a tento by mal byť safe
PORT = 5050

# automaticky vezme IPčku podľa názvu zariadenia
SERVER = socket.gethostbyname(socket.gethostname())

# tuple
ADDR = (SERVER, PORT)

FORMAT = "utf-8"

# ďalej potrebuješ mať nejakú správu kt. serveru oznámi, že sa klient odpája
DISCONNECT_MESSAGE = "!DISCONNECT"

# prvý argument hovorí to socketu aký typ adries bude hľadať
# druhý argument hovorí akým spôsobom sa budú streamovať dáta, akou metódou
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# akoby spojíš socket s tou adresou
server.bind(ADDR)

# táto funkcia bude handlovať všetkú komunikáciu medzi klientom a serverom
def handle_client(conn, addr):
    # výpisok kto sa pripojil
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # blocking line of code
        # argument je koľko bajtov chceš zobrať
        # teda budeš decodovať uvodnú správu kt. bude obsahovať aká veľká správa príde
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:
            msg_length = int(msg_length)

            # tu už nastavíš aká veľká správa ti prijde
            msg = conn.recv(msg_length).decode(FORMAT)

            # keď príjde správa, že sa klient odpája skončíme prijmanie
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[{addr}] Client was disconnected..")
                conn.send("[DISCONNECT] You was disconnected".encode(FORMAT))

            else:
                # posielanie správ server -> client
                print(f"[{addr}] {msg}")
                conn.send("Msg received".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        # čaká na nová pripojenie na server
        # a keď sa niečo pripojí tak to uloží že čo sa pripojilo teda adresu a port toho čo sa pripojilo
        conn, addr = server.accept()

        #teraz si urobíš tread v kt. pobeží handlovanie clienta
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # výpisok bude hovoriť koľko threads beží v tomto python procese
        # - 1 preto lebo jeden tread ti bude bežať vždy
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] Server is starting...")
start()
