import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import socket
import threading
import datetime
import encrypt
import sys

# Global variables
name_entry = code_entry = window = nickname = code = ''
go_on = False

# Connecting To Server
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.56.1', 5050))
except ConnectionRefusedError:
    messagebox.showerror('Error!!!', 'Looks like the server is down now!!!')
    quit()


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def scroll_to_end(self):
        self.canvas.yview_moveto(1)

    def scroll_to_top(self):
        self.canvas.yview_moveto(0)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# GUI to get name and code
def get_nick_and_code():
    global name_entry, code_entry, go_on, window
    go_on = False
    window = tk.Tk()
    window.title('Login Page')
    window.geometry('500x400')

    img = ImageTk.PhotoImage(Image.open(r'./bg_image.jpg'))
    panel = tk.Label(window, image=img)
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

    submit_button = tk.Button(window, text='GO', bg='red', font='Bold 20',
                              activebackground='violet', command=get_name_code)
    submit_button.place(x=350, y=320)

    name_entry.focus_set()
    name_entry.bind('<Return>', lambda x: [code_entry.focus_set()])
    code_entry.bind('<Return>', lambda x: [get_name_code()])
    code_entry.bind('<Up>', lambda x: [name_entry.focus_set()])
    window.mainloop()


# Checking that name and code are OK
def get_name_code():
    global name_entry, code_entry, go_on, nickname, code
    nickname = name_entry.get()
    code = code_entry.get()
    focus = 0
    if '`' in nickname:
        messagebox.showerror('Error', "'`' is not allowed in username")
        name_entry.delete(0, 'end')
        name_entry.focus_set()
        focus = ''
    if not code.isdigit():
        messagebox.showerror('Error', "Code must be a digit")
        code_entry.delete(0, 'end')
        if focus == '':
            name_entry.focus_set()
        else:
            code_entry.focus_set()
    if ('`' not in nickname) and (code.isdigit()):
        code = int(code)
        window.destroy()
        go_on = True


# Splits the message so that it adjusts the frame and adds newline to it
def split_in_parts(message):
    new_str = ''
    no_of_line = 1
    list_of_words = message.split(' ')
    for word in list_of_words:
        if len(new_str) < no_of_line * 20:
            new_str += word
            new_str += ' '
        else:
            new_str += '\n'
            new_str += word
            new_str += ' '
            no_of_line += 1
    return new_str, no_of_line


# Returns a built frame for each message including time stamp and nick name
def message_frame(msg_window, msg, nick, time):
    split_msg, height_of_message = split_in_parts(msg)
    height = (height_of_message * 20) + 50
    msg_frame = tk.Frame(msg_window, height=height, width=200)
    name_head = tk.Label(msg_frame, text=nick, bg='violet', font='system 16 bold')
    msg_label = tk.Label(msg_frame, text=split_msg, bg='violet', fg="blue", font="Times 12")
    time_label = tk.Label(msg_frame, text=time, bg='violet', )
    name_head.place(x=0, y=0)
    msg_label.place(x=5, y=25)
    time_label.place(x=165, y=height - 15)
    return msg_frame, height


# System generated messages frame:
def system_frame(msg_window, msg):
    sys_frame = tk.Frame(msg_window, height=20, width=200)
    label = tk.Label(sys_frame, text=msg, fg="red", font="Times 12", bg='cyan')
    label.pack()
    return sys_frame


# Places message in left side of screen as received message
def receive_msg(message, nick, time=datetime.datetime.now().strftime('%H:%M')):
    global message_placing_height, scrollable_frame
    y = message_placing_height
    msg_frame, msg_height = message_frame(scrollable_frame, encrypt.encrypt(message, -code), nick, time)
    msg_frame.configure(bg='blue')
    msg_frame.place(x=0, y=y)
    message_entry.delete(0, 'end')
    message_placing_height += msg_height + 5
    if message_placing_height > 275:
        scrollable_frame.configure(height=message_placing_height)
    frame.scroll_to_end()


# Places message in right side of screen as sent message
def send_msg(message, nick, time=datetime.datetime.now().strftime('%H:%M')):
    global message_placing_height, scrollable_frame
    y = message_placing_height
    msg_frame, msg_height = message_frame(scrollable_frame, encrypt.encrypt(message, -code), nick, time)
    msg_frame.configure(bg='green')
    msg_frame.place(x=170, y=y)
    message_entry.delete(0, 'end')
    message_placing_height += msg_height + 5
    if message_placing_height > 275:
        scrollable_frame.configure(height=message_placing_height)
    frame.scroll_to_end()


# System generated messages:
def system_msg(message):
    global message_placing_height, scrollable_frame
    y = message_placing_height
    msg_frame = system_frame(scrollable_frame, message)
    msg_frame.place(x=150, y=y)
    message_entry.delete(0, 'end')
    message_placing_height += 25
    if message_placing_height > 275:
        scrollable_frame.configure(height=message_placing_height)
    frame.scroll_to_end()


# Listening to Server and Sending Nickname
def receive():
    try:
        with open(nickname + '.txt') as save_file:
            for message in save_file:
                message_list = message.split('`')
                if message_list[0] == nickname:
                    send_msg(message_list[1], message_list[0], message_list[2])
                else:
                    receive_msg(message_list[1], message_list[0], message_list[2])
    except FileNotFoundError:
        save_file = open(nickname + '.txt', 'w')

    while True:
        try:
            global scrollable_frame
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                message_list = message.split('`')
                if message_list[0] == nickname:
                    send_msg(message_list[1], message_list[0])
                elif message_list[0] == 'sys ':
                    system_msg(message_list[1])
                else:
                    receive_msg(message_list[1], message_list[0])
                with open(nickname + '.txt', 'a') as file:
                    if message_list[0] != 'sys ':
                        file.write(message + '`' + datetime.datetime.now().strftime('%H:%M'))
                        file.write('\n')
            frame.scroll_to_end()

        except:
            # Close Connection When Error
            messagebox.showerror('ERROR!!! ', 'Disconnected from server!!!')
            client.close()
            root.destroy()
            sys.exit()


# Sending Messages To Server
def write(msg):
    if msg != '':
        message = '{}` {}'.format(nickname, encrypt.encrypt(msg, code))
        client.send(message.encode('ascii'))


# Error in case forbidden character typed
def typing_error(event):
    messagebox.showerror("Error", "` is not allowed")
    return "break"


def del_all_msg():
    global message_placing_height
    with open(nickname + '.txt', 'w'):
        pass
    for i in scrollable_frame.winfo_children():
        if i.winfo_class() != 'Label':
            i.destroy()
    scrollable_frame.configure(height=275)
    message_placing_height = 5
    frame.scroll_to_top()


def warning_win(message, function):
    win = tk.Toplevel()
    win.title('WARNING!!')
    tk.Label(win, text=message, font='bold 16').pack()
    yes_button = tk.Button(win, text='YES', bg="red", command=lambda: [win.destroy(), function()])
    yes_button.pack(side='left')
    no_button = tk.Button(win, text='NO', bg="green")
    no_button.pack(side='right')


def on_scroll(event):
    # get the canvas (x, y) of the top-left corner of current viewable area
    x, y = frame.canvas.canvasx(0), frame.canvas.canvasy(0)
    # move the background image
    panel1.place(x=x, y=y)


get_nick_and_code()

if go_on:
    root = tk.Tk()
    root.title('Secure Talk')
    frame = ScrollableFrame(root)

    # Frame to place messages on
    scrollable_frame = tk.Frame(frame.scrollable_frame, height=275, width=900)
    scrollable_frame.pack()
    img1 = ImageTk.PhotoImage(Image.open(r'./chat_bg.jpg'))
    panel1 = tk.Label(scrollable_frame, image=img1)
    panel1.place(x=0, y=0)
    frame.scrollable_frame.bind('<Configure>', on_scroll, '+')

    # Text box to send message
    message_entry = tk.Entry(root, bg='grey')
    message_entry.pack(side='bottom', fill='x')
    message_entry.focus_set()
    message_entry.bind('<Return>', lambda x: write(message_entry.get()))
    message_entry.bind('`', typing_error)
    message_entry.bind('<Next>', frame.scroll_to_end())

    message_placing_height = 5  # Variable to specify the height where message to be placed

    # Sending button
    send_button = tk.Button(root, text="Send", activebackground="pink",
                            command=lambda: [write(message_entry.get())])
    send_button.pack(side='bottom', anchor='ne', in_=message_entry)

    null_frame = tk.Frame(root)
    null_frame.pack(side='top')

    # Clearing chat button
    clear_button = tk.Button(root, text='Clear chat history', activebackground="pink",
                             command=lambda: [warning_win("Do you want to clear all your messages?\nThis can't be "
                                                          "undone", del_all_msg)])
    clear_button.pack(side='left', anchor='nw', in_=null_frame)

    # Quit button
    quit_button = tk.Button(root, text='Quit', activebackground="pink",
                            command=lambda: [warning_win('Do you really want to quit?', sys.exit)])
    quit_button.pack(side='right', anchor='ne', in_=null_frame)

    frame.pack()

    # Threading to receive message
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    # __MAIN__
    root.mainloop()
