from flask import Flask, render_template
from pymongo import MongoClient


app = Flask(__name__)

# MongoDB parameters
mongodb_uri = "#######"
mongo_db_name = "#####"
mongo_collection_name = "#####"

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client[mongo_db_name]
collection = db[mongo_collection_name]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all_data')
def AllData():
    cursor = collection.find()
    data = list(cursor)
    return render_template('DataTable.html', data=data)

@app.route('/alerts')
def Alerts():
    cursor = collection.find({
        "temperature": {
            "$gte": 14.00,
            "$lte": 27.00
        },
        "humidity": {
            "$gte": 10,
            "$lte": 76
        }
    })

    # Convert string values to decimal
    data = list(cursor)
    for entry in data:
        entry["temperature"] = float(entry["temperature"])
        entry["humidity"] = float(entry["humidity"])

    return render_template('Alerts.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
