# ===================================================
# The objective - tree like based execution platform
# ===================================================

# TODO: 
# - execution conditionals (with try catch in decorator?)
# - inter function contracts
# - add error handling support


class exf:
    """
    execution function type (factory) class
    """
    def __init__(self, function) -> None:
        self.function = function
    
    def __rshift__(self, tree): 
        instance = exfi(self.function)       
        if type(tree) is not list:
            tree = [tree]
        for node in tree:
            if type(node) is exf:
                instance.tree.append(exfi(node.function))
            else:
                instance.tree.append(node)
        return instance


class exfi:
    """
    execution function instance class
    """
    def __init__(self, function) -> None:
        self.function = function
        self.name = function.__name__
        self.tree = []

    def execute(self, **kwargs):
        kwargs.update({'name': self.function.__name__})
        rv = self.function(**kwargs)
        for node in self.tree:
            try:
                node.execute(**rv)
            except Exception:
                continue
            
    
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
    raise Exception('bla')
    print(kwargs)
    return {'parent': 'C', 'depth': kwargs.get('depth')+1, 'onlyd':'some_value'}

def _D(**kwargs):
    # raise Exception('bla')
    print(kwargs)
    if kwargs['parent'] == 'C':
        print (kwargs['onlyd'])
    return {'parent': 'D', 'depth': kwargs.get('depth')+1}


root = exf(_root)
A = exf(_A)
B = exf(_B)
C = exf(_C)
D = exf(_D)


# define and execute the functional schema
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
