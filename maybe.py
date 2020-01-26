from __future__ import annotations
from functools import singledispatch, singledispatchmethod

from typing import List, Callable


class Maybe:
    def __eq__(self, x):
        raise TypeError("Use with other types of Maybe")


class Just(Maybe):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Just {self.value}"

    @singledispatchmethod
    def __eq__(self, other):
        raise TypeError("Use with Maybe objects")


class Nothing(Maybe):
    def __repr__(self):
        return "Nothing"

    @singledispatchmethod
    def __eq__(self, x):
        raise TypeError("Use with Maybe objects")


@Just.__eq__.register
def _(self, other: Just) -> bool:
    print("Comparing two Just objects")
    return from_just(self) == from_just(other)


@Just.__eq__.register
def _(self, other: Nothing) -> bool:
    print("Comparing Just and Nothing")
    return False


@Nothing.__eq__.register
def _(self, other: Just) -> bool:
    return False


@Nothing.__eq__.register
def _(self, other: Nothing) -> bool:
    return True


@singledispatch
def maybe(m, f, default_value):
    raise TypeError("Call with Maybe value")


@maybe.register
def _(m: Just, f: callable, default_value: any) -> any:
    return f(from_just(m))


@maybe.register
def _(m: Nothing, f: callable, default_value: any) -> any:
    return default_value


@singledispatch
def isJust(m):
    raise TypeError("Call with Maybe value")


@isJust.register
def _(m: Just) -> bool:
    return True


@isJust.register
def _(m: Nothing) -> bool:
    return False


@singledispatch
def isNothing(x):
    raise TypeError("Call with Maybe value")


@isNothing.register
def _(_: Just) -> bool:
    return False


@isNothing.register
def _(_: Nothing) -> bool:
    return True


@singledispatch
def from_just(x):
    raise TypeError("Use this on a Just object")


@from_just.register
def _(x: Just) -> any:
    return x.value


@singledispatch
def fromMaybe(x, default_value):
    raise TypeError("Use with a Maybe value")


@fromMaybe.register
def _(m: Just, _) -> any:
    return from_just(m)


@fromMaybe.register
def _(_: Nothing, default_value: any) -> any:
    return default_value


@singledispatch
def listToMaybe(_):
    raise TypeError("Must be called on a list")


@listToMaybe.register
def _(l: list) -> Maybe:
    if len(l) >= 1:
        return Just(l[0])
    else:
        return Nothing()


@singledispatch
def maybeToList(_):
    raise TypeError("Use with a Maybe value")


@maybeToList.register
def _(m: Just) -> list:
    return [from_just(m)]


@maybeToList.register
def _(m: Nothing) -> list:
    return []


@singledispatch
def catMaybes(_):
    raise TypeError("Use on a list of Maybe values")


@catMaybes.register
def _(m: list) -> List[any]:
    """Not ideal but cannot specify a list of Maybes"""
    try:
        return [from_just(x) for x in m if isJust(x)]
    except TypeError:
        raise TypeError("Please run on a list of Maybes")


def mapMaybes(f: Callable[any, maybe], x: List[any]) -> List[any]:
    output: List[Maybe] = [f(y) for y in x]
    return catMaybes(output)
