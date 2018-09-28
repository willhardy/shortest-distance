import pytest
import string
from itertools import filterfalse
from typing import Iterable


################################################################################
# Challenge function
################################################################################

def shortest_distance(start: str, end: str):
    """ Wrapper function for the challenge.

    The actual work is done in get_shortest_distance below. I did this because it
    would be a little restrictive for testing to hard code the input file. Plus, we
    can test with non-file objects, which is much more flexible/convenient.
    """
    filename = 'test-input.txt'
    with open(filename, 'r') as f:
        return get_shortest_distance(f, start, end)


################################################################################
# Test suite
# Call pytest on this file and the default test discovery should find them.
################################################################################

def get_shortest_distance(lines: Iterable, start: str, end: str):
    """ Finds the shortest distance between the given words.
    """
    # Make our lookup case-insensitive
    start, end = start.casefold(), end.casefold()

    # We pass the words into the file parser, to allow it to optimise, if it so wishes
    # The data structure we now have lists the positions that the words appear in the text.
    start_positions, end_positions = parse_content(lines, start, end)

    possibilities = find_shortest_distances(start_positions, end_positions)
    return min(possibilities, default=None)


def tokenize(lines):
    """ Tokenize the given file by words.

    This task is done separately because tokenization can be done a number of
    different ways and often needs to be customised. I've just done something
    very simple here: split by whitespace, remove punctuation and case.
    """
    for line in lines:
        for word in line.split():
            yield word.strip(string.punctuation).casefold()


def parse_content(lines, start, end):
    """ Parse the given file and return a data structure that we can use.

    This data structure will be two lists of all the positions of the start and
    end words.
    """

    # Initialise our output data structure (a list of positions for each word)
    start_positions = []
    end_positions = []

    # Add the position of any relevant words
    for i, token in enumerate(tokenize(lines)):
        # Always include the start position if listed
        # Only add end positions if we have already seen a start position
        if token == start:
            start_positions.append(i)
        if start_positions and token == end:
            end_positions.append(i)

    return start_positions, end_positions


def distance(start, end):
    """ Calculate the number of words *between* the given positions.

    This is really only included for readability.
    """
    # Remove 1 so as not to include the endpoints
    return end - start - 1


def find_shortest_distances(start_positions, end_positions):
    """ Move from the middle outwards, the first match will be the shortest distance.

    Another optimisation would be to remove all start indicies after the maximum
    end value, and all end indices before the minimum start value.
    """
    # Work through the start positions from greatest to lowest
    for start in reversed(start_positions):
        for end in end_positions:
            if start < end:
                yield distance(start, end)


################################################################################
# Additional optimisation
# This is in most cases unnecessary and I think adds too much code for the
# benefit. The benefit of this optimisation is mostly theoretical: if you are
# dealing with datasets large enough for this optimisation to make a meaningful
# improvement, you'll probably have a bottleneck elsewhere that renders this
# improvement pointless. I've written it in a way so that the
# find_shortest_distances function would only need to be minimally altered to
# add (and remove) this.
# This isn't included as the default solution, because I don't feel it's worth it.
################################################################################

def ignorewhile(pred, it):
    """ Like itertools.takewhile, but the opposite. """
    it = iter(it)
    yield next(filterfalse(pred, it))
    yield from it


def reduce_search_space(start_positions, end_positions):
    max_end = end_positions[-1]
    min_start = start_positions[-1]

    start_positions = ignorewhile(lambda x: x >= max_end, start_positions)
    end_positions = ignorewhile(lambda x: x <= min_start, end_positions)

    return start_positions, end_positions


def find_shortest_distance2(start_positions, end_positions):
    """ Same as find_shortest_distances, but with an added optimisation.
    """
    # Exit early to allow remaining code to assume that these iterables have content
    if not start_positions or not end_positions:
        return None

    start_positions.reverse()
    start_positions, end_positions = reduce_search_space(start_positions, end_positions)

    for start in start_positions:
        for end in end_positions:
            if start < end:
                yield distance(start, end)


################################################################################
# Test suite
# Call pytest on this file and the default test discovery should find them.
################################################################################

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
    # Use digits as "words" to create a number of multiple options
    content = [' 1 2 3 2 1 1 4 2 2 3 4 1 1 5 3 4 1 1 3']
    assert get_shortest_distance(content, start, end) == exp_distance


@pytest.mark.parametrize('start,end,exp_distance', [
    ('1', '6', 1),
])
def test_shortcut_buster(start, end, exp_distance):
    # A shortcut that ignores possibilities might fail in certain contrived
    # cases, here is one of them.
    content = ['  1 _ 6 x x 1 x x 6 x 1 x x 6']
    assert get_shortest_distance(content, start, end) == exp_distance
