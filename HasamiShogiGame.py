# Author: Shawn Robinson
# Date: 2021/11/24
# Description: Portfolio Project - Hasami Shogi variant 1 made in Python


# =============== DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS ===============
# 1) Determining how to store the board
#       The board will be a list of lists, where the outer list covers the rows and the inner
#       lists covers the columns. board[3[0]] would be space "d1". The lists' values will be
#       either an 'R', 'B', or None.
#
#       The board will have a method that converts an algebraic notation string to the indices
#       of the inner and outer lists.
#
# 2) Initializing the board
#       The board class will be initialized by the HasamiShogiGame class.
#       In the board class's init method, a row list will be created and filled with the column lists.
#       The column lists will be filled with an 'R' in the first index, 'B' in the last, and None in
#       in every other index.
#
# 3) Determining how to track which player's turn it is to play right now
#       The current player's turn will be tracked as a string, either "RED" or "BLACK", in the
#       HasamiShogiGame class.
#       The string will change to the other value whenever a valid move is made via the make_move method
#
# 4) Determining how to validate piece movement
#       Starting with a make_move(origin, destination):
#       1) The origin and destination will be converted from alg notation and checked for validity
#       2) the origin spot will be checked for a piece owned by the player that has the current turn
#       3) The origin and destination will be checked to be in a single row or single column
#       If any above check fails then the move is invalid, else continue
#       4) The row or column will be iterated on in the direction of origin->destination until
#          either a piece or the destination is reached
#       If another piece is reached then the move is invalid, else make the move
#
# 5) Determining when pieces have been captured
#       Immediately after a successful piece movement, check for captures:
#       1) Check all positions adjacent to the moved piece for a piece of the opposite color. (DON'T STOP AT 1st PIECE)
#       2) Check if the opposing piece is in a corner.
#          If its in a corner, check the space orthogonally surrounding it for a piece of the opposite color
#              If its surrounded, capture it
#       3) It isn't in a corner, so check the side opposite to the moved piece.
#          If its the same color as the moved piece, capture the piece in the center
#          if its the opposite color to the moved piece, continue to the next space and repeat step 3
#
# 6) Determining when the game has ended
#       After each capture, check the total number of pieces remaining for each player.
#       The game will have a data member tracking the total number of pieces remaining
#       so that the board isn't iterated over completely after each turn.
#       If any player has <=1 pieces remaining, the game is over and that player loses.
#
#

class InvalidAlgebraicNotation(Exception):
    pass


class Board:
    """The Board class is solely used as a container for board states, used in the HasamiShogiGame class.
        This class will contain the following data members:
        One outer list (representing rows), filled with 9 inner lists (representing columns),
            filled with values representing each space ("BLACK", "RED", or "NONE")"""

    def __init__(self):
        """The constructor for the Board class. Takes no parameters.
        Creates the outer list, fills it with the inner lists representing each row,
        and fills the inner lists with the pieces or empty spaces
        Elements are accessed via self._board[Y][X]. [Y][X] made it easier to implement the board's print method"""
        self._board = [["RED"] * 9,
                       ["NONE"] * 9,
                       ["NONE"] * 9,
                       ["NONE"] * 9,
                       ["NONE"] * 9,
                       ["NONE"] * 9,
                       ["NONE"] * 9,
                       ["NONE"] * 9,
                       ["BLACK"] * 9]

    def get_space(self, xy):
        """
        Method used to get the contents of a space (referenced by (column#, row#)).
        :param xy: An (x, y) coordinate tuple for a square to pull the contents of.
        :return: "BLACK", "RED", or "NONE"
        """
        if xy[0] > 8 or xy[0] < 0 or xy[1] > 8 or xy[1] < 0:
            return "NONE"
        return self._board[xy[1]][xy[0]]

    def set_space(self, xy, val):
        """
        Method used to overwrite the contents of a space (referenced by (column#, row#).
        :param xy: An (x, y) coordinate tuple for a square to set the contents of.
        :param val: "BLACK", "RED", or "NONE"
        :return: None
        """
        self._board[xy[1]][xy[0]] = val

    def print(self):
        """
        Method used to display the board in a human readable format.
        :return: None
        """

        # Create an iterator for row labels
        row_labels = iter("abcdefghi")

        # Draw the top row of column labels
        print("  1 2 3 4 5 6 7 8 9")

        for rows in self._board:
            # Print a single row
            print(next(row_labels), end=" ")  # Print row Label
            for spaces in rows:  # Spaces
                if spaces == "BLACK":
                    print("B", end=" ")
                elif spaces == "RED":
                    print("R", end=" ")
                else:
                    print(".", end=" ")
            print()  # End of line, since end=" " overwrites default \n with " "
        print()

    def is_corner(self, xy):
        """
        Method used to check if any given square is in the corner of the board, used for corner capturing.
        :param xy: An (x, y) coordinate tuple of a square on the board to check
        :return: True if the square is in the corner of the board, false otherwise
        """
        if ((xy[0] == 0 or xy[0] == 8) and
                (xy[1] == 0 or xy[1] == 8)):
            return True
        return False


class HasamiShogiGame:
    """The HasamiShogiGame class is used to represent the game and handles all of the game's logic.
    The class handles ending the game, enforcing turns, piece movement, and piece capturing.
    This class will contain the following data members:
    A board object to track the board state
    A data member to track whose turn it is ("BLACK" or "RED") (init'd as "BLACK")
    A data member to track red's remaining pieces
    A data member to track black's remaining pieces
    A data member tracking the current game state ("UNFINISHED", "RED_WON", or "BLACK_WON") (init'd as "UNFINISHED")"""

    def __init__(self):
        """The constructor for the HasamiShogiGame class. Takes no parameters.
        Initializes all private data members, including a board object."""
        self._active_player = "BLACK"  # This player gets the first turn
        self._board = Board()
        self._game_state = "UNFINISHED"
        self._captured_by_black = 0
        self._captured_by_red = 0

    def alg_to_xy(self, alg: str):
        """
        Method used to convert an algebraic notation space to a coordinate tuple (column_number, row_number).
        Raises an InvalidAlgebraicNotation exception if the input string is not a valid board position.
        :param alg: An algebraic notation for some square: "[a-i]|[A-I][1-9]"
        :return: An (x, y) coordinate tuple for the square
        """
        if len(alg) != 2:
            raise InvalidAlgebraicNotation

        row_num = "abcdefghi".find(alg[0].lower())
        if row_num == -1:
            raise InvalidAlgebraicNotation

        try:
            column_num = int(alg[1]) - 1
        except ValueError:
            raise InvalidAlgebraicNotation

        return column_num, row_num

    def get_game_state(self):
        """
        Method that returns the game state data member.
        :return: "UNFINISHED", "RED_WON", or "BLACK_WON"
        """
        return self._game_state

    def get_active_player(self):
        """
        Method that returns the active player (which player's turn) data member.
        :return: "RED" or "BLACK"
        """
        return self._active_player

    def get_num_captured_pieces(self, player: str):
        """
        Method that returns the number of pieces captured pieces of a specified color
        :param player: "BLACK" or "RED"
        :return: Int, 0-9
        """
        if player == "BLACK":
            return self._captured_by_red
        elif player == "RED":
            return self._captured_by_black
        else:
            return -1

    def make_move(self, origin: str, destination: str):
        """
        Method that handles every aspect of making a move.
        Checks if the game is still ongoing - Check
        Checks if moving the active player's piece - Check
        Checks validity of move
        Moves the piece:
            Handles capturing pieces
            Ends the game if enough pieces captured
        :param origin: Algebraic notation string for the square of the piece making a move
        :param destination: Algebraic notation string for the destination of the move
        :return: True if the move was successful, False otherwise
        """

        # Lowercase the origin+destination strings to avoid issues when comparing them later
        origin = origin.lower()
        destination = destination.lower()

        if self.get_game_state() != "UNFINISHED":
            print("Unable to make move -- Game has concluded")
            return False

        try:
            origin_xy = self.alg_to_xy(origin)
        except InvalidAlgebraicNotation:
            print("Unable to make move -- Origin is not in valid algebraic notation format")
            return False

        try:
            destination_xy = self.alg_to_xy(destination)
        except InvalidAlgebraicNotation:
            print("Unable to make move -- Destination is not in valid algebraic notation format")
            return False

        if self.get_square_occupant(origin) != self.get_active_player():
            print("Unable to make move -- Piece at the origin square is not owned by the active player")
            return False

        # Check if origin and destination are the same
        if origin == destination:
            print("Unable to make move -- Origin and destination are the same squares")
            return False

        # Check if origin and destination are within the same row or column, since the pieces moves by rook rules
        if origin_xy[0] - destination_xy[0] != 0 and origin_xy[1] - destination_xy[1] != 0:
            print("Unable to make move -- Origin and destination are not in a line (Pieces move like rooks)")
            return False

        # Determine direction to iterate down while checking for blocking pieces
        if origin_xy[0] - destination_xy[0] != 0:  # If moving along the X axis
            if origin_xy[0] > destination_xy[0]:
                offset = (-1, 0)  # "LEFT"
            else:
                offset = (1, 0)  # "RIGHT"
        else:  # If moving along the Y axis
            if origin_xy[1] < destination_xy[1]:
                offset = (0, 1)  # "DOWN"
            else:
                offset = (0, -1)  # "UP"

        # Iterate along spaces in a line until either the first blocking piece or destination square is reached
        current_square_xy = (origin_xy[0] + offset[0], origin_xy[1] + offset[1])
        while (self._board.get_space(current_square_xy) == "NONE" and
               current_square_xy != destination_xy):
            current_square_xy = (current_square_xy[0] + offset[0], current_square_xy[1] + offset[1])
        if self._board.get_space(current_square_xy) != "NONE":
            print("Unable to make move -- Movement path is blocked by another piece")
            return False

        # Move the piece
        self._board.set_space(origin_xy, "NONE")
        self._board.set_space(destination_xy, self.get_active_player())

        # Check for and process captures.
        # Even though only 3 directions could have a capture, all can be checked without causing issues.
        for directions in ["LEFT", "RIGHT", "DOWN", "UP"]:
            self._capture(self._check_sandwiched(destination_xy, directions))

        # Check if the game is over
        if self._captured_by_red >= 9 or self._captured_by_black >= 9:
            self._game_state = self.get_active_player() + "_WON"
            print(self.get_game_state())
            return True

        # End the current active player's turn
        if self.get_active_player() == "BLACK":
            self._active_player = "RED"
        else:
            self._active_player = "BLACK"

        # Turn successfully processed
        return True

    def get_square_occupant(self, square: str):
        """
        Method that calls the board's get_space method with the provided alg notation string and returns it.
        :param square: Algebraic notation string for the square to check the occupant of
        :return: "BLACK", "RED", or "NONE
        """
        return self._board.get_space(self.alg_to_xy(square))

    def _capture(self, xys):
        """
        Takes a list of squares to be captured, overwriting them with "NONE" and adjusting the captured pieces count.
        :param xys: A list of (x, y) coordinate tuples for spaces containing pieces to be captured
        :return: None
        """
        for squares in xys:
            self._board.set_space(squares, "NONE")
            if self.get_active_player() == "BLACK":
                self._captured_by_black += 1
            elif self.get_active_player() == "RED":
                self._captured_by_red += 1

    def _check_sandwiched(self, origin, direction):
        """
        Checks a given direction for any pieces that are sandwiched and should be captured
        :param origin: (x, y) coordinate tuple of a piece immediately after a move.
        :param direction: Direction that should be checked in, either "UP", "DOWN", "LEFT", or "RIGHT"
        :return: List of (x, y)s for pieces that should be captured)
        """

        # The board is traversed by adding the current square's (x, y) to an offset.
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        if direction == "UP":
            offset = offsets[0]
        elif direction == "DOWN":
            offset = offsets[1]
        elif direction == "LEFT":
            offset = offsets[2]
        elif direction == "RIGHT":
            offset = offsets[3]
        else:
            return []

        capturing = []
        current_square_xy = (origin[0] + offset[0], origin[1] + offset[1])

        if self._board.is_corner(current_square_xy) is True:  # Check for corner capturing if corner
            # Check all spaces around a corner piece (Including spaces off the board, since those return "NONE")
            # If it has 2 of the active player's pieces next to it, its surrounded
            sandwichers = 0
            for offsets in offsets:
                checking = (current_square_xy[0] + offsets[0], current_square_xy[1] + offsets[1])
                if self._board.get_space(checking) == self.get_active_player():
                    sandwichers += 1
            if sandwichers == 2:
                capturing.append(current_square_xy)
        else:  # If not a corner, check for sandwiches in a line
            # Iterate down a line until the first "NONE" or active player's piece. Add all squares checked to capturing
            while (self._board.get_space(current_square_xy) != "NONE" and
                   self._board.get_space(current_square_xy) != self.get_active_player()):
                capturing.append(current_square_xy)
                current_square_xy = (current_square_xy[0] + offset[0], current_square_xy[1] + offset[1])
            # If the line didn't end with a piece of the active player, the piece isn't sandwiched
            if self._board.get_space(current_square_xy) != self.get_active_player():
                capturing = []

        return capturing


def main():
    b = Board()
    b.print()

    game = HasamiShogiGame()
    move_result = game.make_move('i6', 'b6')
    game._board.print()
    move_result = game.make_move('a9', 'b9')
    game._board.print()
    move_result = game.make_move('b6', 'b8')
    game._board.print()
    move_result = game.make_move('a7', 'b7')
    game._board.print()
    move_result = game.make_move('a7', 'b7')
    game._board.print()
    move_result = game.make_move('i8', 'b8')
    game._board.print()
    move_result = game.make_move('b7', 'b1')
    game._board.print()
    move_result = game.make_move('i2', 'i2')
    game._board.print()

    print(move_result)
    print(game.get_active_player())
    print(game.get_square_occupant('a4'))
    print(game.get_game_state())


if __name__ == "__main__":
    main()
