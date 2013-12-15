from math import sqrt

settings = None
CENTER_POINT = None

def after_settings():
    global CENTER_POINT
    global settings
    CENTER_POINT = (int(settings.board_size / 2), int(settings.board_size / 2))

def set_settings(s):
    global settings
    settings = s
    after_settings()

#################################################

def dist(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def wdist(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

def memodict(f):
    """ Memoization decorator for a function taking a single argument """
    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret
    return memodict().__getitem__

@memodict
def loc_types(loc):
    for i in range(2):
        if not 0 <= loc[i] < settings.board_size:
            return set(['invalid'])

    types = set(['normal'])
    if loc in settings.spawn_coords:
        types.add('spawn')
    if loc in settings.obstacles:
        types.add('obstacle')
    return types

@memodict
def _locs_around(loc):
    x, y = loc
    offsets = ((0, 1), (1, 0), (0, -1), (-1, 0))
    return [(x + dx, y + dy) for dx, dy in offsets]

def locs_around(loc, filter_out=None):
    filter_out = set(filter_out or [])
    return [loc for loc in _locs_around(loc) if len(filter_out & loc_types(loc)) == 0]

def toward(curr, dest):
    if curr == dest:
        return curr

    x0, y0 = curr
    x, y = dest
    x_diff, y_diff = x - x0, y - y0

    if abs(x_diff) < abs(y_diff):
        if (x0, y0 + y_diff / abs(y_diff)) not in settings.obstacles:
            return (x0, y0 + y_diff / abs(y_diff))
    return (x0 + x_diff / abs(x_diff), y0)
