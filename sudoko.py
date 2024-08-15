import copy
import random

import Simulated_Annealing

class Sudoku:
    def __init__(self,table:list):
        self.table = table
        self.missing_numbers =None
    def solve(self):
        self.missing_numbers = self.get_missing_numbers_in_grid()
        dimension = 0
        for i in self.missing_numbers:
            dimension += len(i)
        sa = Simulated_Annealing.SimulatedAnnealing(start_temperature=1, stop_temperature=0, alpha=0.9999,
                                                    iterations_number=10000, print_xn=False,
                                                    temperature_method='logarithmic', print_probabilities=False)
        c, xn = sa.multiple_annealing(3,dimension ,self.count_sudoku_mistakes, self.neighbors, self.initial_random, minimum=0)
        self.print_sudoku(self.fill_table(xn))
        print(f"conflicts is {self.count_sudoku_mistakes(xn)}")
    def print_sudoku(self, sudoku):
        """Function to print the Sudoku grid in a readable format."""
        for i in range(9):
            row = ''
            for j in range(9):
                num = sudoku[i][j]
                if num == 0:
                    row += '. '
                else:
                    row += str(num) + ' '
                if (j + 1) % 3 == 0 and j < 8:
                    row += '| '
            print(row)
            if (i + 1) % 3 == 0 and i < 8:
                print('-' * 21)
        print('\n')

    def get_empty_block_cells(self, block_row, block_col):
        cells = []
        for i in range(3):
            for j in range(3):
                row = block_row * 3 + i
                col = block_col * 3 + j
                if self.table[row][col] == 0:
                    cells.append((row, col))
        return cells

    def get_block_cells(self, block_row, block_col):
        """
        Function to get the list of cell coordinates in a given 3x3 block.
        """
        cells = []
        for i in range(3):
            for j in range(3):
                row = block_row * 3 + i
                col = block_col * 3 + j
                cells.append((row, col))
        return cells

    def complete_obvious_slots(self):
        # complete column if only one slot was missing
        table_transpose = [[self.table[j][i] for j in range(len(self.table))] for i in range(len(self.table[0]))]
        for index, row in enumerate(table_transpose):
            all_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for number in row:
                if number > 0:
                    all_numbers.remove(number)
            if len(all_numbers) == 1:
                for ind in range(len(row)):
                    if row[ind] == 0:
                        row[ind] = all_numbers[0]

        # complete row if only one slot was missing
        for index, row in enumerate(self.table):
            all_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for number in row:
                if number > 0:
                    all_numbers.remove(number)
            if len(all_numbers) == 1:
                for ind in range(len(row)):
                    if row[ind] == 0:
                        row[ind] = all_numbers[0]

        # complete grid if only one slot was missing
        for block_row in range(3):
            for block_column in range(3):
                all_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                slots = self.get_block_cells(block_row, block_column)
                none_index = None
                for slot in slots:
                    row, column = slot
                    number = self.table[row][column]
                    if number > 0:
                        all_numbers.remove(number)
                    else:
                        none_index = (row, column)
                if len(all_numbers) == 1:
                    self.table[none_index[0]][none_index[1]] = all_numbers[0]

    def get_missing_numbers_in_grid(self):
        missing_numbers = []
        for block_row in range(3):
            for block_column in range(3):
                all_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                slots = self.get_block_cells(block_row, block_column)
                for slot in slots:
                    row, column = slot
                    number = self.table[row][column]
                    if number > 0:
                        all_numbers.remove(number)
                missing_numbers.append(all_numbers.copy())
        return missing_numbers

    def initial_random(self):
        for row_index, row in enumerate(self.missing_numbers):
            random.shuffle(row)
        return self.missing_numbers

    def neighbors(self, missing_numbers:list):
        missing_numbers_cop = copy.deepcopy(missing_numbers)
        grid = None
        while True:
            grid = random.choice(missing_numbers_cop)
            if len(grid) > 0:
                break

        index1 = random.choice(range(len(grid)))
        index2 = random.choice(range(len(grid)))
        temp = grid[index1]
        grid[index1] = grid[index2]
        grid[index2] = temp
        return missing_numbers_cop

    def fill_table(self,missing_numbers: list):
        table = copy.deepcopy(self.table)
        for grid_index,grid in enumerate(missing_numbers):
            empty_slots = self.get_empty_block_cells(int(grid_index/3), grid_index%3)
            for index, number in enumerate(grid):
                slot = empty_slots[index]
                row, col = slot
                table[row][col] = number
        return table

    def count_sudoku_mistakes(self,missing_numbers: list):
        """
        Function to count the total number of conflicts in the Sudoku grid.
        Conflicts are counted in rows and columns.
        """
        sudoku = self.fill_table(missing_numbers)
        conflicts = 0
        # Check rows
        for i in range(9):
            counts = [0] * 10  # Numbers 1-9
            for j in range(9):
                num = sudoku[i][j]
                if num != 0:
                    counts[num] += 1
            conflicts += sum([count - 1 for count in counts if count >= 1])
        # Check columns
        for j in range(9):
            counts = [0] * 10  # Numbers 1-9
            for i in range(9):
                num = sudoku[i][j]
                if num != 0:
                    counts[num] += 1
            conflicts += sum([count - 1 for count in counts if count >= 1])
        return conflicts



table1 = [[0,0,0,0,0,0,6,5,0],
          [1,0,0,7,0,0,0,0,0],
          [0,0,0,0,0,0,8,0,0],
          [9,0,0,0,0,5,0,4,0],
          [0,7,0,6,0,0,0,0,0],
          [3,0,0,0,3,8,0,0,0],
          [0,0,0,2,0,0,0,0,9],
          [0,8,3,0,0,0,0,0,0],
          [0,0,6,0,0,0,0,0,0]]

sod = Sudoku(table1)
sod.solve()