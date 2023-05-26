from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://user-images.githubusercontent.com/43302778/106805462-7a908400-6645-11eb-958f-cd72b74a17b3.jpg"

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False, unique=True)

    last_name = db.Column(db.String(50), nullable=False, unique=True)

    image_url = db.Column(db.String(100), nullable=False, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """Return the full name of the user"""

        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):
    """Blog post"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.text, nullable=False)
    created_at =db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    
class PostTag(db.Model):
    """Tag on a blog post"""
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):
    """Tag that can be added to a given post"""
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

