from tictactoe import Tictactoe
from qlearning import QLearning
import numpy as np
import json

def train(num_episodes=1000000):
    game = Tictactoe()
    agent = QLearning()
    for episode in range(num_episodes):
        state = game.reset()
        done = False
        winner = None
        while not done:
            if winner is None:
                valid_moves = game.get_valid_moves()
                if not valid_moves:  # If no valid moves, it's a draw
                    winner = 0
                    done = True
                    reward = 0.5
                else:
                    action = agent.get_action(state, valid_moves)
                    row, col = action
                    game.move(row, col)
                    winner = game.checkWin()
                    
            if not done:
                # Opponent's turn (random move)
                valid_moves = game.get_valid_moves()
                if not valid_moves:  # If no valid moves, it's a draw
                    winner = 0
                    done = True
                    reward = 0.5
                else:
                    opponent_move = valid_moves[np.random.randint(len(valid_moves))]
                    game.move(opponent_move[0], opponent_move[1])
                    next_state = game.get_state()
                    winner = game.checkWin()

            if winner is not None:
                done = True
                if winner == 1:  # AI wins
                    reward = 1
                elif winner == 0:  # Draw
                    reward = 0.5
                else:  # AI loses
                    reward = -1
            else:
                reward = 0

            agent.update(state, action, reward, next_state, done)
            state = next_state

        agent.decay_epsilon()
        if episode % 10000 == 0:
            print(f"Episode {episode} completed. Epsilon: {agent.epsilon:.4f}")
    
    return agent

def save_q_table(q_table, filename):
    def tuple_to_str(item):
        if isinstance(item, dict):
            return {str(k): tuple_to_str(v) for k, v in item.items()}
        elif isinstance(item, tuple):
            return str(item)
        else:
            return item
    with open(filename, 'w') as f:
        q_table_dict = tuple_to_str(dict(q_table))
        json.dump(q_table_dict, f)
# Train the agent
trained_agent = train()
save_q_table(trained_agent.q_table,"qtable")

# Play against the trained AI
game = Tictactoe()