from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Initialize Flask app
app = Flask(__name__)

# SQLAlchemy configuration to use SQLite file in the 'data' directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
