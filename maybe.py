from __future__ import annotations
from functools import singledispatch, singledispatchmethod


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
def from_just(x):
    raise TypeError("Use this on a Just object")


@from_just.register
def _(x: Just) -> any:
    return x.value


@singledispatch
def maybe(m, f, default_value):
    raise TypeError("Call with Maybe value")


@maybe.register
def _(m: Just, f: callable, default_value: any) -> any:
    return f(from_just(m))


@maybe.register
def _(m: Nothing, f: callable, default_value: any) -> any:
    return default_value

