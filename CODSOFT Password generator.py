import random
import string
import sqlite3
from tkinter import *
from tkinter import messagebox

class SimplePassword:

    def __init__(self, root):
        self.root = root
        self.root.title("My Password Maker")
        self.root.geometry("500x450")
        self.root.config(bg="#FFB300")
        self.root.resizable(False, False)

        self.name_var = StringVar()
        self.len_var = StringVar()
        self.pass_var = StringVar()

        self.create_db()
        self.create_widgets()

    def create_db(self):
        conn = sqlite3.connect("myusers.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
        conn.commit()
        conn.close()

    def create_widgets(self):

        Label(self.root, text="PASSWORD GENERATOR",
              font=("Arial", 18, "bold"),
              bg="#CD8718", fg="black").pack(pady=20)

        Label(self.root, text="Enter Username",
              font=("Arial", 13),
              bg="#CD8718").pack()

        Entry(self.root, textvariable=self.name_var,
              font=("Arial", 13)).pack(pady=5)

        Label(self.root, text="Enter Password Length",
              font=("Arial", 13),
              bg="#CD8718").pack()

        Entry(self.root, textvariable=self.len_var,
              font=("Arial", 13)).pack(pady=5)

        Label(self.root, text="Generated Password",
              font=("Arial", 13),
              bg="#CD8718").pack()

        Entry(self.root, textvariable=self.pass_var,
              font=("Arial", 13),
              fg="red").pack(pady=5)

        Button(self.root, text="Generate",
               font=("Arial", 12, "bold"),
               bg="#4CAF50", fg="white",
               command=self.make_password).pack(pady=10)

        Button(self.root, text="Save",
               font=("Arial", 12, "bold"),
               bg="#2196F3", fg="white",
               command=self.save_data).pack(pady=5)

        Button(self.root, text="Reset",
               font=("Arial", 12, "bold"),
               bg="#f44336", fg="white",
               command=self.reset_all).pack(pady=5)

    def make_password(self):

        username = self.name_var.get()
        length_text = self.len_var.get()

        if username == "":
            messagebox.showerror("Error", "Username cannot be empty")
            return

        if not username.isalpha():
            messagebox.showerror("Error", "Username must contain only letters")
            return

        if not length_text.isdigit():
            messagebox.showerror("Error", "Length must be number")
            return

        length = int(length_text)

        if length < 6:
            messagebox.showerror("Error", "Minimum length is 6")
            return

        characters = string.ascii_letters + string.digits + "@#$%&"
        password = ""

        for i in range(length):
            password = password + random.choice(characters)

        self.pass_var.set(password)

    def save_data(self):

        username = self.name_var.get()
        password = self.pass_var.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Fill all fields first")
            return

        conn = sqlite3.connect("myusers.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        data = cur.fetchone()

        if data:
            messagebox.showerror("Error", "Username already exists")
        else:
            cur.execute("INSERT INTO users(username,password) VALUES(?,?)",
                        (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Saved Successfully")

        conn.close()

    def reset_all(self):
        self.name_var.set("")
        self.len_var.set("")
        self.pass_var.set("")

if __name__ == "__main__":
    root = Tk()
    app = SimplePassword(root)
    root.mainloop()
