from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.config.update(
    MAIL_SERVER ='smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail_user'],
    MAIL_PASSWORD=  params['gmail_password']
)
mail = Mail(app)
if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']

db = SQLAlchemy(app)



class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)
    postalcode = db.Column(db.Integer, primary_key=False)
    Model= db.Column(db.String(120), nullable=False)





@app.route("/")
def index2():
    return render_template('index.html',params=params)
@app.route("/index")
def index():
    return render_template('index.html',params=params)
@app.route("/about")
def about():
    return render_template('about.html',params=params)


@app.route("/booking")
def services():
    return render_template('booking.html',params=params)

@app.route("/brand")
def portfoliio():
    return render_template('brand.html',params=params)



@app.route("/special")
def team():
    return render_template('special.html',params=params)



@app.route("/contact", methods = ['GET', 'POST'])
def contactus():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        pc=request.form.get('pc')
        md=request.form.get('md')
        entry = Contacts(name=name, phone_num=phone, msg=message, date=datetime.now(), email=email,postalcode=pc,Model=md)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message in Techmobile from ' + name,
                          sender=email,
                          recipients=[params['gmail_user']],
                          body=message + "\n" + md + "\n" +phone

                          )




    return render_template('contact.html',params=params)








