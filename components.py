class Paddle:
    def __init__(self):
        pass

class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Direction:
    def __init__(self, x,y):
        self.x = x
        self.y = y

class Velocity:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class HitBox:
    def __init__(self,width,height):
        self.width = width
        self.height = height

class Drawable:
    def __init__(self, shape, width, height, color=(255,255,255)):
        self.shape = shape
        self.width = width
        self.height = height
        self.color = color

class Ball:
    def __init__(self):
        pass

class Input:
    def __init__(self, bindings):
        self.bindings = bindings
        self.actions = []