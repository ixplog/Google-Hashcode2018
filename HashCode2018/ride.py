import math as mt

class ride(object):
    def __init__(self, id, start_x, start_y, end_x, end_y, earl_start, lat_finish):
        self.id = id
        self.a = start_x
        self.b = start_y
        self.x = end_x
        self.y = end_y
        self.s = earl_start
        self.f = lat_finish

    def get_price_time(self):
        return int(mt.fabs(self.y-self.b) + mt.fabs(self.x-self.a))

