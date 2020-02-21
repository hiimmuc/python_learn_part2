class Vector:
    def __init__(self, *coordinate):
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.z = coordinate[2]

    def print_value(self):
        print(f"the coordinate of this point is ({self.x},{self.y},{self.z})")
