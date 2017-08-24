"""
Minefield object definition for playing text based minesweeper!

"""


import math
import random
import datetime
from typing import Tuple

# coord = Tuple[int]


class Minefield(object):

    def __init__(self, size: int, mines_n: int):
        self.size = size
        self.field = [['_' for n in range(size)] for i in range(size)]
        self.mines = None    # assignmed in self.laymines()

        self.flags = set()
        self.revealed = set()

        self.lay_mines(mines_n)
        self.game_over = False

    def __repr__(self):
        r = '{0.__class__.__name__}(size={0.size}, mines={0.mines})'.format(self)

    def __str__(self):
        print([str(i) for i in range(len(self))])    # column labels
        for i, row in enumerate(self.field):
            print(i, end='')                         # row labels
            print(row)

        mines_remaining = len(self.mines) - len(self.flags)
        return '{} Mines Remaining.'.format(mines_remaining)

    def __len__(self):
        return self.size

    @staticmethod
    def welcome():
        'Prints a nice welcome screen to stdout.'

        banner = "======================"
        print(banner)
        print('Welcome to Minesweeper.')
        print(banner)

    @classmethod
    def new_game(cls):
        'Initializes a new game with user input'

        board_size = int(input("Enter Board size >? "))
        mines = int(input("Enter number of mines >? "))

        minefield = cls(size=board_size, mines_n=mines)
        return minefield

    def check_win(self):
        'Checks if the game is a winner'

        if self.flags == self.mines:
            self.game_over = True
            return True
        else:
            return False

    def lose(self):
        'Mutate the game board, revealing all cells.'

        self.game_over = True
        for y, row in enumerate(self.field):
            for x, cell in enumerate(row):
                coord = (y, x)
                if coord not in self.mines:
                    value = self.count_mines(coord)
                else:
                    value = 'X'
                self.field[y][x] = value

        print(self)
        return

    def lay_mines(self, mines_n: int):
        'Populates a set of random mines coords.'

        random.seed('mine{}sweeper'.format(datetime.datetime.now()))
        #    mines_n = math.floor(self.size*0.10)    # for now make 10% of tiles mines

        self.mines = set()
        for _ in range(mines_n+1):
            x = random.randint(0, len(self)-1)
            y = random.randint(0, len(self)-1)
            self.mines.add((y, x))

    def count_mines(self, coord: Tuple[int]) -> int:
        neighbors= self.get_neighbors(coord)
        n = len(self.mines&neighbors)
        return n

    def get_neighbors(self, coord: Tuple[int]) -> set:
        """
        Look up, look down, jump around.
        """
        result = set()
        for y in range(-1, 2):
            for x in range(-1, 2):
                if (y, x) == coord:     # this coord
                    continue
                in_y_bounds = -1 < (coord[0]+y) < self.size
                in_x_bounds = -1 < (coord[1]+x) < self.size
                if in_y_bounds and in_x_bounds:
                    result.add((coord[0]+y, coord[1]+x))
        return result

    def flag(self, coord: Tuple[int]):
        if len(self.flags) <= len(self.mines):
            self.flags.add(coord)
            y, x = coord
            self.field[y][x] = 'F'
        return

    def unflag(self, coord Tuple[int]):
        self.flags.discard(coord)
        self.field[y][x] = '_'
        return

    def select(self, coord: Tuple[int]):
        if coord in self.mines:
            self.lose()
            return

        # Calcultate and reveal this coord.
        mines = self.count_mines(coord)
        y, x = coord
        self.field[y][x] = str(mines) if mines else ' '  # mutates board
        self.revealed.add(coord)

        if not mines:
            for n in self.get_neighbors(coord):
                if n not in self.mines and n not in self.flags and n not in self.revealed:
                    self.select(n)    # recursively with neibhor
        return
