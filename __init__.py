__author__ = 'ashutosh.banerjee'
from flask import Flask
from mongoengine import connect
#from delmart.views import CustomJSONEncoder
db = connect('entities', host='localhost', port=27017)
# def connect():
#     connection = MongoClient("localhost",27017)
#     handle = connection["entities"]
#     #handle.authenticate("demo-user","12345678")
#     return handle

app = Flask(__name__)

def register_blueprints(app):
    # Prevents circular imports
    from delmart.views import shipments
    app.register_blueprint(shipments)

register_blueprints(app)
# app.json_encoder = CustomJSONEncoder
if __name__ == '__main__':
    app.run()