import re
import typing
import itertools
from collections import defaultdict, Counter

def lmap(func, *iterables):
    return list(map(func, *iterables))

def ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"-?\d+", s))  # thanks mserrano!
def positive_ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"\d+", s))  # thanks mserrano!
def floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))
def positive_floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))
def words(s: str) -> typing.List[str]:
    return re.findall(r"[a-zA-Z]+", s)

def fst(x):
    return x[0]
def snd(x):
    return x[1]

def splt(data, function=None, separator='\n'):
    split = data.split(separator)
    if function:
        return lmap(function, split)
    else:
        return split

def unique(iterable):
    lst = list(iterable)
    return len(set(lst)) == len(lst)

def pairwise(iterable) -> typing.Iterable[tuple]:
    lst = list(iterable)
    for i in range(len(lst) - 1):
        yield lst[i], lst[i+1]
