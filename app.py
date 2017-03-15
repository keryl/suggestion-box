from flask import Flask, request, session, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug import generate_password_hash, check_password_hash

# create app
app = Flask(__name__)

# set sqlite connection url in app config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///suggestion-box.db'

# set the app secret key
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# create db with help of alchemy
db = SQLAlchemy(app)

# db tables

# user db table class
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    suggestions = db.relationship('Suggestion', backref='suggestion', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = self.gen_password(password)

    def gen_password(self, password):
        """function to encrypt and return the given password"""
        return generate_password_hash(password)

    def check_password(self, password):
        """function to check if the provided password matches the current password for the user"""
        return check_password_hash(self.password, password)

# suggestion db table class
class Suggestion(db.Model):
    __tablename__ = "suggestions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(255))
    flaged = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='suggestion', lazy='dynamic')

# comment db table class
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestions.id'))

# vote db model class
class Vote(db.Model):
    __tablename__ = "votes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestions.id'))
    up_vote = db.Column(db.Boolean, default=True) # whether is up or down vote

# flag db model class
class Flag(db.Model):
    __tablename__ = "flags"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestions.id'))

# define routes/ pages

# home route
@app.route("/")
def home():
    user = get_current_user()
    if user:
        # query any existing suggestions
        suggestions = Suggestion.query.filter_by(flaged=False).all()
        # and render the "home_logged_in" template, passing the user record along
        return render_template('home_logged_in.html', title='Home', user=user, suggestions=suggestions)
    else:
        # if user is logged out, display public page
        return render_template('home_logged_out.html', title='Home')

# signup route
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    error = None

    if request.method == 'POST':
        # if POST, add user to database

        user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(user)
        try:
            db.session.commit()

            # then redirect to login page

            flash('You have successfully signed up! Please login!')

            return redirect("/login")
        except IntegrityError:
            error = 'A user already exists with that username'

    # if GET, display signup page
    return render_template('signup.html', title='Sign Up', error=error)

# login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        # if POST, check if an existing user exists in the DB
        # if so, log them in i.e.

        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            session["user_id"] = user.id

            flash('You were successfully logged in')

            return redirect("/")
        else:
            error = 'Invalid username/password'

    # if GET, display login page
    return render_template('login.html', title='Login', error=error)

# new-suggestion route
@app.route("/new-suggestion", methods=['GET', 'POST'])
def new_suggestion():
    error = None

    # get current user
    user = get_current_user()

    # if user is not logged, redirect to login page
    if not user:
        return redirect('/login')

    if request.method == 'POST':

        # if POST, create suggestion
        suggestion = Suggestion(title=request.form['title'], description=request.form['description'], user_id=user.id, flaged=False)
        db.session.add(suggestion)
        db.session.commit()

        # after creating user, redirect to home page so user can see list of suggestions
        return redirect('/')

    # if GET, display new-suggestion page
    return render_template('new-suggestion.html', title='New Suggestion', error=error, user=user)

# individual suggestion route
@app.route("/suggestions/<int:suggestion_id>", methods=['GET'])
def detailed_suggestion(suggestion_id):
    error = None

    # get current user
    user = get_current_user()

    # if user is not logged, redirect to login page
    if not user:
        return redirect('/login')

    # get suggesiton by id
    suggestion = Suggestion.query.filter_by(id=suggestion_id).first()
    if not suggestion:
        error = "Suggestion not found"

    comments = Comment.query.filter_by(suggestion_id=suggestion_id).all()
    up_votes = Vote.query.filter_by(suggestion_id=suggestion_id, up_vote=True).all()
    down_votes = Vote.query.filter_by(suggestion_id=suggestion_id, up_vote=False).all()

    # if display suggestion page
    return render_template(
        'suggestion.html',
        title='Suggestion',
        error=error,
        user=user,
        suggestion=suggestion,
        up_votes=up_votes,
        down_votes=down_votes,
        comments=comments
    )

# comment route
@app.route("/new-comment/<int:suggestion_id>", methods=['POST'])
def new_comment(suggestion_id):
    # get current user
    user = get_current_user()

    # if user is not logged, redirect to login page
    if not user:
        return redirect('/login')

    # create comment
    comment = Comment(content=request.form['content'], suggestion_id=suggestion_id, user_id=user.id)
    db.session.add(comment)
    db.session.commit()

    # redirect to suggestion page
    return redirect('/suggestions/'+str(suggestion_id))

# upvote/down_vote route
@app.route("/new-vote/<int:suggestion_id>/<int:up_vote>", methods=['GET'])
def new_vote(suggestion_id, up_vote):
    # get current user
    user = get_current_user()

    # if user is not logged, redirect to login page
    if not user:
        return redirect('/login')

    # create vote if user has not yet voted
    vote = Vote.query.filter_by(suggestion_id=suggestion_id, user_id=user.id).first()
    if not vote:
        vote = Vote(suggestion_id=suggestion_id, user_id=user.id)
    # mark as upvoted or downvoted
    vote.up_vote = (up_vote==1)
    db.session.add(vote)
    db.session.commit()

    # # if votes are above or equal to 3, flag suggestion
    # if Vote.query.filter_by(suggestion_id=suggestion_id, up_vote=False).count() == 3:
    #     suggestion = Suggestion.query.filter_by(id=suggestion_id).first()
    #     suggestion.flaged = True
    #     db.session.add(suggestion)
    #     db.session.commit()

    # redirect to suggestion page
    return redirect('/suggestions/'+str(suggestion_id))

# logout route
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    del session["user_id"]
    return redirect("/")

# func to return the current logged in user
def get_current_user():
    # user is logged in, if their id is in session
    is_logged_in = 'user_id' in session
    if not is_logged_in:
        return
    # if logged in,
    # query user record from db
    return User.query.filter_by(id=session['user_id']).first()

# start app

if __name__ == "__main__":
    app.run(port=3000, debug=True)
