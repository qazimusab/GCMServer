import sqlite3
from flask import Flask
from flask import jsonify
from flask import g
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)
mail = Mail(app)

app.config.update(
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USE_TLS=False,
    MAIL_USERNAME='musab.ahmed@gmail.com',
    MAIL_PASSWORD='23201994Cc'
)

mail = Mail(app)
DATABASE = 'database.db'
names = ["Habib", "Okanla"]
apiKey = "APA91bHARLcYAZ-zHZUL99bSEdpVbigGRH7TSn9CH44ov8ss6O8FKC9D6O58s3zNf4YwQmkVWLinq2dTv6hYB1ZgrWfNJUBupvuRzu_c7DX0949t7J-Ls1LWaZ97fuyLtWzK1JnvhuGU"
projectNumber = "933940496191"


def connect_db():
    return sqlite3.connect(DATABASE)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


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


@app.route('/get_all_devices', methods=['GET'])
def get_devices():
    return jsonify({'devices': query_db('select * from devices')})


@app.route('/drop_devices_table', methods=['POST'])
def drop_devices_table():
    cursor = get_db().cursor()
    query = "DROP TABLE devices;"
    cursor.execute(query)
    cursor.close()
    get_db().commit()


@app.route("/device_registration_id/<device_id>", methods=['POST'])
def post_dev_id(device_id):
    cursor = get_db().cursor()
    query = "CREATE TABLE IF NOT EXISTS devices (id VARCHAR(500) NOT NULL PRIMARY KEY);"
    cursor.execute(query)
    query = "INSERT INTO devices (id) VALUES ('" + device_id + "');"
    cursor.execute(query)
    cursor.close()
    get_db().commit()


@app.route("/send_location/<url>", methods=['POST'])
def send_location(url):
    send_email('Location', 'musab.ahmed@gmail.com', ['musab.ahmed@gmail.com'], "http://www.google.com/maps/place/"+url, None)
    return "Sent"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
