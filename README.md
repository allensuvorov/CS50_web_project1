# Project1 - "Books" (Python, Flask, SQL, PostgreSQL, Heroku, API)

- Video overview of the completed project: https://youtu.be/fITOH4iQ7Tg
- Course: Web Programming with Python and JavaScript
- Specification: https://docs.cs50.net/web/2019/x/projects/1/project1.html
- Structure: Web Browser - Server - Database
- Description: basic CRUD web application with user registration, login, book search, review submision, review display, review data from API, and API access.

## Project Files:
1. Create.sql - creates tables (users, books, reviews) by running these Postgres commands. Set data types and restrictions.
2. import.py - imports books.csv to remote DB on Heroku. Adjustments of the initially provided code: 
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
    - users: id, username, password
    - books: id, isbn, title, author, year
    - reviews: id, rating, text, user_id, book_id
2. Import books.CSV
3. Code the server with all interface pages

Good Reads API key:
key: KJpVcIfDHAmjAZxLIt1hKA

https://www.goodreads.com/search.xml?key=KJpVcIfDHAmjAZxLIt1hKA&q=Ender%27s+Game

### Requirements
Alright, it’s time to actually build your web application! Here are the requirements:

- Registration: Users should be able to register for your website, providing (at minimum) a username and password.
- Login: Users, once registered, should be able to log in to your website with their username and password.
- Logout: Logged in users should be able to log out of the site.
- Import: Provided for you in this project is a file called books.csv, which is a spreadsheet in CSV format of 5000 different books. Each one has an ISBN number, a title, an author, and a publication year. In a Python file called import.py separate from your web application, write a program that will take the books and import them into your PostgreSQL database. You will first need to decide what table(s) to create, what columns those tables should have, and how they should relate to one another. Run this program by running python3 import.py to import the books into your database, and submit this program with the rest of your project code.
- Search: Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
- Book Page: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
- Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
- Goodreads Review Data: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.
API Access: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follow the format:
`{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}`
If the requested ISBN number isn’t in your database, your website should return a 404 error.

You should be using raw SQL commands (as via SQLAlchemy’s execute method) in order to make database queries. You should not use the SQLAlchemy ORM (if familiar with it) for this project.
In README.md, include a short writeup describing your project, what’s contained in each file, and (optionally) any other additional information the staff should know about your project.
If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to requirements.txt!
Beyond these requirements, the design, look, and feel of the website are up to you! You’re also welcome to add additional features to your website, so long as you meet the requirements laid out in the above specification!

