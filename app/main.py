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

def flatten_array(arr):
    return [item for sublist in arr for item in sublist]

def get_tweets(arr):
    return [item['globalObjects']["tweets"] for item in arr]

def assoc_to_values(dict):
    return [item for item in dict.values()]

@app.route('/search')
def twsearch():
    """Search Twitter for a query."""
    q = request.args.get('q')
    limit = request.args.get('limit') or 100
    if limit is str:
        limit = int(limit)
    if not q:
        return error_response('Please provide a query.')

    try:
        result = search(q, limit=limit, latest=True)
        if (len(result) == 0):
            return jsonify([])
        else:
            if (len(result[0]) == 0):
                return jsonify([])
            else:
                results = get_tweets(flatten_array(result))
                results = [assoc_to_values(item) for item in results]
                results = flatten_array(results)
                return jsonify(results)
        return jsonify(result)
    except Exception as err:
        return error_response(f'Error searching: {err}')


def error_response(message):
    response = jsonify({
        'message': message,
    })
    return response, 500
