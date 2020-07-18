import sqlite3
import message_windows

class Bookdb:
    def __init__(self):
        self.connection = sqlite3.connect('book.db')
        self.c = self.connection.cursor()
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("CREATE table if not exists books(id INTEGER PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), isbn int)")
        self.connection.commit()

    def __del__(self):
        self.connection.close()
    
    def view(self):
        self.c.execute("SELECT * from books")
        return self.c.fetchall()
    
    def insert(self,title, author, isbn):
        sql = "INSERT INTO books(title, author, isbn) VALUES (?,?,?)"
        values = [title, author, isbn]
        self.c.execute(sql, values)
        self.connection.commit()
        message_windows.MessageInfoWindow(title="Book Database", message="New book was added")

    def update(self, id, title, author, isbn):
        tsql = "UPDATE books SET title=?, author=?, isbn=? WHERE id=?"
        self.c.execute(tsql, [title, author, isbn, id])
        self.connection.commit()
        message_windows.MessageInfoWindow(title="Book Database", message="The book was updated")
    
    def delete(self,id):
        delsql = "DELETE FROM books WHERE id=?"
        self.c.execute(delsql, [id])
        self.connection.commit()
        message_windows.MessageInfoWindow(title="Book Database", message="The book was deleted")

    def filter(self, selected, search_input):
        self.c.execute("SELECT * FROM books WHERE (%s) LIKE (?)" % (selected), ('%'+search_input+'%',))
        return self.c.fetchall()

