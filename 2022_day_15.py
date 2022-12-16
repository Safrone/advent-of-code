data = _data
# data = example
from dataclasses import dataclass
import itertools
from .utils import *

@dataclass
class S:
    x: int
    y: int
    cx: int
    cy: int
    
    def nobeacon(self, y):
        dis_to_beacon = abs(self.cx - self.x) + abs(self.cy - self.y)
        to_line = abs(y - self.y)
        diff = dis_to_beacon - to_line
        xes = []
        if diff >= 0:
            xes = [self.x]
            for i in range(1, diff + 1):
                xes.extend([self.x - i, self.x + i])
        return xes
    
    def nobeacon_rng(self, y):
        dis_to_beacon = abs(self.cx - self.x) + abs(self.cy - self.y)
        to_line = abs(y - self.y)
        diff = dis_to_beacon - to_line
        if diff >= 0:
            return Range(self.x - diff, self.x + diff)
        return None
    
@dataclass
class Range:
    # y: int
    startx: int
    endx: int
    
sensors = []
for line in data.split('\n'):
    # x, y, cx, cy = ints(line)
    sensor = S(*ints(line))
    sensors.append(sensor)
sensors

yb = 2000000
# yb = 10

ybeacons = [s.cx for s in sensors if s.cy == yb]

nobeac = set(itertools.chain.from_iterable([s.nobeacon(yb) for s in sensors])) - set(ybeacons)
print(len(nobeac))

cmin = 0
cmax = 4000000

# cmin = 0
# cmax = 20

from collections import defaultdict

beacons = defaultdict(list)
for s in sensors:
    beacons[s.cy].append(s.cx)

def tune(x, y):
    return x * 4000000 + y

def find_hole(xmin, xmax, rngs, y):
    beacon_xs = beacons.get(y, [])
    # combine ranges
    
    sorted_rng = sorted([r for r in rngs if r is not None], key=lambda x: x.startx)
    rng = None
    for i, r in enumerate(sorted_rng):
        if rng is None:
            rng = r
        else:
            if rng.endx + 1 >= r.startx:
                if r.endx > rng.endx:
                    rng = Range(rng.startx, r.endx)
            else:
                if rng.endx + 2 in beacon_xs:
                    print('beacon')
                    rng = Range(rng.startx, r.endx)
                else:
                    xpos = rng.endx + 1
                    if xmin <= xpos <= xmax:
                        print('no overlap', rng, r, xpos, y, tune(xpos, y))
            

for y in range(cmax + 1):
    rngs = [s.nobeacon_rng(y) for s in sensors]
    find_hole(cmin, cmax, rngs, y)
