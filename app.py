from flask import Flask, render_template, request, session, redirect, url_for, flash, Response
from flask_bcrypt import Bcrypt
from datetime import datetime
import urllib.parse
import pymysql

from models import db, User, Expense
from analytics import get_ai_insights, calculate_health, generate_csv

# Required for PyMySQL + SQLAlchemy
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fintech_ultra_secret_2026'

# ---------------- DATABASE CONFIG (FIXED) ---------------- #

# Your actual RDS credentials
DB_USER = "taanya2630"
DB_PASSWORD = "Taanya263009"   # change if needed
DB_HOST = "database-1.cdw0cieuq78l.eu-north-1.rds.amazonaws.com"
DB_NAME = "mysql"

# Encode password (important if special chars like @)
encoded_password = urllib.parse.quote_plus(Taanya263009)

# Final DB URI (NO spaces, correct format)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:Taanya263009@database-1.cdw0cieuq78l.eu-north-1.rds.amazonaws.com:3306/expense-tracker"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)

# ---------------- AUTH ROUTES ---------------- #

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(
            username=request.form['username'],
            password=hashed_pw,
            monthly_budget=float(request.form.get('budget', 50000))
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful! Please Login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('dashboard'))
        flash('Invalid Username or Password', 'danger')
    return render_template('login.html')


# ---------------- DASHBOARD ---------------- #

@app.route('/')
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.date.desc()).all()

    total = sum(e.amount for e in expenses)
    health_score = calculate_health(total, user.monthly_budget)
    insight, projected = get_ai_insights(expenses, user.monthly_budget)

    return render_template(
        'index.html',
        user=user,
        total=total,
        score=health_score,
        insight=insight,
        expenses=expenses[:5]
    )


# ---------------- EXPENSE MANAGEMENT ---------------- #

@app.route('/expenses')
def expenses_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    expenses = Expense.query.filter_by(user_id=session['user_id']).all()
    return render_template('expenses.html', expenses=expenses)


@app.route('/add', methods=['POST'])
def add_expense():
    new_exp = Expense(
        title=request.form['title'],
        amount=float(request.form['amount']),
        category=request.form['category'],
        user_id=session['user_id']
    )
    db.session.add(new_exp)
    db.session.commit()
    flash('Transaction recorded successfully.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/delete/<int:id>')
def delete_expense(id):
    exp = Expense.query.get(id)
    if exp and exp.user_id == session['user_id']:
        db.session.delete(exp)
        db.session.commit()
    return redirect(url_for('expenses_page'))


# ---------------- EXPORT CSV ---------------- #

@app.route('/export')
def export_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    expenses = Expense.query.filter_by(user_id=session['user_id']).all()

    return Response(
        generate_csv(expenses),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=report.csv"}
    )


# ---------------- LOGOUT ---------------- #

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------------- MAIN ---------------- #

if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # creates tables in RDS

    app.run(host='0.0.0.0', port=5000, debug=True)
