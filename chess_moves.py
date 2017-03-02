"""
chess.py takes the following inputs and returns any legally available moves:
    Current Chess Board Configuration
    Current Active Player

For the purpose of this challenge, I can assume the current configuration
input is 8 lines representing each row with x for empty spaces and 
abbreviations for color & piece (br = black rook).

Active Player input will be one more line of just w or b for color.

    Sample board input for a starting setup:
    
    br,bn,bb,bq,bk,bb,bn,br
    bp,bp,bp,bp,bp,bp,bp,x
    x,x,x,x,x,x,x,x
    x,x,x,x,x,x,x,x
    x,x,x,x,x,x,x,x
    x,x,x,x,x,x,x,x
    wp,wp,wp,wp,wp,wp,wp,wp
    wr,wn,wb,wq,wk,wb,wn,wr

    Sample player input:
    
    w

Output will be provided as a piece by piece breakdown,
using algebraic notation to indicate column and row.

    Algebraic chess board:
    
       a    b    c    d    e    f    g    h
    8 [  ] [  ] [  ] [  ] [  ] [  ] [  ] [  ]   Black King Row
    7 [  ] [  ] [  ] [  ] [  ] [  ] [  ] [  ]   Black Pawns
    6 [  ] [  ] [  ] [  ] [  ] [  ] [  ] [  ]
    5 [  ] [  ] [  ] [  ] [  ] [  ] [  ] [  ]
    4 [  ] [  ] [  ] [  ] [  ] [  ] [  ] [  ]
    3 [  ] [  ] [  ] [  ] [  ] [  ] [  ] [  ]
    2 [  ] [  ] [  ] [  ] [  ] [  ] [  ] [  ]   White Pawns
    1 [  ] [  ] [  ] [  ] [  ] [  ] [wn] [  ]   White King Row

    Sample output:
    Knight (g1): f3, h3

    A white knight at g1 (starting position) has two available moves, f3 & h3

I have the luxury of assuming the inputs will formatted properly, but there are
many potential errors that could be checked for in a larger project:

    incorrect number of rows            (rows != 8)
    incorrect number of spaces in a row (spaces != 8)
    incorrect piece abbreviations       (abbreviation not in 'prnbqk')
    incorrect color codes               (color not in 'wb')
    uppercase letters                   (piece != piece.lower())
    
"""

# Author: Jarvis Mishler <jarvis.mishler@gmail.com>
# no imports, standard library stuff only



##########################################################
# useful functions    

        
def find_moves(piece):
    moves = []
    
    # coordinate shifts for standard movement patterns
    cross_moves = ['U','R','D','L']                                   # cross patterns for up, right, down, left
    diagonal_moves = ['UR','DR','DL','UL']                            # diagonals for up-right, down-right, etc
    move_changes = {'U':(0,-1),'R':(1,0),'D':(0,1),'L':(-1,0),        # coordinat shifts
                    'UR':(1,-1),'DR':(1,1),'DL':(-1,1),'UL':(-1,-1)} 
    move_options = {'rook':(cross_moves,7),                           # movement options and travel distances
                    'bishop':(diagonal_moves,7),
                    'queen':(cross_moves+diagonal_moves,7),
                    'king':(cross_moves+diagonal_moves,1)}

    if piece.name in move_options.keys():                             # rook, bishop, queen, or king
        available_paths, max_distance = move_options[piece.name]
        for path in available_paths:
            moves += walk(piece, move_changes[path], max_distance)
    elif piece.name == 'pawn':                                        # special snowflake move rules for pawn
        moves = pawn_moves(piece)
    else:                                                             # special snowflake move rules for knight
        moves = knight_moves(piece) 

    return moves
    
    
def find_pieces(color):
    player_pieces = []
    order = range(8)
    
    if color == 'b':       # orders by most aggressive positioning
        order.reverse()
        
    for row_index in order:
        row = board[row_index]
        
        for column_index in range(8):
            piece = row[column_index]
            
            if piece[0] == color:
                player_pieces.append(Piece(color, piece[1], column_index, row_index))
                
    return player_pieces


def knight_moves(piece):
    moves = []
    knight_options = [(-1,-2),(1,-2),   # 2 rows up and 1 column left/right
                      (2,-1),(2,1),     # 2 columns right and 1 row up/down
                      (1,2),(-1,2),     # 2 rows down and 1 column right/left
                      (-2,-1),(-2,-1)]  # 2 columns left and 1 row down/up

    for path in knight_options:
        moves += walk(piece, path, 1)
        
    return moves


def labeled_board(board):
    spaces = [space for row in board for space in row]  # concatenate the board

    for index, space in enumerate(spaces):              # pad the x spaces for formatting
        if space == 'x':
            spaces[index] = ' x '
        else:
            spaces[index] = ' ' + space

    output_board = ("   a   b   c   d   e   f   g   h\n"
                    "8 {} {} {} {} {} {} {} {}\n"
                    "7 {} {} {} {} {} {} {} {}\n"
                    "6 {} {} {} {} {} {} {} {}\n"
                    "5 {} {} {} {} {} {} {} {}\n"
                    "4 {} {} {} {} {} {} {} {}\n"
                    "3 {} {} {} {} {} {} {} {}\n"
                    "2 {} {} {} {} {} {} {} {}\n"
                    "1 {} {} {} {} {} {} {} {}")
                    
    return output_board.format(*spaces)


def pawn_moves(piece):
    if piece.color == 'white':            # rules for white pawns
        basic_path = (0,-1)               # up
        capture_paths = [(1,-1),(-1,-1)]  # up-right, up-left
        promotion_row = '8'               # row marking pawn promotion
        
        if piece.row == 6:
            max_distance = 2              # can move 2 spaces from starting row
        else:
            max_distance = 1
            
    else:                                 # rules for black pawns
        basic_path = (0,1)                # down
        capture_paths = [(1,1),(-1,1)]    # down-right, down-left
        promotion_row = '1'               # row marking pawn promotion
        
        if piece.row == 1:
            max_distance = 2              # can move 2 spaces from starting row
        else:
            max_distance = 1

    # can move forward but not capture
    moves = [move for move in walk(piece, basic_path, max_distance) if 'Capture' not in move]
    
    # can move diagonally in two directions but only to capture
    for path in capture_paths:
        moves += [move for move in walk(piece, path, 1) if 'Capture' in move]

    # check for pawn promotions
    for index, space in enumerate(moves):
        if promotion_row in space:
            space = 'Promote on ' + space
            moves[index] = space
            
    return moves

    
def readable_position(column, row):
    column = 'abcdefgh'[column]
    row = '87654321'[row]
    return column+row
    
    
def space_check(moves,color,column,row):
    occupant = board[row][column]
    stop = True
    
    if occupant[0] == 'x':
        moves.append(readable_position(column,row))
        stop = False
    elif occupant[0] != color[0]:
        name = Piece.piece_names[occupant[1]].title()
        moves.append(readable_position(column,row)+' (Capture {})'.format(name))

    return moves, stop


def walk(piece, steps, max_distance):
    column = piece.column
    row = piece.row
    color = piece.color
    column_step = steps[0]
    row_step = steps[1]
    moves = []
    stop = False

    while column in range(8) and row in range(8) and max_distance > 0:
        column += column_step
        row += row_step
        max_distance += -1

        if column not in range(8) or row not in range(8) or stop == True:
            break
        else:
            moves, stop = space_check(moves, color, column, row)
            
    return moves


##########################################################
# the Piece class to hold its attributes and moves

class Piece(object):
    piece_names = {'p':'pawn','r':'rook','n':'knight','b':'bishop','q':'queen','k':'king'}
    piece_colors = {'w':'white','b':'black'}
    
    def __init__(self,color,name,column,row):
        self.color = Piece.piece_colors[color]
        self.name = Piece.piece_names[name]
        self.column = column
        self.row = row
        self.moves = find_moves(self)
        
    def __str__(self):
        name = self.name.title()
        position = readable_position(self.column, self.row)
        
        return '{} ({})'.format(name, position)

       
       
##########################################################
# main logic

if __name__ == "__main__":

    # take input for board configuration and player color
    print
    print "Please provide the current configuration of a chess board:"
    board = [raw_input().split(',') for _ in range(8)]
    print
    print "Who's turn is it? Type w or b for white or black: "
    color = raw_input()

    # find pieces belonging to the active player
    available_pieces = find_pieces(color)

    # output board with row and column labels
    print
    print
    print "***** CURRENT BOARD *****"
    print
    print labeled_board(board)

    # output available moves
    print
    print "***** AVAILABLE MOVES *****"
    print
    for p in available_pieces:
        print '{}: {}'.format(p, ', '.join(p.moves))
