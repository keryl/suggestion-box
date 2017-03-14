from flask import Flask, request, session, render_template, redirect, flash

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home_logged_out.html', title='Home')

# signup route

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    # if GET, display signup page
    return render_template('signup.html', title='Sign Up')

# login route

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Login')

# logout route

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    return redirect("/")

# start app

if __name__ == "__main__":
    app.run(port=3000, debug=True)
