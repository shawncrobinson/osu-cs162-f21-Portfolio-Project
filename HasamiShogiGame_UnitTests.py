# Author: Shawn Robinson
# Date: 2021/12/01
# Description: Unit tests for the HasamiShogiGame and Board classes

import unittest
import unittest.mock
import io
import sys
from HasamiShogiGame import HasamiShogiGame as HasamiShogiGame
from HasamiShogiGame import InvalidAlgebraicNotation as InvalidAlgebraicNotation


def setup_board(game, reds, blacks, nones):
    for squares in reds:
        game._board.set_space(game.alg_to_xy(squares), "RED")
    for squares in blacks:
        game._board.set_space(game.alg_to_xy(squares), "BLACK")
    for squares in nones:
        game._board.set_space(game.alg_to_xy(squares), "NONE")


class Test_alg_to_xy(unittest.TestCase):
    """Contains unit tests for the HasamiShogiGame.alg_to_xy() method."""

    def test1(self):
        game = HasamiShogiGame()
        self.assertEqual((0, 0), game.alg_to_xy("a1"))

    def test2(self):
        game = HasamiShogiGame()
        self.assertEqual((8, 8), game.alg_to_xy("i9"))

    def test3(self):
        game = HasamiShogiGame()
        self.assertEqual((6, 5), game.alg_to_xy("f7"))

    def test4(self):
        game = HasamiShogiGame()
        with self.assertRaises(InvalidAlgebraicNotation):
            game.alg_to_xy("")

    def test5(self):
        game = HasamiShogiGame()
        with self.assertRaises(InvalidAlgebraicNotation):
            game.alg_to_xy("l4")

    def test6(self):
        game = HasamiShogiGame()
        with self.assertRaises(InvalidAlgebraicNotation):
            game.alg_to_xy("55")

    def test7(self):
        game = HasamiShogiGame()
        with self.assertRaises(InvalidAlgebraicNotation):
            game.alg_to_xy("i88")


class Test__check_sandwiched(unittest.TestCase):
    """Contains unit tests for the HasamiShogiGame._check_sandwiched method."""

    directions = ["UP", "DOWN", "LEFT", "RIGHT"]

    # Tests 1-6: Straight line captures in every direction, with 1-8 pieces captured

    def test1(self):
        game = HasamiShogiGame()

        reds = ["e1", "e3"]  # Squares to fill with a red piece
        blacks = ["e2"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "e3"  # Square of a piece to start checking sandwiching from
        direction = "LEFT"  # Direction to check sandwiching
        captures_alg = blacks  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    def test2(self):
        game = HasamiShogiGame()

        reds = ["e1", "e4"]  # Squares to fill with a red piece
        blacks = ["e2", "e3"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "e4"  # Square of a piece to start checking sandwiching from
        direction = "LEFT"  # Direction to check sandwiching
        captures_alg = blacks  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    def test3(self):
        game = HasamiShogiGame()

        reds = ["e1", "e9"]  # Squares to fill with a red piece
        blacks = ["e2", "e3", "e4", "e5", "e6", "e7", "e8"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "e9"  # Square of a piece to start checking sandwiching from
        direction = "LEFT"  # Direction to check sandwiching
        captures_alg = blacks  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    def test4(self):
        game = HasamiShogiGame()

        reds = ["e1", "e3"]  # Squares to fill with a red piece
        blacks = ["e2"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "e1"  # Square of a piece to start checking sandwiching from
        direction = "RIGHT"  # Direction to check sandwiching
        captures_alg = blacks  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    def test5(self):
        game = HasamiShogiGame()

        reds = ["f2", "d2"]  # Squares to fill with a red piece
        blacks = ["e2"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "f2"  # Square of a piece to start checking sandwiching from
        direction = "UP"  # Direction to check sandwiching
        captures_alg = blacks  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    def test6(self):
        game = HasamiShogiGame()

        reds = ["f2", "d2"]  # Squares to fill with a red piece
        blacks = ["e2"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "d2"  # Square of a piece to start checking sandwiching from
        direction = "DOWN"  # Direction to check sandwiching
        captures_alg = blacks  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    # Tests 7-9 : Straight line non-captures

    def test7(self):
        game = HasamiShogiGame()

        reds = ["d2"]  # Squares to fill with a red piece
        blacks = ["e2"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "d2"  # Square of a piece to start checking sandwiching from
        direction = "DOWN"  # Direction to check sandwiching
        captures_alg = []  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    def test8(self):
        game = HasamiShogiGame()

        reds = ["e3"]  # Squares to fill with a red piece
        blacks = ["e2", "e1"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "e3"  # Square of a piece to start checking sandwiching from
        direction = "LEFT"  # Direction to check sandwiching
        captures_alg = []  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    def test9(self):
        game = HasamiShogiGame()

        reds = ["e4"]  # Squares to fill with a red piece
        blacks = ["e3", "e2"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "e4"  # Square of a piece to start checking sandwiching from
        direction = "LEFT"  # Direction to check sandwiching
        captures_alg = []  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    # Tests 10-13: Corner captures

    def test10(self):
        game = HasamiShogiGame()

        reds = []  # Squares to fill with a red piece
        blacks = ["a8", "b9"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "b9"  # Square of a piece to start checking sandwiching from
        direction = "UP"  # Direction to check sandwiching
        captures_alg = ["a9"]  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    def test11(self):
        game = HasamiShogiGame()

        reds = []  # Squares to fill with a red piece
        blacks = ["a8", "b9"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "a8"  # Square of a piece to start checking sandwiching from
        direction = "RIGHT"  # Direction to check sandwiching
        captures_alg = ["a9"]  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    def test12(self):
        game = HasamiShogiGame()

        reds = ["h1", "i2"]  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "h1"  # Square of a piece to start checking sandwiching from
        direction = "DOWN"  # Direction to check sandwiching
        captures_alg = ["i1"]  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    def test13(self):
        game = HasamiShogiGame()

        reds = ["h1", "i2"]  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "i2"  # Square of a piece to start checking sandwiching from
        direction = "LEFT"  # Direction to check sandwiching
        captures_alg = ["i1"]  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    # Tests 14- : Corner non-captures

    def test14(self):
        game = HasamiShogiGame()

        reds = ["h1"]  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = ["i2"]  # Squares to remove pieces from
        checking = "h1"  # Square of a piece to start checking sandwiching from
        direction = "DOWN"  # Direction to check sandwiching
        captures_alg = []  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)

    def test15(self):
        game = HasamiShogiGame()

        reds = ["h1"]  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        checking = "h1"  # Square of a piece to start checking sandwiching from
        direction = "DOWN"  # Direction to check sandwiching
        captures_alg = []  # Pieces expected to be sandwiched

        captures_xy = set()
        for squares in captures_alg:
            captures_xy.add(game.alg_to_xy(squares))

        setup_board(game, reds, blacks, nones)

        game._active_player = game.get_square_occupant(checking)

        returned_captures_xy = set()
        for squares in game._check_sandwiched(game.alg_to_xy(checking), direction):
            returned_captures_xy.add(squares)

        self.assertEqual(captures_xy, returned_captures_xy)


class Test_make_move(unittest.TestCase):
    """Contains unit tests for the HasamiShogiGame.make_move() method."""

    # Making move while the game has concluded
    def test1(self):
        game = HasamiShogiGame()

        reds = []  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "i2"  # Square of a piece to start checking sandwiching from
        destination = "h2"  # Direction to check sandwiching
        active_player = game.get_square_occupant(origin)  # Player to set to the active player
        game._game_state = "RED_WON"

        # Expected console output of failed move
        expected_console_output = "Unable to make move -- Game has concluded"

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        captured_console_output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_console_output  # Redirecting stdout to a string to capture and test console output

        game.make_move(origin, destination)
        sys.stdout = old_stdout

        self.assertEqual(expected_console_output, captured_console_output.getvalue().rstrip('\n'))
        # sys.stdout = sys.__stdout__

    # Making move with invalid alg notation origin
    def test2(self):
        game = HasamiShogiGame()

        reds = []  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "i22"  # Square of a piece to start checking sandwiching from
        destination = "h2"  # Direction to check sandwiching
        active_player = "RED"  # game.get_square_occupant(origin)  # Player to set to the active player

        # Expected console output of failed move
        expected_console_output = "Unable to make move -- Origin is not in valid algebraic notation format"

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        captured_console_output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_console_output  # Redirecting stdout to a string to capture and test console output

        game.make_move(origin, destination)
        sys.stdout = old_stdout  # Resetting stdout to avoid issues

        self.assertEqual(expected_console_output, captured_console_output.getvalue().rstrip('\n'))

    # Making move with invalid alg notation destination
    def test3(self):
        game = HasamiShogiGame()

        reds = []  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "i2"  # Square of a piece to start checking sandwiching from
        destination = "h22"  # Direction to check sandwiching
        active_player = "RED"  # game.get_square_occupant(origin)  # Player to set to the active player

        # Expected console output of failed move
        expected_console_output = "Unable to make move -- Destination is not in valid algebraic notation format"

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        old_stdout = sys.stdout
        captured_console_output = io.StringIO()
        sys.stdout = captured_console_output  # Redirecting stdout to a string to capture and test console output

        game.make_move(origin, destination)
        sys.stdout = old_stdout  # Resetting stdout to avoid issues

        self.assertEqual(expected_console_output, captured_console_output.getvalue().rstrip('\n'))

    # Making move with wrong player's piece
    def test4(self):
        game = HasamiShogiGame()

        reds = []  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "a2"  # Square of a piece to start checking sandwiching from
        destination = "h2"  # Direction to check sandwiching
        active_player = "BLACK"  # game.get_square_occupant(origin)  # Player to set to the active player

        # Expected console output of failed move
        expected_console_output = "Unable to make move -- Piece at the origin square is not owned by the active player"

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        old_stdout = sys.stdout
        captured_console_output = io.StringIO()
        sys.stdout = captured_console_output  # Redirecting stdout to a string to capture and test console output

        game.make_move(origin, destination)
        sys.stdout = old_stdout  # Resetting stdout to avoid issues
        self.assertEqual(expected_console_output, captured_console_output.getvalue().rstrip('\n'))

    # Making move with same origin and destination
    def test5(self):
        game = HasamiShogiGame()

        reds = []  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "a7"  # Square of a piece to start checking sandwiching from
        destination = "a7"  # Direction to check sandwiching
        active_player = "RED"  # game.get_square_occupant(origin)  # Player to set to the active player

        # Expected console output of failed move
        expected_console_output = "Unable to make move -- Origin and destination are the same squares"

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        old_stdout = sys.stdout
        captured_console_output = io.StringIO()
        sys.stdout = captured_console_output  # Redirecting stdout to a string to capture and test console output

        game.make_move(origin, destination)
        sys.stdout = old_stdout

        self.assertEqual(expected_console_output, captured_console_output.getvalue().rstrip('\n'))

    # Making move that violates rook movement rules
    def test6(self):
        game = HasamiShogiGame()

        reds = []  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "a7"  # Square of a piece to start checking sandwiching from
        destination = "b6"  # Direction to check sandwiching
        active_player = "RED"  # game.get_square_occupant(origin)  # Player to set to the active player

        # Expected console output of failed move
        expected_console_output = "Unable to make move -- Origin and destination are not in a line (Pieces move like rooks)"

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        old_stdout = sys.stdout
        captured_console_output = io.StringIO()
        sys.stdout = captured_console_output  # Redirecting stdout to a string to capture and test console output

        game.make_move(origin, destination)
        sys.stdout = old_stdout

        self.assertEqual(expected_console_output, captured_console_output.getvalue().rstrip('\n'))

    # Test 7-10: Making move that is blocked by piece of same color
    def test7(self):
        game = HasamiShogiGame()

        reds = ["c7"]  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "a7"  # Square of a piece to start checking sandwiching from
        destination = "e7"  # Direction to check sandwiching
        active_player = "RED"  # game.get_square_occupant(origin)  # Player to set to the active player

        # Expected console output of failed move
        expected_console_output = "Unable to make move -- Movement path is blocked by another piece"

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        old_stdout = sys.stdout
        captured_console_output = io.StringIO()
        sys.stdout = captured_console_output  # Redirecting stdout to a string to capture and test console output

        game.make_move(origin, destination)
        sys.stdout = old_stdout

        self.assertEqual(expected_console_output, captured_console_output.getvalue().rstrip('\n'))

    def test8(self):
        game = HasamiShogiGame()

        reds = ["b7"]  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "a7"  # Square of a piece to start checking sandwiching from
        destination = "b7"  # Direction to check sandwiching
        active_player = "RED"  # game.get_square_occupant(origin)  # Player to set to the active player

        # Expected console output of failed move
        expected_console_output = "Unable to make move -- Movement path is blocked by another piece"

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        old_stdout = sys.stdout
        captured_console_output = io.StringIO()
        sys.stdout = captured_console_output  # Redirecting stdout to a string to capture and test console output

        game.make_move(origin, destination)
        sys.stdout = old_stdout

        self.assertEqual(expected_console_output, captured_console_output.getvalue().rstrip('\n'))

    def test9(self):
        game = HasamiShogiGame()

        reds = []  # Squares to fill with a red piece
        blacks = ["c7"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "a7"  # Square of a piece to start checking sandwiching from
        destination = "c7"  # Direction to check sandwiching
        active_player = "RED"  # game.get_square_occupant(origin)  # Player to set to the active player

        # Expected console output of failed move
        expected_console_output = "Unable to make move -- Movement path is blocked by another piece"

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        old_stdout = sys.stdout
        captured_console_output = io.StringIO()
        sys.stdout = captured_console_output  # Redirecting stdout to a string to capture and test console output

        game.make_move(origin, destination)
        sys.stdout = old_stdout

        self.assertEqual(expected_console_output, captured_console_output.getvalue().rstrip('\n'))

    def test10(self):
        game = HasamiShogiGame()

        reds = []  # Squares to fill with a red piece
        blacks = ["c7"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "a7"  # Square of a piece to start checking sandwiching from
        destination = "c7"  # Direction to check sandwiching
        active_player = "RED"  # game.get_square_occupant(origin)  # Player to set to the active player

        # Expected console output of failed move
        expected_console_output = "Unable to make move -- Movement path is blocked by another piece"

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        old_stdout = sys.stdout
        captured_console_output = io.StringIO()
        sys.stdout = captured_console_output  # Redirecting stdout to a string to capture and test console output

        game.make_move(origin, destination)
        sys.stdout = old_stdout

        self.assertEqual(expected_console_output, captured_console_output.getvalue().rstrip('\n'))

    # Test 11-13: Making move that captures pieces
    def test11(self):
        game = HasamiShogiGame()

        reds = ["c8"]  # Squares to fill with a red piece
        blacks = ["c7"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "a6"  # Square of a piece to start checking sandwiching from
        destination = "c6"  # Direction to check sandwiching
        active_player = "RED"  # game.get_square_occupant(origin)  # Player to set to the active player
        expected_captured_pieces = 1

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        game.make_move(origin, destination)

        self.assertEqual(expected_captured_pieces, game.get_num_captured_pieces(game.get_active_player()))

    def test12(self):
        game = HasamiShogiGame()

        reds = ["c8", "c3"]  # Squares to fill with a red piece
        blacks = ["c7", "c5", "c4"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "a6"  # Square of a piece to start checking sandwiching from
        destination = "c6"  # Direction to check sandwiching
        active_player = "RED"  # game.get_square_occupant(origin)  # Player to set to the active player
        expected_captured_pieces = 3

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        game.make_move(origin, destination)

        self.assertEqual(expected_captured_pieces, game.get_num_captured_pieces(game.get_active_player()))

    def test13(self):
        game = HasamiShogiGame()

        reds = ["i2", "e1", "h5"]  # Squares to fill with a red piece
        blacks = ["g1", "f1"]  # Squares to fill with a black piece
        nones = []  # Squares to remove pieces from
        origin = "h5"  # Square of a piece to start checking sandwiching from
        destination = "h1"  # Direction to check sandwiching
        active_player = "RED"  # game.get_square_occupant(origin)  # Player to set to the active player
        expected_captured_pieces = 3

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        game.make_move(origin, destination)

        self.assertEqual(expected_captured_pieces, game.get_num_captured_pieces(game.get_active_player()))

    # Test that the game ends upon reaching 9 pieces captured
    def test14(self):
        game = HasamiShogiGame()

        reds = ["i1"]  # Squares to fill with a red piece
        blacks = []  # Squares to fill with a black piece
        nones = ["i9"]  # Squares to remove pieces from
        origin = "a9"  # Square of a piece to start checking sandwiching from
        destination = "i9"  # Direction to check sandwiching
        active_player = "RED"  # game.get_square_occupant(origin)  # Player to set to the active player
        expected_game_state = "RED_WON"
        game._captured_by_red = 2

        setup_board(game, reds, blacks, nones)
        game._active_player = active_player

        game.make_move(origin, destination)

        self.assertEqual(expected_game_state, game.get_game_state())

    # Test that the active player is changed back and forth after a successful move
    def test15(self):
        game = HasamiShogiGame()

        self.assertTrue(game.make_move("i5", "h5"))
        self.assertTrue(game.make_move("a9", "h9"))
        self.assertTrue(game.make_move("i1", "b1"))
        self.assertTrue(game.make_move("a2", "b2"))

        self.assertEqual("BLACK", game.get_active_player())


if __name__ == "__main__":
    unittest.main()
