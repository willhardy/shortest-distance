import pytest


def tokenize_file(filename):
    """ Tokenize the given file by words. """
    with open(filename, 'r') as f:
        for line in f:
            for word in line.split():
                yield word.casefold()


def parse_file(filename, start, end):
    """ Parse the given file and record the locations of the given relevant words. """

    # Initialise our output data structure (a list of positions for each word)
    db = {start: [], end: []}

    # Add the position of any relevant words
    for i, token in enumerate(tokenize_file(filename)):
        if token in db:
            db[token].append(i)

    return db


def distance(start, end):
    """ Calculate the number of words *between* the given positions. """
    # Remove 1 so as not to include the endpoints
    return end - start - 1


def shortest_distance(start, end):
    # Make our lookup case-insensitive
    start, end = start.casefold(), end.casefold()

    # We pass the words into the file parser, to allow it to optimise, if it so wishes
    db = parse_file('test-input.txt', start, end)

    try:
        return min(distance(s, e) for e in db[end] for s in db[start])

    # An empty sequence will raise a ValueError, we choose to return None
    except ValueError:
        return None


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
def test_shortest_distance(start, end, exp_distance):
    assert shortest_distance(start, end) == exp_distance
