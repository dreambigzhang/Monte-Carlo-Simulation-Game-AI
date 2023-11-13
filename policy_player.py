from board import GoBoard
from board_util import GoBoardUtil
from typing import List, Tuple
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
def policy_moves(board: GoBoard, color: GO_COLOR, policy, board_size) -> GO_POINT:
    if policy == 'random':
        return 'Random', scanRandom(board, color, board_size)
    winMoves = scanWin(board, color, board_size)
    if len(winMoves) > 0:
        return 'Win', winMoves
    blockWinMoves = scanBlockWin(board, color, board_size)
    if len(blockWinMoves) > 0:
        return 'BlockWin',blockWinMoves
    openFourMoves = scanOpenFour(board, color, board_size)
    if len(openFourMoves) > 0:
        return 'OpenFour', openFourMoves
    captureMoves = scanCapture(board, color, board_size)
    if len(captureMoves) > 0:
        return 'Capture', captureMoves
    return 'Random', scanRandom(board, color, board_size)

def scanWin(board: GoBoard, color, board_size):
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
                winMoves.append(format_point(point_to_coord(point,board_size)).lower() )
    return sorted(winMoves)

def scanBlockWin(board: GoBoard, color, board_size):
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
                blockWinMoves.append(format_point(point_to_coord(point,board_size)).lower() )
    return sorted(blockWinMoves)

def scanOpenFour(board: GoBoard, color, board_size):
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
                openFourMoves.append(format_point(point_to_coord(point,board_size)).lower() )
    return sorted(openFourMoves)

def scanCapture(board: GoBoard, color, board_size):
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
                captureMoves.append(format_point(point_to_coord(point,board_size)).lower() )
    return sorted(captureMoves)

def scanRandom(board: GoBoard, color, board_size):
    return sorted(format_point(point_to_coord(point,board_size)).lower() for point in board.get_empty_points())


def point_to_coord(point: GO_POINT, boardsize: int) -> Tuple[int, int]:
    """
    Transform point given as board array index 
    to (row, col) coordinate representation.
    Special case: PASS is transformed to (PASS,PASS)
    """
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