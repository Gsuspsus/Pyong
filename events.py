class InputActionHappened:
    def __init__(self, entity, action):
        self.entity = entity
        self.action = action

class BallOutOfBounds:
    def __init__(self, collider):
        self.collider = collider 