from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app
from flask_login import login_user, login_required, logout_user, current_user
from .models import RegisteredUser, Venues, Movie, Show, Ticket
from . import db
import os
import secrets
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
def home():
    shows=Show.query.all()
    movies=Movie.query.order_by(Movie.id.desc()).all()
    return render_template('home.html',user=current_user,movies=movies)

@views.route('/search')
def search():
    query = request.args.get('query')
    results = []
    if query:
        try:
            rating = float(query)
            results = Movie.query.filter(Movie.rating >= rating).all()
        except ValueError:
            results = Movie.query.filter((Movie.title.ilike(f'%{query}%')) | (Movie.tags.ilike(f'%{query}%'))).all()
    return render_template('search.html', movies=results, query=query,user=current_user)






@views.route('/movies')
@login_required
def movies():
    if current_user.is_admin==True:
        movies=Movie.query.order_by(Movie.id.desc()).all()
        return render_template('movies.html',user=current_user,movies=movies)
    return redirect(url_for('views.home'))






#movies




@views.route('/add_movies',methods=['GET','POST'])
@login_required
def add_movies():
    if current_user.is_admin==True:
        if request.method=='POST':
            movie_title=request.form.get('title')
            movie_starring=request.form.get('starring')
            movie_production_house=request.form.get('production_house')
            movie_tags=request.form.get('tags')
            movie_poster=save(request.files['poster'])
            if len(movie_title)>=1 and len(movie_starring)>=1 and len(movie_production_house)>=1:
                new_movie=Movie(poster=movie_poster,title=movie_title,starring=movie_starring,production_house=movie_production_house,tags=movie_tags,movie_admin_id=current_user.id)
                db.session.add(new_movie)
                db.session.commit()
                flash('Successful',category='success')
                return redirect(url_for('views.movies'))
            else:
                flash('Make sure that you have entered all the fields correctly',category='error')
                return render_template('add_movies.html',user=current_user)
        else:
            return render_template('add_movies.html',user=current_user)
    return redirect(url_for('views.home'))





@views.route('/update_movies/<int:id>',methods=['POST','GET'])
@login_required
def update_movies(id):
    if current_user.is_admin==True:
        movie_to_update=Movie.query.get(int(id))
        if request.method=='POST':
            movie_to_update.poster=save(request.files['poster'])
            movie_to_update.title=request.form.get('title')
            movie_to_update.starring=request.form.get('starring')
            movie_to_update.production_house=request.form.get('production_house')
            movie_to_update.tags=request.form.get('tags')
            db.session.commit()
            flash('Successful',category='success')
            return redirect(url_for('views.movies'))
        else:
            if movie_to_update:
                return render_template('update_movies.html',user=current_user,movie=movie_to_update)
    else:
        return redirect(url_for('movies.home'))



    

@views.route('/delete_movies/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_movies(id):
    if current_user.is_admin==True:
        if request.method == 'GET':
                return render_template('deleteconfirmmovies.html', id=id,user=current_user)
        else:
            movie_to_delete=Movie.query.get(int(id))
            try:
                db.session.delete(movie_to_delete)
                db.session.commit()
                flash("Successful")
                return redirect(url_for('views.movies'))
            except:
                flash("Unsuccessful")
                return redirect(url_for('views.movies'))





#venues





@views.route('/my_venues')
@login_required
def my_venues():
    if current_user.is_admin==True:
        venues=Venues.query.all()
        return render_template('my_venues.html',user=current_user,venues=venues)
    return redirect(url_for('views.home'))





@views.route('/select_venues/<int:id>')
def select_venues(id):
    shows=Show.query.filter_by(movie_screened=int(id)).all()
    movie=Movie.query.get(int(id))
    if shows:
        return render_template('select_venues.html',user=current_user,shows=shows,movie=movie)
    else:
        flash('This movie has no shows currently',category='note')
        return redirect(url_for('views.home'))





@views.route('/add_venues',methods=['GET','POST'])
@login_required
def add_venues():
    if current_user.is_admin==True:
        if request.method=='POST':
            venue_name=request.form.get('name')
            venue_address=request.form.get('address')
            venue_location=request.form.get('location')
            venue_city=request.form.get('city')
            venue_contact_no=request.form.get('contact_no')
            venue_photo=save_images(request.files['photo'])
            if len(venue_name)>=1 and len(venue_address)>=1 and len(venue_location)>=1 and len(venue_city)>=1:
                new_venue = Venues(name=venue_name,address=venue_address,location=venue_location,city=venue_city,contact_no=venue_contact_no,venue_admin_id=current_user.id,photo=venue_photo)
                db.session.add(new_venue)
                db.session.commit()
                flash('Successful',category='success')
                return redirect(url_for('views.my_venues'))
            else:
                flash('Make sure that you have entered all the fields correctly',category='error')
                return render_template('add_venues.html',user=current_user)
        else:
            return render_template('add_venues.html',user=current_user)
    return redirect(url_for('views.home'))





@views.route('/update_venues/<int:id>',methods=['POST','GET'])
@login_required
def update_venues(id):
    if current_user.is_admin==True:
        theatre_to_update=Venues.query.get(int(id))
        if request.method=='POST':
            theatre_to_update.name=request.form.get('name')
            theatre_to_update.photo=save_images(request.files['photo'])
            db.session.commit()
            flash('Successful',category='success')
            return redirect(url_for('views.my_venues'))
        else:
            if theatre_to_update:
                return render_template('update_venues.html',user=current_user,venue=theatre_to_update)
    else:
        return redirect(url_for('views.home'))
    




@views.route('/delete_venues/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_venues(id):
    if current_user.is_admin==True:
        if request.method == 'GET':
                return render_template('deleteconfirmvenues.html', id=id,user=current_user)
        else:
            theatre_to_delete=Venues.query.get(int(id))
            try:
                db.session.delete(theatre_to_delete)
                db.session.commit()
                flash("Successful")
                return redirect(url_for('views.my_venues'))
            except:
                flash("Unsuccessful")
                return redirect(url_for('views.my_venues'))



@views.route('/venue/<int:id>', methods=['POST', 'GET'])
@login_required
def venue(id):
    venue=Venues.query.get(int(id))
    return render_template('venue.html',id=id,venue = venue,user=current_user)




#tickets





@views.route('/my_tickets')
@login_required
def my_tickets():
    return render_template('my_tickets.html',user=current_user)

@views.route('/rating/<int:id>',methods=['POST','GET'])
@login_required
def rating(id):
    if request.method=='GET':
        return render_template('rating.html', user=current_user)
    else:
        movie=Movie.query.get(int(id))
        user_rating = request.form.get('rating')
        movie.rating_count += 1
        movie.rating += int(user_rating)
        movie.avg_rating = round(movie.rating / movie.rating_count,2)
        db.session.add(movie)
        db.session.commit()
        return render_template('my_tickets.html', user=current_user)
        
        





@views.route('/book_tickets/<int:id>',methods=['GET','POST'])
@login_required
def book_tickets(id):
    if current_user.is_admin==False:
        show_to_book=Show.query.get(int(id))
        if request.method=='POST':
            venue=Venues.query.filter_by(name=str(show_to_book.venue)).first()
            ticket_no_of_seats=request.form.get('no_of_seats')
            show_to_book.seats_available=int(show_to_book.seats_available)-int(ticket_no_of_seats)
            new_ticket=Ticket(show_booked=show_to_book.id,movie_booked=show_to_book.movie_screened,venue_booked=show_to_book.venue_screened_in,user=current_user.id,movie_name=show_to_book.movie,venue_name=show_to_book.venue,venue_address=venue.address,venue_address_link=venue.location,no_of_seats=ticket_no_of_seats,total_cost=int(show_to_book.cost_per_seat)*int(ticket_no_of_seats),show_timing=show_to_book.datetime_screened)
            db.session.add(new_ticket)
            db.session.commit()
            flash('Successful', category='success')
            return redirect(url_for('views.my_tickets'))
        else:
            return render_template('book_tickets.html',user=current_user,show=show_to_book)
    else:
        return redirect(url_for('views.select_venues'))





#shows





@views.route('/add_shows',methods=['GET','POST'])
@login_required
def add_shows():
    movies=Movie.query.order_by(Movie.id.desc()).all()
    venues=Venues.query.filter_by(venue_admin_id=int(current_user.id)).all()
    if current_user.is_admin==True:
        if request.method=='POST':
            show_movie_screened=Movie.query.filter_by(title=request.form.get('movie_screened')).first().id
            if show_movie_screened:
                show_venue_screened_in=request.form.get('venue_screened_in')
                show_movie=request.form.get('movie_screened')
                show_venue=Venues.query.filter_by(id=request.form.get('venue_screened_in')).first()
                show_date_time_screened=datetime.strptime(request.form.get('date_time_screened'), '%Y-%m-%dT%H:%M')
                show_seats_available=request.form.get('seats_available')
                show_cost_per_seat=request.form.get('cost_per_seat')
            else:
                flash('Movie does not exist',category='warning')
                return render_template('add_shows.html',user=current_user,movies=movies,venues=venues)

            if show_movie_screened>=1 and int(show_seats_available)>=1:
                new_show=Show(movie_screened=show_movie_screened,venue_screened_in=show_venue_screened_in,movie=show_movie,venue=show_venue.name,venue_address=show_venue.address,venue_address_link=show_venue.location,datetime_screened=show_date_time_screened,venue_admin_id=current_user.id,seats_available=show_seats_available,cost_per_seat=show_cost_per_seat)
                db.session.add(new_show)
                db.session.commit()
                flash('Successful',category='success')
                return redirect(url_for('views.my_venues'))
            else:
                flash('Make sure that you have entered all the fields correctly',category='error')
                return render_template('add_shows.html',user=current_user,movies=movies,venues=venues)
            
        else:
            return render_template('add_shows.html',user=current_user,movies=movies)
        
    else:
        return render_template('home.html',user=current_user,movies=movies)





@views.route('/update_shows/<int:id>',methods=['POST','GET'])
@login_required
def update_shows(id):
    if current_user.is_admin==True:
        show_to_update=Show.query.get(int(id))
        if request.method=='POST':
            show_to_update.seats_available=request.form.get('seats_available')
            show_to_update.cost_per_seat=request.form.get('cost_per_seat')
            show_to_update.datetime_screened=datetime.strptime(request.form.get('datetime_screened'),'%Y-%m-%dT%H:%M')
            db.session.commit()
            flash('Successful',category='success')
            return redirect(url_for('views.my_venues'))
        else:
            movies=Movie.query.order_by(Movie.id.desc()).all()
            venues=Venues.query.all()
            if show_to_update:
                return render_template('update_shows.html',user=current_user,show=show_to_update,movies=movies,venues=venues)
    else:
        return redirect(url_for('views.home'))
    





@views.route('/delete_shows/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_shows(id):
    if current_user.is_admin==True:
        if request.method=='GET':
                return render_template('deleteconfirmshows.html', id=id,user=current_user)
        else:
            show_to_delete=Show.query.get(int(id))
            try:
                db.session.delete(show_to_delete)
                db.session.commit()
                flash("Successful")
                return redirect(url_for('views.my_venues'))
            except:
                flash("Unsuccessful")
                return redirect(url_for('views.my_venues'))





@views.route('show_tickets/<int:id>')
@login_required
def show_tickets(id):
    if current_user.is_admin==True:
        tickets=Ticket.query.filter_by(show_booked=int(id)).all()
        show=Show.query.get(int(id))
        return render_template('show_tickets.html',user=current_user,tickets=tickets,show=show,no_of_tickets=len(tickets))
    else:
        return render_template('home.html',user=current_user,movies=movies)





def save(poster):
    hash_photo=secrets.token_urlsafe(10)
    _, file_extension=os.path.splitext(poster.filename)
    image_name=hash_photo+file_extension
    file_path=os.path.join(current_app.root_path,'static/movie_posters',image_name)
    poster.save(file_path)
    return image_name

def save_images(photo):
    hash_photo=secrets.token_urlsafe(10)
    _, file_extension=os.path.splitext(photo.filename)
    image_name=hash_photo+file_extension
    file_path=os.path.join(current_app.root_path,'static/venue_posters',image_name)
    photo.save(file_path)
    return image_name
