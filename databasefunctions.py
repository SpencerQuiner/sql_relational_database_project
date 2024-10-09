import sqlite3
import datetime
#gets and prints a list of authors from the author table
def get_author_list():
    print('starting get author function')
#opens a connection to the database.
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
#gets the data from the author table.
    cursor.execute('SELECT author_id, fname, lname FROM authors ORDER BY lname')
    authors = cursor.fetchall()
#prints out the data pulled from the table.
    print('\n Author List:')
    for idx, author in enumerate(authors, start=1):
        print(f'{idx}. {author[1]}{author[2]} (ID: {author[0]})')
#closes the connection to the database.
    connection.close()
    return authors

def add_author():
    print('starting add author function')
    author_fname = input('Enter Author\'s First Name: ')
    author_lname = input('Enter Author\'s Last Name: ')

    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO authors (fname, lname) VALUES(?, ?)',(author_fname, author_lname))
    connection.commit()

    new_author_id = cursor.lastrowid
    print(f"\nNew Author Added: {author_fname} {author_lname} (ID: {new_author_id})")
    connection.close()
    return new_author_id


def add_book():
    print('begining add book fuction.')
    
    author_choice = ''
    while author_choice != 'cancel':
        authors = get_author_list()
        author_choice = input('\nSelect an author from the list by number or type "new" to add a new author or "cancel" to return to the main menu: ').strip().lower()
        if author_choice == 'new':
            author_id = add_author()
        elif author_choice == 'cancel':
            return
        else:
            try: 
                selected_index = int(author_choice)-1
                if selected_index < 0 or selected_index >= len(authors):
                    print('Invalid selection, please try again.')
                    continue

                author_id = authors[selected_index][0]
                print(f"\nSelected Author: {authors[selected_index][1]} {authors[selected_index][2]} (ID: {author_id})")
                break
            except ValueError:
                print("Invalid input. Please enter a valid number,'new' or 'cancel'.")
                continue       

    title = input('Enter book title: ')
    isbn = input('Enter ISBN: ')
    published = input('Enter year of publication: ')

    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO books (title, isbn, year_published, author_id) VALUES (?, ?, ?, ?)', (title, isbn, published, author_id))
    connection.commit()

    print(f"\nBook Added: {title} (ISBN: {isbn}) by Author ID: {author_id} published {published}")
    connection.close()

def get_book_list():
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
#gets the data from the books table.
    cursor.execute('SELECT book_id, title FROM books ORDER BY title')
    books = cursor.fetchall()
#prints out the data pulled from the table.
    print('\n Book List:')
    for idx, book in enumerate(books, start=1):
        print(f'{idx}. {book[1]} (ID: {book[0]})')
#closes the connection to the database.
    connection.close()
    return books

def delete_book():
    
    book_to_delete = ''
    while book_to_delete != 'cancel':
        books = get_book_list()
        book_to_delete = input('Enter the ID number of the book to delete or type "cancel" to return to the main menu: ').strip().lower()
        if book_to_delete == 'cancel':
            return
        else:
            try: 
                book_to_delete = int(book_to_delete)
                connection = sqlite3.connect('library.db')
                cursor = connection.cursor()
                cursor.execute('DELETE FROM books WHERE book_id= ?',(book_to_delete,))
                connection.commit()
                connection.close()
                print(f'book ID {book_to_delete} deleted.')
                break
            except ValueError:
                print("Invalid input. Please enter a valid number, or 'cancel'.")
                continue

def get_user_list():
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
#gets the data from the library user table table.
    cursor.execute('SELECT user_id, user_fname, user_lname FROM library_users ORDER BY user_lname')
    users = cursor.fetchall()
#prints out the data pulled from the table.
    print('\n Book List:')
    for idx, user in enumerate(users, start=1):
        print(f'{idx}. {user[1]} {user[2]}(ID: {user[0]})')
#closes the connection to the database.
    connection.close()
    return users

def add_user():
    get_user_list()
    user_fname = input('Enter first name: ')
    user_lname = input('Enter last name: ')

    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO library_users (user_fname, user_lname) VALUES (?, ?)', (user_fname, user_lname))
    connection.commit()

    print(f"\nUser Added: {user_fname} {user_lname}")
    
    connection.close()

def checkout_book():
    get_user_list()
    library_user = input('Enter user ID: ')
    choice = 0
    while True:
        print('Book Check out menu.\n')
        print('1. Checkout book to current user.')
        print('2. Return to main menu.')
    
        choice = input('Enter selection: ')
        try:
            choice = int(choice)
        except ValueError:
            print('Invalid selection. please choose and option from the list.')

        if choice == 1:
            get_book_list()
            book = input('Enter Book ID: ')
            currentDate = datetime.datetime.now()
            chkout_date =currentDate.strftime('%d/%m/%Y')

            connection = sqlite3.connect('library.db')
            cursor = connection.cursor()

            cursor.execute('INSERT INTO borrow_record (user_id, book_id, checkout_date) VALUES (?,?,?)',(library_user, book, chkout_date))
            connection.commit()
            connection.close()

        elif choice == 2:
            break
        else:
            print('Invalid selection, please choose an option from the list')

def return_book():
    get_user_list()
    library_user = input('Enter user ID: ')
    choice = 0
    while True:
        print('Book Check out menu.\n')
        print('1. Mark book as returned.')
        print('2. Return to main menu.')
    
        choice = input('Enter selection: ')
        try:
            choice = int(choice)
        except ValueError:
            print('Invalid selection. please choose and option from the list.')

        if choice == 1:
            get_book_list()
            book = input('Enter Book ID: ')
            currentDate = datetime.datetime.now()
            return_date =currentDate.strftime('%d/%m/%Y')

            connection = sqlite3.connect('library.db')
            cursor = connection.cursor()

            cursor.execute('UPDATE borrow_record SET return_date = ? WHERE book_id = ? AND user_id = ? AND return_date IS NULL',(return_date, book, library_user))
            connection.commit()
            connection.close()
        elif choice == 2:
            break
        else:
            print('Invalid selection, please choose an option from the list')

def get_checked_out_list(query, user= None, date= None):
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()

    if user is not None:
        cursor.execute(query, (user,))
        
    elif date is not None:
        cursor.execute(query, (date,))
        
    else:
        cursor.execute(query)
        
    checked_out_books = cursor.fetchall()
    print("\nChecked Out Books:")
    for book in checked_out_books:
        if len(book)==4:
            title, checkout_date, user_fname, user_lname = book
            print(f"Title: {title}, Checked out on: {checkout_date}, Borrowed by: {user_fname} {user_lname}")
        elif len(book)==3:
            title, user_fname, user_lname = book
            print(f"Title: {title}, Borrowed by: {user_fname} {user_lname}")
        elif len(book)==2:
            title, checkout_date = book
            print(f"Title: {title}, Checked out on: {checkout_date}")

    connection.close()

def view_borrow_books():
    selection = 0
    while True:
        print('1. All checked out books.')
        print('2. books checked out by a specific user.')
        print('3. books checked out on a specific date.')
        print('4. return to main menu.')
        selection = input('What would you like to do? ')

        try:
            selection =int(selection)
        except ValueError:
            print('Invalid selection. please choose and option from the list.')

        if selection == 1:
            query = '''SELECT books.title, borrow_record.checkout_date, library_users.user_fname, library_users.user_lname
            FROM borrow_record
            JOIN books ON borrow_record.book_id = books.book_id
            JOIN library_users ON borrow_record.user_id = library_users.user_id;'''
            get_checked_out_list(query)

        elif selection == 2:
            get_user_list()
            user = input('Enter the ID of the user: ')
            query = '''SELECT books.title, borrow_record.checkout_date
            FROM borrow_record
            JOIN books ON borrow_record.book_id = books.book_id
            WHERE borrow_record.user_id = ?;'''
            get_checked_out_list(query, user)

        elif selection == 3:
            date = input('Enter user date (DD/MM/YYYY): ')
            query = '''SELECT books.title, library_users.user_fname, library_users.user_lname
            FROM borrow_record
            JOIN books ON borrow_record.book_id = books.book_id
            JOIN library_users ON borrow_record.user_id = library_users.user_id
            WHERE borrow_record.checkout_date = ?;'''
            get_checked_out_list(query, date =date)

        else:
            return
        
