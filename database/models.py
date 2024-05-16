
import os
from sqlalchemy import Column, String, create_engine, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
from config import SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()

def setup_db(app, database_path=SQLALCHEMY_DATABASE_URI):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    actor_one = Actor(
        name='Mai Thu Huyền',
        age = 25,
        gender = "Female"
    )

    actor_second = Actor(
        name='Việt Anh',
        age = 30,
        gender = "Male"
    )

    movie_one = Movie(
        title='Chạy án',
        release_date='2012-10-05 11:18:42'
    )

    movie_second = Movie(
        title='Vừa đi vừa khóc',
        release_date='2015-11-02 11:18:42'
    )

    new_property_one = Property.insert().values(
        actor_id=actor_one.id,
        movie_id=movie_second.id,
    )

    new_property_second = Property.insert().values(
        actor_id=actor_second.id,
        movie_id=movie_second.id,
    )

    actor_one.insert()
    actor_second.insert()
    movie_one.insert()
    movie_second.insert()
    db.session.execute(new_property_one)
    db.session.execute(new_property_second)
    db.session.commit()

Property = db.Table(
    'Property', db.Model.metadata,
    Column('movie_id', Integer, db.ForeignKey("Movie.id")),
    Column('actor_id', Integer, db.ForeignKey("Actor.id"))
)


class Movie(db.Model):
    __tablename__ = 'Movie'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), unique=True)
    release_date = Column(DateTime, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class Actor(db.Model):
    __tablename__ = 'Actor'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    age = Column(Integer, nullable=False)
    gender = Column(String(10))
    movies = db.relationship(
        'Movie',
        secondary=Property,
        backref=db.backref('Actor', lazy=True)
    )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
