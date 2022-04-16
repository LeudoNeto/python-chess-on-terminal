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
    emoji = '♟'
    def move_possibilites(self):
        poss = []
        startx,starty = self.x,self.y
        if self.color == 'white':
            for c in range(0,2):
                self.y += 1
                poss.append([self.x,self.y])
                if [self.x,self.y] in pieces_coords:
                    break
        elif self.color == 'black':
            for c in range(0,2):
                self.y -= 1
                poss.append([self.x,self.y])
                if [self.x,self.y] in pieces_coords:
                    break
        self.x,self.y = startx,starty
        return poss

class Rook(Pieces):
    emoji = '♜'
    def move_possibilites(self):
        poss = []
        startx,starty = self.x,self.y
        while self.y < 8:
            self.y += 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.y = starty
        while self.y > -1:
            self.y -= 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.y = starty
        while self.x < 8:
            self.x += 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x = startx
        while self.x > -1:
            self.x -= 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x = startx
        return poss

class Horse(Pieces):
    emoji = '♞'
    def move_possibilites(self):
        return [[self.x+1,self.y+2],[self.x+2,self.y+1],[self.x+2,self.y-1],[self.x+1,self.y-2],[self.x-1,self.y-2],[self.x-2,self.y-1],[self.x-2,self.y+1],[self.x-1,self.y+2]]

class Bishop(Pieces):
    emoji = '♝'
    def move_possibilites(self):
        poss = []
        startx,starty = self.x,self.y
        for c in range(0,8):
            self.x += 1
            self.y += 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        for c in range(0,8):
            self.x -= 1
            self.y += 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        for c in range(0,8):
            self.x += 1
            self.y -= 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        for c in range(0,8):
            self.x -= 1
            self.y -= 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        return poss

class King(Pieces):
    emoji = '♚'
    def move_possibilites(self):
        poss = []
        for x in range(0,8):
            for y in range(0,8):
                if (-2 < x - self.x < 2) and (-2 < y - self.y < 2):
                    if (x,y) != (self.x,self.y):
                        poss.append([x,y])
        return poss

class Queen(Pieces):
    emoji = '♛'
    def move_possibilites(self):
        poss = []
        startx,starty = self.x,self.y
        while self.y < 8:
            self.y += 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.y = starty
        while self.y > -1:
            self.y -= 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.y = starty
        while self.x < 8:
            self.x += 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x = startx
        while self.x > -1:
            self.x -= 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x = startx
        for c in range(0,8):
            self.x += 1
            self.y += 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        for c in range(0,8):
            self.x -= 1
            self.y += 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        for c in range(0,8):
            self.x += 1
            self.y -= 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        for c in range(0,8):
            self.x -= 1
            self.y -= 1
            poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        return poss

def board(piece=0):
    print('-'*35)
    for y in range(7,-1,-1):
        print(f'{y+1} ',end = ' ')
        for x in range(0,8):
            if (x+y) % 2 == 0:
                if piece != 0 and [x,y] in whites_coords and piece.color == 'black' and [x,y] in piece.move_possibilites():
                    print(f'\033[37;41m{Pieces.whites[whites_coords.index([x,y])].emoji:^3} \033[m',end = '')
                elif piece != 0 and ([x,y] in blacks_coords and piece.color == 'white') and [x,y] in piece.move_possibilites():
                    print(f'\033[30;41m{Pieces.blacks[blacks_coords.index([x,y])].emoji:^3} \033[m',end = '')
                elif [x,y] in whites_coords:
                    print(f'\033[37;40m{Pieces.whites[whites_coords.index([x,y])].emoji:^3} \033[m',end = '')
                elif [x,y] in blacks_coords:
                    print(f'\033[30;40m{Pieces.blacks[blacks_coords.index([x,y])].emoji:^3} \033[m',end = '')
                elif piece != 0 and [x,y] in piece.move_possibilites():
                    print(f'\033[30;44m    \033[m',end='')
                elif [x,y] not in pieces_coords:
                    print(f'\033[40m    \033[m',end='')
            else:
                if piece != 0 and [x,y] in whites_coords and piece.color == 'black' and [x,y] in piece.move_possibilites():
                    print(f'\033[37;41m{Pieces.whites[whites_coords.index([x,y])].emoji:^3} \033[m',end = '')
                elif piece != 0 and ([x,y] in blacks_coords and piece.color == 'white') and [x,y] in piece.move_possibilites():
                    print(f'\033[30;41m{Pieces.blacks[blacks_coords.index([x,y])].emoji:^3} \033[m',end = '')
                elif [x,y] in whites_coords:
                    print(f'\033[37;47m{Pieces.whites[whites_coords.index([x,y])].emoji:^3} \033[m',end = '')
                elif [x,y] in blacks_coords:
                    print(f'\033[30;47m{Pieces.blacks[blacks_coords.index([x,y])].emoji:^3} \033[m',end = '')
                elif piece != 0 and [x,y] in piece.move_possibilites():
                    print(f'\033[37;46m    \033[m',end='')
                elif [x,y] not in pieces_coords:
                    print(f'\033[47m    \033[m',end='')
        print('')
    print('    a   b   c   d   e   f   g   h')
    print('-'*35)

def event(txt):
    print('-='*(int(len(txt)/2)+2))
    print(txt.center(len(txt)+4))
    print('-='*(int(len(txt)/2)+2))

def move_event(a,b=0):
    print('-='*15)
    print(f'{a.color.capitalize()} {type(a).__name__} moved to b1'.center(30))
    if b != 0:
        print(f'{a.color.capitalize()} {type(a).__name__} ate {b.color.capitalize()} {type(b).__name__}'.center(30))
    print('-='*15)

wp1 = Pawn(0,1,'white')
wp2 = Pawn(1,1,'white')
wp3 = Pawn(2,1,'white')
wp4 = Pawn(3,1,'white')
wp5 = Pawn(4,1,'white')
wp6 = Pawn(5,1,'white')
wp7 = Pawn(6,1,'white')
wp8 = Pawn(7,1,'white')
bp1 = Pawn(0,6,'black')
bp2 = Pawn(1,6,'black')
bp3 = Pawn(2,6,'black')
bp4 = Pawn(3,6,'black')
bp5 = Pawn(4,6,'black')
bp6 = Pawn(5,6,'black')
bp7 = Pawn(6,6,'black')
bp8 = Pawn(7,6,'black')
wr1 = Rook(0,0,'white')
wr2 = Rook(7,0,'white')
br1 = Rook(0,7,'black')
br2 = Rook(7,7,'black')
wh1 = Horse(1,0,'white')
wh2 = Horse(6,0,'white')
bh1 = Horse(1,7,'black')
bh2 = Horse(6,7,'black')
wb1 = Bishop(2,0,'white')
wb2 = Bishop(5,0,'white')
bb1 = Bishop(2,7,'black')
bb2 = Bishop(5,7,'black')
wq = Queen(3,0,'white')
bq = Queen(4,7,'black')
wk = King(4,0,'white')
bk = King(3,7,'black')

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