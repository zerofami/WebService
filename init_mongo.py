from imposm.parser import OSMParser
import pymongo

from place import Place


places= []

def save_places(nodes):
    for osm_id, tags, coords in nodes:
        if 'amenity' in tags:
            places.append(Place(coords, tags['amenity'], tags.get('name') or ''))
        if 'shop' in tags:
            places.append(Place(coords, 'shop_' + tags['shop'], tags.get('name') or ''))


def init_mongo():
    osm_parser = OSMParser(nodes_callback=save_places)
    osm_parser.parse('belarus-latest.osm.pbf')

    mongo_client = pymongo.MongoClient()
    places_collection = mongo_client.map.places
    places_collection.remove()
    places_collection.create_index([('location', pymongo.GEOSPHERE)])
    try:
        places_collection.insert([p.as_dict() for p in places], continue_on_error=True)
    except pymongo.errors.DuplicateKeyError:
        pass


init_mongo()
