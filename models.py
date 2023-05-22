import datetime
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin


db: SQLAlchemy = SQLAlchemy()
bcrypt: Bcrypt = Bcrypt()


class Users(db.Model, UserMixin):

    __tablename__: str = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text(), nullable=True)
    create_at = db.Column(db.DateTime(), defalute=datetime.datetime.now)
    updated_at = db.Column(db.DateTime(), defalute=datetime.datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    is_staff = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Define the relationships between tables
    articles = db.relationship(
        'Articles', backref='users', lazy=True, cascade='all, delete')
    comments = db.relationship(
        'Comments', backref='users', lazy=True, cascade='all, delete')
    favorites = db.relationship(
        'Favorites', backref='users', lazy=True, cascade='all, delete')
    follows = db.relationship(
        'Follows', backref='users', lazy=True, cascade='all, delete')
    notifications = db.relationship(
        'Notifications', backref='users', lazy=True, cascade='all, delete')
    likes = db.relationship('Likes', backref='users',
                            lazy=True, cascade='all, delete')

    def __init__(self, username: str, email: str, password: str, bio: str, is_active: bool, is_admin: bool, is_staff: bool) -> None:

        self.username = username
        self.email = email
        self.password = password
        self.bio = bio
        self.is_active = is_active
        self.is_admin = is_admin
        self.is_staff = is_staff

    def __repr__(self) -> str:
        return f"User('{self.username}' , '{self.email}', '{self.password}')"

    @classmethod
    def create_admin(cls, username: str, email: str, password: str, bio: str) -> None:
        """
        Creates a Admin and saves it to the database.
        """
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        admin = cls(username=username, email=email,
                    password=password, bio=bio, is_admin=True, is_staff=True, is_active=True)
        db.session.add(admin)
        db.session.commit()

    @classmethod
    def create_user(cls, username: str, email: str, password: str, bio: str) -> None:
        """
        Creates a new regular user and saves it to the database.
        """
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = cls(username=username, email=email,
                   password=password, bio=bio, is_admin=False, is_staff=False, is_active=True)
        db.session.add(user)
        db.session.commit()

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def update(self) -> None:
        self.username
        self.email
        self.password = bcrypt.generate_password_hash(
            self.password).decode('utf-8')
        self.bio

        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict[str]:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
        }


class Articles(db.Model):

    __tablename__: str = 'articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    body = db.Column(db.Text(), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)

    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Define the relationships between tables
    comments = db.relationship(
        'Comments', backref='articles', lazy=True, cascade='all, delete')
    favorites = db.relationship(
        'Favorites', backref='articles', lazy=True, cascade='all, delete')
    likes = db.relationship('Likes', backref='articles',
                            lazy=True, cascade='all, delete')

    def __init__(self, title: str, slug: str, body: str, category: str, author_id: int) -> None:

        self.title = title
        self.slug = slug
        self.body = body
        self.category = category
        self.author_id = author_id

    def __repr__(self) -> str:
        return f"Article('{self.title}', '{self.body}')"

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        self.title
        self.slug
        self.body
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict[str]:
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "body": self.body,
            "category": self.category,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "author_id": self.author_id,
        }


class Comments(db.Model):

    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)

    commenter_id = db.Column(
        db.Integer, ForeignKey('users.id'), nullable=False)
    article_id = db.Column(db.Integer, ForeignKey(
        'articles.id'), nullable=False)


class Favorites(db.Model):

    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    article_id = db.Column(db.Integer, ForeignKey(
        'articles.id'), unllable=False)
    favorited_by_id = db.Column(
        db.Integer, ForeignKey('users.id'), unllable=False)


class Follows(db.Model):

    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    follower_id = db.Column(db.Integer, ForeignKey(
        'users.id'), unllable=False)
    followed_id = db.Column(db.Integer, ForeignKey(
        'users.id'), unllable=False)


class Notifications(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text(), nullable=False)

    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    sender_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)


class Likes(db.Model):

    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    article_id = db.Column(db.Integer, ForeignKey(
        'articles.id'), nullable=False)
