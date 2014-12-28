import json

import pymongo
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict
from flask import Flask, request

from utils import require
from place import Place


app = Flask(__name__)
app.config.from_object(__name__)

places_collection = pymongo.MongoClient().map.places


def response(code, result):
    return json.dumps({'code': code, 'result': result}, ensure_ascii=False)


@app.route('/')
def home():
    with open('README.md') as f:
        return f.read()


@app.route('/place_types')
def place_types():
    place_types = places_collection.aggregate([
            {'$group': {'_id': '$type', 'count':{'$sum': 1}}},
            {'$sort': {'count': -1 }}
        ])['result']
    place_types = [(p['_id'], p['count']) for p in place_types]
    return response(200, place_types)


@app.route('/places')
def places():
   return response(200, list(places_collection.find()))


@app.route('/places', methods=['PUT'])
def create_place():
    require(request.mimetype == 'application/json',
            UnsupportedMediaType('Only Content-Type: application/json is supported.'))
    require(all(field in request.json for field in ('name', 'type', 'coords')),
            BadRequest('Fields "name", "type" and "coords" must be specified.'))
    require(len(request.json['coords']) == 2,
            BadRequest('Field "coords" must contains 2 coordinates.'))

    try:
        places_collection.insert(Place.from_json(request.json).as_dict())
    except pymongo.errors.DuplicateKeyError:
        raise Conflict('Object is already exists')
    return response(200, True)


@app.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    places_collection.remove({'_id': place_id})
    return response(200, True)


@app.route('/nearest/<type>,<lon>,<lat>', methods=['POST'])
def nearest(type, lon, lat):
    nearest = places_collection.find_one({
            'type': type if type != 'shop' else {'$regex': 'shop.*'},
            'location': {
                '$near': {
                    'type': 'Point',
                    'coordinates': [float(lon), float(lat)]
        }}})
    return response(200, nearest)


if __name__ == "__main__":
    app.run()
