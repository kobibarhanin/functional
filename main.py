# ===================================================
# The objective - tree like based execution platform
# ===================================================

# TODO: 
# - execution conditionals
# - add error handling support


class exnf:
    def __init__(self, function) -> None:
        self.function = function
    
    def __rshift__(self, tree): 
        instance = exn(self.function)       
        if type(tree) is not list:
            tree = [tree]
        for node in tree:
            if type(node) is exnf:
                instance.tree.append(exn(node.function))
            else:
                instance.tree.append(node)
        return instance


class exn:
    
    def __init__(self, function) -> None:
        self.function = function
        self.name = function.__name__
        self.tree = []

    def execute(self, **kwargs):
        kwargs.update({'name': self.function.__name__})
        rv = self.function(**kwargs)
        for node in self.tree:
            node.execute(**rv)
            
    
def _root(**kwargs):
    print(kwargs)
    return {'parent': 'root', 'depth': kwargs.get('depth')+1}

def _A(**kwargs):
    print(kwargs)
    return {'parent': 'A', 'depth': kwargs.get('depth')+1}

def _B(**kwargs):
    print(kwargs)
    return {'parent': 'B', 'depth': kwargs.get('depth')+1}

def _C(**kwargs):
    print(kwargs)
    return {'parent': 'C', 'depth': kwargs.get('depth')+1, 'onlyd':'some_value'}

def _D(**kwargs):
    print(kwargs)
    if kwargs['parent'] == 'C':
        print (kwargs['onlyd'])
    return {'parent': 'D', 'depth': kwargs.get('depth')+1}


root = exnf(_root)
A = exnf(_A)
B = exnf(_B)
C = exnf(_C)
D = exnf(_D)


(root >> 
    [
        A >> 
            [
                B >> C,
                C >> D,
                D >> A
            ],
        B >> B,
        A >> C
    ]
).execute(**{'parent': None, 'depth': 0})
