import socket, threading, tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
from plyer import notification
import os
with open("chat.key", "rb") as f:
    KEY = f.read()
cipher = Fernet(KEY)
client = socket.socket()
client.connect(("localhost", 9999))
current_user = ""
def notify(msg):
    notification.notify(
        title="New Message",
        message=msg,
        timeout=3
    )
def receive():
    while True:
        try:
            data = client.recv(4096)
            msg = cipher.decrypt(data).decode("utf-8")
            chat.config(state="normal")
            chat.insert(tk.END, msg + "\n")
            chat.config(state="disabled")
            chat.see(tk.END)
            if not msg.startswith(current_user + ":"):
                notify(msg)
        except:
            break
def send_msg():
    msg = msg_box.get("1.0", tk.END).strip()
    if msg:
        full_msg = f"{current_user}: {msg}"
        client.send(cipher.encrypt(full_msg.encode("utf-8")))
        chat.config(state="normal")
        chat.insert(tk.END, f"You: {msg}\n")
        chat.config(state="disabled")
        chat.see(tk.END)
        msg_box.delete("1.0", tk.END)
def send_file():
    path = filedialog.askopenfilename()
    if not path:
        return
    filename = os.path.basename(path)
    filesize = os.path.getsize(path)
    header = f"FILE|{filename}|{filesize}"
    client.send(cipher.encrypt(header.encode("utf-8")))
    with open(path, "rb") as f:
        while chunk := f.read(4096):
            client.send(chunk)
def login():
    global current_user
    auth = f"{user.get()}|{pwd.get()}"
    client.send(cipher.encrypt(auth.encode("utf-8")))
    res = cipher.decrypt(client.recv(1024)).decode()
    if res == "AUTH_SUCCESS":
        current_user = user.get()
        login_frame.pack_forget()
        chat_frame.pack()
        threading.Thread(target=receive, daemon=True).start()
    else:
        messagebox.showerror("Error", "Login Failed")
root = tk.Tk()
root.title("Advanced Chat App")
root.geometry("520x550")
login_frame = tk.Frame(root)
login_frame.pack()
tk.Label(login_frame, text="Username").pack()
user = tk.Entry(login_frame)
user.pack()
tk.Label(login_frame, text="Password").pack()
pwd = tk.Entry(login_frame, show="*")
pwd.pack()
tk.Button(login_frame, text="Login/Register", command=login).pack()
chat_frame = tk.Frame(root)
chat = tk.Text(chat_frame, height=20, width=60, state="disabled")
chat.pack()
msg_box = tk.Text(chat_frame, height=3, width=50)
msg_box.pack()
tk.Button(chat_frame, text="Send", command=send_msg).pack()
tk.Button(chat_frame, text="File", command=send_file).pack()
root.mainloop()