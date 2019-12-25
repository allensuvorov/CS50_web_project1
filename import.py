import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://vjekliourmbpjj:4930b0496bd6c1895dbf1dadbeaa9dbc2cfee3699d7e7b3807ac2d91ab2c9f8d@ec2-107-21-125-211.compute-1.amazonaws.com:5432/d17niucrtkt0tk")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    import_counter = 0 # show the number of books imported to the DB
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        import_counter += 1
        print(f"Added book number {import_counter} isbn {isbn} title {title} author {author} year {year}.")
    db.commit()
    print (f"Added {import_counter} books")

if __name__ == "__main__":
    main()
