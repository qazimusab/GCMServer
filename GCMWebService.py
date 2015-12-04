from flask import Flask
from flask import jsonify, request, abort

app = Flask(__name__)

names = ["Habib", "Okanla"]
apiKey = "APA91bHARLcYAZ-zHZUL99bSEdpVbigGRH7TSn9CH44ov8ss6O8FKC9D6O58s3zNf4YwQmkVWLinq2dTv6hYB1ZgrWfNJUBupvuRzu_c7DX0949t7J-Ls1LWaZ97fuyLtWzK1JnvhuGU"
projectNumber = "933940496191"


@app.route('/')
def hello_world():
    return 'Hello World Jason!!'


@app.route('/get_names', methods=['GET'])
def get_tasks():
    return jsonify({'names': names})


@app.route('/get_api_key', methods=['GET'])
def get_api_key():
    return jsonify({'apiKey': apiKey})



@app.route('/get_project_number', methods=['GET'])
def get_project_number():
    return jsonify({'projectNumber': projectNumber})


# #Add 2 numbers passed as json.
@app.route('/add', methods=['POST'])
def add_nums():
    if not request.json or not 'num1' in request.json or not 'num2' in request.json:
        abort(400)
    return jsonify({'result': request.json['num1'] + request.json['num2']}), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0")