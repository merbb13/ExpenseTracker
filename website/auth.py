from sqlite3 import IntegrityError
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .expense import db
from flask_login import login_user, login_required, logout_user, current_user
import re


def is_valid_email(email):
    # Check if email contains @ and .
    if "@" not in email or "." not in email:
        return False

    parts = email.split("@")
    if len(parts) != 2:
        return False  # Invalid if there are multiple @ symbols

    username, domain = parts
    dot_splits = domain.split(".")

    # Ensure the dot is not the last character and no empty segments
    if len(dot_splits) < 2 or any(len(part) == 0 for part in dot_splits):
        return False

    return True


auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password.', category='error')
        else:
            flash('User does not exist', category='error')
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password1 = request.form.get('password1')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email is already registered', category='error')
        elif not is_valid_email(email) or len(email) < 4:
            flash('Invalid Email', category='error')
        elif len(username) < 4:
            flash('Username should have 4 characters or more', category='error')
        elif len(password) < 6:
            flash('Password should have 6 characters or more', category='error')
        elif password1 != password:
            flash('Confirm password should match password', category='error')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email,
                            password=hashed_password)

            try:
                print("Attempting to commit new user to DB...")
                db.session.add(new_user)
                db.session.commit()
                print("User successfully committed!")

                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
            except IntegrityError:
                db.session.rollback()
                flash("Email already in use. Choose a different one.",
                      category="error")
                return redirect(url_for('auth.signup'))

    return render_template("sign_up.html", user=current_user)
