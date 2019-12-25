CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR (50) UNIQUE NOT NULL,
    password VARCHAR (50) NOT NULL
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR (50) UNIQUE NOT NULL,
    title VARCHAR (50) NOT NULL,
    author VARCHAR (50) NOT NULL,
    year VARCHAR (4) NOT NULL
);
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    rating INTEGER CHECK (rating > 0 AND rating < 6),
    text VARCHAR (500) NOT NULL, 
    user_id INTEGER REFERENCES users,
    book_id INTEGER REFERENCES books
);
