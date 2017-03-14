from flask import Flask, request, session, render_template, redirect, flash

# create app

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

if __name__ == "__main__":
    app.run(port=3000, debug=True)
