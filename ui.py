import base64
import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox
from database import DBManager
from encryptdec import Security
import hashlib
import pytesseract
from PIL import Image
import cv2
from pytesseract import Output
from tkinter import filedialog


class UI:

    def __init__(self, root):
        self.root = root
        self.key_for_db = "batman"
        self.root.title("Password manager")
        self.user_id = None
        self.show_login_screen()
        self.database_manager = DBManager()
        self.file_path_for_automaticLogin = None
        self.crypto_manager = None
    def show_login_screen(self):

        self.login_frame = tk.Frame(self.root)
        self.login_frame.grid(row=0, column=0)

        self.username_lable = tk.Label(self.login_frame, text="Username")
        self.username_lable.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_frame, text="Password")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2)

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.register)
        self.register_button.grid(row=3, column=0, columnspan=2)

        self.automatic_login = tk.Button(self.login_frame, text="Automatic login", command=self.login_automatic)
        self.automatic_login.grid(row=4, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.database_manager.get_user(username)
        if user and Security.check_password(user[1], password):
            self.user_id = user[0]
            self.login_frame.destroy()
            self.crypto_manager = Security(base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest()))
            self.create_main_ui()
        else:
            messagebox.showerror("Error", "Not good user, pa")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        pass_hash = Security.hashPass(password)

        if not username or not password:
            messagebox.showerror("Error", "Completeaza")
            return
        try:
            self.database_manager.insert_user(username, pass_hash)
            messagebox.showinfo("Success", "U are registered")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "U are registered already")

    def create_main_ui(self):
        self.service_label = tk.Label(self.root, text="Sevice")
        self.service_label.grid(row=0, column=0)
        self.service_entry = tk.Entry(self.root)
        self.service_entry.grid(row=0, column=1)

        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.grid(row=1, column=0)
        self.username_entry1 = tk.Entry(self.root)
        self.username_entry1.grid(row=1, column=1)

        self.password_label1 = tk.Label(self.root, text="Password")
        self.password_label1.grid(row=2, column=0)
        self.password_entry1 = tk.Entry(self.root, show="*")
        self.password_entry1.grid(row=2, column=1)

        self.add_button_entry = tk.Button(self.root, text="Add", command=self.add_password)
        self.add_button_entry.grid(row=3, column=0, columnspan=2)

        self.view_button = tk.Button(self.root, text="View Passwords", command=self.view_passwords)
        self.view_button.grid(row=4, column=0, columnspan=2)

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Pics",
                                                          "*.png*"),
                                                         ("all files",
                                                          "*.*")))
        print(filename)
        self.file_path_for_automaticLogin = filename
        if filename:
            self.loghimin(filename)
    def loghimin(self, filepath):

        username, password = self.functionThatParsesThePicture(filepath)

        user = self.database_manager.get_user(username)
        if user and Security.check_password(user[1], password):
            self.user_id = user[0]
            self.login_frame.destroy()
            self.automaticLog_frame.destroy()
            self.crypto_manager = Security(base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest()))
            self.create_main_ui()
        else:
            messagebox.showerror("Error", "Not good user, pa")

    def login_automatic(self):

        self.automaticLog_frame = tk.Toplevel(self.root)
        self.automaticLog_frame.title("Load your credentials")

        label_file_explorer = tk.Label(self.automaticLog_frame,
                                    text="File Explorer using Tkinter",
                                    width=100, height=4,
                                    fg="blue")

        button_explore = tk.Button(self.automaticLog_frame,
                                text="Browse Files",
                                command=self.browseFiles)

        label_file_explorer.grid(row=0, column=0)
        button_explore.grid(row=1, column=0)

    def add_password(self):
        service = self.service_entry.get()
        username = self.username_entry1.get()
        password = self.password_entry1.get()

        if not service or not username or not password:

            messagebox.showerror("Error", "Completeaza ma")
            return

        enc_pass = self.crypto_manager.encryptPass(password)
        self.database_manager.insertInTable(self.user_id, service, username, enc_pass)
        messagebox.showinfo("Succes", "Added to db")

    def view_passwords(self):
        passwords = self.database_manager.get_passwords(self.user_id)
        passwords_list = []

        for service, username, enc_pass in passwords:
            passwords_list.append(f"Service {service}, \nUsername: {username}, \nPassword: "
                                  f"{self.crypto_manager.decryptPass(enc_pass)}")

        pass_str = '\n'.join(passwords_list)
        if pass_str:
            messagebox.showinfo("Stored passwords", pass_str)
        else:
            messagebox.showinfo("Stored passwords", "No passwords yet")

    def functionThatParsesThePicture(self, imgPath):
        myconfig = r"--psm 6 --oem 3"

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'

        img = cv2.imread(imgPath)
        height, width, _ = img.shape

        data = pytesseract.image_to_data(img, config=myconfig, output_type=Output.DICT)

        username = ""
        password = ""
        index = 0
        amountOfBoxes = len(data['text'])
        for i in range(amountOfBoxes):
            if float(data['conf'][i]) > 60:
                if index == 0:
                    username = data['text'][i]
                    index += 1
                elif index == 1:
                    password = data['text'][i]
                    index += 1

        return username, password


if __name__ == '__main__':
    root = tk.Tk()
    app = UI(root)
    root.mainloop()