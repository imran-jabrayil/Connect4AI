import random as rnd
from queue import Queue
import numpy as np


def alpha_beta_decision(board, turn: int, ai_level, queue: Queue, max_player: bool):
    resulting_move, _ = minimax(board, turn, ai_level, max_player)
    queue.put(resulting_move)


def minimax(board, turn: int, ai_level: int, max_player: bool) -> tuple[int, int]:
    current_player = 2 if turn % 2 == 0 else 1
    
    if ai_level == 1:
        return None, evaluate(board, current_player)
    
    possible_moves = board.get_possible_moves()
    move_result = possible_moves[0]
    
    if max_player:
        maximum = float('-inf')    
        for move in possible_moves:
            updated_board = board.copy()
            updated_board.add_disk(move, current_player, update_display=False)
            
            _, decision = minimax(updated_board, turn + 1, ai_level - 1, False)
            if decision > maximum:
                maximum = decision
                move_result = move
        return move_result, maximum
    else:
        minimum = float('inf')
        for move in possible_moves:
            updated_board = board.copy()
            updated_board.add_disk(move, current_player, update_display=False)
            
            _, decision = minimax(updated_board, turn + 1, ai_level - 1, True)
            if minimum > decision:
                minimum = decision
                move_result = move
        return move_result, minimum

def evaluate(board, player_id: int):
    count = 0
    
    for row in range(6):
        for col in range(4):
            count += check_horizontal(board, player_id, row, col)
            count -= check_horizontal(board, 3 - player_id, row, col)
    
    for row in range(3):
        for col in range(7):
            count += check_vertical(board, player_id, row, col)
            count -= check_vertical(board, 3 - player_id, row, col)
    
    for row in range(3):
        for col in range(4):
            count += check_diagonal_positive(board, player_id, row, col)
            count -= check_diagonal_positive(board, 3 - player_id, row, col)
            
    for row in range(3, 6):
        for col in range(4):
            count += check_diagonal_negative(board, player_id, row, col)
            count -= check_diagonal_negative(board, 3 - player_id, row, col)
            
    return count

    
def check_horizontal(board, player_id: int, row: int, start_col: int) -> int:
    assert start_col >= 0 and start_col < 4
    
    count = 0
    for col in range(start_col, start_col + 4):
        if board.grid[col][row] == player_id:
            count += 1
    return count

def check_vertical(board, player_id: int, start_row: int, col: int) -> int:
    assert start_row >= 0 and start_row < 3
    
    count = 0
    for row in range(start_row, start_row + 4):
        if board.grid[col][row] == player_id:
            count += 1
    return count

def check_diagonal_positive(board, player_id: int, start_row: int, start_col: int) -> int:
    assert start_col >= 0 and start_col < 4
    assert start_row >= 0 and start_row < 3
    
    count = 0
    for i in range(4):
        if board.grid[start_col + i][start_row + i] == player_id:
            count += 1
    return count

def check_diagonal_negative(board, player_id: int, start_row: int, start_col: int) -> int:
    assert start_col >= 0 and start_col < 4
    assert start_row >= 3 and start_row < 6
    
    count = 0
    for i in range(4):
        if board.grid[start_col + i][start_row - i] == player_id:
            count += 1
    return count