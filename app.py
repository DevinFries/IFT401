from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Hashed password for security
    cash_balance = db.Column(db.Float, default=0.0)
    is_admin = db.Column(db.Boolean, default=False)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    ticker = db.Column(db.String(10), unique=True, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    initial_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    transactions = db.relationship('Transaction', backref='stock', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    action = db.Column(db.String(10), nullable=False)  # Buy or Sell
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

# Initialize the database
db.create_all()

# Generate initial stock data (for demonstration purposes)
def generate_initial_stocks():
    stocks_data = [
        {"company_name": "Apple Inc.", "ticker": "AAPL", "volume": 1000, "initial_price": 150.0},
        {"company_name": "Microsoft Corporation", "ticker": "MSFT", "volume": 800, "initial_price": 300.0},
        {"company_name": "Alphabet Inc.", "ticker": "GOOGL", "volume": 600, "initial_price": 2500.0},
        {"company_name": "Facebook, Inc.", "ticker": "FB", "volume": 700, "initial_price": 350.0}
    ]
    for stock_data in stocks_data:
        stock = Stock(**stock_data)
        stock.current_price = stock.initial_price  # Set current price initially
        db.session.add(stock)
    db.session.commit()

# Check if initial stocks are already generated
if not Stock.query.first():
    generate_initial_stocks()

# Define routes
@app.route("/")
def home():
    stocks = Stock.query.all()
    return render_template('index.html', stocks=stocks)

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/trade", methods=['GET', 'POST'])
def trade():
    if request.method == 'POST':
        stock_ticker = request.form['stock_ticker']
        number_of_shares = int(request.form['number_of_shares'])
        action = request.form['action']  # Buy or sell
        user = User.query.first()  # For demonstration purposes, get the first user

        stock = Stock.query.filter_by(ticker=stock_ticker).first()
        if stock:
            total_cost = number_of_shares * stock.current_price
            if action == 'buy':
                if total_cost <= user.cash_balance:
                    # Deduct cash balance
                    user.cash_balance -= total_cost
                    # Update stock volume
                    stock.volume += number_of_shares
                    # Record transaction
                    transaction = Transaction(user_id=user.id, stock_id=stock.id, action='Buy', quantity=number_of_shares, price=stock.current_price)
                    db.session.add(transaction)
                    flash('Stock purchased successfully', 'success')
                else:
                    flash('Insufficient funds', 'failure')
            elif action == 'sell':
                if number_of_shares <= stock.volume:
                    # Add cash balance
                    user.cash_balance += total_cost
                    # Update stock volume
                    stock.volume -= number_of_shares
                    # Record transaction
                    transaction = Transaction(user_id=user.id, stock_id=stock.id, action='Sell', quantity=number_of_shares, price=stock.current_price)
                    db.session.add(transaction)
                    flash('Stock sold successfully', 'success')
                else:
                    flash('Insufficient shares to sell', 'failure')
            db.session.commit()
        else:
            flash('Invalid stock ticker', 'failure')

        return redirect(url_for('trade'))

    return render_template('trade.html')

@app.route("/portfolio")
def portfolio():
    user = User.query.first()  # For demonstration purposes, get the first user
    return render_template('portfolio.html', user=user)

@app.route("/transaction_history")
def transaction_history():
    user = User.query.first()  # For demonstration purposes, get the first user
    transactions = user.transactions
    return render_template('transaction_history.html', transactions=transactions)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Check if user is authenticated and authorized as admin
        # For demonstration
