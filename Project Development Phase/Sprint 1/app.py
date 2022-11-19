from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key ="any random string"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register',methods = ['POST', 'GET'])
def register():
    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["email"] = None
    return redirect(url_for("login"))

@app.route('/profile', methods=['POST', "GET"])
def profile():
    if 'email' in session:
        return render_template('error.html')

if __name__ == "__main__":
    app.run('0.0.0.0',port=8080,debug=True)