# Project 1

Course: Web Programming with Python and JavaScript
Project1: Books
Link: https://docs.cs50.net/web/2019/x/projects/1/project1.html
Structure: Web Browser - Server - Database
Description: basic CRUD web application with user registration, login, book search, review submision, review display, review data from API, and API access.

## Project Files:
1. Create.sql
    * creates tables (users, books, reviews) by running these Postgres commands. Set data types and restrictions.
2. import.py
    * imports books.csv to remote DB on Heroku. 
    * idjustments of the initially provided code: 
        - On line 7 where create_engine removed "os.getenv("
        - and replaced DATABASE_URL with the URI of the remote DB.
        - added import_counter to monitor the import process
3. layout.html
    * the HTML template for other pages
    * it has a navigation menu, with jinja2 condition
4. index.html
    * the home page, where users register or login
5. search.html
    * a search form and a jinja2 loop that lists search results
6. book.html
    * book data, review submit form, user reviews, other people's reviews, goodreads number of ratings and average rating
7. success.html
    * a simple success page with a message
8. error.html
    * a simple error page with a message
9. application.py

    * Removed that part from the original code:
        <!-- 
        # Check for environment variable
        if not os.getenv("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL is not set") -->
        
    * Function and routes:
        - index:    /
        - register: /registered
        - login:    /logged_in
        - search:   /search_result
        - logout:   /logout
        - book:     /book/<int:book_id>
   
Plan:
1. Create Tables: 
    * users: id, username, password
    * books: id, isbn, title, author, year
    * reviews: id, rating, text, user_id, book_id
2. Import books.CSV
3. Code the server with all interface pages

Good Reads API key:
key: KJpVcIfDHAmjAZxLIt1hKA
link: https://www.goodreads.com/search.xml?key=KJpVcIfDHAmjAZxLIt1hKA&q=Ender%27s+Game



