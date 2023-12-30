from colorama import init, Fore, Back, Style
init(autoreset=True)  # Initialize Colorama and automatically reset styles after each print statement
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
    choice = input(Fore.MAGENTA +  "Do you want to clear the screen each turn? (yes/no): ").lower()
    return choice == "yes"

def get_player_name():
    """Prompt the player to enter their name, ensuring it's valid (letters only, single word)."""
    while True:
        name = input(Fore.MAGENTA + "Please enter your name (letters only, no spaces): ")
        if name.isalpha() and " " not in name:
            return name
        else:
            print(Fore.RED + "Invalid name. Please enter a name with letters only and no spaces.")


# Initialize the game board
def create_board(size):
    """Initialize the game board with the specified size."""
    return [["."] * size for _ in range(size)]



def print_board(board, board_type, hide_ships=False):
    """Prints the game board with color-coded symbols and borders."""
    board_color = Fore.GREEN if board_type == 'player' else Fore.YELLOW

    # Create top border
    top_border = "  +" + "---+" * GRID_SIZE
    print(board_color + top_border)

    # Print header row with column numbers
    header = "   " + "   ".join(str(i + 1) for i in range(GRID_SIZE))
    print(board_color + header)

    # Print each row with a border
    for row_index, row in enumerate(board):
        colored_row = [
            Fore.RED + HIT_SYMBOL if cell == HIT_SYMBOL else
            Fore.BLUE + MISS_SYMBOL if cell == MISS_SYMBOL else
            board_color + SHIP_SYMBOL if cell == SHIP_SYMBOL and not hide_ships else
            board_color + cell
            for cell in row
        ]
        row_str = " | ".join(colored_row)
        print(board_color + f"{chr(65 + row_index)} | {row_str} |")

    # Create bottom border
    print(board_color + top_border)



# Initialize the guess board
def create_guess_board(size):
    """Initialize the guess board with the specified size."""
    return [["~"] * size for _ in range(size)]


# Game rules display
def display_game_rules():
    """Display the game rules to the player."""
    print(Fore.CYAN + "Welcome to Battleship the game in Python.")
    print(Fore.CYAN + "Board size: 8x8")
    print(Fore.CYAN + "Number of ships: 4")
    print(Fore.CYAN + "Length of each ship: 3")
    print(Fore.CYAN + "Top left corner is: Row A, Column 1")
    print(Fore.CYAN + "'S' represents ships on your board.")

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
    # Loop until the specified number of ships are placed
    while ships_placed < num_ships:
        # Randomly choose a starting position and orientation for the ship
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        orientation = random.choice(['horizontal', 'vertical'])
        
        # Check if the ship can be placed at the chosen position
        if can_place_ship(board, row, col, ship_size, orientation):
            # Place the ship and increment the counter
            set_ship(board, row, col, ship_size, orientation)
            ships_placed += 1

def is_valid_placement(board, start_row, start_col, ship_size, orientation):
    """
    Check if a ship can be placed at the specified location without overlapping other ships.
    """
    if orientation == 'horizontal':
        if start_col + ship_size > GRID_SIZE:
            return False
        for c in range(start_col, start_col + ship_size):
            if board[start_row][c] == SHIP_SYMBOL:
                return False
    else:  # vertical
        if start_row + ship_size > GRID_SIZE:
            return False
        for r in range(start_row, start_row + ship_size):
            if board[r][start_col] == SHIP_SYMBOL:
                return False
    
    return True



# Check if a ship can be placed at the specified location
def can_place_ship(board, row, col, ship_size, orientation):
    """ 
    Check if a ship can be placed at the specified location with proper spacing.
    """
    # Ensure the ship doesn't overlap with another ship and is within grid boundaries
    if not is_valid_placement(board, row, col, ship_size, orientation):
        return False

    # Check for spacing around the ship
    if orientation == 'horizontal':
        for c in range(max(0, col - 1), min(GRID_SIZE, col + ship_size + 1)):
            if any(board[r][c] == SHIP_SYMBOL for r in range(max(0, row - 1), min(GRID_SIZE, row + 2))):
                return False
    else:  # vertical
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
        user_input = input(Fore.CYAN + "Enter your move (e.g., A3): ").upper()
        try:
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


def enemy_move(player_board, previous_moves, last_hit):
    """Generate a move for the enemy with a strategy after a hit."""
    if last_hit and isinstance(last_hit, tuple) and len(last_hit) == 2 and all(isinstance(coord, int) for coord in last_hit):
        # Strategy: Check adjacent cells in a specific order after a hit
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, down, left, right
            new_row, new_col = last_hit[0] + dx, last_hit[1] + dy
            # Validate the new position is within the board and not previously tried
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                if (new_row, new_col) not in previous_moves and player_board[new_row][new_col] != MISS_SYMBOL:
                    # Add the new move to previous moves and process the guess
                    previous_moves.add((new_row, new_col))
                    return make_enemy_guess(player_board, new_row, new_col)

    # Random move if no hit to follow up or all adjacent cells have been guessed
    return random_enemy_guess(player_board, previous_moves)



def make_enemy_guess(player_board, row, col):
    """Process the enemy's guess."""
    if player_board[row][col] == SHIP_SYMBOL:
        player_board[row][col] = HIT_SYMBOL
        return (row, col), f"Enemy hit your ship at {chr(65 + row)}{col + 1}!"
    else:
        player_board[row][col] = MISS_SYMBOL
        return None, f"Enemy missed at {chr(65 + row)}{col + 1}."

def random_enemy_guess(player_board, previous_moves):
    """Generate a random move for the enemy."""
    while True:
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (row, col) not in previous_moves:
            previous_moves.add((row, col))
            return make_enemy_guess(player_board, row, col)

        
def update_board_after_move(board, guess_board, row, col, is_player_turn):
    """Update the board after a move."""
    pass

def is_game_over(player_board, guess_board, NUM_SHIPS, SHIP_SIZE):
    """Check if the game is over (all ships on either board have been hit)."""
    player_hits = sum(row.count(HIT_SYMBOL) for row in player_board)
    enemy_hits = sum(row.count(HIT_SYMBOL) for row in guess_board)
    total_ship_segments = NUM_SHIPS * SHIP_SIZE
    return player_hits == total_ship_segments or enemy_hits == total_ship_segments

def prompt_for_restart():
    """Ask the player if they want to restart the game."""
    while True:
        choice = input(Fore.MAGENTA + "Do you want to play again? (Please enter 'yes' to play again or 'no' to quit.): ").lower()
        if choice in [Fore.MAGENTA + "yes", "no"]:
            return choice == "yes"
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def display_initial_menu():
    """Displays the initial game menu and handles the player's choice."""
    while True:
        print(Fore.CYAN + Style.BRIGHT + r"""
                  |__
                  |\/
                  ---
                  / | [
           !      | |||
         _/|     _/|-++'
     +  +--|    |--|--|_ |-
  { /|__|  |/\__|  |--- |||__/
 +---------------___[}-_===_.'____                 /\
 /\   \____    \_       \ \_____|__ \           /    \  
  / \   \___>   \ \______]_|__      \_________/_       \ 
 /   \______-/  \         /         /     |  /           \ 
/___/___________|        /_________/     /__________/_  
                   \    /             \  /   /      
                    \  /               \/   /        
                     \/                   \/
    """)
        print(Fore.YELLOW + "-------------------------------")
        print(Fore.GREEN + Style.BRIGHT + "      Battleship Game")
        print(Fore.YELLOW + "-------------------------------")
        print("1. Start Game")
        print("2. Quit")
        choice = input("Select an option: ")

        if choice == '1':
            return True  # Continue to the game
        elif choice == '2':
            return False  # Exit the game
        else:
            print("Invalid choice. Please select 1 or 2.")


def main():
    if not display_initial_menu():
        print("Exiting the game. Goodbye!")
        return

    display_game_rules() 
    player_name = get_player_name()
    clear_screen_enabled = get_player_preference()
    player_wins = 0  # Counter for player's wins
    player_losses = 0  # Counter for player's losses
    
   
    while True:
        print(f"Welcome to Battleship, {player_name}!")

        player_board = create_board(GRID_SIZE)
        enemy_board = create_board(GRID_SIZE)
        guess_board = create_guess_board(GRID_SIZE)

        place_ships(player_board, NUM_SHIPS, SHIP_SIZE)
        place_ships(enemy_board, NUM_SHIPS, SHIP_SIZE)

        enemy_previous_moves = set()
        last_move_summary = ""
        last_hit = None 
        

        while True:
            if clear_screen_enabled and last_move_summary:
                clear_screen()
                print(last_move_summary)


            if not clear_screen_enabled or last_move_summary:
                print(Fore.GREEN + f"\n{player_name}'s Board:")
                print_board(player_board, 'player')
                print(Fore.GREEN + f"\n{player_name}'s Guesses on Enemy's Board:")
                print_board(guess_board, 'enemy', hide_ships=True)

                
        
            player_row, player_col = player_move(guess_board)
            player_result = player_guess(enemy_board, guess_board, player_row, player_col)
            last_move_summary = f"Last Move: {player_result}"


            if is_game_over(player_board, guess_board, NUM_SHIPS, SHIP_SIZE):
                print(Fore.RED + f"Congratulations, {player_name}! You have won the game!")
                player_wins += 1
                break

            enemy_result, hit_coords = enemy_move(player_board, enemy_previous_moves, last_hit)
            last_move_summary += f" | {enemy_result}"
            if hit_coords:
                last_hit = hit_coords  # Update last_hit if there's a new hit
            else:
                last_hit = None  # Reset last_hit if the enemy misses


            if is_game_over(player_board, guess_board, NUM_SHIPS, SHIP_SIZE):
                print(Fore.RED + f"Sorry, {player_name}, you lost the game.")
                player_losses += 1
                break
                
         # Ask if the player wants to play again or quit
        if not prompt_for_restart():
            print("Thanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()

# Testing the setup with a sample guess (replace with actual gameplay logic later)
print("Player's Board View:")
print_board(board)

# Sample guess (row 2, column 3)
player_guess(board, guess_board, 2, 3)  # Replace with player input

print("\nPlayer's Guess Board:")
print_board(guess_board)