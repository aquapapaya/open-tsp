# Solve Open TSP (not required to go back to the origin)

## Package
[PyConcorde](https://github.com/jvkersch/pyconcorde)

## Input
[testData10.txt](testData10.txt) with x and y coordinates at every line

## Run
<code>python3 pyconcorde_EXPLICIT.py</code>

## Output
Tour and distance

## Comment
It will create a [distance matrix](data.tsp) from a input file. To solve open TSP, a pseudo city whose distance to all the others is zero is added to the matrix.
