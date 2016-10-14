# ai-iddfs-astar-alphabeta

## Tile Puzzle

Developed two solvers for a generalized version of the Eight Puzzle, in which the board can have any number of rows and columns. 

### IDDFS

Yields all optimal solutions to the current board, represented as lists of moves. Valid moves include the four strings "up", "down", "left", and "right", where each move indicates a single swap of the empty tile with its neighbor in the indicated direction. Implemented using an iterative deepening depth-first search, consisting of a series of depth-first searches limited at first to 00 moves, then 11 move, then 22 moves, and so on.

### A Star

Returns an optimal solution to the current board, represented as a list of direction strings. If multiple optimal solutions exist, any of them may be returned. Implemented as an A* search using the Manhattan distance heuristic.

## Grid Nivigation

Implemented A* search.

## Linear Disk Movement

Implemented A* search.

## Dominoes Game

Develop an AI for a game in which two players take turns placing 1×21×2 dominoes on a rectangular grid. One player must always place his dominoes vertically, and the other must always place his dominoes horizontally. The last player who successfully places a domino on the board wins.

### Alpha Beta Search

Returns a 3-element tuple containing the best move for the current player as a (row, column) tuple, its associated value, and the number of leaf nodes visited during the search. 

Implementation of the alpha-beta search, with the restriction that it should look no further than limit moves into the future.
