import random

# Constants
GRID_SIZE = 8
NUM_SHIPS = 4
SHIP_SIZE = 3
SHIP_SYMBOL = '@'
HIT_SYMBOL = 'X'
MISS_SYMBOL = '0'

# Initialize the game board
def create_board(size):
    return [["."] * size for _ in range(size)]

# Function to display the board
def print_board(board):
    for row in board:
        print(" ".join(row))

# Initialize the guess board
def create_guess_board(size):
    return [["~"] * size for _ in range(size)]

# Function to handle player's guess
def player_guess(board, guess_board, target_row, target_col):
    if board[target_row][target_col] == SHIP_SYMBOL:
        guess_board[target_row][target_col] = HIT_SYMBOL
        print("Hit at " + chr(65 + target_row) + str(target_col + 1))
    else:
        guess_board[target_row][target_col] = MISS_SYMBOL
        print("Miss at " + chr(65 + target_row) + str(target_col + 1))

# Place ships randomly on the board
def place_ships(board, num_ships, ship_size):
    for _ in range(num_ships):
        while True:
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            orientation = random.choice(['horizontal', 'vertical'])
            
            if can_place_ship(board, row, col, ship_size, orientation):
                set_ship(board, row, col, ship_size, orientation)
                break

# Check if a ship can be placed at the specified location
def can_place_ship(board, row, col, ship_size, orientation):
    if orientation == 'horizontal':
        if col + ship_size > GRID_SIZE:
            return False
        return all(board[row][c] == '.' for c in range(col, col + ship_size))
    else:  # vertical
        if row + ship_size > GRID_SIZE:
            return False
        return all(board[r][col] == '.' for r in range(row, row + ship_size))

# Place the ship on the board
def set_ship(board, row, col, ship_size, orientation):
    if orientation == 'horizontal':
        for c in range(col, col + ship_size):
            board[row][c] = SHIP_SYMBOL
    else:  # vertical
        for r in range(row, row + ship_size):
            board[r][col] = SHIP_SYMBOL


# Create the game board and place ships
board = create_board(GRID_SIZE)
guess_board = create_guess_board(GRID_SIZE)
place_ships(board, NUM_SHIPS, SHIP_SIZE)

# Testing the setup with a sample guess (replace with actual gameplay logic later)
print("Player's Board View:")
print_board(board)

# Sample guess (row 2, column 3)
player_guess(board, guess_board, 2, 3)  # Replace with player input

print("\nPlayer's Guess Board:")
print_board(guess_board)

# Game rules display
def display_game_rules():
    print("Welcome to Battleship the game in Python.")
    print("Board size: 8x8")
    print("Number of ships: 4")
    print("Length of each ship: 3")
    print("Top left corner is: Row 0, Column 0")

display_game_rules()