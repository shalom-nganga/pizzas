from flask import jsonify, make_response,request
from models import Restaurant, RestaurantPizza, Pizza,app,db
from flask_migrate import Migrate


migrate = Migrate(app, db)

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = []
    for restaurant in Restaurant.query.all():
        restaurant_dict = {
            "name": restaurant.name,  
            "address": restaurant.address  
        }
        restaurants.append(restaurant_dict)

    response = make_response(
        jsonify(restaurants),
        200
    )
    return response



@app.route('/restaurants/<restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        return jsonify(
            id =restaurant.id,
            name=restaurant.name,
        )
    else:
        return jsonify({'message': 'Restaurant not found'}), 404


@app.route('/restaurants/<restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        # Delete associated RestaurantPizzas first
        restaurant_pizzas = RestaurantPizza.query.filter_by(restaurant_id=restaurant_id).all()
        for restaurant_pizza in restaurant_pizzas:
            db.session.delete(restaurant_pizza)
        
        # Then delete the Restaurant
        db.session.delete(restaurant)
        db.session.commit()
        
        return '', 204  # Empty response body with HTTP status code 204 (No Content)
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/restaurants_pizzas/create', methods=['POST'])
def add_new_restaurant_pizza():
    data = request.get_json()

    # Extract the properties from the request data
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    # Check if all required properties are provided
    if price is None or pizza_id is None or restaurant_id is None:
        return jsonify({'errors': ['validation errors']}), 400

    # Check if the Pizza and Restaurant exist
    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if pizza is None or restaurant is None:
        return jsonify({'errors': ['Pizza or Restaurant not found']}), 404

    # Create a new RestaurantPizza
    new_restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
    db.session.add(new_restaurant_pizza)
    db.session.commit()

    # Return the data related to the Pizza
    return jsonify({
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    }), 201


if __name__ == '__main__':
    with app.app_context():
       db.create_all()
    app.run(port=5555)