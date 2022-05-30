from flask import Flask, url_for, render_template, request, redirect, session, flash, redirect, g, Response
from flask_sqlalchemy import SQLAlchemy
#from flask import current_app
#------for password hashing----
#from werkzeug.security import generate_password_hash, check_password_hash
#-------
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_mail import *
import secrets
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import math
import uuid
import sqlite3
#from flask.ext.mail import Mail,Message
#----
from flask import Flask,send_from_directory,render_template
from flask import send_from_directory
from flask_restful import Resource, Api
from package.land import Lands, Land
from package.seller import Sellers, Seller
from package.appointment import Appointments, Appointment
from package.common import Common
from package.caveat import Caveat, Caveats
from package.landtitle import Landtitle, Landtitles
from package.location import Location, Locations
from package.buyer import Buyer, Buyers
from package.procedure import Procedure, Procedures
from package.agreement import Agreement, Agreements
from package.buy_sell_transaction import Buy_sell_transactions, Buy_sell_transaction
import json
import os



#import pyautogui
#import time
#------

#PEOPLE_FOLDER = os.path.join('static', 'images')
with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='')

#app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

bcrypt = Bcrypt(app)



api = Api(app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///employer.sqlite3'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hosp.db'
app.config['SECRET_KEY'] = '0527'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config['TESTING'] = False


app.config['MAIL_SERVER'] = 'arinetfred@gmail.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL'] = 'True'
app.config['MAIL_USE_TSL'] = 'False'
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''

db = SQLAlchemy(app)

api.add_resource(Lands, '/land')
api.add_resource(Land, '/land/<int:id>')
#api.add_resource(Projects, '/project')
#api.add_resource(Project, '/project/<int:id>')
api.add_resource(Sellers, '/seller')
api.add_resource(Seller, '/seller/<int:id>')
api.add_resource(Appointments, '/appointment')
api.add_resource(Appointment, '/appointment/<int:app_id>')
api.add_resource(Common, '/common')
api.add_resource(Caveats, '/caveat')
api.add_resource(Caveat, '/caveat/<int:code>')
api.add_resource(Landtitles, '/landtitle')
api.add_resource(Landtitle, '/landtitle/<int:land_title_no>')
api.add_resource(Procedures, '/procedure')
api.add_resource(Procedure, '/procedure/<int:buy_code>')
api.add_resource(Locations, '/location')
api.add_resource(Location, '/location/<int:plot_id>')
api.add_resource(Buyers, '/buyer')
api.add_resource(Buyer, '/buyer/<int:id>')
api.add_resource(Agreements, '/agreement')
api.add_resource(Agreement, '/agreement/<int:agreement_code>')
api.add_resource(Buy_sell_transactions, '/buy_sell_transaction')
#api.add_resource(Projects, '/projects')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    token = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    #---hashing password below added---
    #password = db.Column(db.String(128))

    #---below already present------
    def __init__(self, username, password, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        #----hashing password below added above already present---

    #@property
    #def unhashed_password(self):

    #    raise AttributeError('cannot view unhased password')

    #@unhashed_password.setter
    #def unhashed_password(self,unhashed_password):
    #    self.password = generate_password_hash(unhashed_password )
#@property
#def unhashed_password(self):
#     raise AttributeError('cannot view unhased password')

#@unhashed_password.setter
#def unhashed_password(self,unhashed_password):
#      self.password = generate_password_hash(unhashed_password )

# Routes

#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'),
#                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET','POST'])
def index():
    #full_name1 = os.path.join(app.config['UPLOAD_FOLDER'], 'case1.jpg')
    #return render_template("index.html", user_image1=full_name1)
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Hello!")
        #return render_template('index.html', message=<a href="/static/index2.html">/static/index2.html</a>")

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password'], email=request.form['email']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists or Error occured")
    else:
        return render_template('register.html')

#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'),
#                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        #u = request.form['username']
        #p = request.form['password']
        username = request.form['username']
        password = request.form['password']
        data = User.query.filter_by(username=username).first()
        #data = User.query.filter_by(username=u, password=p).first()
        if data and check_password_hash(data.password, password):
        #if data is not None:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")
@app.route('/adminlogin/', methods=['GET', 'POST'])
def adminlogin():
  #below added# 
  ##username = request.form['username']
  ##password = request.form['password']
  #owner = User.query.filter_by(email=email,password=password,admin=True).first()
  ##owner = User.query.filter_by(username=username,password=password,admin=True).first()
  ##if owner:
          #flash("Username or password is wrong")
          #return   redirect(url_for('home'))
     #else: 

          #login_user(owner)
          #flash("Welcome")
          #return   redirect(url_for('get_signin_admin'))   
  #above added #

    if request.method == 'GET':
        return render_template('adminlogin.html')
         #return render_template('static/index2.html')
    else:
        u = request.form['username']
        p = request.form['password_hash']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")
     # below case currently added #
        ##else:
       ##flash("You are not Admin")
          #return redirect(url_for('index'))
     


#rows = db.session.query(User.doctor==0,User.admin==0).count()
#appoint_rows = db.session.query(Appointments).count()
#owner = User.query.filter_by(email=current_user.email,password=current_user.password,admin=True).first()
#    if not owner:
#        flash("The logins provided is not an admin!")
#        return redirect(url_for('home'))
     
#    else:

#          return render_template('admin_dash.html' ,rows = rows )
# above added #

@app.route('/index2/', methods=['GET', 'POST'])
def index2():
    #if session.get('logged_in') and admin=True:
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return redirect(url_for(adminlogin))
        return render_template('adminlogin.html', message="Hello!")




@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))



if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p"
    db.create_all()
    app.run(debug= True,host ="localhost")
