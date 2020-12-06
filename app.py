from flask import Flask, jsonify
from flask import request
from flask_session import Session
import redis


app = Flask(__name__)
redis_session = redis.Redis(host='localhost', port=6379, db=0)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)


@app.route('/getquotes/<philosopher>', methods=['GET'])
def get_quote(philosopher):
    dictionary = redis_session.get(philosopher)
    json_response = jsonify(dictionary)
    return json_response


@app.route('/modifyquotes', methods=['PATCH'])
def modify_quote():
    author = request.headers.get('author')
    quotes = request.headers.get('quotes')

    redis_session.delete(author, quotes)
    return "{'status': 'success'}"


@app.route('/uploadquotes', methods=['POST'])
def upload_quote():
    author = request.headers.get('author')
    quotes = request.headers.get('quotes')

    redis_session.set(author, quotes)
    return "{'status': 'success'}"


@app.route('/deletequotes', methods=['DELETE'])
def delete_quote():
    author = request.headers.get('author')
    quotes = request.headers.get('quotes')

    redis_session.delete(author, quotes)
    return "{'status': 'success'}"


if __name__ == '__main__':
    app.run()
