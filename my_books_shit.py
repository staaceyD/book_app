from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

connection = sqlite3.connect('book.db')
c = connection.cursor()

class Bookdb:
    def __init__(self):
        self.connection = sqlite3.connect('book.db')
        self.c = connection.cursor()
        print("You have connetected to db")
        print(connection)

    def __del__(self):
        self.connection.close()
    
    def view(self):
        self.c.execute("SELECT title, author, isbn from books")
        return self.c.fetchall()
    
    def insert(self,title, author, isbn):
        sql = "INSERT INTO books(title, author, isbn) VALUES (?,?,?)"
        values = [title, author, isbn]
        self.c.execute(sql, values)
        self.connection.commit()
        MessageInfoWindow(title="Book Database", message="New book was added")

    def update(self, id, title, author, isbn):
        tsql = "UPDATE books SET title=?, author=?, isbn=? WHERE id=?"
        self.c.execute(tsql, [title, author, isbn, id])
        self.connection.commit()
        MessageInfoWindow(title="Book Database", message="The book was updated")
    
    def delete(self,id):
        delsql = "DELETE FROM books WHERE id=?"
        self.c.execute(delsql, [id])
        self.connection.commit()
        MessageInfoWindow(title="Book Database", message="The book was deleted")
    

db = Bookdb()

root_width = 700
root_height = 550
    
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
        Label(self, text=message).grid(row=0, column=0, columnspan=3, pady=(7, 7), padx=(7, 7), sticky="ew")
        Button(self, text="OK", command=self.destroy, highlightbackground='#3E4149').grid(row=1, column=2, padx=(7, 7))

class MessageExitWindow(MessageInfoWindow):
    def __init__(self, title, message):
        super().__init__()
        Button(self, text="Cancel", command=self.destroy, highlightbackground='#3E4149').grid(row=1, column=2)
    
def empty_fields_warning():
    MessageInfoWindow(title="Nothing was selected", message="""Please make sure you've selected book
    through 'View all records' screen""")

def get_selected_row(event):
    global selected_tuple
    index = list_bx.curselection()[0]
    selected_tuple = list_bx.get(index)
    title_entry.delete(0, "end")
    title_entry.insert("end", selected_tuple[0])
    author_entry.delete(0, "end")
    author_entry.insert("end", selected_tuple[1])
    isbn_entry.delete(0, "end")
    isbn_entry.insert("end", selected_tuple[2])

def view_records():
    list_bx.delete(0, 'end')
    for row in db.view():
        list_bx.insert('end', row)
  
def add_records():
    if not title_text.get() and not author_text.get() and not isbn_text.get():
        MessageInfoWindow("Required data", "Please add information to all required fields")
    else:
        db.insert(title_text.get(),author_text.get(), isbn_text.get())
        list_bx.delete(0, 'end')
        list_bx.insert('end', (title_text.get(),author_text.get(), isbn_text.get()))
        title_entry.delete(0,'end')
        author_entry.delete(0,'end')
        isbn_entry.delete(0,'end')
        connection.commit()
        

def delete_record():
    if not title_text.get() and not author_text.get() and not isbn_text.get():
        empty_fields_warning()
    else:
        db.delete(selected_tuple[0])
        title_entry.delete(0,'end')
        author_entry.delete(0,'end')
        isbn_entry.delete(0,'end')
        connection.commit()
        view_records()

def clear_screen():
    list_bx.delete(0, 'end')
    title_entry.delete(0,'end')
    author_entry.delete(0,'end')
    isbn_entry.delete(0,'end')

def update_record():
    if not title_text.get() and not author_text.get() and not isbn_text.get():
        empty_fields_warning()
    else:
        db.update(selected_tuple[0], title_text.get(),author_text.get(), isbn_text.get())
        title_entry.delete(0,'end')
        author_entry.delete(0,'end')
        isbn_entry.delete(0,'end')
        connection.commit()
        view_records()

def on_closing():
    dd = db
    if messagebox.askokcancel('Quit', 'Do you want to quit?'):
        root.destroy()
        del dd



root = Tk()
#window settings
root.title("My Book Shit App")
root.configure(background = "#e0b72f")
root_size = str(root_width)+'x'+str(root_height)
root.geometry(root_size)
root.resizable(width = False, height = False)
s = ttk.Style()
s.theme_use("alt")
# Positions the window in the center of the page.
position_right = int(root.winfo_screenwidth()/2 - root_width/2)
position_down = int(root.winfo_screenheight()/2.5 - root_height/2)
root.geometry("+{}+{}".format(position_right, position_down))

#Title settings
title_label = ttk.Label(root, text = "Title  ", background = "#e0b72f", font = ("Times New Roman", 19))
title_label.grid(row=0, column=0, sticky=W)
title_text = StringVar()
title_entry = ttk.Entry(root, width=15, textvariable=title_text)
title_entry.grid(row=0, column=1, sticky = W)
title_entry.focus_set()

#Author settings
author_label = ttk.Label(root, text = "Author  ",background = "#e0b72f", font = ("Times New Roman", 19))
author_label.grid(row=0, column=2, sticky=W)
author_text = StringVar()
author_entry = ttk.Entry(root, width=15, textvariable=author_text)
author_entry.grid(row=0, column=3, sticky = W)


#ISBN settings
isbn_label = ttk.Label(root, text = "ISBN  ",background = "#e0b72f", font = ("Times New Roman", 19))
isbn_label.grid(row=0, column=4, sticky=W)
isbn_text = StringVar()
isbn_entry = ttk.Entry(root, width=15, textvariable=isbn_text)
isbn_entry.grid(row=0, column=5, sticky = W)


#window for displaying books with scrollbar
list_bx = Listbox(root,height=16,font=("Times New Roman", 16),bg="#d5d6b6")
list_bx.grid(row=3,column=1, columnspan=5,sticky=W + E,pady=40,padx=10)
list_bx.bind('<<ListboxSelect>>', get_selected_row)

scroll_bar = Scrollbar(root)

list_bx.configure(yscrollcommand=scroll_bar.set) # Enables vetical scrolling
scroll_bar.configure(command=list_bx.yview)

#control buttons
ttk.Style().configure("TButton", padding=4, font = ("Times New Roman", 14))
add_button = ttk.Button(root, text="Add a Book", command=add_records)
add_button.grid(row=1, column = 3, sticky = W)


modify_button = ttk.Button(root, text="Modify", command=update_record)
modify_button.grid(row=15, column = 1)

delete_button = ttk.Button(root, text="Delete a Book", command=delete_record)
delete_button.grid(row=15, column = 2)

view_button = ttk.Button(root, text="View all records", command=view_records)
view_button.grid(row=15, column = 3)

clear_button = ttk.Button(root, text="Clear screen", command=clear_screen)
clear_button.grid(row=15, column = 4)

exit_button = ttk.Button(root, text="Exit App", command=root.destroy)
exit_button.grid(row=15, column = 5)



root.mainloop()