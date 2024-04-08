

import random

def in_grid(board, row, col):
    """Helper function for is_valid_move to to check if a given row and 
    column pair is within the bounds of the grid.
    """
    if row >= 0 and row < len(board):
        return col >= 0 and col < len(board[0])
    else:
        return False

def any_helper(board, row_temp, col_temp, color_code, dx, dy):
    """Helper function for is_valid_move to essentially check conditions
    for possible moves.
    """
    x, y = row_temp + dx, col_temp + dy
    found_opponent = False
    while in_grid(board, x, y) and board[x][y] != 0:
        if board[x][y] == color_code:
            return found_opponent
        found_opponent = True
        x, y = x + dx, y + dy
    return False

def is_valid_move(board, row, col, color):
    """Function returns True if the specified row, column is a valid move
    for the given color and False in all other cases.
    """ 
    row_temp, col_temp = row, col
    if not in_grid(board, row_temp, col_temp) or board[row_temp][col_temp]!=0:
        return False
    color_code = 2 if color == "black" else 1
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
    (-1, -1), (-1, 1), (1, -1), (1, 1)]
    return any(any_helper(board, row_temp, col_temp, color_code, dx, dy)
        for dx, dy in directions)

def get_valid_moves(board, color):
    """Function which will take in a board state and a color and return
    a list of all valid moves, where each move is a tuple of row, 
    column values in the list.
    """
    valid_moves = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if is_valid_move(board, row, col, color):
                valid_moves.append((row, col))
    return valid_moves

def select_next_play_random(board, color):
    """Function which will take in a board state and color and return 
    a randomly selected move from the list of valid moves, returned as a tuple
    of row, column index values.
    """
    valid_moves = get_valid_moves(board, color) 
    if not valid_moves: return None 
    return random.choice(valid_moves)

def count_flips(board, row, col, color):
    """Helper function for AI to calculate the number of opponent pieces that
    would be flipped if a piece were placed at specific location on the board. 
    This is for AI to decide which move to make, bcs it aims
    to maximize the number of opponent pieces flipped with each move, 
    to gain an advantage.
    """
    color_code = 2 if color == "black" else 1
    opponent_code = 1 if color == "black" else 2
    total_flips = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
    (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        flips = 0
        x, y = row + dx, col + dy
        while in_grid(board, x, y) and board[x][y] == opponent_code:
            flips += 1
            x += dx
            y += dy
        if flips > 0 and in_grid(board, x, y) and board[x][y] == color_code:
            total_flips += flips
    return total_flips

def select_next_play_ai(board, color):
    """Function which will take in a board state and a color and return
    a selected move from the list of valid moves, returned as a tuple of row,
    column index values, like you play with AI.
    """
    valid_moves = get_valid_moves(board, color)
    best_move = None
    max_flips = -1
    for move in valid_moves:
        flips = count_flips(board, move[0], move[1], color)
        if flips > max_flips:
            max_flips = flips
            best_move = move
    return best_move

def select_next_play_human(board, color):
    """Function which will take in a board state and a color and return a move
    selected by a player from the list of valid moves, returned as a tuple of
    row, column index values. 
    """
    valid_moves = get_valid_moves(board, color)
    if not valid_moves:
        print("No valid moves available")
        row = int(input("Select a row: "))
        col = int(input("Select a column: "))
        return (row, col)
    else:
        while True:
            try:
                row = int(input("Select a row: "))
                col = int(input("Select a column: "))
                if (row, col) in valid_moves:
                    return (row, col)
                else:
                    print("Invalid")
            except ValueError:
                print("Invalid input: enter an integer")

def get_board_as_string(board):
    """Function that returns the current board state as a string.
    """
    white_token = "\u25CB" 
    black_token = "\u25CF"
    empty_cell = " "
    board_string = "   " 
    board_size = len(board[0])
    column_indexes = ''
    for i in range(board_size):
        column_indexes += str(i)
        if i < board_size - 1:
            column_indexes += ' '
    board_string += column_indexes + "\n"
    board_string += "  +" + "-+" * board_size + "\n"
    for row_index, row in enumerate(board):
        row_string = str(row_index) + " |"
        for cell in row:
            if cell == 1:
                token = white_token
            elif cell == 2:
                token = black_token
            else:
                token = empty_cell
            row_string += token + "|"
        board_string += row_string + "\n"
        if row_index < len(board) - 1:
            board_string += "  +" + "-+" * board_size + "\n"
    board_string += "  +" + "-+" * board_size
    return board_string

def set_up_board(width, height):
    """Function which takes two integers, width and height, and return a list
    of size height, which contains a sublist of length width 
    filled with zeros.
    """
    board = [[0 for _ in range(width)] for _ in range(height)]
    cntr_x, cntr_y = width // 2, height // 2
    board[cntr_y - 1][cntr_x - 1] = 1 
    board[cntr_y][cntr_x] = 1      
    board[cntr_y - 1][cntr_x] = 2   
    board[cntr_y][cntr_x - 1] = 2   
    return board

def calculate_score(board):
    """Helper function which returns a tuple with the scores 
    (white score, black score).
    """
    white_score = sum(row.count(2) for row in board)
    black_score = sum(row.count(1) for row in board)
    return white_score, black_score

def human_vs_random():
    """Function to allow a person play with random algorithm.
    """
    board = set_up_board(8, 8)
    current_color = 'white'
    while True:
        if not get_valid_moves(board, current_color):
            if not get_valid_moves(board, 'black' 
            if current_color == 'white' else 'white'):
                break 
        if current_color == 'white':
            move = select_next_play_human(board, current_color)
        else:
            move = select_next_play_random(board, current_color)
        if move:
            play_move(board, move, current_color)
            print(get_board_as_string(board))
        current_color = 'black' if current_color == 'white' else 'white'  
    white_score, black_score = calculate_score(board)
    if white_score > black_score:
        print("Player 1 Wins")
        return 1
    elif black_score > white_score:
        print("Player 2 Wins")
        return 2
    else:
        print("It was a tie")
        return 0

def ai_vs_random():
    """Function to allow AI and random algorithms play.
    """
    board = set_up_board(8, 8)
    current_color = 'white' 
    while True:
        valid_moves = get_valid_moves(board, current_color)
        if not valid_moves:
            if not get_valid_moves(board, 'black' 
            if current_color == 'white' else 'white'):
                break 
        if current_color == 'white':
            move = select_next_play_ai(board, current_color)
        else:
            move = select_next_play_random(board, current_color)
        if move:
            play_move(board, move, current_color)
            print(get_board_as_string(board))
        current_color = 'black' if current_color == 'white' else 'white'
    white_score, black_score = calculate_score(board)
    if white_score > black_score:
        print("Player 1 Wins")
        return 1
    elif black_score > white_score:
        print("Player 2 Wins")
        return 2
    else:
        print("It was a tie")
        return 0

def random_vs_random():
    """Function to see the most chaotic random algorithms play.
    """
    board = set_up_board(8, 8)
    current_color = 'white' 
    while True:
        valid_moves = get_valid_moves(board, current_color)
        if not valid_moves:
            if not get_valid_moves(board, 'black' 
            if current_color == 'white' else 'white'):
                break 
        move = select_next_play_random(board, current_color)  
        if move:
            play_move(board, move, current_color)
            print(get_board_as_string(board))        
        current_color = 'black' if current_color == 'white' else 'white'
    white_score, black_score = calculate_score(board)
    if white_score > black_score:
        print("Player 1 Wins")
        return 1
    elif black_score > white_score:
        print("Player 2 Wins")
        return 2
    else:
        print("It was a tie")
        return 0

def play_move(board, move, color):
    """Helper function to handle the actual placing of a token on the board
    and flipping of the opponent's tokens after each move.
    """
    row, col = move
    color_code = 2 if color == "black" else 1
    opponent_code = 1 if color == "black" else 2
    board[row][col] = color_code
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
    (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        x, y = row + dx, col + dy
        pieces_to_flip = []
        while in_grid(board, x, y) and board[x][y] == opponent_code:
            pieces_to_flip.append((x, y))
            x += dx
            y += dy
        if in_grid(board, x, y) and board[x][y] == color_code:
            for flip_x, flip_y in pieces_to_flip:
                board[flip_x][flip_y] = color_code
