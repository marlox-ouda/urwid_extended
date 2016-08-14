
VERSION = (0,0,1)
__version__ = ''.join('-.'[isinstance(x, int)]+str(x) for x in VERSION)[1:]
