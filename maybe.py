from __future__ import annotations
from functools import singledispatch, singledispatchmethod


class Maybe:
    pass


class Just(Maybe):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Just {self.value}"

    @singledispatchmethod
    def __eq__(self, x):
        raise TypeError("Use with other types of Maybe")

    @__eq__.register
    def _(self, other: None) -> bool:
        return False

    @__eq__.register
    def _(self, x: Maybe) -> bool:
        return self.value == x.value


class Nothing(Maybe):
    def __repr__(self):
        return "Nothing"

    @singledispatchmethod
    def __eq__(self, x):
        raise TypeError("Use with other types of Maybe")

    @__eq__.register
    def _(self, other: Just) -> bool:
        return False

    @__eq__.register
    def _(self, x: Maybe) -> bool:
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
