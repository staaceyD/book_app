from tkinter import Button, E, END, Frame, Label, Listbox, N, OptionMenu, S, Scrollbar, StringVar, Tk, Toplevel, W 
from tkinter import ttk
from tkinter import messagebox
import message_windows
import data_base_connection


db = data_base_connection.Bookdb()



def empty_fields_warning():
    message_windows.MessageInfoWindow(title="Nothing was selected", message="""Please make sure you've selected book
    through 'View all records' screen""")

def get_selected_row(event):
    title_entry.delete(0, "end")
    author_entry.delete(0, "end")
    isbn_entry.delete(0, "end")
    
    global content
    for nm in tree.selection():
        content = tree.item(nm, 'values')
        title_entry.insert(END, content[1])
        author_entry.insert(END, content[2])
        isbn_entry.insert(END, content[3])
    print(content)

def changed_value(var, indx, mode):
    global selected
    selected = option_variable.get().lower()
    return selected

def search():
    search_input = search_entry.get()
    if not search_input:
        message_windows.MessageInfoWindow("Search", "Search field is empty")
    else:
        tree.delete(*tree.get_children())
        for r_row in db.filter(selected, search_input):
            tree.insert("", 'end', values=r_row)
    
def update_record():
    if not title_text.get() and not author_text.get() and not isbn_text.get():
        empty_fields_warning()
    else:
        db.update(content[0], title_text.get(),author_text.get(), isbn_text.get())
        title_entry.delete(0,'end')
        author_entry.delete(0,'end')
        isbn_entry.delete(0,'end')
        db.connection.commit()
        view_records()

def view_records():
    tree.delete(*tree.get_children())
    for row in db.view():
        tree.insert("", 'end', values=row)
  
def add_records():
    if not title_text.get() and not author_text.get() and not isbn_text.get():
        message_windows.MessageInfoWindow("Required data", "Please add information to all required fields")
    else:
        db.insert(title_text.get(),author_text.get(), isbn_text.get())
        tree.delete(*tree.get_children())
        tree.insert("", 'end', values = (db.c.lastrowid, title_text.get(),author_text.get(), isbn_text.get()))
        title_entry.delete(0,'end')
        author_entry.delete(0,'end')
        isbn_entry.delete(0,'end')
        db.connection.commit()
        

def delete_record():
    if not title_text.get() and not author_text.get() and not isbn_text.get():
        empty_fields_warning()
    else:
        db.delete(content[0])
        title_entry.delete(0,'end')
        author_entry.delete(0,'end')
        isbn_entry.delete(0,'end')
        db.connection.commit()
        view_records()

def clear_screen():
    search_entry.delete(0, 'end')
    tree.delete(*tree.get_children())
    title_entry.delete(0,'end')
    author_entry.delete(0,'end')
    isbn_entry.delete(0,'end')


def on_closing():
    message_windows.MessageExitWindow('Quit', 'Do you want to quit?', root)
    


# root_width = 700
# root_height = 450
root = Tk()
# message_windows.root = Tk()
#window settings
root.title("My Book Shit App")
root.configure(background = "#e0b72f")
root_size = str(message_windows.root_width)+'x'+str(message_windows.root_height)
root.geometry(root_size)
root.resizable(width = False, height = False)
s = ttk.Style()
s.theme_use("alt")
# Positions the window in the center of the page.
position_right = int(root.winfo_screenwidth()/2 - message_windows.root_width/2)
position_down = int(root.winfo_screenheight()/2.5 - message_windows.root_height/2)
root.geometry("+{}+{}".format(position_right, position_down))

#search

option_variable = StringVar(root)
option_variable.trace_add("write", changed_value)
option_menu = ttk.OptionMenu(root, option_variable,"Title", "Title", "Author", "ISBN")
option_menu.grid(row = 0, column = 3)

search_entry = ttk.Entry(root)
search_entry.grid(column = 1, row = 0)
search_button = ttk.Button(root, text='Search', command=search)
search_button.grid(column = 2, row = 0)

#Title settings
title_label = ttk.Label(root, text = "Title  ", background = "#e0b72f", font = ("Times New Roman", 19))
title_label.grid(row = 1, column=0, sticky=W)
title_text = StringVar()
title_entry = ttk.Entry(root, width=15, textvariable=title_text)
title_entry.grid(row = 1, column=1, sticky = W)
title_entry.focus_set()

#Author settings
author_label = ttk.Label(root, text = "Author  ",background = "#e0b72f", font = ("Times New Roman", 19))
author_label.grid(row = 1, column=2, sticky=W)
author_text = StringVar()
author_entry = ttk.Entry(root, width=15, textvariable=author_text)
author_entry.grid(row = 1, column=3, sticky = W)


#ISBN settings
isbn_label = ttk.Label(root, text = "ISBN  ",background = "#e0b72f", font = ("Times New Roman", 19))
isbn_label.grid(row = 1, column=4, sticky=W)
isbn_text = StringVar()
isbn_entry = ttk.Entry(root, width=15, textvariable=isbn_text)
isbn_entry.grid(row = 1, column=5, sticky = W)


#window for displaying books with scrollbar

tree= ttk.Treeview(root, column=("column1", "column2", "column3", "column4"), show='headings')
tree.heading("#1", text="ID")
tree.column("#1", minwidth=0, width=100)
tree.heading("#2", text="TITLE")
tree.column("#2", minwidth=0, width=100)
tree.heading("#3", text="AUTHOR")
tree.column("#3", minwidth=0, width=100)
tree.heading("#4", text="ISBN")
tree.column("#4", minwidth=0, width=100)
tree.grid(row=3,column=1, columnspan=6,sticky=W + E,pady=40,padx=10)
tree.bind('<<TreeviewSelect>>', get_selected_row)

#control buttons
ttk.Style().configure("TButton", padding=4, font = ("Times New Roman", 14))
add_button = ttk.Button(root, text="Add a Book", command=add_records)
add_button.grid(row=2, column = 3, sticky = W)


modify_button = ttk.Button(root, text="Modify", command=update_record)
modify_button.grid(row=15, column = 1)

delete_button = ttk.Button(root, text="Delete a Book", command=delete_record)
delete_button.grid(row=15, column = 2)

view_button = ttk.Button(root, text="View all records", command=view_records)
view_button.grid(row=15, column = 3)

clear_button = ttk.Button(root, text="Clear screen", command=clear_screen)
clear_button.grid(row=15, column = 4)

exit_button = ttk.Button(root, text="Exit App", command=on_closing)
exit_button.grid(row=15, column = 5)



root.mainloop()

