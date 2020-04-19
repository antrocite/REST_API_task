from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import sqlite3
from pathlib import Path
from flask_cors import CORS

DB_NAME = "CurrData.db"

path = Path(__file__).parent
path = str(path)
path_DB = path + '/' + DB_NAME

class CurItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('buy_rate',
        type=float,
        required= True,
        help="This field cannot be blank!"
        )
    parser.add_argument('sell_rate',
        type=float,
        required=True,
        help="This field cannot be blank!"
        )

    def get(self, name):
        con = sqlite3.connect(path_DB)
        cursor = con.cursor()

        query = "SELECT * FROM currencies WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        con.close()
        if row:
            return {'item' : {'currency' : row[0], 'buy_rate' : row[1], 'sell_rate' : row[2]}}, 200 
        else:
            return None, 404

    def post(self, name):
        item = self.get(name)

        if item[1] == 404:
            con = sqlite3.connect(path_DB)
            cursor = con.cursor()

            data = CurItem.parser.parse_args()

            new_item = []
            new_item.append(name)
            new_item.append(data['buy_rate'])
            new_item.append(data['sell_rate'])

            cursor.execute('INSERT INTO currencies(name, buy_rate, sell_rate) VALUES(?, ?, ?)', new_item)
            con.commit()
            con.close()
            return(new_item), 201
        else:
            return {'message' : "An item with name '{}' already exists.".format(name)}, 400

    def put(self, name):
        item = self.get(name)

        con = sqlite3.connect(path_DB)
        cursor = con.cursor()

        data = CurItem.parser.parse_args()

        new_item = []
        new_item.append(name)
        new_item.append(data['buy_rate'])
        new_item.append(data['sell_rate'])

        if item[1] == 404:
            cursor.execute('INSERT INTO currencies(name, buy_rate, sell_rate) VALUES(?, ?, ?)', new_item)
        else:
            new_item.append(name)
            cursor.execute('UPDATE currencies SET name=?, buy_rate=?, sell_rate=? WHERE name=?', new_item)

        con.commit()
        con.close()
        return(new_item), 201

    def delete(self, name):
        item = self.get(name)

        if item[1] != 404:
            con = sqlite3.connect(path_DB)
            cursor = con.cursor()
            cursor.execute('DELETE FROM currencies WHERE name=?', [name])
            con.commit()
            return {'deleted?' : 'Yes'}, 202
        else:
            return{'message' : "Item '{}' not found!".format(name)}, 404
        
class Curr(Resource):
    def get(self):
        con = sqlite3.connect(path_DB)
        cursor = con.cursor()

        result = cursor.execute("SELECT * FROM currencies")
        items = []
        for row in result:
            items.append({'currency': row[0], 'buy_rate': row[1], 'sell_rate': row[2]})

        con.close()

        return {'currencies' : items}, 200 if items else 404


class Home(Resource):
    def get(self):
        msg = []
        msg.append("This is home page for task 'Developer'")
        msg.append("GET /curr  to show all currencies")
        msg.append("GET /curr/<cur_name> to get a specific currency")
        msg.append("POST /curr/<cur_name> to post a specific currency :")
        msg.append("Headers : Content-Type application/json")
        msg.append("Body : { ""buy_price"" : <price>, ""sell_price"" : <price>}")
        msg.append("")
        msg.append("PUT /curr/<cur_name> to create or update currency :")
        msg.append("Headers : Content-Type application/json")
        msg.append("Body : {""buy_price"" : <price>, ""sell_price"" : <price>}")  
        msg.append("")
        msg.append("DELETE /curr/<cur_name> to delete specific currency")
    
        return {'msg' : msg}, 200
def create_DB_table():
    try:
        conn = sqlite3.connect(path_DB)
        cursor = conn.cursor()

        create_table = "CREATE TABLE currencies (name text, buy_rate real, sell_rate real)"
        cursor.execute(create_table)
    except:
        pass


app = Flask(__name__)
api = Api(app)
CORS(app)

create_DB_table()

api.add_resource(CurItem, "/curr/<string:name>")
api.add_resource(Curr, "/curr")
api.add_resource(Home, "/")

app.run(port=5001, debug = True)





