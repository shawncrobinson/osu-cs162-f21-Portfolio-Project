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

class Board:
    """The Board class is solely used as a container for board states, used in the HasamiShogiGame class.
    This class will contain the following data members:
    One outer list (representing rows), filled with 9 inner lists (representing columns),
        filled with values representing each space ("BLACK", "RED", or "NONE")"""

    def __init__(self):
        """The constructor for the Board class. Takes no parameters.
        Creates the outer list, fills it with the inner lists, and fills those with "BLACK", "None" x7, "R" """

    def _alg_to_indices(self, alg: str):
        """Private method used to convert an algebraic notation space to board[x[y]] notation space.
        Returns (x, y) as a tuple"""
        pass

    def get_space(self, space: str):
        """Method used to get the contents of a space referenced by algebraic notation.
        Returns "BLACK", "RED", or "NONE" """
        pass

    def set_space(self, space: str, val):
        """Method used to overwrite the contents of a space referenced by algebraic notation."""
        pass

    def print(self):
        """Method used to display the board in a human readable format."""



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
        self._active_player = "BLACK"
        self._board = Board()
        pass

    def get_game_state(self):
        """Method that returns the game state data member.
        Returns "UNFINISHED", "RED_WON", or "BLACK_WON" """
        pass

    def get_active_player(self):
        """Method that returns the active player (which player's turn) data member.
        Returns "RED" or "BLACK" """
        pass

    def get_num_captured_pieces(self, player: str):
        """Method that returns 9 minus the remaining pieces data member for the specified player."""
        pass

    def make_move(self, origin: str, destination: str):
        """Method that handles every aspect of making a move.
        Checks if the game is still ongoing
        Checks if moving the active player's piece
        Checks validity of move
        Moves the piece:
            Handles capturing pieces
            Ends the game if enough pieces captured"""
        pass

    def get_square_occupant(self, square: str):
        """Method that calls the board's get_space method with the provided alg notation string and returns it."""
        pass
