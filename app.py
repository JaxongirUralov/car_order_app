import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- Persistent SQLite folder on Render ---
BASE_DIR = '/opt/render/project/data'
os.makedirs(BASE_DIR, exist_ok=True)

DB_PATH = os.path.join(BASE_DIR, 'orders.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database model ---
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    model = db.Column(db.String(50))
    color = db.Column(db.String(50))

# --- Create database if it doesn't exist ---
with app.app_context():
    db.create_all()

# --- Routes ---
@app.route('/')
def index():
    return render_template('order.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    model = request.form['model']
    color = request.form['color']
    new_order = Order(name=name, model=model, color=color)
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return "✅ Thank you! Your order has been submitted."

@app.route('/admin')
def admin():
    orders = Order.query.all()
    return render_template('admin.html', orders=orders)

# --- Debug route to check database path ---
@app.route('/db_path')
def db_path():
    return DB_PATH

if __name__ == '__main__':
    app.run(debug=True)
