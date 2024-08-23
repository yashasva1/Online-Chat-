import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import subprocess
import encrypt

message_label = ''

root = tk.Tk()
root.title('SecureTalk')
root.geometry('600x400')

img = ImageTk.PhotoImage(Image.open(r'./main_bg.jpg'))
panel = tk.Label(root, image=img)
panel.place(x=0, y=0)


def copy2clip(txt):
    cmd = 'echo ' + txt.strip() + '|clip'
    return subprocess.check_call(cmd, shell=True)


def chat():
    root.destroy()
    import client_GUI


def encr():
    global message_label, co_entry
    for i in root.winfo_children()[1:]:
        i.destroy()
    message = tk.Label(root, text="Message :", bg='green', font="Console 20")
    message.place(x=15, y=60)

    code = tk.Label(root, text="Code :", bg='green', font='Console 20')
    code.place(x=15, y=150)

    me_entry = tk.Entry(root, bg='grey', font='Console 20')
    me_entry.place(x=200, y=60)

    co_entry = tk.Entry(root, bg='grey', font='Console 20')
    co_entry.place(x=200, y=150)

    me_entry.bind('<Return>', lambda x: [co_entry.focus_set()])
    co_entry.bind('<Return>', lambda x: [en(me_entry.get(), co_entry.get()), me_entry.focus_set()])

    message_label = tk.Label(root, text="", font="Console 15")

    en_button = tk.Button(root, text='Encrypt', bg='green', font='Bold 20',
                          command=lambda: [en(me_entry.get(), co_entry.get()), me_entry.focus_set()])
    de_button = tk.Button(root, text='Decrypt', bg='green', font='Bold 20',
                          command=lambda: [en(me_entry.get(), co_entry.get(), False), me_entry.focus_set()])
    back_button = tk.Button(root, text='Back', bg='red', font='Bold 20',
                            command=main)
    copy_button = tk.Button(root, text='Copy', bg='red', font='Bold 20',
                            command=lambda: [copy2clip(message_label.cget('text'))])
    en_button.place(x=15, y=250)
    de_button.place(x=200, y=250)
    back_button.place(x=415, y=250)
    copy_button.place(x=500, y=340)


def en(message, code, encry=True):
    global message_label, co_entry
    try:
        code = int(code)
        if not encry:
            code = -code
        ms = encrypt.encrypt(message, code)
        message_label.forget()
        message_label.configure(text=ms)
        message_label.place(x=30, y=340)
    except ValueError:
        messagebox.showerror('ERROR!', 'Code must be an integer')
        co_entry.delete(0, 'end')
        co_entry.focus_set()


def main():
    for i in root.winfo_children()[1:]:
        i.destroy()

    tk.Label(root, text='Welcome to Secure Talk', bg='violet', font='Bold 35').place(x=30, y=0)
    chat_button = tk.Button(root, text='Chat', bg='red', font='Bold 20',
                            activebackground='violet', command=chat)
    chat_button.place(x=50, y=270)
    encr_button = tk.Button(root, text='Encrypt/ decrypt \nmessages', bg='red', font='Bold 20',
                            activebackground='violet', command=encr)
    encr_button.place(x=270, y=270)


main()
root.mainloop()
