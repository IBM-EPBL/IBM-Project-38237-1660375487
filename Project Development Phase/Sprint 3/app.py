from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
from flask_session import Session
import ibm_db
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=gsb32688;PWD=zf9ZX1tCsEJaN3K0",'','')
print("connection successful")
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
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt) 
        account = ibm_db.fetch_assoc(stmt)
        if account:
            return render_template("login.html")
        else:
            insert_sql = "INSERT INTO users VALUES (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, fullname)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, phone)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)
            return redirect(url_for("login"))
    else:
        return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        session["email"] = email
        sql = "SELECT * FROM users WHERE email =? and password =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt) 
        account = ibm_db.fetch_assoc(stmt)
        if account:
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["email"] = None
    return redirect(url_for("login"))

@app.route('/profile', methods=['POST', "GET"])
def profile():
    if 'email' in session:
        checkingEmail = session["email"]
        check_sql = "SELECT * FROM users WHERE email =?"
        check_stmt = ibm_db.prepare(conn, check_sql)
        ibm_db.bind_param(check_stmt,1,checkingEmail)
        ibm_db.execute(check_stmt) 
        account = ibm_db.fetch_assoc(check_stmt)
        print(account)
        return render_template('profile.html',userprofile = account)
    else:
        return render_template('error.html')

@app.route('/viewJobs')
def viewJobs():
    return render_template('viewJobs.html')

@app.route('/viewDetail/<int:jobID>')
def viewDetail(jobID):
    return render_template('jobDetail.html',id=jobID)

@app.route('/applyJob/<int:jobID>')
def applyJob(jobID):
    return render_template('applyJob.html',id=jobID)

@app.route('/confirmation',methods=['POST', "GET"])
def sendMail():
    if 'email' in session:
        sendGridEmail = session["email"]
        sendGird_sql = "SELECT * FROM users WHERE email =?"
        sendGrid_stmt = ibm_db.prepare(conn, sendGird_sql)
        ibm_db.bind_param(sendGrid_stmt,1,sendGridEmail)
        ibm_db.execute(sendGrid_stmt) 
        account = ibm_db.fetch_assoc(sendGrid_stmt)
        recipient = account["EMAIL"]
        message = Mail(
            from_email='agneslily.23ec@licet.ac.in',
            to_emails=recipient,
            subject='You have applied successfully',
            html_content='<div><strong>Good day, Your application has been successfully submitted. Stay calm and hope for the best.</strong></div>')
        try:
            sg = SendGridAPIClient("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")
            response = sg.send(message)
            print(response.status_code,"successfully sent")
            return redirect(url_for("viewJobs"))
        except Exception as e:
            print(e.body)
    else:
        return redirect(url_for('login')) 

if __name__ == "__main__":
    app.run('0.0.0.0',port=8080,debug=True)