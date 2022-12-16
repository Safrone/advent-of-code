from dataclasses import dataclass
from typing import List
from .utils import *

data = _data
# data = example

minutes = 30

start = 'AA'

@dataclass
class Valve:
    name: str
    flow: int
    to: List[str]

    def score(self, dijs, start: 'Valve', minutes_left, other: 'Valve' = None):
        dists, prevs = dijs[start.name]
        dist = dists[self.name]
        open_time = minutes_left - dist - 1
        if other:
            return self.flow * open_time / dist + self.flow * open_time * dijs[other.name][0][self.name]
        return self.flow * open_time / dist
        
    
valves = {}
for line in data.split('\n'):
    flow_rate = ints(line)[0]
    name = line[6:8]
    to = line.replace('valves', 'valve').split('valve ')[-1].split(', ')
    valves[name] = Valve(name, flow_rate, to)

valves


def dij(valves, start_name):
    dist = {}
    previous = {}
    for v in valves.values():
        dist[v.name] = float('infinity')
        previous[v.name] = None
    dist[start_name] = 0
    Q = {k:v for k, v in valves.items()}
    while Q:
        u = sorted(Q.values(), key=lambda q: dist[q.name])[0]
        Q.pop(u.name)
        for neighbor_name in u.to:
            neighbor = valves[neighbor_name]
            dist_between = 1
            alt = dist[u.name] + dist_between
            if alt < dist[neighbor_name]:
                dist[neighbor_name] = alt
                previous[neighbor_name] = u
    return dist, previous



dijs = {name: dij(valves, name) for name in valves}

has_flow = {k: v for k, v in valves.items() if v.flow}

totals = []

def generate_paths(path: typing.Tuple[str], minutes_left=30):
    cur = valves[path[-1]]
    options = sorted([(v.score(dijs, cur, minutes_left), v) for v in has_flow.values() if v.name not in path], reverse=True,
                       key=fst)
    valid_opts = [o for o in options if (minutes_left - dijs[cur.name][0][o[1].name]) > 0]
    cnt = 10
    for opt in valid_opts[:cnt]:
        dist = dijs[cur.name][0][opt[1].name]
        yield from generate_paths(path + (opt[1].name,), minutes_left - dist - 1)
    if not valid_opts:
        yield path[1:]


options = list(generate_paths(('AA',), minutes))

for order in sorted(options):
    total = 0
    minute = minutes
    cur = valves[start]
    
    for name in order:
        dists, prevs = dijs[cur.name]
        dist = dists[name]
        minute = minute - dist - 1
        if minute <= 0:
            break

        total += minute * valves[name].flow
        cur = valves[name]
    totals.append(total)
print(max(totals))

def generate_path_set(path1: typing.Tuple[str], path2: typing.Tuple[str], minutes_left_1=26, minutes_left_2=26):
    cur1 = valves[path1[-1]]
    cur2 = valves[path2[-1]]
    unopened = [v for v in has_flow.values() if v.name not in path1 and v.name not in path2]
    options1 = sorted([(v.score(dijs, cur1, minute, other=cur2), v) for v in unopened], reverse=True, key=fst)
    options2 = sorted([(v.score(dijs, cur2, minute, other=cur1), v) for v in unopened], reverse=True, key=fst)
    valid_opts1 = [o for o in options1 if (minutes_left_1 - dijs[cur1.name][0][o[1].name]) > 1]
    valid_opts2 = [o for o in options2 if (minutes_left_2 - dijs[cur2.name][0][o[1].name]) > 1]
    cnt = 8
    # cnt = 3
    for opt1 in valid_opts1[:cnt]:
        for opt2 in valid_opts2[:cnt]:
            if opt1[1] is opt2[1]:
                continue
            dist1 = dijs[cur1.name][0][opt1[1].name]
            dist2 = dijs[cur2.name][0][opt2[1].name]
            yield from generate_path_set(path1 + (opt1[1].name,), path2 + (opt2[1].name,), minutes_left_1 - dist1 - 1, minutes_left_2 - dist2 - 1)
            
    if valid_opts1 or valid_opts2:
        pass
        if not valid_opts1:
            for opt2 in valid_opts2[:cnt]:
                dist2 = dijs[cur2.name][0][opt2[1].name]
                yield from generate_path_set(path1, path2 + (opt2[1].name,), minutes_left_1, minutes_left_2 - dist2 - 1)
        elif not valid_opts2:
            for opt1 in valid_opts1[:cnt]:
                dist1 = dijs[cur1.name][0][opt1[1].name]
                yield from generate_path_set(path1 + (opt1[1].name,), path2, minutes_left_1 - dist1 - 1, minutes_left_2)
    else:
        yield path1[1:], path2[1:]
    
        


minutes_2 = 26

double_paths = list(generate_path_set(('AA',), ('AA',)))

totals2 = []

for order1, order2 in double_paths:
    total = 0

    minute = minutes_2
    cur = valves[start]
    for name in order1:
        dists, prevs = dijs[cur.name]
        dist = dists[name]
        minute = minute - dist - 1
        if minute <= 0:
            break

        total += minute * valves[name].flow
        cur = valves[name]

    minute = minutes_2
    cur = valves[start]

    for name in order2:
        dists, prevs = dijs[cur.name]
        dist = dists[name]
        minute = minute - dist - 1
        if minute <= 0:
            break

        total += minute * valves[name].flow
        cur = valves[name]
    
    totals2.append(total)
print(max(totals2))
