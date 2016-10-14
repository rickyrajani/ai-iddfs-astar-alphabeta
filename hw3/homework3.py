############################################################
# CIS 521: Homework 3
############################################################

student_name = "Ricky Rajani"

############################################################
# Imports
############################################################

import random
import copy
import itertools
import Queue as Q

############################################################
# Section 1: Tile Puzzle
############################################################


def create_tile_puzzle(rows, cols):
    board = []
    new = []
    cnt = 1
    for i in range(0, rows):
        for j in range(0, cols):
            new.append(cnt)
            cnt += 1
        board.append(new)
        new = []
    board[rows - 1][cols - 1] = 0

    return TilePuzzle(board)


class TilePuzzle(object):
    
    def __init__(self, board):
        self.board = board
        self.r = len(board)
        self.c = len(board[0])
        for i in range(self.r):
            for j in range(self.c):
                if board[i][j] == 0:
                    self.loc = (i, j)
        self.sol = self.solved_board()
        self.h = 0
        self.f = 0
        self.g = 0
        self.route = []

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        loc = self.loc
        if direction == "up":
            if loc[0] == 0:
                return False
            else:
                self.board[loc[0]][loc[1]] = self.board[loc[0] - 1][loc[1]]
                self.board[loc[0] - 1][loc[1]] = 0
                self.loc = (loc[0] - 1, loc[1])
                return True
        elif direction == "down":
            if loc[0] == self.r - 1:
                return False
            else:
                self.board[loc[0]][loc[1]] = self.board[loc[0] + 1][loc[1]]
                self.board[loc[0] + 1][loc[1]] = 0
                self.loc = (loc[0] + 1, loc[1])
                return True
        elif direction == "left":
            if loc[1] == 0:
                return False
            else:
                self.board[loc[0]][loc[1]] = self.board[loc[0]][loc[1] - 1]
                self.board[loc[0]][loc[1] - 1] = 0
                self.loc = (loc[0], loc[1] - 1)
                return True
        elif direction == "right":
            if loc[1] == self.c - 1:
                return False
            else:
                self.board[loc[0]][loc[1]] = self.board[loc[0]][loc[1] + 1]
                self.board[loc[0]][loc[1] + 1] = 0
                self.loc = (loc[0], loc[1] + 1)
                return True
        return False

    def scramble(self, num_moves):
        directions = ["up", "down", "left", "right"]
        for i in range(num_moves):
            self.perform_move(random.choice(directions))

    def is_solved(self):
        solved = create_tile_puzzle(self.r, self.c)
        if self.board == solved.get_board():
            return True
        return False

    def copy(self):
        return TilePuzzle(copy.deepcopy(self.board))

    def successors(self):
        p = self.copy()
        if p.perform_move("up"):
            yield ("up", p)
        p = self.copy()
        if p.perform_move("down"):
            yield ("down", p)
        p = self.copy()
        if p.perform_move("left"):
            yield ("left", p)
        p = self.copy()
        if p.perform_move("right"):
            yield ("right", p)

    def solved_board(self):
        board = []
        new = []
        cnt = 1
        for i in range(0, self.r):
            for j in range(0, self.c):
                new.append(cnt)
                cnt += 1
            board.append(new)
            new = []
        board[self.r - 1][self.c - 1] = 0
        return board

    # Required
    def find_solutions_iddfs(self):
        is_found_solution = False
        limit = 0
        while not is_found_solution:
            for move in self.iddfs_helper(limit, []):
                yield move
                is_found_solution = True
            limit += 1

    def iddfs_helper(self, limit, route):
        if self.board == self.sol:
            yield route
        elif len(route) < limit:
            for move, puzzle in self.successors():
                for sol in puzzle.iddfs_helper(limit, route + [move]):
                    yield sol

    # Required
    def find_solution_a_star(self):
        open_set = set()
        closed_set = set()
        open_set.add(self)
        self.h = self.manhattan(self.sol)
        self.route = []

        while open_set:
            curr = min(open_set, key=lambda x: x.f)

            if curr.board == self.sol:
                return curr.route
            open_set.remove(curr)

            for move, puzzle in curr.successors():
                if puzzle.board == self.sol:
                    puzzle.route = curr.route + [move]
                    return puzzle.route

                puzzle.g = curr.g + curr.manhattan(puzzle.board)
                puzzle.h = puzzle.manhattan(self.sol)
                puzzle.f = puzzle.g + puzzle.h

                go = True
                for board in open_set:
                    if board.board == puzzle.board and board.f < puzzle.f:
                        go = False
                        continue
                for board in closed_set:
                    if board.board == puzzle.board and board.f < puzzle.f:
                        go = False
                        continue
                if go:
                    open_set.add(puzzle)
                    puzzle.route = curr.route + [move]

            closed_set.add(curr)

    def manhattan(self, t1):
        total = 0
        pos = {}

        for x in range(self.r):
            for y in range(self.c):
                pos[t1[x][y]] = (x, y)

        for x in range(self.r):
            for y in range(self.c):
                a = self.board[x][y]
                pos2 = pos[a]
                total += abs(x - pos2[0]) + abs(y - pos2[1])
        return total


############################################################
# Section 2: Grid Navigation
############################################################


class GridPuzzle(object):

    def __init__(self, loc):
        self.loc = loc
        self.g = 0
        self.h = 0
        self.f = 0
        self.route = []

    def successors(self, scene):
        x, y = self.loc
        r = len(scene) - 1
        c = len(scene[0]) - 1
        if x > 0:
            if not scene[x - 1][y]:
                yield GridPuzzle((x - 1, y))  # up
        if y > 0:
            if not scene[x][y - 1]:
                yield GridPuzzle((x, y - 1))  # left
        if x < r:
            if not scene[x + 1][y]:
                yield GridPuzzle((x + 1, y))  # down
        if y < c:
            if not scene[x][y + 1]:
                yield GridPuzzle((x, y + 1))  # right
        if x < r and y < c:
            if not scene[x + 1][y + 1]:
                yield GridPuzzle((x + 1, y + 1))  # down-right
        if x < r and y > 0:
            if not scene[x + 1][y - 1]:
                yield GridPuzzle((x + 1, y - 1))  # down-left
        if x > 0 and y < c:
            if not scene[x - 1][y + 1]:
                yield GridPuzzle((x - 1, y + 1))  # up-right
        if x > 0 and y > 0:
            if not scene[x - 1][y - 1]:
                yield GridPuzzle((x - 1, y - 1))  # up-left

    def heuristic(self, b):
        x1, y1 = self.loc
        x2, y2 = b
        return abs(x1 - x2) + abs(y1 - y2)


def find_path(start, goal, scene):
    open_set = set()
    closed_set = set()
    a = GridPuzzle(start)
    open_set.add(a)
    a.h = a.heuristic(goal)
    a.route = [start]

    while open_set:
        curr = min(open_set, key=lambda x: x.f)

        if curr.loc == goal:
            return curr.route
        open_set.remove(curr)

        for point in curr.successors(scene):
            if point.loc == goal:
                point.route = curr.route + [point.loc]
                return point.route

            point.g = curr.g + curr.heuristic(point.loc)
            point.h = point.heuristic(goal)
            point.f = point.g + point.h

            go = True
            for loc in open_set:
                if loc.loc == point.loc and loc.f < point.f:
                    go = False
                    continue
            for loc in closed_set:
                if loc.loc == point.loc and loc.f < point.f:
                    go = False
                    continue
            if go:
                open_set.add(point)
                point.route = curr.route + [point.loc]

        closed_set.add(curr)


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################
class LinearDiskMovement(object):

    def __init__(self, n, length, disks):
        self.n = n
        self.length = length
        self.disks = list(disks)
        self.g = 0
        self.h = 0
        self.f = 0
        self.route = []

    def successors(self):
        for i in range(len(self.disks)):
            if self.disks[i]:
                if i + 1 < self.length:
                    if self.disks[i + 1] == 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i + 1] = disk
                        yield ((i, i + 1), LinearDiskMovement(self.n, self.length, replace))

                if i + 2 < self.length:
                    if self.disks[i + 2] == 0 and self.disks[i + 1] != 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i + 2] = disk
                        yield ((i, i + 2), LinearDiskMovement(self.n, self.length, replace))

                if i - 1 >= 0:
                    if self.disks[i - 1] == 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i - 1] = disk
                        yield ((i, i - 1), LinearDiskMovement(self.n, self.length, replace))

                if i - 2 >= 0:
                    if self.disks[i - 2] == 0 and self.disks[i - 1] != 0:
                        replace = list(self.disks)
                        disk = replace[i]
                        replace[i] = 0
                        replace[i - 2] = disk
                        yield ((i, i - 2), LinearDiskMovement(self.n, self.length, replace))

    def heuristic(self, b):
        pos = {}
        for i, x in enumerate(b):
            pos[x] = i

        total = 0
        for i, x in enumerate(self.disks):
            total += abs(i - pos[x])

        return total


def solve_distinct_disks(length, n):
    start = [x + 1 for x in range(n)]
    for x in range(length - n):
        start.append(0)
    goal = list(reversed(copy.deepcopy(start)))

    if start == goal:
        return [()]

    open_set = set()
    a = LinearDiskMovement(n, length, start)
    open_set.add(a)

    closed_set = set()
    a.h = a.heuristic(goal)

    while open_set:
        curr = min(open_set, key=lambda ldm: ldm.f)

        if curr.disks == goal:
            return curr.route
        open_set.remove(curr)

        for move, disk in curr.successors():
            if disk.disks == goal:
                disk.route = curr.route + [move]
                return disk.route

            disk.g = curr.g + curr.heuristic(disk.disks)
            disk.h = disk.heuristic(goal)
            disk.f = disk.g + disk.h

            go = True
            for loc in open_set:
                if loc.disks == disk.disks and loc.f < disk.f:
                    go = False
                    continue
            for loc in closed_set:
                if loc.disks == disk.disks and loc.f < disk.f:
                    go = False
                    continue
            if go:
                open_set.add(disk)
                disk.route = curr.route + [move]

        closed_set.add(curr)

############################################################
# Section 4: Dominoes Game
############################################################


def create_dominoes_game(rows, cols):
    board = [[False for x in range(cols)] for y in range(rows)]
    return DominoesGame(board)


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.r = len(board)
        self.c = len(board[0])

    def get_board(self):
        return self.board

    def reset(self):
        self.board = [[False for x in range(self.c)] for y in range(self.r)]

    def is_legal_move(self, row, col, vertical):
        if vertical:
            if row == self.r - 1:
                return False
            if self.board[row + 1][col] or self.board[row][col]:
                return False
        else:
            if col == self.c - 1:
                return False
            if self.board[row][col + 1] or self.board[row][col]:
                return False
        return True

    def legal_moves(self, vertical):
        for x in range(self.r):
            for y in range(self.c):
                if self.is_legal_move(x, y, vertical):
                    yield (x, y)

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            if vertical:
                self.board[row + 1][col] = True
            else:
                self.board[row][col + 1] = True
            self.board[row][col] = True

    def game_over(self, vertical):
        if list(self.legal_moves(vertical)):
            return False
        return True

    def copy(self):
        return DominoesGame(copy.deepcopy(self.board))

    def successors(self, vertical):
        for x, y in list(self.legal_moves(vertical)):
            g = self.copy()
            g.perform_move(x, y, vertical)
            yield ((x, y), g)

    def get_random_move(self, vertical):
        x = list(self.legal_moves(vertical))
        return random.choice(x)

    # Required
    def get_best_move(self, vertical, limit):
        return self.max_value(-float('inf'), float('inf'), None, vertical, limit)

    def max_value(self, alpha, beta, m, vertical, limit):
        l = list(self.successors(vertical))
        o = list(self.successors(not vertical))

        if limit == 0 or self.game_over(vertical):
            return m, len(l) - len(o), 1

        v = -float('inf')
        s = 0
        curr_move = m
        for pos, child in l:
            move, temp, cnt = child.min_value(alpha, beta, pos, not vertical, limit - 1)
            s += cnt
            if temp > v:
                v = temp
                curr_move = pos
            if v >= beta:
                return curr_move, v, s
            alpha = max(alpha, v)

        return curr_move, v, s

    def min_value(self, alpha, beta, m, vertical, limit):
        l = list(self.successors(vertical))
        o = list(self.successors(not vertical))

        if limit == 0 or self.game_over(vertical):
            return m, len(o) - len(l), 1

        v = float('inf')
        s = 0
        curr_move = m
        for pos, child in l:
            move, temp, cnt = child.max_value(alpha, beta, pos, not vertical, limit - 1)
            s += cnt
            if temp < v:
                v = temp
                curr_move = pos
            if v <= alpha:
                return curr_move, v, s
            beta = min(beta, v)

        return curr_move, v, s


############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
I spent around 10 hours on this assignment.
"""

feedback_question_2 = """
Understanding and implementing A* search for the first time was challenging.
"""

feedback_question_3 = """
Parts two and three were almost identical, so I did not gain much from implementing both sections.
"""
