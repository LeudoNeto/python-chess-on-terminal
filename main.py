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
    def move_possibilites(self):
        if self.color == 'white':
            return [[self.x,self.y+1],[self.x,self.y+2]]
        elif self.color == 'black':
            return [[self.x,self.y-1],[self.x,self.y-2]]

class Rook(Pieces):
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
    def move_possibilites(self):
        return [[self.x+1,self.y+2],[self.x+2,self.y+1],[self.x+2,self.y-1],[self.x+1,self.y-2],[self.x-1,self.y-2],[self.x-2,self.y-1],[self.x-2,self.y+1],[self.x-1,self.y+2]]

class Bishop(Pieces):
    def move_possibilites(self):
        poss = []
        for x in range(0,8):
            for y in range(0,8):
                if (x - self.x == y - self.y) or (x - self.x == self.y - y):
                    if (x,y) != (self.x,self.y):
                        poss.append([x,y])
        return poss

class King(Pieces):
    def move_possibilites(self):
        poss = []
        for x in range(0,8):
            for y in range(0,8):
                if (-2 < x - self.x < 2) and (-2 < y - self.y < 2):
                    if (x,y) != (self.x,self.y):
                        poss.append([x,y])
        return poss

class Queen(Pieces):
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