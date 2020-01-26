"""Code to test the maybe class"""
import pytest


from maybe import *


def test_maybe_applied_to_just_returns_executed_function():
    assert maybe(1, lambda x: x * 2, Just(5)) == 10
    assert maybe(0, lambda x: x[3:], Just([1, 2, 3, 4, 5])) == [4, 5]


def test_maybe_applied_to_nothing_returns_default():
    assert maybe(1, lambda x: x * 2, Nothing) == 1
    assert maybe(0, lambda x: x[3:], Nothing) == 0


def test_just_values_are_equal():
    assert Just(5) == Just(5)
    assert Just("some string") == Just("some string")
    assert Just(Just(0)) == Just(Just(0))


def test_nothing_objects_are_equal():
    assert Nothing == Nothing


def test_just_never_equal_to_nothing():
    assert (Just(5) == Nothing) is False
    assert (Nothing == Just(Nothing)) is False


def test_comparing_non_just_object_to_just_raises_type_error():
    with pytest.raises(TypeError):
        Just(5) == 5
    with pytest.raises(TypeError):
        Just("Some string") == "Not a Just value"


def test_is_just_with_just_x_returns_true():
    assert isJust(Just(5)) == True
    assert isJust(Just("This is a string")) == True
    assert isJust(Just(Nothing)) == True


def test_is_just_with_nothing_returns_false():
    assert isJust(Nothing) == False


def test_is_nothing_with_just_x_returns_false():
    assert isNothing(Just(5)) == False
    assert isNothing(Just("This is a string")) == False
    assert isNothing(Just(Nothing)) == False


def test_is_just_with_nothing_returns_true():
    assert isNothing(Nothing) == True


def test_from_just_value_is_value():
    assert fromJust(Just(5)) == 5
    assert fromJust(Just("A string")) == "A string"
    assert fromJust(Just(Nothing)) == Nothing
    assert 2 * fromJust(Just(10)) == 20


def test_from_just_nothing_raises_error():
    with pytest.raises(TypeError):
        fromJust(Nothing)


def test_from_maybe_returns_inner_value_when_just():
    assert fromMaybe(Just("Hello, World"), "") == "Hello, World"
    assert fromMaybe(Just(Nothing), 5) == Nothing


def test_from_maybe_returns_default_value_when_nothing():
    assert fromMaybe(Nothing, "nothing") == "nothing"


def test_list_to_maybe_with_empty_lists_and_non_empty_lists():
    assert listToMaybe([9]) == Just(9)
    assert listToMaybe([]) == Nothing
    assert listToMaybe([1, 2, 3]) == Just(1)


def test_maybe_to_list_with_nothing_and_just_items():
    assert maybeToList(Nothing) == []
    assert maybeToList(Just(3)) == [3]
    assert maybeToList(Just([3])) == [[3]]


def test_list_to_maybe_and_maybe_to_list_identity_on_singleton_list():
    assert maybeToList(listToMaybe([5])) == [5]
    assert maybeToList(listToMaybe([])) == []


def test_cat_maybes():
    assert catMaybes([Just(1), Nothing, Just(3)]) == [1, 3]


def test_map_maybes():
    assert mapMaybes(lambda x: Just(x), [1, 2, 3]) == [1, 2, 3]
