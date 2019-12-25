import os
import requests #library for requesting API data

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://vjekliourmbpjj:4930b0496bd6c1895dbf1dadbeaa9dbc2cfee3699d7e7b3807ac2d91ab2c9f8d@ec2-107-21-125-211.compute-1.amazonaws.com:5432/d17niucrtkt0tk")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    
    #check if user_id in current session has some value in it, meaning a user is logged in. If so, user is redirected to search page.
    if session.get('user_id') is not None:
        #get username of current user from database
        username = db.execute("SELECT username FROM users WHERE id = :id", {"id": session['user_id']}).fetchone()[0]
        nav_menu = True
        return render_template("search.html", username=username, nav_menu=nav_menu)

    #else they are offered to register or login.
    nav_menu = False
    return render_template("index.html", nav_menu=nav_menu)

@app.route("/registered/", methods=["POST"])
def register():
    """Register a New User."""

    # Get form information.
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Make sure the username field is not empty/spaces
    if not username.strip():
        return render_template("error.html", message="Empty username. Please enter a username.")
    
    # Make sure the password field is not empty/spaces

    if not password.strip():
        return render_template("error.html", message="Empty password. Please enter a password.")

    # Make sure the username is not in the database already.
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount != 0:
        return render_template("error.html", message=f"{username} is already registered as a user. Please try a different username.")

    # Insert new user into database.
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
    db.commit()

    return render_template("success.html", message =f"{username} is now a new registered user!")

@app.route("/logged_in", methods=["POST"])
def login():
    # Get form information.
    username = request.form.get("username")
    password = request.form.get("password")

    # Make sure the user exists.
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
        return render_template("error.html", message="No registered user with such username.")
    
    # Check entered password.    
    if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 0:    
        # if there is no match
        return render_template("error.html", message="Incorrent input. Please check the password.")
        
    # else, meaning there is a match, session user_id gets set current user ID
    session['user_id'] = db.execute("SELECT id FROM users WHERE username = :username", {"username": username}).fetchone()[0]
    
    # navigation menu is shown
    nav_menu = True
    return render_template("search.html", username=username, message=f"Hello {username}! What book are you looking for?", nav_menu=nav_menu)

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return render_template("index.html", message="You have logged out!")

@app.route("/search_result", methods=["POST", "GET"])
def search():
    
    search_string = request.form.get("search_string")
    
    #put this query in to a string variable, just for lighter code
    query = "SELECT * FROM books WHERE year LIKE :search_string OR isbn LIKE :search_string OR title LIKE :search_string OR author LIKE :search_string"

    books = db.execute(query, {"search_string": f"%{search_string}%"}).fetchall()
    
    books_found_count = db.execute(query, {"search_string": f"%{search_string}%"}).rowcount

    username = db.execute("SELECT username FROM users WHERE id = :id", {"id": session['user_id']}).fetchone()[0]
    nav_menu = True
    return render_template("search.html", username=username, books=books, nav_menu=nav_menu, message=f"Number of books found: {books_found_count} with text '{search_string}'")

@app.route("/book/<int:book_id>", methods=["POST", "GET"])
def book(book_id):
    #get selected book data from DB and put in book variable
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    
    #get review data from forms
    rating = request.form.get("rating")
    text = request.form.get("text")

    #if there is no review yet from this user for that book AND the field TEXT is not empty
    if db.execute("SELECT * FROM reviews WHERE book_id = :book_id AND user_id= :user_id", {"book_id": book_id, "user_id": session['user_id']}).rowcount == 0 and text != None: 
        #add TEXT and rating as a review to database
        db.execute("INSERT INTO reviews (text, rating, user_id, book_id) VALUES (:text, :rating, :user_id, :book_id)", {"rating": rating, "text": text, "user_id": session['user_id'], "book_id": book_id})
        db.commit()

    #selects review for that user
    user_review = db.execute("SELECT * FROM reviews WHERE book_id = :book_id AND user_id = :user_id", {"book_id": book_id, "user_id": session['user_id']}).fetchone()
    
    current_user_review_heading = "Your Review and Rating for this book"
    
    #selects reviews of other users
    other_reviews = db.execute("SELECT text, rating, username FROM reviews JOIN users ON reviews.user_id = users.id WHERE book_id = :book_id AND user_id != :user_id", {"book_id": book_id, "user_id": session['user_id']}).fetchall()
    
    other_users_reviews_heading = "Other Reviews and Ratings for this book"

    # getting goodreads ratings data via API

    res = requests.get("https://www.goodreads.com/book/review_counts.json", 
                       params={"key": "KJpVcIfDHAmjAZxLIt1hKA", "isbns": book.isbn})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()

    goodreads_average_rating = data["books"][0]["average_rating"]
    goodreads_ratings_count = data["books"][0]["work_ratings_count"]

    username = db.execute("SELECT username FROM users WHERE id = :id", {"id": session['user_id']}).fetchone()[0]
    nav_menu = True
    return render_template("book.html", username=username, book=book, nav_menu=nav_menu, other_reviews=other_reviews, user_review=user_review, current_user_review_heading=current_user_review_heading, other_users_reviews_heading=other_users_reviews_heading, goodreads_average_rating=goodreads_average_rating, goodreads_ratings_count=goodreads_ratings_count)

@app.route("/api/<string:isbn>")
def book_api(isbn):
    """Return details about a single book."""

    # Get book data.
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    # Make sure book exists.
    if book is None:
        return jsonify({"error": "Invalid isbn"}), 404

    # Get average score
    # Count reviews for that book.
    review_count = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book.id}).rowcount
    
    # Get all ratings for that book.
    ratings = db.execute("SELECT rating FROM reviews WHERE book_id = :book_id", {"book_id": book.id}).fetchall()
    
    # Count the sum of ratings for that book.
    rating_sum = 0
    for rating in ratings:
        rating_sum += rating[0]

    average_score = 0

    # Make sure review_count is not a zero
    if review_count > 0:
        average_score = rating_sum/review_count

    return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": review_count,
            "average_score": average_score,
            "rating_sum": rating_sum
        })