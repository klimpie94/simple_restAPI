from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# we don't need jsonify with flask-restful, it's being jsonified automatically by flask-rest
class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
            type=float,
            required=True,
            help="This field cannot be left blank!"
        )
    parser.add_argument("store_id",
            type=int,
            required=True,
            help="Every item needs a store id!"
        )    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        
        if item:
            return item.json()
        return {"Message": "Item not found"}, 404  # if not, return http status code, 404 NOT FOUND

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exists"}, 400 # The request went wrong

        data = Item.parser.parse_args()

        item = ItemModel(name, data["price"], data["store_id"])

        try:
            item.save_to_db()
        except:
            return {"Message": "An error occured while inserting the item."}, 500 # Internal Server Error, (The server messed up)

        return item.json(), 201 # return http status 201 Created, you could also return 202 Accepted (if it takes longer time to create)...

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"Message": "Item deleted!"}

    def put(self, name): # idempotent
        
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):

    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]} # or list(map(lambda x: x.json, ItemModel.query.all()))