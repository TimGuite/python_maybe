"""Code to test the maybe class"""
import pytest


from maybe import *


def test_from_just_value_is_value():
    assert from_just(Just(5)) == 5
    assert from_just(Just("A string")) == "A string"
    assert from_just(Just(Nothing())) == Nothing()


def test_maybe_applied_to_just_returns_executed_function():
    assert maybe(Just(5), lambda x: x * 2, 1) == 10
    assert maybe(Just([1, 2, 3, 4, 5]), lambda x: x[3:], 0) == [4, 5]


def test_maybe_applied_to_nothing_returns_default():
    assert maybe(Nothing(), lambda x: x * 2, 1) == 1
    assert maybe(Nothing(), lambda x: x[3:], 0) == 0


def test_just_values_are_equal():
    assert Just(5) == Just(5)
    assert Just("some string") == Just("some string")
    assert Just(Just(0)) == Just(Just(0))


def test_nothing_objects_are_equal():
    assert Nothing() == Nothing()


def test_just_never_equal_to_nothing():
    assert (Just(5) == Nothing()) is False
    assert (Nothing() == Just(Nothing())) is False


def test_comparing_non_just_object_to_just_raises_type_error():
    with pytest.raises(TypeError):
        Just(5) == 5
    with pytest.raises(TypeError):
        Just("Some string") == "Not a Just value"
