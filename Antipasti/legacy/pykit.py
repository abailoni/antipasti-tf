__author__ = 'nasimrahaman'

__doc__ = """ Functions to help with Python """

import itertools as it
import random
import numpy as np


# Python's equivalent of MATLAB's unique (legacy)
def unique(items):
    """
    Python's equivalent of MATLAB's unique (legacy)
    :type items: list
    :param items: List to operate on
    :return: list
    """
    found = set([])
    keep = []

    for item in items:
        if item not in found:
            found.add(item)
            keep.append(item)

    return keep


# Add two lists elementwise
def addelems(list1, list2):
    """
    Adds list1 and list2 element wise. Summands may contain None, which are ignored.
    :type list1: list
    :param list1: First summand
    :type list2: list
    :param list2: Second summand
    :return: list
    """
    # Make sure the lists are of the same length
    assert len(list1) == len(list2), "Summands must have the same length."

    # Add
    return [(item1 + item2 if not (item1 is None or item2 is None) else None) for item1, item2 in zip(list1, list2)]


# Convert a tuple or a non iterable to a list, simultaneously
def obj2list(obj, ndarray2list=True):
    listlike = (list, tuple, np.ndarray) if ndarray2list else (list, tuple)
    # Try-except clause may not work here because layertrain is an iterator and can be converted to list
    if isinstance(obj, listlike):
        return list(obj)
    elif hasattr(obj, 'as_list'):
        return obj.as_list()
    else:
        return [obj]


# Try to convert an object to int
def try2int(obj):
    """Try to convert an object to int."""
    try:
        return int(obj)
    except:
        return obj


# Convert a list of one element to element
def delist(l):
    """Convert a list of one element to element"""
    if isinstance(l, (list, tuple)) and len(l) == 1:
        return l[0]
    else:
        return l


# Smart len function that doesn't break when input is not a list/tuple
def smartlen(l):
    """Compute length of a list `l`. If l is not a list or a tuple, return 1."""
    if isinstance(l, (list, tuple)):
        return len(l)
    else:
        return 1


# Function to remove singleton sublists
def removesingletonsublists(l):
    """Remove singleton sublists given a list `l`."""
    return [elem[0] if isinstance(elem, (list, tuple)) and len(elem) == 1 else elem for elem in l]


# Function to convert a list to a list of list if it isn't one already,
# i.e. [l] --> [[l]] but [[l]] = [[l]].
def list2listoflists(l):
    """
    Convert a list to a list of lists if it isn't one already,
    i.e. `[l] --> [[l]] but [[l]] = [[l]]`.
    """
    if islistoflists(l):
        return l
    else:
        return [l]


# Function to convert a list of tuples to a list of list
def listoftuples2listoflists(l):
    """Convert a list of tuples to a list of lists."""
    assert islistoflists(l), "Input must be a list of tuples or a list of lists."
    l = [list(elem) for elem in l]
    return l


def listoflists2listoftuples(l):
    """Convert a list of lists to a list of tuples."""
    assert islistoflists(l)
    l = [tuple(elem) for elem in l]
    return l


# Function to chain lists (concatenate lists in a list of lists)
def chain(l):
    """Concatenate lists in a given list of lists `l`."""
    return list(it.chain.from_iterable(l))


# Function to flatten a list of list (of list of list of li...) to a list
def flatten(*args):
    """Flatten a list of list (of list of list of li...) to a list."""
    return (result
            for mid in args
            for result in (flatten(*mid)
                           if isinstance(mid, (tuple, list))
                           else (mid,)))


# Function to fold a list according to a given lenlist.
# For l = [a, b, c, d, e] and lenlist = [1, 1, 2, 1], unflatten(l) = [a, b, [c, d], e]
def unflatten(l, lenlist):
    """
    Fold a list according to a given lenlist.
    For l = [a, b, c, d, e] and lenlist = [1, 1, 2, 1], unflatten(l) = [a, b, [c, d], e]
    """
    assert len(l) == sum(lenlist), "Provided length list is not consistent with the list length."

    lc = l[:]
    outlist = []

    for len_ in lenlist:
        outsublist = []
        for _ in range(len_):
            outsublist.append(lc.pop(0))
        outlist.append(delist(outsublist))

    return outlist


def delistlistoflists(l):
    if islistoflists(l):
        # Delist
        if len(l) == 1:
            return l[0]
        else:
            return l
    else:
        # Don't delist
        return l


def islistoflists(l):
    return all([isinstance(elem, (list, tuple))for elem in l])

islistoflistsortuples = islistoflists


# Function to update a list (list1) with another list (list2) (similar to dict.update,
# but with lists)
def updatelist(list1, list2):
    return list1 + [elem for elem in list2 if elem not in list1]


# Append only if object not in list
def appendunique(l, x):
    if x not in l:
        l.append(x)


def updatedictlist(list1, list2):
    dict1 = dict(list1)
    dict1.update(dict(list2))
    return dict1.items()


def broadcast(obj, numtimes):
    # Check if obj is a list already
    if smartlen(obj) == numtimes:
        # Nothing to broadcast; make sure object is a list and go home
        return obj2list(obj)
    elif smartlen(obj) == 1:
        # Single element in a list. Broadcast away!
        return obj2list(obj) * numtimes
    else:
        raise ValueError("Cannot broadcast list of shape {} to {}.".format(smartlen(obj), numtimes))


def getindex(obj, idx, lol=False):
    # lol: list of lists, lol
    if not isinstance(obj, (list, tuple)):
        assert idx == 0, "Object is not a list; only index = 0 is defined."
        return obj
    else:
        if lol:
            # Expecting a list of lists
            return list2listoflists(obj)[idx]
        else:
            return obj[idx]


def smartappend(obj1, obj2, ndarray2list=False):
    obj1 = obj2list(obj1, ndarray2list=ndarray2list)[:]
    obj2 = obj2list(obj2, ndarray2list=ndarray2list)[:]
    return obj1 + obj2


# Function to migrate attributes from one instance of a class to another.
# This was written to be used for weight sharing.
def migrateattributes(source, target, attributes):
    """
    Function to migrate attributes from one instance (source) of a class to another (target).
    This function does no checks, so please don't act like 10 year olds with chainsaws.
    :type source: object
    :param source: Source object
    :type target: object
    :param target: Target object
    :type attributes: list of str or tuple of str
    :param attributes: List/tuple of attribute names.
    """
    for attribute in attributes:
        target.__setattr__(attribute, source.__getattribute__(attribute))

    return target


# TODO Test
# Shuffle a python generator
def shufflegenerator(gen, buffersize=20, rngseed=None):
    # Seed RNG
    if rngseed is not None:
        random.seed(rngseed)

    # Flag to check if generator is exhausted
    genexhausted = False
    # Buffer
    buf = []
    while True:
        # Check if stopping condition is fulfilled
        if genexhausted and len(buf) == 0:
            raise StopIteration

        # Fill up buffer if generator is not exhausted
        if not genexhausted:
            for _ in range(0, buffersize - len(buf)):
                try:
                    buf.append(gen.next())
                except StopIteration:
                    genexhausted = True

        # Pop a random element from buffer random number of times
        numpops = random.randint(0, len(buf))
        for _ in range(numpops):
            popindex = random.randint(0, len(buf) - 1)
            yield buf.pop(popindex)
