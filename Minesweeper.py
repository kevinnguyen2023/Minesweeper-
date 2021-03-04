import random
import re


# Creating a board object that shows the Minesweeper game
class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.making_board() # Planting the bombs
        self.assign_values_on_board()

        # Initialize a set to keep track which locations that's uncovered
        self.dug = set() # If digging at 0, 0 then self.dug = {(0,0)}
    
    def making_board(self):
        # Making a new board based on dim size and number of bombs
        # Construct the list of lists 

        # Making a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # Planting the bombs
        bombs_planted = 0 
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1) # Returns random integer N such that a <= n <= b
            row = loc // self.dim_size # Number of times dim_size going to location knowing which row to look
            col = loc % self.dim_size # The remainder that shows which index in the row to look at

            if board[row][col] == '*':
                # Planted the bomb successfully which keeps going
                continue

            board[row][col] = '*'
            bombs_planted += 1 
        return board

    def assign_values_on_board(self):
        # Assign a number 0 - 8 for all empty spaces showing how many neighboring bombs are there 
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue 
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)
    
    def get_num_neighboring_bombs(self, row, col):
        # Iterating through each of the neighboring positions and sum number of bombs
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)
        # Do not go out of bounds!

        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size - 1, row+1) + 1):
            for c in range(max(0, col-1), min(self.dim_size - 1, col+1) + 1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
    
        return num_neighboring_bombs

    def dig(self, row, col):
        # Dig at this location!
        # Return True if successful, False if digging bomb

        # Scenarios:
        # Hit a bomb = Game Over
        # Dig at location with neighboring bombs = Complete dig
        # Dig at location with no neighboring bombs = Recursively dig neighbors

        self.dug.add((row, col)) # Keep track of digging here

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        for r in range (max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r,c) in self.dug:
                    continue  # don't dig where you already dug
                self.dig(r, c)

        # If initial dig didn't hit bomb, should not hit a bomb here
        return True 

    def __str__(self):
        # Returns a string that shows board to the player

        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

            # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len
        
        return string_rep


# Playing the Minesweeper game
def play(dim_size = 10, num_bombs = 10):
    # 1. Create board and plant the bombs
    board = Board(dim_size, num_bombs)

    # 2. show user the board and ask where they choose to dig
    # 3a. if location is a bomb, show game over message
    # 3b. if location is not a bomb, dig using recursion until each square is next to a bomb
    # 4. repeat steps 2 and 3a/3b until there are no more places to dig (Victory!)
    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where do you choose to dig? Give input of numbers in this format: row,column"))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue

        # if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            break # (Game Over)

    # 2 ways to end loop
    if safe:
        print("CONGRATULATIONS!! YOU FINSIHED THIS GAME!")
    else:
        print("Game Over... You lost")
        # Revealing the whole board!
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__': 
    play()