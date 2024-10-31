import numpy as np

n = 3

class Tictactoe:
    def __init__(self):
        self.board = np.zeros(shape=(n,n))
        self.currentPlayer = 1
        
    def reset(self):
        self.board = np.zeros(shape=(n,n))
        self.currentPlayer = 1
        return self.get_state()

    def get_state(self):
        return tuple(self.board.flatten())
    
    def isValid(self,row,col):
        return self.board[row][col] == 0
    
    def move(self,row,col):
        if self.isValid(row,col):
            self.board[row][col] = self.currentPlayer
            self.currentPlayer = 3 - self.currentPlayer
            return True
        return False
    
    def checkWin(self):
        for i in range(3):
            if np.all(self.board[i, :] == 1) or np.all(self.board[:, i] == 1):
                return 1
            if np.all(self.board[i, :] == 2) or np.all(self.board[:, i] == 2):
                return 2
        if np.all(np.diag(self.board) == 1) or np.all(np.diag(np.fliplr(self.board)) == 1):
            return 1
        if np.all(np.diag(self.board) == 2) or np.all(np.diag(np.fliplr(self.board)) == 2):
            return 2
        if np.all(self.board != 0):
            return 0  
        return None  
    
    def get_valid_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    def print_board(self):
        symbols = {0: ' ', 1: 'X', 2: 'O'}
        for row in self.board:
            print('|' + '|'.join(symbols[cell] for cell in row) + '|')
            print('-' * 7)

"""tic = Tictactoe()
for i in range(100):
    m = eval(input("Enter a move: "))
    row, col = m
    tic.move(row,col)
    tic.print_board()
    if tic.checkWin():
        break
print("Yo you win!")
"""