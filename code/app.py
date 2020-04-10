from flask import Flask
from flask_restful import Api, Resource  # a resource is just a thing or object that our api can return
from flask_jwt import JWT #jwt = Jason Web Token => encoding some data. 

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "anis" # better to use ENV variable ofcourse... Make this long, random, and secret in a real app!
jwt = JWT(app, authenticate, identity)
api = Api(app) # this allows us very easily to add the resources to it

@app.before_first_request
def create_tables():
    db.create_all() # it will create all the tables unless it exists

jwt = JWT(app, authenticate, identity) # JWT creates a new endpoint: /auth


class Student(Resource): #it inherits from the class Resource
    
    def get(self, name):
        return {"Student": name}

api.add_resource(Student, "/student/<string:name>") # access student like so: http://127.0.0.1:4999/student/Anis

# help(Student) # show method resolution order

api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")

api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=4999, debug=True)

