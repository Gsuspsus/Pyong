class EventQueue:
    def __init__(self):
        self.events = []

    def __iadd__(self, event):
        """Shortcut for using += to add a listener."""
        self.add(event)
        return self

    def add(self,event):
        self.events.append(event)

    def remove(self,event):
        self.events.remove(evnt)

    def try_get_event(self,type):
        return list(filter(lambda e: isinstance(e, type), self.events))

    def get_event(self,type):
        return self.try_get_event(type)[0]

    def has_event(self,type):
        for event in self.events:
            if isinstance(event,type):
                return True
        return False

    def clear(self):
        self.events.clear()