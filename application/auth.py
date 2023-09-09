from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from.models import RegisteredUser
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .views import views
import re

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user = RegisteredUser.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Login successful',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password',category='error')
        else:
            flash('Account does not exist, please Register',category='error')
    return render_template('login.html',user=current_user)

@auth.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        name=request.form.get('name')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user_type=request.form.get('user_type')
        print(user_type)
        if password1!=password2:
            flash('Passwords are not matching',category='error')
        elif len(name) < 3:
            flash('Name must be more than 2 characters',category='error')
        else:
            user=RegisteredUser.query.filter_by(email=email).first()
            if user:
                flash('Account already exists, please login',category='warning')
            else:
                if user_type=="1":
                    new_user=RegisteredUser(email=email,name=name,password=generate_password_hash(password1,method='sha256'),is_admin=True)
                else:
                    new_user=RegisteredUser(email=email,name=name,password=generate_password_hash(password1,method='sha256'),is_admin=False)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created',category='success')
                return redirect(url_for('views.home'))
    return render_template('sign_up.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))