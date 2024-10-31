import json
from collections import defaultdict
import ast
import numpy as np

def parse_numpy_array(array_str):
    # Remove brackets and split by spaces
    return tuple(float(x) for x in array_str.strip('[]').split())

def load_q_table(filename):
    try:
        with open(filename, 'r') as f:
            q_table_dict = json.load(f)
        
        converted_table = {}
        for state_str, moves in q_table_dict.items():
            state = parse_numpy_array(state_str)
            converted_table[state] = {
                ast.literal_eval(move_str): value
                for move_str, value in moves.items()
            }
        
        return defaultdict(lambda: defaultdict(float), converted_table)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred while loading the Q-table: {str(e)}")
    
    return defaultdict(lambda: defaultdict(float))

def print_q_values(state, q_table):
    if state in q_table:
        print(f"Q-values for state {state}:")
        for move, value in q_table[state].items():
            print(f"  Move {move}: {value:.4f}")
    else:
        print(f"No Q-values found for state {state}")

# Example usage:
loaded_q_table = load_q_table('qtable.json')


from tictactoe import Tictactoe  # Assuming you have the TicTacToe class in tictactoe.py
import numpy as np
from collections import defaultdict

# Assuming you already have this function
def get_best_action(state, valid_moves, q_table):
    state_tuple = tuple(float(x) for x in state)
    if state_tuple in q_table:
        return max(valid_moves, key=lambda move: q_table[state_tuple].get(move, float('-inf')))
    return valid_moves[np.random.randint(len(valid_moves))]

# Function to play the game where AI goes first
def play_against_ai(q_table):
    game = Tictactoe()
    game.reset()
    
    while True:
        game.print_board()
        
        # Check if the game is over
        winner = game.checkWin()
        if winner is not None:
            if winner == 1:
                print("AI (Player X) wins!")
            elif winner == 2:
                print("Human (Player O) wins!")
            else:
                print("It's a tie!")
            break

        # AI's move (Player 1 - X)
        if game.currentPlayer == 1:
            valid_moves = game.get_valid_moves()
            current_state = game.get_state()
            best_move = get_best_action(current_state, valid_moves, q_table)
            print(f"AI chooses move: {best_move}")
            game.move(*best_move)

        # Human's move (Player 2 - O)
        else:
            valid_moves = game.get_valid_moves()
            move = eval(input(f"Your move (row, col): {valid_moves} "))  # Expecting input as tuple (row, col)
            row, col = move
            if not game.move(row, col):
                print("Invalid move, try again.")
                continue

# Example usage:
# Assuming the Q-table is loaded and stored in loaded_q_table
loaded_q_table = load_q_table('qtable.json')
play_against_ai(loaded_q_table)
