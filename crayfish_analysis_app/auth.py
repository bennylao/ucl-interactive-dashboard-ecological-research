from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db

main_bp = Blueprint('auth', __name__)

@main_bp.route('/')
@main_bp.route("/home")
@login_required
def home():
    """Returns home page """
    return render_template('home.html', name=current_user.username)

@main_bp.route("/signup", methods=['GET','POST'])
def signup():
    """Render signup page and handle signup form submission"""
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short', category='error')
        elif len(password1)< 6:
            flash('Password is too short', category='error')
        elif len(email) <4:
            flash('email is invalid', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('auth.home'))

    return render_template('signup.html')

@main_bp.route("/login", methods=['GET','POST'])
def login():
    """Returns login page"""
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html')

@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))

# @main_bp.route('/about', methods=['GET',])
# def about():
#     """Returns about page """
#     return 'Returns about page'

# @main_bp.route('/user/<username>')
# def user(username):
#     """Returns user account page """
#     return f"Returns account page for {username}"