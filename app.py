from flask import Flask, request, session, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug import generate_password_hash, check_password_hash

# create app

app = Flask(__name__)

# set sqlite connection url in app config

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///suggestion-box.db'

# set the secret key

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# create db

db = SQLAlchemy(app)

# user db table class

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = self.gen_password(password)

    def gen_password(self, password):
        return generate_password_hash(password)

# login route

@app.route("/")
def home():
    is_logged_in = 'user_id' in session
    if is_logged_in:
        return render_template('home_logged_in.html', title='Home')
    else:
        return render_template('home_logged_out.html', title='Home')

# signup route

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    error = None

    if request.method == 'POST':
        # if POST, add user to database
        pass
    # if GET, display signup page
    return render_template('signup.html', title='Sign Up', error=error)

# login route

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        # if POST, check if an existing user exists in the DB
        # if so, log them in i.e.
        pass
    # if GET, display login page
    return render_template('login.html', title='Login', error=error)

# logout route

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if 'user_id' in session:
        del session["user_id"]
    return redirect("/")

# start app

if __name__ == "__main__":
    app.run(port=3000, debug=True)
