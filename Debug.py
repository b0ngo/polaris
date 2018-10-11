class Debugger(object):
    flag = None
    data = None

    def activate(self):
        self.flag = True
        self.data = { }

    def deactivate(self):
        self.flag = False

    def is_active(self):
        if self.flag == None:
            return False

        return self.flag

def set_offline_mode(offline_mode):
    if not debugger.is_active():
        debugger.activate()

    debugger.data[OFFLINE_MODE] = offline_mode

def set_offline():
    if not debugger.is_active():
        debugger.activate()

    set_offline_mode(True)

def set_online():
    if not debugger.is_active():
        debugger.activate()

    set_offline_mode(False)

def is_offline():
    return debugger.data[OFFLINE_MODE]

def is_online():
    return not debugger.data[OFFLINE_MODE]

OFFLINE_MODE = "offline_mode"

debugger = Debugger()
set_offline_mode(False)
debugger.deactivate()
