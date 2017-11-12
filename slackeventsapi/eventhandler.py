class EventHandler:
    def __init__(self):
        self.callbacks = {}

    def trigger(self, event, *args, **kargs):
        args = args or ()
        kargs = kargs or {}

        if event in self.callbacks:
            for func in self.callbacks[event]:
                func(*args, **kargs)

    def hook(self, event):
        def wrap(func):
            if event not in self.callbacks:
                self.callbacks[event] = []
            self.callbacks[event].append(func)
            return func
        return wrap
