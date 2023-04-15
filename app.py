import re
from flask import Flask, request, jsonify
from twitter.search import search
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    """Home page."""
    return 'Wow, it works!'

@app.route('/search')
def twsearch():
    """Search Twitter for a query."""
    q = request.args.get('q')
    if not q:
        return error_response('Please provide a query.')

    try:
        result = search('Elon Musk')
        return jsonify(result)
    except Exception as err:
        return error_response(f'Error searching: {err}')


def error_response(message):
    response = jsonify({
        'message': message,
    })
    return response, 500
