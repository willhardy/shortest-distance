Shortest Distance
=================

To run the test suite, install pytest and run

```
pytest shortest_distance.py
```

To find the shortest distance in the provided file, run the following:

```
from shortest_distance import shortest_distance
shortest_distance(start, end)
```

To find the distance on any given file, run the following:

```
from shortest_distance import get_shortest_distance
with open('myfilename.txt') as f:
    get_shortest_distance(f, start, end)
```


Notes
=====

This was a nice exercise! In most cases, it would have been fine to stop when the tests were passing (2cfb5a3f). If performance is very important, the optimisation work should speed things up marginally.

I think it took roughly 35 minutes from start to passing tests, which is a little longer than I estimated. The cleanup for readability and optimisation was only done as an enjoyable academic exercise, there wouldn't normally be too much need, unless I felt that it was important for maintainability.

I've included slightly more comments than I normally would to make sure it's clear why I did the things I did.

