from Tkinter import *
import math, time
import pickle
from Wemo import wemo


def load_wemo():
    global switch, ip
    try:
        file2 = open(r'd.pkl', 'rb')
        new_d = pickle.load(file2)
        file2.close()
        ip = new_d["ip"]
    except IOError:
        ip_popup()
    
    switch = wemo(ip)

def return_press(event):
    start_timer_add()

def backspace_press(event):
    if len(display) > 0:
        if state == "Enter":
            display.pop()
        elif state == "Timer":
            clear()

def press_down(event):
    if len(display) < 4 and re.match("[0-9]",event.char) != None:
        display.append(event.char)

    update_display()

def click_down(event):
    global ip, switch
    event.widget.config(bg = "#B71C1C")

    if event.widget.name == "clear":
        clear()
    elif event.widget.name == "enter":
        start_timer_add()
    elif event.widget.name == "ip":
        ip_popup()
    elif event.widget.name == "save":
        d = {"ip" : msg.get()}
        afile = open(r'd.pkl', 'wb')
        pickle.dump(d, afile)
        afile.close()
        ip = msg.get()
        switch = wemo(ip)
        top.destroy()
    elif len(display) < 4:
        display.append(event.widget.cget("text"))
    update_display()

def ip_popup():
    global msg, top
    top = Toplevel()
    top.title("IP Settings")
    top.configure(background='#757575')

    msg = Entry(top, text="test")
    msg.grid(column=0,row=0,sticky=N+S+W+E,padx=XPAD,pady=YPAD,columnspan=1)
    msg.delete(0, END)
    try:
        msg.insert(0, ip)
    except NameError:
        msg.insert(0, "Enter IP")

    s1 = Label(top, text="Save", bg="#F44336", fg="white", name="save")
    s1.grid(column=0,row=1,sticky=N+S+W+E,padx=XPAD,pady=YPAD,columnspan=1)
    s1.bind("<Button-1>", click_down)
    s1.bind("<ButtonRelease-1>", click_up)
    s1.name = "save"

    for x in range(root.grid_size()[0]):
        root.grid_columnconfigure(x, weight=1, minsize=70)

    for x in range(root.grid_size()[1] - 1):
        root.grid_rowconfigure(x, weight=1)



def update_display():
    global l
    minute = "  "
    second = "  "
    for idx, val in enumerate(display[::-1]):
        if (idx == 0):
            second = " " + str(val)
            minute = "  "
        if (idx == 1):
            second = str(val) + second[1]
        if (idx == 2):
            minute = " " + str(val)
        if (idx == 3):
            minute = str(val) + minute[1]

    l.config(text=minute+colon+second)
    root.update()

def click_up(event):
    event.widget.config(bg = "#F44336")
    root.update()


def display_to_seconds():
    seconds = 0
    for idx, val in enumerate(display[::-1]):
        if (idx == 0):
            seconds += int(val)
        if (idx == 1):
            seconds += int(val) * 10
        if (idx == 2):
            seconds += int(val) * 60
        if (idx == 3):
            seconds += int(val) * 600
    return seconds

def seconds_to_display(seconds):
    m, s = divmod(int(seconds), 60)
    m = str(m).zfill(2)
    s = str(s).zfill(2)
    return [int(m[0]), int(m[1]), int(s[0]), int(s[1])]

def change_colon():
    global colon
    if state == "Timer":
        colon = ":"
    elif colon == ":":
        colon = " "
    else:
        colon = ":"
    update_display()
    root.after(1000, change_colon)

def start_timer_add():
    global state, seconds, start
    if state == "Enter":
        seconds = display_to_seconds()
        start = math.floor(time.time())
        end = math.floor(time.time())
        state = "Timer"

        switch.on()
        root.nametowidget("enter").config(text="Add 30")
        root.nametowidget("clear").config(text="Stop")
        end_text = "Stop"
    elif state == "Timer":
        seconds += 30

def clear():
    global state
    del display[:]
    state = "Enter"
    switch.off()
    root.nametowidget("enter").config(text="Enter")
    root.nametowidget("clear").config(text="Clear")

def main_timer():
    global display, state
    if state == "Timer":
        end = math.floor(time.time())
        elapsed = end - start
        display = seconds_to_display(max(seconds - elapsed, 0))
        if (elapsed > seconds):
            clear()
    update_display()
    root.after(200, main_timer)

def create_labels():
    global l, s
    l = Label(root, text="", bg="white", fg="black",font=("Courier", 30))
    l.grid(column=0,row=0,sticky=N+S+W+E,padx=XPAD,pady=YPAD,columnspan=3)

    current = 0
    for row in range(1, ROWS):
        for col in range(COLUMNS):
            b = Label(root, text=NUMS[current], bg="#F44336", fg="white", name=NUMS[current].lower())
            b.bind("<Button-1>", click_down)
            b.bind("<ButtonRelease-1>", click_up)
            b.name = NUMS[current].lower()
            b.grid(column=col,row=row,sticky=N+S+W+E,padx=XPAD,pady=YPAD)
            current += 1

    s = Label(root, text="IP Address Settings", bg="#F44336", fg="white", name="ip")
    s.grid(column=0,row=5,sticky=N+S+W+E,padx=XPAD,pady=YPAD,columnspan=3)
    s.bind("<Button-1>", click_down)
    s.bind("<ButtonRelease-1>", click_up)
    s.name = "ip"

def resize_labels():
    for x in range(root.grid_size()[0]):
        root.grid_columnconfigure(x, weight=1, minsize=70)

    for x in range(root.grid_size()[1] - 1):
        root.grid_rowconfigure(x, weight=2)

    root.grid_rowconfigure(5, weight=1)

def root_settings():
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass

    root.bind("<Key>", press_down)
    root.bind("<BackSpace>", backspace_press)
    root.bind("<Return>", return_press)
    root.title("Compressor Control")
    root.geometry("250x300")
    root.minsize("250","300")
    root.configure(background='#757575')
    root.after(1000, change_colon)
    root.after(500, main_timer)
    root.after(200, load_wemo)
    root.focus_force()
    root.mainloop()


root = Tk()

XPAD = 5
YPAD = 5
COLUMNS = 3
ROWS = 5
NUMS = ["1","2","3",
        "4","5","6",
        "7","8","9",
        "Clear","0","Enter"]
display = []
colon = ":"
state = "Enter"
seconds = 0

create_labels()
resize_labels()
root_settings()

