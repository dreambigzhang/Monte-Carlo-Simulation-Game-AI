from board import GoBoard
from board_util import GoBoardUtil
from engine import GoEngine
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
"""
policy_moves
This command prints the set of moves considered by the simulation policy for the current player in the current position, in the format

= MoveType movelist 
Where MoveType is one of: {Win, BlockWin, OpenFour, Capture, Random}. Movelist is an alphabetically sorted list of moves (same sorting order as implemented in gogui-rules_legal_moves).
"""

def scanWin(board: GoBoard, color):
    # scan for win moves
    winMoves = []
    for point in board.get_empty_points():
        for noc in board.neighbors_of_color(point, color):
            isWinMove = True
            direction = noc - point
            try:
                for i in range(2, 5):
                    if board.get_color(point+direction*i) != color:
                        raise Exception
            except:
                isWinMove = False
            if isWinMove:
                winMoves.append(point)
    return sorted(winMoves)

def scanBlockWin(board: GoBoard, color):
    # scan for block win moves
    blockWinMoves = []
    for point in board.get_empty_points():
        for noc in board.neighbors_of_color(point, opponent(color)):
            isBlockWinMove = True
            direction = noc - point
            try:
                for i in range(2, 5):
                    if board.get_color(point+direction*i) != opponent(color):
                        raise Exception
            except:
                isBlockWinMove = False
            if isBlockWinMove:
                blockWinMoves.append(point)
    return sorted(blockWinMoves)

def scanOpenFour(board: GoBoard, color):
    # scan for open four moves
    openFourMoves = []
    for point in board.get_empty_points():
        for noc in board.neighbors_of_color(point, color):
            isOpenFourMove = True
            direction = noc - point
            try:
                for i in range(2, 5):
                    if board.get_color(point+direction*i) != color:
                        raise Exception
                if board.get_color(point+direction*5) != EMPTY:
                    raise Exception
            except:
                isOpenFourMove = False
            if isOpenFourMove:
                openFourMoves.append(point)
    return sorted(openFourMoves)

def scanCapture(board: GoBoard, color):
    captureMoves = []
    for point in board.get_empty_points():
        for noc in board.neighbors_of_color(point, opponent(color)):
            isCaptureMove = True
            direction = noc - point
            try:
                if not (board.get_color(point+direction*2) == opponent(color) and board.get_color(point+direction*3) == opponent(color) and board.get_color(point+direction*3) == color):
                    raise Exception
            except:
                isCaptureMove = False

            if isCaptureMove:
                captureMoves.append(point)
    return sorted(captureMoves)

def scanRandom(board: GoBoard, color):
    return sorted(board.get_empty_points())