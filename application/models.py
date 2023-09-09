from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin
from sqlalchemy.sql import func

class RegisteredUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean)
    venues = db.relationship('Venues', cascade='all, delete')
    movies = db.relationship('Movie')
    shows = db.relationship('Show')
    tickets_booked = db.relationship('Ticket')

class Venues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    address = db.Column(db.String(150))
    location = db.Column(db.String(150))
    photo = db.Column(db.String(255))
    city =  db.Column(db.String(150))
    contact_no = db.Column(db.String(10))
    venue_admin_id = db.Column(db.Integer, db.ForeignKey('registered_user.id'))
    shows = db.relationship('Show', cascade='all, delete')
    tickets_booked = db.relationship('Ticket')

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poster = db.Column(db.String(255))
    title = db.Column(db.String(150))
    starring = db.Column(db.String(250))
    production_house = db.Column(db.String(150))
    tags = db.Column(db.String(150))
    movie_admin_id = db.Column(db.Integer, db.ForeignKey('registered_user.id'))
    shows = db.relationship('Show',cascade='all, delete')
    tickets_booked = db.relationship('Ticket')
    rating = db.Column(db.Integer, default = 0)
    rating_count = db.Column(db.Integer, default = 0)
    avg_rating = db.Column(db.Integer, default = 0)


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_screened = db.Column(db.Integer, db.ForeignKey('movie.id'))
    venue_screened_in = db.Column(db.Integer, db.ForeignKey('venues.id'))
    movie = db.Column(db.String(150))
    venue = db.Column(db.String(150))
    venue_address = db.Column(db.String(150))
    venue_address_link = db.Column(db.String(150))
    datetime_screened = db.Column(db.DateTime(timezone=True), default=func.now())
    venue_admin_id = db.Column(db.Integer, db.ForeignKey('registered_user.id'))
    seats_available = db.Column(db.Integer)
    cost_per_seat = db.Column(db.Integer)
    tickets_booked = db.relationship('Ticket')

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_booked = db.Column(db.Integer, db.ForeignKey('show.id'))
    movie_booked = db.Column(db.Integer, db.ForeignKey('movie.id'))
    venue_booked = db.Column(db.Integer, db.ForeignKey('venues.id'))
    user = db.Column(db.Integer, db.ForeignKey('registered_user.id'))
    movie_name = db.Column(db.String(150))
    venue_name = db.Column(db.String(150))
    venue_address = db.Column(db.String(150))
    venue_address_link = db.Column(db.String(150))
    no_of_seats = db.Column(db.Integer)
    total_cost = db.Column(db.Integer)
    show_timing = db.Column(db.DateTime(timezone=True), default=func.now())


