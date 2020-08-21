from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model"""

    __tablename__ = users

    username = db.Column(db.Text(20), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text(50), nullable=False, unique=True)
    first_name = db.Column(db.Text(30), nullable=False)
    last_name = db.Column(db.text(30), nullable=False)