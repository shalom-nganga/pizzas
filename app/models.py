from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///pizza.db'
db = SQLAlchemy(app)

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

# add any models you may need. 