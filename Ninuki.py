#!/usr/bin/python3
# Set the path to your python3 above

"""
Go0 random Go player
Cmput 455 sample code
Written by Cmput 455 TA and Martin Mueller
"""
from gtp_connection import GtpConnection
from board_base import DEFAULT_SIZE, GO_POINT, GO_COLOR
from board import GoBoard
from board_util import GoBoardUtil
from engine import GoEngine
from typing import Any, Callable, Dict, List, Tuple
import numpy as np
from gtp_connection import point_to_coord, format_point

class Go0(GoEngine):
    def __init__(self) -> None:
        """
        Go player that selects moves randomly from the set of legal moves.
        Does not use the fill-eye filter.
        Passes only if there is no other legal move.
        """
        GoEngine.__init__(self, "Go0", 1.0)

    def get_move(self, board: GoBoard, color: GO_COLOR) -> GO_POINT:
        return GoBoardUtil.generate_random_move(board, color, 
                                                use_eye_filter=False)
    
    def solve(self, board: GoBoard):
        """
        A2: Implement your search algorithm to solve a board
        Change if deemed necessary
        """
        # assert the game is not over (Are these necessary here)
        #assert self.board.get_empty_points().size != 0
        #assert 5 in a row not found

        # get all legal moves and put them into a list
        legal_moves = self.board.get_empty_points()
        gtp_moves: List[str] = []
        for move in legal_moves:
            coords: Tuple[int, int] = point_to_coord(move, self.board.size)
            gtp_moves.append(format_point(coords))
        sorted_moves = " ".join(sorted(gtp_moves))
        score = [0] * sorted_moves

        # loop through the legal moves
            # assign move to the current index
            # assign the score to that index by calling simulation and determine its score
        for i in range(sorted_moves):
            move = sorted_moves[i]
            score[i] = self.simulate(move)

        # find the best score in the list
        bestIndex = score.index(max(score))
        best = sorted_moves[bestIndex]
        #assert best in legal_moves (?, is this necessary)

        # play that best move (?, is this done here or should best move just be returned)

        pass
def simulate(move):
    ''' Runs simulation on the given move, returns the score '''
    pass


def run() -> None:
    """
    start the gtp connection and wait for commands.
    """
    board: GoBoard = GoBoard(DEFAULT_SIZE)
    con: GtpConnection = GtpConnection(Go0(), board)
    con.start_connection()


if __name__ == "__main__":
    run()
