from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.sql import func 
import datetime
import os
app = Flask(__name__)
app.debug = True

basedir = os.path.abspath(os.path.dirname(__file__))

'''
app.config['mysql://root:password@host:3306/localhost'] ='sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql-pymysql://root:password@host:3306/localhost'

app.config['SQLALCEHMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
'''


@app.route("/")
def home():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())

@app.route("/contact")
def contact():
    tickers = ['This is apple.',
               'This is microsoft',
               'This is google',
               'This is facebook',
               ]
    return render_template('contact.html', tickers=tickers)

@app.route("/trade")
def trade():
    return render_template('trade.html')

@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')

@app.route("/transaction")
def transaction():
    return render_template('transaction.html')


@app.route("/account")
def account():
    return render_template('account.html')

@app.route("/newacc")
def newacc():
    return render_template('newacc.html')


#Models
'''
class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String[10])
    price = db.Column(db.Float)
    date = db.Column(db.DateTime, default=func.now())

    def __init__(self, ticker, price):
        self.ticker = ticker
        self.price = price

    def __repr__(self):
        return f'{self.ticker} at {self.price}'
'''
    
