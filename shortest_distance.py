import pytest


def shortest_distance(start, end):
    pass


@pytest.mark.parametrize('start,end,exp_distance', [
    ('motivation', 'development', 2),
])
def test_shortest_distance(start, end, exp_distance):
    assert shortest_distance(start, end) == exp_distance
