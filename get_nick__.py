import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

name_entry = code_entry = window = ''
go_on = False


def get_nick_and_code():
    global name_entry, code_entry, go_on, window
    go_on = False
    window = tk.Tk()
    window.geometry('500x400')

    img = ImageTk.PhotoImage(Image.open(r'./bg_image.jpg'))
    panel = tk.Label(window, image=img)
    # panel.pack(side="bottom", fill="both", expand="yes")
    panel.place(x=0, y=0)

    heading = tk.Label(window, text='Welcome to Secure Talk', bg='violet', font='Bold 30')
    heading.place(x=30, y=0)

    name_label = tk.Label(window, text="Enter your name :", bg='green', font="Console 20")
    name_label.place(x=15, y=60)

    code_label = tk.Label(window, text="Enter your code :", bg='green', font='Console 20')
    code_label.place(x=15, y=200)

    name_entry = tk.Entry(window, bg='grey', font='Console 20')
    name_entry.place(x=100, y=120)

    code_entry = tk.Entry(window, bg='grey', font='Console 20')
    code_entry.place(x=100, y=260)

    submit_button = tk.Button(window, text='GO', bg='red', font='Bold 20', activebackground='violet')
    submit_button.place(x=350, y=320)

    name_entry.focus_set()
    name_entry.bind('<Return>', lambda x: [code_entry.focus_set()])
    code_entry.bind('<Return>', lambda x: [get_name_code(), test_go_on()])
    code_entry.bind('<Up>', lambda x: [name_entry.focus_set()])
    print(go_on)

    window.mainloop()


def get_name_code():
    global name_entry, code_entry, go_on
    name = name_entry.get()
    code = code_entry.get()
    focus = 0
    if '`' in name:
        messagebox.showerror('Error', "'`' is not allowed in username")
        name_entry.delete(0, 'end')
        name_entry.focus_set()
        focus = ''
    else:
        go_on = True
    if not code.isdigit():
        messagebox.showerror('Error', "Code must be a digit")
        code_entry.delete(0, 'end')
        if focus == '':
            name_entry.focus_set()
        else:
            code_entry.focus_set()
    else:
        go_on = True


def test_go_on():
    global window
    print(go_on)
    print('test_go_on executed')
    if go_on:
        l = [name_entry.get(), int(code_entry.get())]
        window.destroy()
        return l


if __name__ == '__main__':
    get_nick_and_code()
