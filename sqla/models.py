from flask_sqlalchemy import SQLAlchemy


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
    
    
