import sqlite3
from flask import Flask
from flask import jsonify
from flask import g

app = Flask(__name__)

DATABASE = 'database.db'
names = ["Habib", "Okanla"]
apiKey = "APA91bHARLcYAZ-zHZUL99bSEdpVbigGRH7TSn9CH44ov8ss6O8FKC9D6O58s3zNf4YwQmkVWLinq2dTv6hYB1ZgrWfNJUBupvuRzu_c7DX0949t7J-Ls1LWaZ97fuyLtWzK1JnvhuGU"
projectNumber = "933940496191"


def connect_db():
    return sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
    return db

@app.before_request
def before_request():
    g.db = get_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        get_db().close()


@app.route('/get_project_number', methods=['GET'])
def get_project_number():
    return jsonify({'projectNumber': projectNumber})


@app.route("/device_registration_id/<device_id>", methods=['POST'])
def post_dev_id(device_id):
    cursor = get_db().cursor()
    query = "CREATE TABLE IF NOT EXISTS devices (id VARCHAR(500) NOT NULL PRIMARY KEY);"
    cursor.execute(query)
    query = "INSERT INTO devices (id) VALUES ('" + device_id + "');"
    cursor.execute(query)
    cursor.close()
    get_db().commit()


if __name__ == '__main__':
    app.run(host="0.0.0.0")