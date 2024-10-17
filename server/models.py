from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)  # Ensures name is unique and not null
    phone_number = db.Column(db.String, nullable=False)  # Phone number can't be null
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name.")
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author:
            raise ValueError(f"Author with name '{name}' already exists.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        # Ensure the phone number contains exactly 10 digits and is all numeric
        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits.")
        if len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'



class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)  # Title can't be null
    content = db.Column(db.String, nullable=False)  # Content can't be null
    category = db.Column(db.String, nullable=False)  # Category can't be null
    summary = db.Column(db.String, nullable=False)  # Summary can't be null
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validator for content, summary, category, and title
    @validates('content')
    def validate_content(self, key, content):
        # Ensures that content is at least 250 characters
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        # Ensures that summary is a maximum of 250 characters
        if len(summary) > 250:
            raise ValueError("Summary must be a maximum of 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        # Ensures that category is either 'Fiction' or 'Non-Fiction'
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'.")
        return category

    @validates('title')
    def validate_title(self, key, title):
        # Ensures that the title contains one of the clickbait keywords
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Title must contain a clickbait phrase: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
