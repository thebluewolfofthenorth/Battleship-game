import random

GRID_SIZE = 8
NUM_SHIPS = 4
SHIP_SIZE = 3
SHIP_SYMBOL = '@'

# Initialize the game board
def create_board(size):
    return [["."] * size for _ in range(size)]

# Function to display the board
def print_board(board):
    for row in board:
        print(" ".join(row))

board = create_board(GRID_SIZE)
print("Initial 8x8 Board:")
print_board(board)

# Place ships randomly on the board
def place_ships(board, num_ships, ship_size):
    for _ in range(num_ships):
        while True:
            row, col = random.randint(0, size - 1), random.randint(0, size - 1)
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

# Place ships randomly on the board
def place_ships(board, num_ships, ship_size):
    for _ in range(num_ships):
        while True:
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            orientation = random.choice(['horizontal', 'vertical'])
            
            if can_place_ship(board, row, col, ship_size, orientation):
                set_ship(board, row, col, ship_size, orientation)
                break

board = create_board(GRID_SIZE)
place_ships(board, NUM_SHIPS, SHIP_SIZE)

print("Board with Ships Placed:")
print_board(board)

# Add functions to print the board, handle player moves, and game logic

def display_game_rules():
    print("Welcome to Battleship the game in Python.")
    print("Board size: 8x8")
    print("Number of ships: 4")
    print("Length of each ship: 3")
    print("Top left corner is: Row 0, Column 0")

display_game_rules()
