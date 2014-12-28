from imposm.parser import OSMParser
import pymongo


class Place(object):
    def __init__(self, coords, type, name):
        self.coords = [round(coord, 7) for coord in coords]
        self.type = type
        self.name = name

    def as_dict(self):
        return {
            'location': self.coords,
            'type': self.type,
            'name': self.name
        }


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
    places_collection.insert([p.as_dict() for p in places])


init_mongo()
