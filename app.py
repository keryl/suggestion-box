from flask import Flask, request, session, render_template, redirect, flash

app = Flask(__name__)

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
