import numpy as np
from collections import defaultdict


class QLearning:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=1.0, min_epsilon=0.1, epsilon_decay=0.000001):
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay

    def get_action(self, state, valid_moves):
        if np.random.random() < self.epsilon:
            return self.get_random_action(valid_moves)
        else:
            return self.get_best_action(state, valid_moves)

    def decay_epsilon(self):
        self.epsilon -= self.epsilon_decay
        self.epsilon = max(self.min_epsilon, self.epsilon)

    def get_random_action(self, valid_moves):
        return valid_moves[np.random.randint(len(valid_moves))]

    def get_best_action(self, state, valid_moves):
        best_action = None
        best_value = float('-inf')
        for action in valid_moves:
            action_value = self.q_table[state][action]
            if action_value > best_value:
                best_value = action_value
                best_action = action
        return best_action

    def update(self, state, action, reward, next_state, done):
        best_next_value = max(self.q_table[next_state].values()) if self.q_table[next_state] and not done else 0
        current_value = self.q_table[state][action]
        new_value = current_value + self.alpha * (reward + self.gamma * best_next_value - current_value)
        self.q_table[state][action] = new_value
