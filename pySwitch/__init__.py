class Switch:
    def __init__(self, var = None, errOnCaseExist = True, fast = False):
        import threading
        self.var = var
        self.errOnCaseExist = errOnCaseExist
        self.valFunc = {None: lambda: print("Default function")}
        self.funcToRun = self.valFunc[None]
        self.fast = fast
        if fast:
            self.checking = True
            checkChangeThread = threading.Thread(target=self.checkChange)
            checkChangeThread.start()

    def changeFuncToRun (self):
        var = self.var
        if var in self.valFunc.keys():
            self.funcToRun = self.valFunc[var]
        else:
            self.funcToRun = self.valFunc[None]

    def checkChange (self):
        lastVar = self.var
        while self.checking:
            var = self.var
            if var != lastVar:
                self.changeFuncToRun()
                lastVar = var
    
    def case (self, value, func, *args, **kwargs):
        if value in self.valFunc.keys() and self.errOnCaseExist:
            raise KeyError("Value already exists")
        else:
            self.valFunc[value] = lambda: func(*args, **kwargs)
        self.changeFuncToRun()
    
    def default (self, func, *args, **kwargs):
        self.valFunc[None] = lambda: func(*args, **kwargs)

    def __call__(self):
        var = self.var
        if self.fast:
            self.funcToRun()
        else:
            if var in self.valFunc.keys():
                self.valFunc[var]()
            else:
                self.valFunc[None]()

    def kill(self):
        self.checking = False

def help():
    print("""
    Switch case
    To make a new switch-case, write:
    
    from pySwitch import Switch
    switch = Switch(VALUE)
    
    Make a new case by writing:
    
    switch.case(POSSIBILITY, FUNCTION_NAME, ARGUKENTS, KEYWORD_ARGUMENTS)
    
    If you want to make the switch-case quicker, use the fast keyword:
    
    switch = Switch(VALUE, fast = True)
    
    Beware, if fast mode is on, to delete the object you must call:
    
    switch.kill()
    
    """)
