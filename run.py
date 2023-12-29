import os
import random

# Constants
GRID_SIZE = 8
NUM_SHIPS = 4
SHIP_SIZE = 3
SHIP_SYMBOL = 'S'
HIT_SYMBOL = 'X'
MISS_SYMBOL = '0'

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_player_preference():
    """Asks the player if they want to enable screen clearing."""
    choice = input("Do you want to clear the screen each turn? (yes/no): ").lower()
    return choice == "yes"

def get_player_name():
    """Prompt the player to enter their name, ensuring it's valid (letters only, single word)."""
    while True:
        name = input("Please enter your name (letters only, no spaces): ")
        if name.isalpha() and " " not in name:
            return name
        else:
            print("Invalid name. Please enter a name with letters only and no spaces.")


# Initialize the game board
def create_board(size):
    """Initialize the game board with the specified size."""
    return [["."] * size for _ in range(size)]

# Function to display the board
def print_board(board, hide_ships=False):
    """Print the current state of the board."""
    print("  " + " ".join(str(i + 1) for i in range(GRID_SIZE)))
    for i, row in enumerate(board):
        print_row = [HIT_SYMBOL if cell == SHIP_SYMBOL else cell for cell in row] if hide_ships else row
        print(chr(65 + i) + " " + " ".join(print_row))


# Initialize the guess board
def create_guess_board(size):
    """Initialize the guess board with the specified size."""
    return [["~"] * size for _ in range(size)]


# Game rules display
def display_game_rules():
    """Display the game rules to the player."""
    print("Welcome to Battleship the game in Python.")
    print("Board size: 8x8")
    print("Number of ships: 4")
    print("Length of each ship: 3")
    print("Top left corner is: Row A, Column 1")
    print("'S' represents ships on your board.")

# Function to handle player's guess
def player_guess(board, guess_board, target_row, target_col):
    """Process the player's guess and update the guess board."""
    if board[target_row][target_col] == SHIP_SYMBOL:
        guess_board[target_row][target_col] = HIT_SYMBOL
        return f"Hit at {chr(65 + target_row)}{target_col + 1}"
    else:
        guess_board[target_row][target_col] = MISS_SYMBOL
        return f"Miss at {chr(65 + target_row)}{target_col + 1}"


# Place ships randomly on the board
def place_ships(board, num_ships, ship_size):
    """Place ships randomly on the board."""
    ships_placed = 0
    while ships_placed < num_ships:
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        orientation = random.choice(['horizontal', 'vertical'])
        
        if can_place_ship(board, row, col, ship_size, orientation):
            set_ship(board, row, col, ship_size, orientation)
            ships_placed += 1


# Check if a ship can be placed at the specified location
def can_place_ship(board, row, col, ship_size, orientation):
    """Check if a ship can be placed at the specified location with spacing."""
    # Horizontal placement checks
    if orientation == 'horizontal':
        if col + ship_size > GRID_SIZE or (col > 0 and board[row][col - 1] == SHIP_SYMBOL) or (col + ship_size < GRID_SIZE and board[row][col + ship_size] == SHIP_SYMBOL):
            return False
        for c in range(max(0, col - 1), min(GRID_SIZE, col + ship_size + 1)):
            if any(board[r][c] == SHIP_SYMBOL for r in range(max(0, row - 1), min(GRID_SIZE, row + 2))):
                return False
    # Vertical placement checks
    else:
        if row + ship_size > GRID_SIZE or (row > 0 and board[row - 1][col] == SHIP_SYMBOL) or (row + ship_size < GRID_SIZE and board[row + ship_size][col] == SHIP_SYMBOL):
            return False
        for r in range(max(0, row - 1), min(GRID_SIZE, row + ship_size + 1)):
            if any(board[r][c] == SHIP_SYMBOL for c in range(max(0, col - 1), min(GRID_SIZE, col + 2))):
                return False
    return True


# Place the ship on the board
def set_ship(board, row, col, ship_size, orientation):
    """Place the ship on the board at the specified location."""
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


def player_move(guess_board):
    """Get the player's move and validate it."""
    while True:
        try:
            user_input = input("Enter your move (e.g., A3): ").upper()
            row, col = ord(user_input[0]) - 65, int(user_input[1:]) - 1

            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                if guess_board[row][col] == '~':
                    return row, col
                else:
                    print("You've already guessed that spot. Try again.")
            else:
                print("Invalid move. Please enter a valid coordinate.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid coordinate.")


        
def enemy_move(player_board, previous_moves):
    """Generate a smarter move for the enemy. Avoid repeating previous moves."""
    while True:
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (row, col) not in previous_moves:
            previous_moves.add((row, col))
            if player_board[row][col] == SHIP_SYMBOL:
                player_board[row][col] = HIT_SYMBOL
                return f"Enemy hit your ship at {chr(65 + row)}{col + 1}!"
            else:
                player_board[row][col] = MISS_SYMBOL
                return f"Enemy missed at {chr(65 + row)}{col + 1}."

        
def update_board_after_move(board, guess_board, row, col, is_player_turn):
    """Update the board after a move."""
    pass

def is_game_over(player_board, guess_board, NUM_SHIPS, SHIP_SIZE):
    """Check if the game is over (all ships on either board have been hit)."""
    player_hits = sum(row.count(HIT_SYMBOL) for row in player_board)
    enemy_hits = sum(row.count(HIT_SYMBOL) for row in guess_board)
    total_ship_segments = NUM_SHIPS * SHIP_SIZE
    return player_hits == total_ship_segments or enemy_hits == total_ship_segments


def main():
    """Main function to run the Battleship game."""
    player_name = get_player_name()
    clear_screen_enabled = get_player_preference()
    last_move_summary = ""  # Initialize an empty string for the last move summary

    print(f"Welcome to Battleship, {player_name}!")

    player_board = create_board(GRID_SIZE)  # Player's board
    enemy_board = create_board(GRID_SIZE)  # Enemy's board
    guess_board = create_guess_board(GRID_SIZE)  # Player's guess board

    place_ships(player_board, NUM_SHIPS, SHIP_SIZE)  # Place player's ships
    place_ships(enemy_board, NUM_SHIPS, SHIP_SIZE)  # Place enemy's ships

    enemy_previous_moves = set()  # Track enemy's previous moves

def main():
    """Main function to run the Battleship game."""
    player_name = get_player_name()
    clear_screen_enabled = get_player_preference()
    last_move_summary = ""  # Initialize an empty string for the last move summary

    print(f"Welcome to Battleship, {player_name}!")

    player_board = create_board(GRID_SIZE)  # Player's board
    enemy_board = create_board(GRID_SIZE)  # Enemy's board
    guess_board = create_guess_board(GRID_SIZE)  # Player's guess board

    place_ships(player_board, NUM_SHIPS, SHIP_SIZE)  # Place player's ships
    place_ships(enemy_board, NUM_SHIPS, SHIP_SIZE)  # Place enemy's ships

    enemy_previous_moves = set()  # Track enemy's previous moves

def main():
    player_name = get_player_name()
    clear_screen_enabled = get_player_preference()
    last_move_summary = ""

    print(f"Welcome to Battleship, {player_name}!")

    player_board = create_board(GRID_SIZE)
    enemy_board = create_board(GRID_SIZE)
    guess_board = create_guess_board(GRID_SIZE)

    place_ships(player_board, NUM_SHIPS, SHIP_SIZE)
    place_ships(enemy_board, NUM_SHIPS, SHIP_SIZE)

    enemy_previous_moves = set()

    while True:
        if clear_screen_enabled and last_move_summary:
            clear_screen()
            print(last_move_summary)

        if not clear_screen_enabled or last_move_summary:
            print(f"\n{player_name}'s Board:")
            print_board(player_board)
            print(f"\n{player_name}'s Guesses on Enemy's Board:")
            print_board(guess_board, hide_ships=True)

        player_row, player_col = player_move(guess_board)
        player_result = player_guess(enemy_board, guess_board, player_row, player_col)
        last_move_summary = f"Last Move: {player_result}"

        if is_game_over(player_board, guess_board, NUM_SHIPS, SHIP_SIZE):
            print(f"Congratulations, {player_name}! You have won the game!")
            break

        enemy_result = enemy_move(player_board, enemy_previous_moves)
        last_move_summary += f" | {enemy_result}"

        if is_game_over(player_board, guess_board, NUM_SHIPS, SHIP_SIZE):
            print(f"Sorry, {player_name}, you lost the game.")
            break

        if not clear_screen_enabled:
            print(last_move_summary)

if __name__ == "__main__":
    main()

# Testing the setup with a sample guess (replace with actual gameplay logic later)
print("Player's Board View:")
print_board(board)

# Sample guess (row 2, column 3)
player_guess(board, guess_board, 2, 3)  # Replace with player input

print("\nPlayer's Guess Board:")
print_board(guess_board)



