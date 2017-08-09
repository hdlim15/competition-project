from __future__ import print_function # Debugging purposes
import sys

# Debugging purposes
def dbg(text):
    print(text, file=sys.stderr)
    sys.stderr.flush()


DIRS = [
    ((-1, 0), "up"),
    ((0, 1), "right"),
    ((1, 0), "down"),
    ((0, -1), "left")
]


# can modify this to look at string directly
def get_field_index(row, col):
    return row*16 + col

class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell = [["." for col in range (0, width)] for row in range(0, height)]

        self.my_botid = "-1"
        self.other_botid = "-1"
        self.my_bot_position = (-1, -1)
        self.other_bot_position = (-1, -1)

    def find_starting_pos(self, my_botid, field):
        self.my_botid = str(my_botid)
        self.other_botid = str(1 - my_botid)
        field_array = field.split(",")
        for row in range(1, 15):
            for col in range(1, 7):
                cell_value = field_array[get_field_index(row, col)]
                if (cell_value == "0" or cell_value == "1"):
                    if (self.my_botid == cell_value):
                        self.my_bot_position = (row, col)
                        self.other_bot_position = (row, 15-col)
                        self.cell[row][col] = self.my_botid
                        self.cell[row][15-col] = self.other_botid
                    else:
                        self.my_bot_position = (row, 15-col)
                        self.other_bot_position = (row, col)
                        self.cell[row][15-col] = self.my_botid
                        self.cell[row][col] = self.other_botid

    def block_cell(self, position):
        (row, col) = position
        self.cell[row][col] = "x"

    def update_board(self, new_board):
        new_board = new_board.split(",")
        self.output()

        self.block_cell(self.my_bot_position)
        self.block_cell(self.other_bot_position)

        for (row, col) in self.get_adjacent(self.my_bot_position):
            potential_pos = new_board[get_field_index(row, col)]
            if potential_pos == self.my_botid:
                self.my_bot_position = (row, col)
                self.cell[row][col] = self.my_botid
                break

        for (row, col) in self.get_adjacent(self.other_bot_position):
            potential_pos = new_board[get_field_index(row, col)]
            if potential_pos == self.other_botid:
                self.other_bot_position = (row, col)
                self.cell[row][col] = self.other_botid
                break


    def is_legal(self, row, col):
        return self.cell[row][col] == "." and row>=0 and col>=0 and col<self.width and row<self.height

    def is_legal_tuple(self, loc):
        row, col = loc
        return self.is_legal(row, col)

    def get_adjacent(self, position):
        row, col = position
        result = []
        for (o_row, o_col), _ in DIRS:
            t_row, t_col = o_row + row, o_col + col
            if self.is_legal(t_row, t_col):
                result.append((t_row, t_col))
        return result

    def legal_moves(self):
        result = []
        (row, col) = self.my_bot_position
        for ((o_row, o_col), order) in DIRS:
            t_row = row + o_row
            t_col = col + o_col
            if self.is_legal(t_row, t_col):
                result.append(order)
        return result   

    def output(self):
        for row in self.cell:
            dbg(str(row) + "\n")
