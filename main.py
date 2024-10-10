import databasesetup
import databasefunctions

def main():
    selection = 0
    databasesetup.setup_database()

    while True:
        print('Welcome to the library administration system.\n')
        print('1. Add new book.\n')
        print('2. Remove book.\n')
        print('3. Add new library User.\n')
        print('4. Checkout book.\n')
        print('5. Return book.\n')
        print('6. Reports.\n')
        print('7. Exit program.')

        selection = input('what would you like to do? ')

        try:
            selection = int(selection)
        except ValueError:
            print('Invalid selection, please select a number between 1 and 7.')
            continue

        if selection == 1:
            databasefunctions.add_book()
            print('add book selected')
        elif selection == 2:
            databasefunctions.delete_book()
        elif selection == 3:
            databasefunctions.add_user()
        elif selection == 4:
            databasefunctions.checkout_book()
        elif selection == 5:
            databasefunctions.return_book()
        elif selection == 6:
            databasefunctions.reports()
        elif selection == 7:
            print('Program exiting . . .')
            break
        else:
            print('Invalid selection, please select a number between 1 and 7.')

if __name__ == '__main__':
    main()