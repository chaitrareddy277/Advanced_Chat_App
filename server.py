import socket, threading, json, os
from cryptography.fernet import Fernet
with open("chat.key", "rb") as f:
    KEY = f.read()
cipher = Fernet(KEY)
users_file = "users.json"
history_file = "history.txt"
if not os.path.exists(users_file):
    with open(users_file, "w") as f:
        json.dump({}, f)
clients = []
def load_users():
    with open(users_file) as f:
        return json.load(f)
def save_users(data):
    with open(users_file, "w") as f:
        json.dump(data, f)
def broadcast(message, sender):
    for client in clients:
        try:
            if client != sender:
                client.send(cipher.encrypt(message.encode("utf-8")))
        except:
            clients.remove(client)
def handle(client):
    try:
        auth = cipher.decrypt(client.recv(1024)).decode("utf-8")
        username, password = auth.split("|")
        users = load_users()
        if username in users:
            if users[username] != password:
                client.send(cipher.encrypt(b"AUTH_FAIL"))
                return
        else:
            users[username] = password
            save_users(users)
        client.send(cipher.encrypt(b"AUTH_SUCCESS"))
        clients.append(client)
        while True:
            data = client.recv(4096)
            try:
                header = cipher.decrypt(data).decode("utf-8")
            except:
                continue
            if header.startswith("FILE|"):
                _, filename, filesize = header.split("|")
                filesize = int(filesize)
                os.makedirs("received_files", exist_ok=True)
                with open(f"received_files/{filename}", "wb") as f:
                    received = 0
                    while received < filesize:
                        chunk = client.recv(min(4096, filesize - received))
                        f.write(chunk)
                        received += len(chunk)
                print(f"File received: {filename}")
                continue 
            msg = header
            with open(history_file, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
            broadcast(msg, client)
    except Exception as e:
        print("Client error:", e)
    finally:
        if client in clients:
            clients.remove(client)
        client.close()
server = socket.socket()
server.bind(("localhost", 9999))
server.listen()
print("Server running...")
while True:
    c, a = server.accept()
    threading.Thread(target=handle, args=(c,), daemon=True).start()