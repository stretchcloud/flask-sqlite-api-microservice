from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import uuid


db_connect = create_engine('sqlite:///titanic.db')
app = Flask(__name__)
api = Api(app)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Titanic"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###


class Passengers(Resource):
    def get(self):
        conn = db_connect.connect() 
        query = conn.execute("select * from titanic") 
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor.fetchall()]}
        return jsonify(result)

class Passenger_UUID(Resource):
    def get(self, UUID):
        conn = db_connect.connect()
        query = conn.execute("select * from titanic where UUID =?", (UUID))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class PassengersPost(Resource):
    def post(self):
        conn = db_connect.connect()
        survived = request.json['survived']
        passengerClass = request.json['passengerClass']
        name = request.json['name']
        sex = request.json['sex']
        age = request.json['age']
        siblingsOrSpousesAboard = request.json['siblingsOrSpousesAboard']
        parentsOrChildrenAboard = request.json['parentsOrChildrenAboard']
        fare = request.json['fare']
        UUID = uuid.uuid1()
        conn.execute("insert into titanic values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(survived, passengerClass, name, sex, age, siblingsOrSpousesAboard, parentsOrChildrenAboard, fare, UUID))
        return jsonify(dict(request.json, uuid=UUID))

class PassengersDel(Resource):
    def delete(self, UUID):
        conn = db_connect.connect()
        conn.execute("delete from titanic where UUID =?", (UUID))
        

class PassengersPut(Resource):
    def put(self, UUID):
        conn = db_connect.connect()
        print(request.json)
        passenger = {
        'survived' : request.json['survived'],
        'passengerClass' : request.json['passengerClass'],
        'name' : request.json['name'],
        'sex' : request.json['sex'],
        'age' : request.json['age'],
        'siblingsOrSpousesAboard' : request.json['siblingsOrSpousesAboard'],
        'parentsOrChildrenAboard' : request.json['parentsOrChildrenAboard'],
        'fare' : request.json['fare'],
        }
        conn.execute("update titanic set Survived=?, Pclass=?, Name=?, Sex=?, Age=?, 'Siblings/Spouses Aboard'=?, 'Parents/Children Aboard'=?, Fare=? where UUID =(UUID)", (passenger['survived'], passenger['passengerClass'], passenger['name'], passenger['sex'], passenger['age'], passenger['siblingsOrSpousesAboard'], passenger['parentsOrChildrenAboard'], passenger['fare']))


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


api.add_resource(Passengers, '/people', methods = ['GET'])
api.add_resource(Passenger_UUID, '/people/<UUID>', methods = ['GET'])
api.add_resource(PassengersPost, '/people/', methods = ['POST'])
api.add_resource(PassengersDel, '/people/<UUID>', methods = ['DELETE'])
api.add_resource(PassengersPut, '/people/<UUID>', methods = ['PUT'])


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')
