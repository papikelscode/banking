
from locale import currency
import re
from turtle import pos
from flask import Flask, render_template, request, redirect, url_for,jsonify,abort
# from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from werkzeug.security  import generate_password_hash, check_password_hash
from  flask_login import UserMixin, LoginManager, login_required, login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
#from flask_migrate import Migrate, MigrateCommand
#from flask_script import Manager
#from sys import argv


from random import randint
from datetime import datetime
#from flask_marshmallow import Marshmallow



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname((__file__)))
database = "app.db"
con = sqlite3.connect(os.path.join(basedir,database))

app.config['SECRET_KEY'] = "jhkxhiuydu"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)



class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.Integer)
    dob = db.Column(db.Integer)
    sex = db.Column(db.String(255))
    house_address = db.Column(db.String(255))
    city =  db.Column(db.String(255))
    postal_code = db.Column(db.Integer)
    country = db.Column(db.String(255))
    state = db.Column(db.String(255))
    currency =  db.Column(db.String(255))
    national_id = db.Column(db.Integer)
    employer_address =  db.Column(db.String(255))
    employ_type =  db.Column(db.String(255))
    salary = db.Column(db.Integer)
    name_kin =  db.Column(db.String(255))
    kin_work =  db.Column(db.String(255))
    password =  db.Column(db.String(500))
    con_password =  db.Column(db.String(500))
    account_type = db.Column(db.String(255))
    passport = db.Column(db.String(255))
    account_number = db.Column(db.String(255))
    Book_balance = db.Column(db.String(255))
    loan_limit = db.Column(db.String(255))
    card_limit = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    transactions = db.relationship('Transactions', backref='users', lazy=True)
    payments = db.relationship('Payments', backref='users', lazy=True)


    referID = db.Column(db.String(500),unique=True)

    def check_password(self, password):
            return check_password_hash(self.password, password)
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')


    def create(self, Firstname='',  email='', lastname='', phone='', dob='', sex='', house_address='', city='', postal_code='', country='', state='', currency='', national__id='',  employer_address='', employ_type='', salary='', name_kin='', kin_work='', password='', con_password='' , account_type='' , passport='', referID=''):
        self.Firstname	 = Firstname
        self.email	 = email
        self.lastname 	 = lastname
        account_type = account_type
        phone = phone
        dob = dob
        sex = sex
        house_address = house_address
        city = city
        postal_code = postal_code
        country = country
        state = state
        currency = currency
        national__id = national__id
        employer_address = employer_address
        employ_type = employ_type
        salary = salary
        name_kin = name_kin
        kin_work = kin_work
        password = password
        con_password = con_password
        passport = passport
        self.referID = referID
        self.password= generate_password_hash(password, method='sha256')


    def save(self):
        db.session.add(self)
        db.session.commit()

    def commit(self):
        db.session.commit()

class Transactions(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    txtype = db.Column(db.String(255))
    cost = db.Column(db.String(255))
    timestamp = db.Column(db.String(255),default=datetime.now())
    user = db.Column(db.Integer, db.ForeignKey(User.id))

class Payments(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    paymentID = db.Column(db.String(500),unique=True)
    confirm = db.Column(db.Boolean,default=False)
    paymentwallet = db.Column(db.String(500))
    user = db.Column(db.Integer, db.ForeignKey(User.id))




class Secure(ModelView):
    def is_accessible(self):

        return current_user.is_authenticated
    

admin = Admin(app, name='administration', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Transactions, db.session))

login_manager = LoginManager()
login_manager.login_view = "signin"
login_manager.init_app(app)
@login_manager.user_loader
def user_loader(homepage_id):
    return User.query.get(homepage_id)





@app.route('/')
def index():
    return render_template('index.html')
@app.route('/services.html')
def service():
    return render_template('services.html')
@app.route('/home.html')
def about():
    return render_template('home.html')
@app.route('/dash.html')
def dash():
    return render_template('dash.html')
@app.route('/loans.html')
def loans():
    return render_template('loans.html')
@app.route('/personal.html')
def personal():
    return render_template('personal.html')
@app.route('/saving.html')
def saving():
    return render_template('saving.html')
@app.route('/login.html')
def login():
    return render_template('login.html')
@app.route('/signup.html')
def register():
    return render_template('signup.html')

@app.route('/apply.html')
def apply():
    return render_template('apply.html')
@app.route('/transfer.html')
def modal():
    return render_template('transfer.html')
@app.route('/profile.html')
def profile():
    return render_template('profile.html')
@app.route('/modals.html')
def modals():
    return render_template('modal.html')




@login_required
def profile():
    siteSettings = Settings.query.all()
    return render_template('profile.html', siteSettings=siteSettings)

@app.route("/signin",methods=['GET','POST'])
def signin():
    users = User()
    if request.method == "POST":
        data = request.json
        userByusername = users.query.filter_by(username=data['username']).first()
        userByemail = users.query.filter_by(email=data['username']).first()
        mainUser = None
        #sir at this point i need help 
        #if current_user.is_admin == True:
            #return redirect('admin')
        if userByusername:
            mainUser = userByusername
        if userByemail:
            mainUser = userByemail
        if mainUser.active==False:
            return jsonify({"status":401,'msg':"your accoubt has been deactivated"})
        if mainUser:
            if mainUser.check_password(data['password']):
                login_user(mainUser,remember=True,fresh=True)
                return jsonify({'status':200,'msg':'user authenticated'})
            return jsonify({"status":404,"msg":"Inavlid password provided!!!"})
        return jsonify({"status":404,"msg":"invalid email or username"})

    return render_template("signin.html")




@app.route("/signup",methods=['GET','POST'])
def signup():
   
    if request.method == 'POST':
        data = request.json
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        phone = data['phone']
        dob = data['dob']
        house_address = data['house_address']
        city = data['city']
        postal_code = data['postal']
        country = data['country']
        state = data['state']
        currency = data['currency']
        national_id = data['id_card']
        employer_address = data['employer_address']
        employ_type = data['work']
        salary = data['salary']
        name_kin = data['name_kin']
        kin_work = data['kin_work']
        password = data['password']
        con_password =data['confirm']
        account_type = data['account_type']
        passport = data['passport']
        if User.query.filter_by(national_id= national_id).first():
            return jsonify({"status":404,"msg":"national ID already exist!!!"})
        if User.query.filter_by(email=email).first():
            return jsonify({"status":404,"msg":"email already exist!!!"})
        User.create(firstname=firstname,
                            lastname = lastname,
                            email=email,
                            phone =phone,
                            dob = dob,
                            house_address = house_address,
                            city = city,
                            postal_code = postal_code,
                            country = country,
                            state = state,
                            currency = currency,
                            national_id = national_id,
                            employer_address = employer_address,
                            employ_type = employ_type,
                            salary = salary,
                            name_kin = name_kin,
                            kin_work = kin_work,
                            password= password,
                            con_password = con_password,
                            account_type= account_type,
                            passport = passport,
                            referID=randint(456463276,7656562565))
        User.save()

        login_user(User)
        # return redirect(url_for("dashboard"))
        return jsonify({'status':200,"msg":"registration compelete!!!"})

    return render_template("signup.html")

@app.route('/payments',methods=['POST'])
def makepayment():
    data = request.json
    if Payments.query.filter_by(paymentID=data['paymentID']).first():
        return jsonify({'status':404,'msg':'payment already exist'})
    new_payment = Payments(
        paymentID=data['paymentID'],
        user = current_user.id,
        paymentwallet=data['walletid'])
    new_transaction = Transactions(description='Account funding',
                                    txtype='Payment Deposit',
                                    user=current_user.id)
    db.session.add(new_transaction)
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'status':200,'msg':'payement submmited'})
    
















@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login.html"))



@app.route("/db")
def database():
    db.drop_all()
    db.create_all()
    return "Hello done!!!"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)