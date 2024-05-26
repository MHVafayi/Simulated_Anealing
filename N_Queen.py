import random
import turtle
import Simulated_Annealing


def generate_chess_board():
    board = []
    for i in range(8):
        board.append(8*random.choice(range(8))+i)
    return board


def checkNeighboursSA(board):
    place = random.choice(range(8))
    # if queen is in the first row who's neighbours are being checked
    if board[place] <= 7:
        board[place] += 8

    # if queen is in the last row who's neighbours are being checked
    elif board[place] >= 56:
        board[place] -= 8

    # if in between first and last row
    else:
        check = random.randrange(0, 2)  # randomly choose any neighbour
        if check == 1:
            board[place] -= 8
        else:
            board[place] += 8
    return board


def n_queen(board: list):
    temp_board =[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
    for i in board:
        temp_board[int(i/8)][i%8] = 1
    count = 0
    for i in range(8):
        for j in range(8):
            if temp_board[i][j] == 1:
                # checking other queens in the same row
                col = 0
                while col != 8:
                    if col != j and temp_board[i][col] == 1:
                        count += 1
                    col += 1

                # checking queens in the same column
                row = 0
                while row != 8:
                    if row != i and temp_board[row][j] == 1:
                        count += 1
                    row += 1

                # checking queens in the area above main diagonal
                row = i - 1
                col = j - 1
                while row != -1 and col != -1:
                    if temp_board[row][col] == 1:
                        count += 1
                    row -= 1
                    col -= 1

                # checking queens in the area below main diagonal
                row = i + 1
                col = j + 1
                while row != 8 and col != 8:
                    if temp_board[row][col] == 1:
                        count += 1
                    row += 1
                    col += 1

                # checking queens in the area above reverse diagonal
                row = i - 1
                col = j + 1
                while row != -1 and col != 8:
                    if temp_board[row][col] == 1:
                        count += 1
                    row -= 1
                    col += 1

                # checking queens in the area below reverse diagonal
                row = i + 1
                col = j - 1
                while row != 8 and col != -1:
                    if temp_board[row][col] == 1:
                        count += 1
                    row += 1
                    col -= 1
    return int(count/2)


sa = Simulated_Annealing.SimulatedAnnealing(start_temperature=50000, stop_temperature=0.00000001, alpha=0.99, iterations_number=10000, print_xn=False)
c, xn = sa.start_annealing(8, n_queen, checkNeighboursSA, generate_chess_board)

# create screen object
sc = turtle.Screen()
# create turtle object
pen = turtle.Turtle()
# method to draw square
# def draw_circle():
def draw():
    for i in range(4):
        pen.forward(30)
        pen.left(90)

    pen.forward(30)

sc.setup(600, 600)

# set turtle object speed
pen.speed(1000)
# loops for board
for i in range(8):
    # not ready to draw
    pen.up()

    # set position for every row
    pen.setpos(-120, 30 * i - 120)

    # ready to draw
    pen.down()

    # row
    for j in range(8):
        if i*8+j in xn:
            col = 'red'
        # conditions for alternative color
        elif (i + j) % 2 == 0:
            col = 'black'
        else:
            col = 'white'

        # hide the turtle
        pen.hideturtle()

        # fill with given color
        pen.fillcolor(col)

        # start filling with colour
        pen.begin_fill()

        # call method
        draw()

        # stop filling
        pen.end_fill()

sc.mainloop()