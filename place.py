class Place(object):
    def __init__(self, coords, type, name):
        self.coords = [round(coord, 7) for coord in coords]
        self.type = type
        self.name = name

    @staticmethod
    def from_json(json_place):
        return Place(json_place['coords'],
                     json_place['type'],
                     json_place['name'])

    def as_dict(self):
        return {
            'location': self.coords,
            'type': self.type,
            'name': self.name,
            '_id': '%s_%f_%f' % (self.type, self.coords[0], self.coords[1])
        }
