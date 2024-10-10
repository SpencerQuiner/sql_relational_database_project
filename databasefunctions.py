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

#This function is used to add a new author to the author table and pass back the new ID number.
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

#This function is use to choose an author when adding a new book to the library.
def select_author():
    author_choice = ''
    while author_choice != 'cancel':
        authors = get_author_list()
        author_choice = input('\nSelect an author from the list by number or type "new" to add a new author or "cancel" to return to the main menu: ').strip().lower()
        if author_choice == 'new':
            author_choice = add_author()
        elif author_choice == 'cancel':
            return None
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
    return author_id  

#This function is used to add a new book to the library. It calls the select_author function to find out which author the book is related too. 
def add_book():
    author_id = select_author()
    if author_id == None:
        return
    else:
        title = input('Enter book title: ')
        isbn = input('Enter ISBN: ')
        published = input('Enter year of publication: ')

        connection = sqlite3.connect('library.db')
        cursor = connection.cursor()

        cursor.execute('INSERT INTO books (title, isbn, year_published, author_id) VALUES (?, ?, ?, ?)', (title, isbn, published, author_id))
        connection.commit()

        print(f"\nBook Added: {title} (ISBN: {isbn}) by Author ID: {author_id} published {published}")
        connection.close()

#This function pulls a list of books in the library
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

#this function is used to remove a book permenantly from the list.
def delete_book():
    
    book_to_delete = ''
    while book_to_delete != 'cancel':
        get_book_list()#displays list of books in the library
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

#Gets a list of users from the database and displays them.
def get_user_list():
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
#gets the data from the library user table.
    cursor.execute('SELECT user_id, user_fname, user_lname FROM library_users ORDER BY user_lname')
    users = cursor.fetchall()
#prints out the data pulled from the table.
    print('\n Book List:')
    for idx, user in enumerate(users, start=1):
        print(f'{idx}. {user[1]} {user[2]}(ID: {user[0]})')
#closes the connection to the database.
    connection.close()
    return users

#This function is used to add a new user to the table of library users.
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

#this function is used to check out a book to a library user.
def checkout_book():
    get_user_list() #pulls a list of user to choose from.
    library_user = input('\nEnter user ID: ')
    choice = 0
    while True:
        print('Book Check out menu.\n')
        print('1. Checkout book to current user.')
        print('2. Return to main menu.')
    
        choice = input('\nEnter selection: ')
        try:
            choice = int(choice)
        except ValueError:
            print('Invalid selection. please choose and option from the list.\n')

        if choice == 1:
            get_book_list()#pulls a list of books.
            book = input('Enter Book ID: ')
            chkout_date = datetime.datetime.now().date().strftime('%Y-%m-%d')#gets the current date and formats it for use by SQL.

            connection = sqlite3.connect('library.db')
            cursor = connection.cursor()

            cursor.execute('INSERT INTO borrow_record (user_id, book_id, checkout_date) VALUES (?,?,?)',(library_user, book, chkout_date))
            connection.commit()
            connection.close()

        elif choice == 2:
            break
        else:
            print('Invalid selection, please choose an option from the list\n')

#thsi function is used to mark a book as returned.
def return_book():
    get_user_list()#displays list of users to choose from.
    library_user = input('\nEnter user ID: ')
    choice = 0
    while True:
        print('Book Check out menu.\n')
        print('1. Mark book as returned.')
        print('2. Return to main menu.')
    
        choice = input('\nEnter selection: ')
        try:
            choice = int(choice)
        except ValueError:
            print('Invalid selection. please choose and option from the list.\n')

        if choice == 1:
            get_book_list()
            book = input('Enter Book ID: ')
            return_date =datetime.datetime.now().date().strftime('%Y-%m-%d')#gets current date to use as return date.

            connection = sqlite3.connect('library.db')
            cursor = connection.cursor()

            cursor.execute('UPDATE borrow_record SET return_date = ? WHERE book_id = ? AND user_id = ? AND return_date IS NULL',(return_date, book, library_user))#updates borrow record with return_date.
            connection.commit()
            connection.close()
        elif choice == 2:
            break
        else:
            print('Invalid selection, please choose an option from the list\n')

#this function pulls a list of books checked out depending on the query passed by the reports function.
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
    print('\nChecked Out Books:')
    for book in checked_out_books:
        if len(book)==4:
            title, checkout_date, user_fname, user_lname = book
            print(f'Title: {title}, Checked out on: {checkout_date}, Borrowed by: {user_fname} {user_lname}\n')
        elif len(book)==3:
            title, user_fname, user_lname = book
            print(f'Title: {title}, Borrowed by: {user_fname} {user_lname}\n')
        elif len(book)==2:
            title, checkout_date = book
            print(f'Title: {title}, Checked out on: {checkout_date}\n')

    connection.close()

#this function gets the numbers of books checked out in various situations.
def get_checkout_numbers(query, user= None, date= None):
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()

    if user is not None:
        cursor.execute(query, (user,))
        count = cursor.fetchone()[0]
        print(f'The user with ID {user} currently has {count} books checked out.\n')
        
    elif date is not None:
        cursor.execute(query, (date,))
        count = cursor.fetchone()[0]
        print(f'Number of books checked out on {date}: {count}\n')  
        
    else:
        cursor.execute(query)
        count = cursor.fetchone()[0]
        print(f'Total number of books currently checked out: {count}\n')
    
    connection.close()

# opens a report menu and calls functions to run certain sql querys. 
def reports():
    selection = 0
    while True:
        print('1. All checked out books.')
        print('2. books checked out by a specific user.')
        print('3. books checked out on a specific date.')
        print('4. Number of books Checked out to a specific user.')
        print('5. Total number of books checked out.')
        print('6. Number of book checked out on a specific date.')
        print('7. return to main menu.')
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
            date = input('Enter user date (YYYY-MM-DD): ')
            query = '''SELECT books.title, library_users.user_fname, library_users.user_lname
            FROM borrow_record
            JOIN books ON borrow_record.book_id = books.book_id
            JOIN library_users ON borrow_record.user_id = library_users.user_id
            WHERE borrow_record.checkout_date = ?;'''
            get_checked_out_list(query, date =date)

        elif selection == 4:
            get_user_list()
            user = input('Enter the ID of the user: ')
            query = '''SELECT COUNT(*)
            FROM borrow_record
             WHERE user_id = ? AND return_date IS NULL;'''
            get_checkout_numbers(query, user)

        elif selection ==5:
            query = '''SELECT COUNT(*)
            FROM borrow_record
            WHERE return_date IS NULL;'''
            get_checkout_numbers(query)

        elif selection ==6:
            date = input('Enter user date (YYYY-MM-DD): ')
            query = '''SELECT COUNT(*)
            FROM borrow_record
            WHERE checkout_date = ? AND return_date IS NULL;'''
            get_checkout_numbers(query, date=date)

        else:
            return
        
