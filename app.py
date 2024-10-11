import os
from flask import Flask
from models.data_models import db

# Initialize Flask app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data/library.sqlite')

# SQLAlchemy configuration to use the absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect the database with the Flask app
db.init_app(app)

# Create the database and tables (only needs to run once)
with app.app_context():
    db.create_all()

# Example route for testing (optional)
@app.route('/')
def home():
    return "Welcome to the Digital Library!"

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)