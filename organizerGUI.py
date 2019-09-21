import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import simpledialog
import calendar
from datetime import datetime



class Organizer(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Aidan's Organizer")

        container = tk.Frame(self)
        container.pack(side="left", fill="both", expand=True)
        container.grid_rowconfigure(5, weight=1)
        container.grid_columnconfigure(5, weight=1)
        self.frames = {}
        for F in (Mainmenu, Rempage, Calpage, Alpage, Addpage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Mainmenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def page_to_string(self, pag):

        if pag == "Reminder":
            sfile = "RemFile.txt"
        elif pag == "Calender":
            sfile = "CalFile.txt"
        elif pag == "Alarm":
            sfile = "AlFile.txt"
        return sfile

    def file_write(self, text, pag):
        with open(self.page_to_string(pag), 'a', encoding='utf-8') as file:
            file.writelines(text)

    def file_read(self, pag):
        with open(self.page_to_string(pag), 'r', encoding='utf-8') as file:
            lines = file.read()
            return lines

    def add_button(self, pag, tex):

        text = self.prompt(pag)
        self.file_write(text, pag)
        if pag == "Reminder":
            self.show_frame(Rempage)
        elif pag == "Calender":
            self.show_frame(Calpage)
        elif pag == "Alarm":
            self.show_frame(Alpage)
        self.text_update(pag, tex)

    def prompt(self, pag):
        tex = ""
        date = ""
        time = ""
        for x in range(3):
            if x == 0:
                tex = simpledialog.askstring("New" + pag, "Enter text")
            elif x == 1:
                date = simpledialog.askstring("New" + pag, "Enter date")
            elif x == 2:
                time = simpledialog.askstring("New" + pag, "Enter time")
        text = [tex + "\n", date + "\n", time + "\n"]
        return text

    def rev_button(self, pag, tex):
        revint = simpledialog.askinteger("Remove", "Which reminder would you like to remove")
        revline = ((revint - 1) * 3)
        text = self.file_read(pag)
        texlines = text.splitlines(True)
        del texlines[revline: revline + 3]
        file = open(self.page_to_string(pag), 'w', encoding='utf-8')
        file.writelines(texlines)
        file.close()
        self.text_update(pag, tex)

    def text_update(self, pag, tex):
        textf = self.file_read(pag)
        tex.set(textf)


class Mainmenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("OrganizerTitle.png")
        render = ImageTk.PhotoImage(load)
        imgtitle = tk.Label(self, image=render)
        imgtitle.image = render
        imgtitle.grid(rowspan=5, row=0, column=5, pady=10, padx=10)

        rembutton = ttk.Button(self, text="Reminders", command=lambda: controller.show_frame(Rempage))
        rembutton.grid(row=0, column=0, pady=5, padx=20)

        calbutton = ttk.Button(self, text="Calender", command=lambda: controller.show_frame(Calpage))
        calbutton.grid(row=1, column=0, pady=5, padx=20)

        albutton = ttk.Button(self, text="Alarms", command=lambda: controller.show_frame(Alpage))
        albutton.grid(row=2, column=0, pady=5, padx=20)

        mombutton = ttk.Button(self, text="Mom Mode :)", command=lambda: controller.show_frame())
        mombutton.grid(row=3, column=0, pady=5, padx=20)

        endbutton = ttk.Button(self, text="Quit", command=controller.destroy)
        endbutton.grid(row=4, column=0)


class Rempage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Reminders")
        label.grid(row=0, column=1)
        page = "Reminder"

        texr = tk.StringVar()
        remsf = controller.file_read("Reminder")
        texr.set(remsf)
        lab = tk.Label(self, textvariable=texr, anchor='w')
        lab.grid(row=1, column=1, rowspan=3, sticky='w')

        retbutton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Mainmenu))
        retbutton.grid(row=1, column=0)
        addbutton = ttk.Button(self, text="Add", command=lambda: controller.add_button(page, texr))
        addbutton.grid(row=2, column=0)
        revbutton = ttk.Button(self, text="Remove", command=lambda: controller.rev_button(page, texr))
        revbutton.grid(row=3, column=0)


class Addpage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        page = "Reminder"
        label = ttk.Label(self, text="Add new reminder.")
        label.grid(row=0, column=0, columnspan=2)
        label2 = ttk.Label(self, text=page)
        label2.grid(row=1, column=0)
        label3 = ttk.Label(self, text="Date")
        label3.grid(row=2, column=0)
        label4 = ttk.Label(self, text="Time")
        label4.grid(row=3, column=0)

        tex = tk.Entry(self)
        tex.grid(row=1, column=1)
        date = tk.Entry(self)
        date.grid(row=2, column=1)
        time = tk.Entry(self)
        time.grid(row=3, column=1)

        addbutton = ttk.Button(self, text="Add", command=lambda: controller.add_button(page))
        addbutton.grid(row=4, column=0)
        canbutton = ttk.Button(self, text="Cancel", command=lambda: controller.show_frame(Rempage))
        canbutton.grid(row=4, column=1)


class Calpage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Calender")
        label.grid(row=0, column=1, columnspan=2, pady=10, padx=10)

        page = "Calender"

        calw = self.cal_widg()
        callab = ttk.Label(self, text=calw)
        callab.config(font=('Courier', '10'))
        callab.grid(row=1, column=1, rowspan=12)

        texr = tk.StringVar()
        remsf = controller.file_read(page)
        texr.set(remsf)
        lab = tk.Label(self, textvariable=texr, anchor='w')
        lab.grid(row=13, column=1, rowspan=3, sticky='w')

        retbutton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Mainmenu))
        retbutton.grid(row=1, column=0)
        addbutton = ttk.Button(self, text="Add", command=lambda: controller.add_button(page, texr))
        addbutton.grid(row=2, column=0)
        revbutton = ttk.Button(self, text="Remove", command=lambda: controller.rev_button(page, texr))
        revbutton.grid(row=3, column=0)

    def cal_widg(self):
        cal = calendar.TextCalendar(firstweekday=6).formatmonth(datetime.now().year, datetime.now().month, w=10, l=4)
        return cal


class Alpage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Alarms")
        label.grid(row=0, column=1, columnspan=2, pady=10, padx=10)

        page = "Alarm"
        texr = tk.StringVar()
        remsf = controller.file_read(page)
        texr.set(remsf)
        lab = tk.Label(self, textvariable=texr, anchor='w')
        lab.grid(row=1, column=1, rowspan=3, sticky='w')

        retbutton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Mainmenu))
        retbutton.grid(row=1, column=0)
        addbutton = ttk.Button(self, text="Add", command=lambda: controller.add_button(page, texr))
        addbutton.grid(row=2, column=0)
        revbutton = ttk.Button(self, text="Remove", command=lambda: controller.rev_button(page, texr))
        revbutton.grid(row=3, column=0)




app = Organizer()
app.mainloop()
