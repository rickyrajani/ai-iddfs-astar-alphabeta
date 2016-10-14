import homework3 as hw
import unittest


class TestTilePuzzle(unittest.TestCase):

    def test_get_board(self):
        p = hw.TilePuzzle([[1, 2], [3, 0]])
        self.assertEqual(p.get_board(), [[1, 2], [3, 0]])

    def test_get_board2(self):
        p = hw.TilePuzzle([[0, 1], [3, 2]])
        self.assertEqual(p.get_board(), [[0, 1], [3, 2]])

    def test_create(self):
        p = hw.create_tile_puzzle(3, 3)
        self.assertEqual(p.get_board(), [[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    def test_create2(self):
        p = hw.create_tile_puzzle(2, 4)
        self.assertEqual(p.get_board(), [[1, 2, 3, 4], [5, 6, 7, 0]])

    def test_perform_move(self):
        p = hw.create_tile_puzzle(3, 3)
        self.assertEqual(p.perform_move("up"), True)
        self.assertEqual(p.get_board(), [[1, 2, 3], [4, 5, 0], [7, 8, 6]])

    def test_perform_move2(self):
        p = hw.create_tile_puzzle(3, 3)
        self.assertEqual(p.perform_move("down"), False)
        self.assertEqual(p.get_board(), [[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    def test_is_solved(self):
        p = hw.TilePuzzle([[1, 2], [3, 0]])
        self.assertEqual(p.is_solved(), True)

    def test_is_solved2(self):
        p = hw.TilePuzzle([[0, 1], [3, 2]])
        self.assertEqual(p.is_solved(), False)

    def test_copy(self):
        p = hw.create_tile_puzzle(3, 3)
        p2 = p.copy()
        self.assertEqual(p.get_board() == p2.get_board(), True)

    def test_copy2(self):
        p = hw.create_tile_puzzle(3, 3)
        p2 = p.copy()
        p.perform_move("left")
        self.assertEqual(p.get_board() == p2.get_board(), False)

    def test_successors(self):
        p = hw.create_tile_puzzle(3, 3)
        for move, new_p in p.successors():
            print move, new_p.get_board()
            # up[[1, 2, 3], [4, 5, 0], [7, 8, 6]]
            # left[[1, 2, 3], [4, 5, 6], [7, 0, 8]]

    def test_successors2(self):
        b = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
        p = hw.TilePuzzle(b)
        for move, new_p in p.successors():
            print move, new_p.get_board()
        # up[[1, 0, 3], [4, 2, 5], [6, 7, 8]]
        # down[[1, 2, 3], [4, 7, 5], [6, 0, 8]]
        # left[[1, 2, 3], [0, 4, 5], [6, 7, 8]]
        # right[[1, 2, 3], [4, 5, 0], [6, 7, 8]]

    def test_iddfs(self):
        b = [[4, 1, 2], [0, 5, 3], [7, 8, 6]]
        p = hw.TilePuzzle(b)
        solutions = p.find_solutions_iddfs()
        self.assertEqual(next(solutions), ['up', 'right', 'right', 'down', 'down'])

    def test_iddfs2(self):
        b = [[1, 2, 3], [4, 0, 8], [7, 6, 5]]
        p = hw.TilePuzzle(b)
        self.assertEqual(list(p.find_solutions_iddfs()), [['down', 'right', 'up', 'left', 'down', 'right'],
                                                          ['right', 'down', 'left', 'up', 'right', 'down']])

    def test_a_star(self):
        b = [[4, 1, 2], [0, 5, 3], [7, 8, 6]]
        p = hw.TilePuzzle(b)
        self.assertEqual(p.find_solution_a_star(), ['up', 'right', 'right', 'down', 'down'])

    def test_a_star2(self):
        b = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
        p = hw.TilePuzzle(b)
        self.assertEqual(list(p.find_solution_a_star()), ['right', 'down', 'left', 'left', 'up',
                                                          'right', 'down', 'right', 'up', 'left',
                                                          'left', 'down', 'right', 'right'])

    def test_a_star3(self):
        p = hw.create_tile_puzzle(9, 1)
        p.perform_move('up')
        self.assertEqual(list(p.find_solution_a_star()), ['down'])

    def test_a_star4(self):
        p = hw.create_tile_puzzle(1, 9)
        p.perform_move('left')
        self.assertEqual(list(p.find_solution_a_star()), ['right'])

    def test_a_star5(self):
        p = hw.create_tile_puzzle(3, 3)
        self.assertEqual(list(p.find_solution_a_star()), [])
        p.perform_move('up')
        self.assertEqual(list(p.find_solution_a_star()), ['down'])

    def test_a_star6(self):
        b = [[4, 1, 2], [0, 5, 3], [7, 8, 6]]
        p = hw.TilePuzzle(b)
        self.assertEqual(list(p.find_solution_a_star()), ['up', 'right', 'right', 'down', 'down'])


class TestGridNavigation(unittest.TestCase):
    def test_find_path(self):
        scene = [[False, False, False], [False, True, False], [False, False, False]]
        self.assertEqual(hw.find_path((0, 0), (2, 1), scene), [(0, 0), (1, 0), (2, 1)])

    def test_find_path1(self):
        scene = [[False, True, False], [False, True, False], [False, True, False]]
        self.assertEqual(hw.find_path((0, 0), (0, 2), scene), None)


class TestLinearDiskMovement(unittest.TestCase):
    def test_solve_distinct_disks(self):
        s = [(1, 3), (0, 1), (2, 0), (3, 2), (1, 3), (0, 1)]
        self.assertEqual(hw.solve_distinct_disks(4, 3), s)

    def test_solve_distinct_disks2(self):
        s = [(0, 2), (1, 3), (2, 4)]
        self.assertEqual(hw.solve_distinct_disks(5, 2), s)

    def test_solve_distinct_disks3(self):
        s = [(1, 3), (2, 1), (0, 2), (2, 4), (1, 2)]
        self.assertEqual(hw.solve_distinct_disks(5, 3), s)

    def test_solve_distinct_disks4(self):
        s = [(1, 3), (0, 1), (2, 0), (3, 2), (1, 3), (0, 1)]
        self.assertEqual(hw.solve_distinct_disks(4, 3), s)

    def test_solve_distinct_disks5(self):
        self.assertEqual(hw.solve_distinct_disks(1, 1), [()])


class TestDominoesGame(unittest.TestCase):
    def test_get_board(self):
        b = [[False, False], [False, False]]
        g = hw.DominoesGame(b)
        self.assertEqual(g.get_board(), [[False, False], [False, False]])

    def test_get_board2(self):
        b = [[True, False], [True, False]]
        g = hw.DominoesGame(b)
        self.assertEqual(g.get_board(), [[True, False], [True, False]])

    def test_create_game(self):
        g = hw.create_dominoes_game(2, 2)
        self.assertEqual(g.get_board(), [[False, False], [False, False]])

    def test_create_game2(self):
        g = hw.create_dominoes_game(2, 3)
        self.assertEqual(g.get_board(), [[False, False, False], [False, False, False]])

    def test_reset(self):
        b = [[False, False], [False, False]]
        g = hw.DominoesGame(b)
        self.assertEqual(g.get_board(), [[False, False], [False, False]])
        g.reset()
        self.assertEqual(g.get_board(), [[False, False], [False, False]])

    def test_reset2(self):
        b = [[True, False], [True, False]]
        g = hw.DominoesGame(b)
        self.assertEqual(g.get_board(), [[True, False], [True, False]])
        g.reset()
        self.assertEqual(g.get_board(), [[False, False], [False, False]])

    def test_is_legal_move(self):
        b = [[False, False], [False, False]]
        g = hw.DominoesGame(b)
        self.assertEqual(g.is_legal_move(0, 0, True), True)
        self.assertEqual(g.is_legal_move(0, 0, False), True)

    def test_is_legal_move2(self):
        b = [[True, False], [True, False]]
        g = hw.DominoesGame(b)
        self.assertEqual(g.is_legal_move(0, 0, False), False)
        self.assertEqual(g.is_legal_move(0, 1, True), True)
        self.assertEqual(g.is_legal_move(1, 1, True), False)

    def test_legal_moves(self):
        g = hw.create_dominoes_game(3, 3)
        self.assertEqual(list(g.legal_moves(True)), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)])
        self.assertEqual(list(g.legal_moves(False)), [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)])

    def test_legal_moves2(self):
        b = [[True, False], [True, False]]
        g = hw.DominoesGame(b)
        self.assertEqual(list(g.legal_moves(True)), [(0, 1)])
        self.assertEqual(list(g.legal_moves(False)), [])

    def test_perform_move(self):
        g = hw.create_dominoes_game(3, 3)
        g.perform_move(0, 1, True)
        self.assertEqual(g.get_board(), [[False, True, False], [False, True, False], [False, False, False]])

    def test_perform_move2(self):
        g = hw.create_dominoes_game(3, 3)
        g.perform_move(1, 0, False)
        self.assertEqual(g.get_board(), [[False, False, False], [True, True, False], [False, False, False]])

    def test_game_over(self):
        b = [[False, False], [False, False]]
        g = hw.DominoesGame(b)
        self.assertEqual(g.game_over(True), False)
        self.assertEqual(g.game_over(False), False)

    def test_game_over2(self):
        b = [[True, False], [True, False]]
        g = hw.DominoesGame(b)
        self.assertEqual(g.game_over(True), False)
        self.assertEqual(g.game_over(False), True)

    def test_copy(self):
        g = hw.create_dominoes_game(4, 4)
        g2 = g.copy()
        self.assertEqual(g.get_board() == g2.get_board(), True)

    def test_copy2(self):
        g = hw.create_dominoes_game(4, 4)
        g2 = g.copy()
        g.perform_move(0, 0, True)
        self.assertEqual(g.get_board() == g2.get_board(), False)

    def test_successors(self):
        b = [[False, False], [False, False]]
        g = hw.DominoesGame(b)
        for m, new_g in g.successors(True):
            print m, new_g.get_board()
        # (0, 0)[[True, False], [True, False]]
        # (0, 1)[[False, True], [False, True]]

    def test_successors2(self):
        b = [[True, False], [True, False]]
        g = hw.DominoesGame(b)
        for m, new_g in g.successors(True):
            print m, new_g.get_board()
        # (0, 1)[[True, True], [True, True]]

    def test_get_best_move(self):
        b = [[False] * 3 for i in range(3)]
        g = hw.DominoesGame(b)
        self.assertEqual(g.get_best_move(True, 1), ((0, 1), 2, 6))
        self.assertEqual(g.get_best_move(True, 2), ((0, 1), 3, 10))

    def test_get_best_move2(self):
        b = [[False] * 3 for i in range(3)]
        g = hw.DominoesGame(b)
        g.perform_move(0, 1, True)
        self.assertEqual(g.get_best_move(False, 1), ((2, 0), -3, 2))
        self.assertEqual(g.get_best_move(False, 2), ((2, 0), -2, 5))

if __name__ == '__main__':
    unittest.main()
