from datetime import datetime
import os
from flask import Flask, flash, redirect, render_template, request, url_for
from models.data_models import Author, Book, db

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Used for flashing messages


basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "data/library.sqlite")

# SQLAlchemy configuration to use the absolute path
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect the database with the Flask app
db.init_app(app)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        name = request.form["name"]
        birth_date = request.form["birth_date"]
        date_of_death = request.form["date_of_death"]

        # Convert birth_date and date_of_death to date objects (if provided)
        birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date() if birth_date else None
        date_of_death_obj = datetime.strptime(date_of_death, '%Y-%m-%d').date() if date_of_death else None

        # Create a new Author instance
        new_author = Author(name=name, birth_date=birth_date_obj, date_of_death=date_of_death_obj)

        # Add author to the database
        db.session.add(new_author)
        db.session.commit()

        # Flash success message
        flash("Author added successfully!", "success")
        return redirect(url_for("add_author"))

    return render_template("add_author.html")


# Route to add books
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        isbn = request.form["isbn"]
        publication_year = request.form["publication_year"]
        author_id = request.form["author_id"]

        # Create a new Book instance
        new_book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=author_id,
        )

        # Add book to the database
        db.session.add(new_book)
        db.session.commit()

        # Flash success message
        flash("Book added successfully!", "success")
        return redirect(url_for("add_book"))

    # Get all authors to display in the dropdown
    authors = Author.query.all()
    return render_template("add_book.html", authors=authors)


# Create the database and tables (only needs to run once)
# with app.app_context():
#     db.create_all()


# Home page route
@app.route("/")
def home():
    # Sorting logic
    sort_by = request.args.get("sort_by", "title")  # Default to sorting by title
    if sort_by == "author":
        books = (
            Book.query.join(Author).order_by(Author.name).all()
        )  # Sort by author name
    else:
        books = Book.query.order_by(Book.title).all()  # Sort by book title

    return render_template("home.html", books=books)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
