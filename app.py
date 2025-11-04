from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- Database setup ---
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'orders.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print("Database path:", app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)

# --- Database model ---
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    model = db.Column(db.String(50))
    color = db.Column(db.String(50))

# --- Create the database file if not exists ---
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

if __name__ == '__main__':
    app.run(debug=True)
