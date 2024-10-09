import sqlite3

def setup_database():

#connect to or create the database
    connection = sqlite3.connect('library.db')

#setting up the cursor that makes it possible to interact with the database.
    cursor = connection.cursor()

#use cursor.execute function to create each of the tables in the database. This database has 6 tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books(
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100) NOT NULL,
        isbn INTEGER(13),
        year_published INTEGER(4) NOT NULL,
        author_id INTEGER,
        FOREIGN KEY(author_id) REFERENCES authors(author_id))
        ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS authors(
        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fname VARCHAR(100) NOT NULL,
        lname VARCHAR(100) NOT NULL)
        ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS genre(
        genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre_name VARCHAR(100) NOT NULL)
        ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS book_genre(
        book_id INTEGER,
        genre_id INTEGER,
        FOREIGN KEY(book_id) REFERENCES books(book_id),
        FOREIGN KEY(genre_id) REFERENCES genre(genre_id))
        ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS library_users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_fname VARCHAR(45) NOT NULL,
        user_lname VARCHAR(45) NOT NULL)
        ''')

#This table stores a record of everytime a book is borrowed and who borrowed it. 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS borrow_record(
        user_id INTEGER,
        book_id INTEGER,
        checkout_date DATE NOT NULL,
        return_date DATE,
        FOREIGN KEY(user_id) REFERENCES library_users(user_id),
        FOREIGN kEY(book_id) REFERENCES books(book_id))
        ''')
#saves the changes made 
    connection.commit()

#closes the connection to the database to avoid tying up system resources unnecessarily.
    connection.close()
    print('Database setup successfully.')


