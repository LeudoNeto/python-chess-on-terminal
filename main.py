class Pieces:
    alives = []
    whites = []
    blacks = []
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
        if self.color == 'white':
            Pieces.whites.append(self)
        elif self.color == 'black':
            Pieces.blacks.append(self)
        Pieces.alives.append(self)

class Pawn(Pieces):
    white_emoji = '♙'
    black_emoji = '♟'
    def move_possibilites(self):
        if self.color == 'white':
            return [[self.x,self.y+1],[self.x,self.y+2]]
        elif self.color == 'black':
            return [[self.x,self.y-1],[self.x,self.y-2]]

class Rook(Pieces):
    white_emoji = '♖'
    black_emoji = '♜'
    def move_possibilites(self):
        poss = []
        for x in range(0,8):
            if x != self.x:
                poss.append([x,self.y])
        for y in range(0,8):
            if y != self.y:
                poss.append([self.x,y])
        return poss

class Horse(Pieces):
    white_emoji = '♘'
    black_emoji = '♞'
    def move_possibilites(self):
        return [[self.x+1,self.y+2],[self.x+2,self.y+1],[self.x+2,self.y-1],[self.x+1,self.y-2],[self.x-1,self.y-2],[self.x-2,self.y-1],[self.x-2,self.y+1],[self.x-1,self.y+2]]

class Bishop(Pieces):
    white_emoji = '♗'
    black_emoji = '♝'
    def move_possibilites(self):
        poss = []
        for x in range(0,8):
            for y in range(0,8):
                if (x - self.x == y - self.y) or (x - self.x == self.y - y):
                    if (x,y) != (self.x,self.y):
                        poss.append([x,y])
        return poss

class King(Pieces):
    white_emoji = '♔'
    black_emoji = '♚'
    def move_possibilites(self):
        poss = []
        for x in range(0,8):
            for y in range(0,8):
                if (-2 < x - self.x < 2) and (-2 < y - self.y < 2):
                    if (x,y) != (self.x,self.y):
                        poss.append([x,y])
        return poss

class Queen(Pieces):
    white_emoji = '♕'
    black_emoji = '♛'
    def move_possibilites(self):
        poss = []
        for x in range(0,8):
            if x != self.x:
                poss.append([x,self.y])
            for y in range(0,8):
                if (x - self.x == y - self.y) or (x - self.x == self.y - y):
                    if (x,y) != (self.x,self.y):
                        poss.append([x,y])
        for y in range(0,8):
            if y != self.y:
                poss.append([self.x,y])
        return poss

def board():
    print('-'*27)
    for y in range(7,-1,-1):
        print(f'{y+1} ',end = ' ')
        for x in range(0,8):
            if (x+y) % 2 == 0:
                print(f'\033[40m   \033[m',end='')
            else:
                print(f'\033[47m   \033[m',end='')
        print('')
    print('    a  b  c  d  e  f  g  h')
    print('-'*27)

p1 = Pawn(0,0,'white')

while True:
    pieces_coords = []
    whites_coords = []
    blacks_coords = []
    for piece in Pieces.alives:
        pieces_coords.append([piece.x,piece.y])
    for white in Pieces.whites:
        whites_coords.append([white.x,white.y])
    for black in Pieces.blacks:
        blacks_coords.append([black.x,black.y])
    board()
    break

print(pieces_coords.index([0,0]))