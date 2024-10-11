from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, ForeignKey, Integer, String

# Initialize the SQLAlchemy object
db: SQLAlchemy = SQLAlchemy()


# Define the Book model
class Book(db.Model):
    __tablename__ = "books"  # Table name in the database
    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto-incrementing PK
    isbn = Column(String(13), nullable=False, unique=True)  # Unique ISBN field
    title = Column(String(200), nullable=False)
    publication_year = Column(Integer, nullable=False)
    author_id = Column(
        Integer, ForeignKey("authors.id"), nullable=False
    )  # FK to Author

    # Optional: Custom string representation for debugging and display purposes
    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, isbn={self.isbn})>"

    def __str__(self):
        return f"Book: {self.title} (ISBN: {self.isbn})"


# Define the Author model
class Author(db.Model):
    __tablename__ = "authors"  # Table name in the database
    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto-incrementing PK
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=True)
    date_of_death = Column(Date, nullable=True)
    books = db.relationship(
        "Book", backref="author", lazy=True
    )  # Relationship with Book

    # Optional: Custom string representation for debugging and display purposes
    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name})>"

    def __str__(self):
        return f"Author: {self.name} (ID: {self.id})"


# Association table for the many-to-many relationship between Book and Author
book_author = db.Table(
    "book_author",
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("author_id", Integer, ForeignKey("authors.id")),
)
