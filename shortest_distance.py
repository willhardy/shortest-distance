import pytest
import string
from typing import Iterable


"""
* To run the test suite, install pytest and run `pytest shortest_distance.py`.
* To find the shortest distance on the provided file, call:
    `shortest_distance(start, end)`
* To find the distance on any given file, use:
    `get_shortest_distance(lines, start, end)`
"""


def shortest_distance(start: str, end: str):
    filename = 'test-input.txt'
    with open(filename, 'r') as f:
        return get_shortest_distance(f, start, end)


def get_shortest_distance(lines: Iterable, start: str, end: str):
    # Make our lookup case-insensitive
    start, end = start.casefold(), end.casefold()

    # We pass the words into the file parser, to allow it to optimise, if it so wishes
    db = parse_content(lines, start, end)

    try:
        return min(get_candidate_distances(db[start], db[end]))

    # An empty sequence will raise a ValueError, we choose to return None
    except ValueError:
        return None


def tokenize(lines):
    """ Tokenize the given file by words. """
    for line in lines:
        for word in line.split():
            yield word.strip(string.punctuation).casefold()


def parse_content(lines, start, end):
    """ Parse the given file and return a data structure that we can use.

    This data structure will be two lists of positions of start and end words.
    """

    # Initialise our output data structure (a list of positions for each word)
    db = {start: [], end: []}

    # Add the position of any relevant words
    for i, token in enumerate(tokenize(lines)):
        seen_start_token = bool(db[start])

        # Always include the start position if listed
        # Only add end positions if we have already seen a start position
        if token == start or (seen_start_token and token == end):
            db[token].append(i)

    return db


def distance(start, end):
    """ Calculate the number of words *between* the given positions. """
    # Remove 1 so as not to include the endpoints
    return end - start - 1


def get_candidate_distances(start_positions, end_positions):
    # This only includes one optimisation, but it might be possible to include
    # more, for example by iterting through the start positions in reverse
    for start in start_positions:
        for end in end_positions:
            if start < end:
                yield distance(start, end)
                # There's no need to consider any other end positions, they will
                # only be longer.
                continue


@pytest.mark.parametrize('start,end,exp_distance', [
    # Given example
    ('motivation', 'development', 2),

    # No match
    ('motivation', 'blah', None),
    ('blah', 'development', None),
    ('blah', 'bleh', None),

    # Case insensitive
    ('Development', 'key', 2),
    ('deVELopMEnt', 'KEY', 2),
    ('skill', 'devop', 2),

    # Limits
    ('we', 'devop', 16),
    ('we', 'do', 0),

    # Tokenizer
    ('team', 'is', 1),

    # Same word must appear twice to be counted (my decision)
    ('motivation', 'motivation', None),
    ('development', 'development', 1),
])
def test_with_provided_content(start, end, exp_distance):
    assert shortest_distance(start, end) == exp_distance


@pytest.mark.parametrize('start,end,exp_distance', [
    ('1', '1', 0),
    ('2', '4', 1),
    ('4', '3', 2),
])
def test_with_difficult_content(start, end, exp_distance):
    content = ['  1 2 3 2 1 1 4 2 2 3 4 1 1 5 3 4 1 1 3']
    assert get_shortest_distance(content, start, end) == exp_distance
