# Overview

I have never worked with SQL and code before. This project was intended to teach me a little bit of how SQL databases work and how to work with SQL in a coding language. 

I created a relational database for a library. it is setup to enable a user to add and remove books from the library as well as add library users and check books out to them. 

My purpose in writing this software was to gain experiance in creating something like this that connects relational databases and code. I like books, and I like Libraries. My program is extremely simple but it let me see how involved a simple thing like keeping track of books can be and how much effort goes into creating systems todo that job. 

{Provide a link to your YouTube demonstration. It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of how created the Relational Database.}

[Software Demo Video](https://www.youtube.com/watch?v=z_KBHuTsryE)

# Relational Database

I created a database to enable a library to control it's catalogue of books. 

The database I built had four tables. The first contained the individual books. The second contained the authors of the books. The third contained the library users, the people checking out the books. The fourth contained a record of when the books were checked out who they were checked out to, and when they were returned. Each book, author, and user had an ID number assigned that was used to connect them to each other. for example the books table had the author ID as a foreign Key, and the book ID and User ID where used to track which book was borrowed by who.

# Development Environment

this program was developed in Visual Studio Code, with sqlite3 to interface with the database.

This program is written in Python.

# Useful Websites



- [sqlite.org](https://www.sqlite.org/index.html)
- [w3schools.com - SQL tutorial](https://www.w3schools.com/sql/default.asp)
- [w3schools.com - Python tutorial](https://www.w3schools.com/python/default.asp)
- [sqlite tutorial](https://www.sqlitetutorial.net/)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}

- a GUI would make using this program much easier
- I need to build in more error handeling
- The database could be expanded to track other data like the genre of the books
- new functions like ones that enable searching the database for books based on who the author is or what genre or year of publication.