from tkinter import Frame, W, E, N,S, Tk
from tkinter import ttk
import tkinter.font as tkFont
import sqlite3

connection = sqlite3.connect('book.db')
c = connection.cursor()

class Bookdb:
    def __init__(self):
        self.connection = sqlite3.connect('book.db')
        self.c = connection.cursor()
        print("You have connetected to db")
        print(connection) 

    def view(self):
        self.c.execute("SELECT title, author, isbn from books")
        return self.c.fetchall()

db = Bookdb()


def view_records():
    for row in db.view():
        tree.insert("", 'end', values=row)

root = Tk()

tree= ttk.Treeview(root, column=("column1", "column2", "column3"), show='headings')
tree.heading("#1", text="NUMBER")
tree.heading("#2", text="FIRST NAME")
tree.heading("#3", text="SURNAME")
tree.grid(row=3,column=1, columnspan=5,sticky=W + E,pady=40,padx=10)

view_button = ttk.Button(root, text="View all records", command=view_records)
view_button.grid(row=15, column = 3)

root.mainloop()