from board import GoBoard
from board_util import GoBoardUtil
from typing import List, Tuple
from engine import GoEngine
import random
from board_base import (
    BLACK,
    WHITE,
    EMPTY,
    BORDER,
    GO_COLOR, GO_POINT,
    PASS,
    MAXSIZE,
    coord_to_point,
    opponent
)

class SimulationPlayer(object):
    def __init__(self):
        self.numSimulations = 10
        self.moves = []
        self.board = GoBoard()
        self.toPlay = BLACK

    def genmove(self, state):
        '''1. Generate a list of all legal moves
           2. Simulate 10 games for each legal move
           3. Pick highest winrate
           4. Player resigns or passes when the game is over
           5. Returns the best move, but maybe should play it?
        '''
        # assert not state.endOfGame()

        # Get all legal moves and put it into a list 
        legal_moves = GoBoard.get_empty_points()
        gtp_moves: List[str] = []
        for move in legal_moves:
            coords: Tuple[int, int] = self.point_to_coord(move, GoBoard.size)
            gtp_moves.append(self.format_point(coords))
        sorted_moves = " ".join(sorted(gtp_moves))
        score = [0] * sorted_moves

        # Simulate each legal move and assign a value
        for i in range(sorted_moves):
            move = legal_moves[i]
            score[i] = self.simulate(state, move)

        # Get the best score
        bestIndex = score.index(max(score))
        best = legal_moves[bestIndex]
        return best

    def simulate(self, state, move):
        stats = [0] * 3
        state.play(move)
        moveNr = state.moveNumber()
        for _ in range(self.numSimulations):
            winner, _ = state.simulate1()
            stats[winner] += 1
            state.resetToMoveNumber(moveNr)
        assert sum(stats) == self.numSimulations
        assert moveNr == state.moveNumber()
        state.undoMove()
        eval = (stats[BLACK] + 0.5 * stats[EMPTY]) / self.numSimulations
        if state.toPlay == WHITE:
            eval = 1 - eval
        return eval
    
    # simulate one game from the current state until the end
    def simulate1(self):
        i = 0
        if not self.endOfGame():
            allMoves = self.legalMoves()
            random.shuffle(allMoves)
            while not self.endOfGame():
                self.play(allMoves[i])
                i += 1
        return self.winner(), i

    def resetToMoveNumber(self, moveNr):
        numUndos = self.moveNumber() - moveNr
        assert numUndos >= 0
        for _ in range(numUndos):
            self.undoMove()
        assert self.moveNumber() == moveNr

    def switchToPlay(self):
        self.toPlay = opponent(self.toPlay)

    def play(self, location):
        #assert not self.endOfGame()
        assert self.board[location] == EMPTY
        self.board[location] = self.toPlay
        self.moves.append(location)
        self.switchToPlay()

    def undoMove(self):
        location = self.moves.pop()
        self.board[location] = EMPTY
        self.switchToPlay()

    def moveNumber(self):
        return len(self.moves)
    
#==============================================================================================
# Copied here for easy use
#==============================================================================================

    def point_to_coord(point: GO_POINT, boardsize: int) -> Tuple[int, int]:
        if point == PASS:
            return (PASS, PASS)
        else:
            NS = boardsize + 1
            return divmod(point, NS)

    def format_point(move: Tuple[int, int]) -> str:
        """
        Return move coordinates as a string such as 'A1', or 'PASS'.
        """
        assert MAXSIZE <= 25
        column_letters = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
        if move[0] == PASS:
            return "PASS"
        row, col = move
        if not 0 <= row < MAXSIZE or not 0 <= col < MAXSIZE:
            raise ValueError
        return column_letters[col - 1] + str(row)