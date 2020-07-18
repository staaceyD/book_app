from tkinter import Toplevel, Label, Button, Tk

root_width = 700
root_height = 450


# root = Tk()
class MessageInfoWindow(Toplevel):
    def __init__(self, title, message):
        super().__init__()
        self.title(title)
        msg_box_width = 350
        msg_box_height = 100
        msg_box_size = str(msg_box_width)+'x'+str(msg_box_height)
        move_messagebox_x = int(root_width/2 - msg_box_width/2)
        move_messagebox_y = int(root_height/2 - msg_box_height/2)
        self.geometry(msg_box_size)
        self.geometry("+{}+{}".format(self.master.winfo_x() + move_messagebox_x, self.master.winfo_y() + move_messagebox_y))
        self.resizable(False, False)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        Label(self, text=message).grid(row = 1, column=0, columnspan=3, pady=(7, 7), padx=(7, 7), sticky="ew")
        Button(self, text="OK", command=self.destroy, highlightbackground='#3E4149').grid(row=2, column=2, padx=40, pady = 5)

class MessageExitWindow(MessageInfoWindow):
    def __init__(self, title, message, root):
        MessageInfoWindow.__init__(self, title, message)
        Button(self, text="OK", command=root.destroy, highlightbackground='#3E4149').grid(row=2, column=0, pady = 5)
        Button(self, text="Cancel", command=self.destroy, highlightbackground='#3E4149').grid(row=2, column=2, padx=40, pady = 5)
    