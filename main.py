from time import sleep
from random import randint
import json

class RLbot:
    def __init__(self, color):
        self.color = color
        with open('RL_bot/bot_db.json','r') as db:
            self.database = json.load(db)
            self.good_db = self.database['good']
            self.bad_db = self.database['bad']

    def play(self):
        if self.color == 'white':
            self.start_team = Pieces.whites[:]
            self.start_enemy_team = Pieces.blacks[:]
        else:
            self.start_team = Pieces.blacks[:]
            self.start_enemy_team = Pieces.whites[:]
        pieces_initial_letter = ['K','Q','R','H','B','P']
        self.vision = []
        y_range = range(7,-1,-1)
        if self.color == 'black':
            y_range = reversed(y_range)
        for y in y_range:
            self.vision.append([])
            for x in range(0,8):
                if [x,y] in pieces_coords:
                    piece_initial_letter = pieces_initial_letter[[King,Queen,Rook,Horse,Bishop,Pawn].index(type(Pieces.alives[pieces_coords.index([x,y])]))]
                    if self.color == 'white':
                        if Pieces.alives[pieces_coords.index([x,y])].color == 'white':
                            piece_team = 'M'
                        else:
                            piece_team = 'E'
                        self.vision[7-y].append(piece_team+piece_initial_letter)
                    else:
                        if Pieces.alives[pieces_coords.index([x,y])].color == 'white':
                            piece_team = 'E'
                        else:
                            piece_team = 'M'
                        self.vision[y].append(piece_team+piece_initial_letter)
                else:
                    if self.color == 'white':
                        self.vision[7-y].append(0)
                    else:
                        self.vision[y].append(0)
        if str(self.vision) in self.good_db.keys():
            self.bot_move = self.good_db[str(self.vision)]
            return self.bot_move[0]
        elif str(self.vision) in self.bad_db.keys():
            for i in range(50):
                while True:
                    try:
                        if self.color == 'white':
                            choice = randint(0,len(Pieces.whites)-1)
                            self.bot_move = [choice,randint(0,len(Pieces.whites[choice].move_possibilites())-1)]
                        else:
                            choice = randint(0,len(Pieces.blacks)-1)
                            self.bot_move = [choice,randint(0,len(Pieces.blacks[choice].move_possibilites())-1)]
                        if self.bot_move not in self.bad_db.values():
                            return self.bot_move[0]
                    except ValueError:
                        continue
                    else:
                        break
        elif self.color == 'white':
            while True:
                try:
                    choice = randint(0,len(Pieces.whites)-1)
                    self.bot_move = [choice,randint(0,len(Pieces.whites[choice].move_possibilites())-1)]
                except ValueError:
                    continue
                else:
                    break
        else:
            while True:
                try:
                    choice = randint(0,len(Pieces.blacks)-1)
                    self.bot_move = [choice,randint(0,len(Pieces.blacks[choice].move_possibilites())-1)]
                except ValueError:
                    continue
                else:
                    break
        return self.bot_move[0]
            
    def move(self):
        return self.bot_move[1]

    def analyze(self):
        if self.color == 'white':
            self.final_team = Pieces.whites[:]
            self.final_enemy_team = Pieces.blacks[:]
        else:
            self.final_team = Pieces.blacks[:]
            self.final_enemy_team = Pieces.whites[:]
        
        priority = [King,Queen,Rook,Bishop,Horse,Pawn]

        self.eated_piece = None
        self.lost_piece = None

        if len(self.final_team) < len(self.start_team):
            self.lost_piece = list(set(self.start_team).difference(set(self.final_team)))[0]
        if len(self.final_enemy_team) < len(self.start_enemy_team):
            self.eated_piece = list(set(self.start_enemy_team).difference(set(self.final_enemy_team)))[0]
        
        if self.eated_piece and self.lost_piece:
            if priority.index(type(self.eated_piece)) < priority.index(type(self.lost_piece)):
                self.good_db[str(self.vision)] = self.bot_move
            else:
                self.bad_db[str(self.vision)] = self.bot_move
        elif self.eated_piece:
            self.good_db[str(self.vision)] = self.bot_move
        elif self.lost_piece:
            self.bad_db[str(self.vision)] = self.bot_move

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
            if [self.x+1,self.y+1] in blacks_coords:
                poss.append([self.x+1,self.y+1])
            if [self.x-1,self.y+1] in blacks_coords:
                poss.append([self.x-1,self.y+1])
            for c in range(0,2):
                self.y += 1
                if self.y < 8 and [self.x,self.y] not in pieces_coords:
                    poss.append([self.x,self.y])
                if [self.x,self.y] in pieces_coords:
                    break
        elif self.color == 'black':
            if [self.x+1,self.y-1] in whites_coords:
                poss.append([self.x+1,self.y-1])
            if [self.x-1,self.y-1] in whites_coords:
                poss.append([self.x-1,self.y-1])
            for c in range(0,2):
                self.y -= 1
                if self.y > -1 and [self.x,self.y] not in pieces_coords:
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
        while self.y < 7:
            self.y += 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.y = starty
        while self.y > 0:
            self.y -= 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.y = starty
        while self.x < 7:
            self.x += 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x = startx
        while self.x > 0:
            self.x -= 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x = startx
        return poss

class Horse(Pieces):
    emoji = '♞'
    def move_possibilites(self):
        poss = []
        startx,starty = self.x,self.y
        for c in [[self.x+1,self.y+2],[self.x+2,self.y+1],[self.x+2,self.y-1],[self.x+1,self.y-2],[self.x-1,self.y-2],[self.x-2,self.y-1],[self.x-2,self.y+1],[self.x-1,self.y+2]]:
            self.x = c[0]
            self.y = c[1]
            if -1 < self.x < 8 and -1 < self.y < 8:
                if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                    poss.append(c)
        self.x,self.y = startx,starty
        return poss

class Bishop(Pieces):
    emoji = '♝'
    def move_possibilites(self):
        poss = []
        startx,starty = self.x,self.y
        while self.y < 7 and self.x < 7:
            self.x += 1
            self.y += 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        while self.y < 7 and self.x > 0:
            self.x -= 1
            self.y += 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        while self.x < 7 and self.y > 0:
            self.x += 1
            self.y -= 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        while self.x > 0 and self.y > 0:
            self.x -= 1
            self.y -= 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
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
                        if (self.color == 'white' and [x,y] not in whites_coords) or (self.color == 'black' and [x,y] not in blacks_coords):
                            poss.append([x,y])
        return poss

class Queen(Pieces):
    emoji = '♛'
    def move_possibilites(self):
        poss = []
        startx,starty = self.x,self.y
        while self.y < 7:
            self.y += 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.y = starty
        while self.y > 0:
            self.y -= 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.y = starty
        while self.x < 7:
            self.x += 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x = startx
        while self.x > 0:
            self.x -= 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x = startx
        while self.y < 7 and self.x < 7:
            self.x += 1
            self.y += 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        while self.y < 7 and self.x > 0:
            self.x -= 1
            self.y += 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        while self.y > 0 and self.x < 7:
            self.x += 1
            self.y -= 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
                poss.append([self.x,self.y])
            if [self.x,self.y] in pieces_coords:
                break
        self.x,self.y = startx,starty
        while self.y > 0 and self.x > 0:
            self.x -= 1
            self.y -= 1
            if (self.color == 'white' and [self.x,self.y] not in whites_coords) or (self.color == 'black' and [self.x,self.y] not in blacks_coords):
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

def move_event(a,pos,b=0):
    print('-='*15)
    print(f'{a.color.capitalize()} {type(a).__name__} moved to {letters[pos[0]]}{pos[1]+1}'.center(30))
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

letters = ['a','b','c','d','e','f','g','h']
end = False

event("Whites's player type:")
print('[ 1 ] Real Player')
print('[ 2 ] RL Bot')
whites_type = input('Your choice: ')
while whites_type not in ['1','2']:
    whites_type = input('Invalid choice, please try again: ')
event("Blacks's player type:")
print('[ 1 ] Real Player')
print('[ 2 ] RL Bot')
blacks_type = input('Your choice: ')
while blacks_type not in ['1','2']:
    blacks_type = input('Invalid choice, please try again: ')
if whites_type == '2':
    whites = RLbot('white')
if blacks_type == '2':
    blacks = RLbot('black')

while True:
    event("Whites' turn:")
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
    event('Which piece do you want to move?')
    print('OBS: You can write the number on left, or the respective board position')
    i = 0
    for c,piece in enumerate(Pieces.whites):
        print(f'{f"[{c+1}] {type(piece).__name__}":<11} ({letters[piece.x]}{piece.y+1})      ',end='')
        i += 1
        if i == 4:
            print('')
            i = 0
    print('')
    if whites_type == '1':
        choice = input('Your choice: ')
    elif whites_type == '2':
        print('Bot is thinking',end='',flush=True)
        sleep(0.5)
        print('.',end='',flush=True)
        sleep(0.5)
        print('.',end='',flush=True)
        sleep(0.5)
        print('.')
        sleep(0.5)
        choice = whites.play() + 1
        print(choice)
    while True:
        try:
            int(choice)
            if int(choice) in range(1,len(Pieces.whites)+1):
                choice = Pieces.whites[int(choice)-1]
                break
            else:
                choice = input('Invalid choice, please try again: ')
        except ValueError:
            if len(choice) == 2 and choice[0].isalpha() and choice[1].isnumeric():
                if [letters.index(choice[0]),int(choice[1])-1] in whites_coords:
                    choice = Pieces.whites[whites_coords.index([letters.index(choice[0]),int(choice[1])-1])]
                    break
                else:
                    choice = input('Invalid choice, please try again: ')
            else:
                choice = input('Invalid choice, please try again: ')
    event(f'You choose {choice.color.capitalize()} {type(choice).__name__} ({letters[choice.x]}{choice.y+1})')
    board(choice)
    event(f'Where do you want to move {choice.color.capitalize()} {type(choice).__name__}?')
    print('OBS: You can write the number on left, or the respective board position')
    i = 0
    for c,pos in enumerate(choice.move_possibilites()):
        print(f'{f"[{c+1}] {letters[pos[0]]}{pos[1]+1}":<14}',end='')
        i += 1
        if i == 4:
            print('')
            i = 0
    print('[0] BACK')
    if whites_type == '1':
        poschoice = input('Your choice: ')
    elif whites_type == '2':
        print('Bot is thinking',end='',flush=True)
        sleep(0.5)
        print('.',end='',flush=True)
        sleep(0.5)
        print('.',end='',flush=True)
        sleep(0.5)
        print('.')
        sleep(0.5)
        poschoice = whites.move() + 1
        print(poschoice)
    if poschoice == '0':
        continue
    else:
        while True:
            try:
                int(poschoice)
                if int(poschoice) == 0:
                    break
                elif int(poschoice) in range(1,len(choice.move_possibilites())+1):
                    poschoice = choice.move_possibilites()[int(poschoice)-1]
                    break
                else:
                    poschoice = input('Invalid choice, please try again: ')
            except ValueError:
                if len(poschoice) == 2 and poschoice[0].isalpha() and poschoice[1].isnumeric():
                    if [letters.index(poschoice[0]),int(poschoice[1])-1] in choice.move_possibilites():
                        poschoice = [letters.index(poschoice[0]),int(poschoice[1])-1]
                        break
                    else:
                        poschoice = input('Invalid choice, please try again: ')
                else:
                    poschoice = input('Invalid choice, please try again: ')
        if poschoice in blacks_coords:
            move_event(choice,poschoice,Pieces.blacks[blacks_coords.index(poschoice)])
            if type(Pieces.blacks[blacks_coords.index(poschoice)]) == King:
                event('Whites won the game.')
                break
            Pieces.blacks.pop(blacks_coords.index(poschoice))
            Pieces.alives.pop(pieces_coords.index(poschoice))
            [choice.x,choice.y] = poschoice
        elif type(poschoice) == list:
            move_event(choice,poschoice)
            [choice.x,choice.y] = poschoice
        else:
            continue
        if poschoice != 0:
            while True:
                event("Blacks' turn:")
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
                event('Which piece do you want to move?')
                print('OBS: You can write the number on left, or the respective board position')
                i = 0
                for c,piece in enumerate(Pieces.blacks):
                    print(f'{f"[{c+1}] {type(piece).__name__}":<11} ({letters[piece.x]}{piece.y+1})      ',end='')
                    i += 1
                    if i == 4:
                        print('')
                        i = 0
                print('')
                if blacks_type == '1':
                    choice = input('Your choice: ')
                elif blacks_type == '2':
                    print('Bot is thinking',end='',flush=True)
                    sleep(0.5)
                    print('.',end='',flush=True)
                    sleep(0.5)
                    print('.',end='',flush=True)
                    sleep(0.5)
                    print('.')
                    sleep(0.5)
                    choice = blacks.play() + 1
                    print(choice)
                while True:
                    try:
                        int(choice)
                        if int(choice) in range(1,len(Pieces.blacks)+1):
                            choice = Pieces.blacks[int(choice)-1]
                            break
                        else:
                            choice = input('Invalid choice, please try again: ')
                    except ValueError:
                        if len(choice) == 2 and choice[0].isalpha() and choice[1].isnumeric():
                            if [letters.index(choice[0]),int(choice[1])-1] in blacks_coords:
                                choice = Pieces.blacks[blacks_coords.index([letters.index(choice[0]),int(choice[1])-1])]
                                break
                            else:
                                choice = input('Invalid choice, please try again: ')
                        else:
                            choice = input('Invalid choice, please try again: ')
                event(f'You choose {choice.color.capitalize()} {type(choice).__name__} ({letters[choice.x]}{choice.y+1})')
                board(choice)
                event(f'Where do you want to move {choice.color.capitalize()} {type(choice).__name__}?')
                print('OBS: You can write the number on left, or the respective board position')
                i = 0
                for c,pos in enumerate(choice.move_possibilites()):
                    print(f'{f"[{c+1}] {letters[pos[0]]}{pos[1]+1}":<14}',end='')
                    i += 1
                    if i == 4:
                        print('')
                        i = 0
                print('[0] BACK')
                if blacks_type == '1':
                    poschoice = input('Your choice: ')
                elif blacks_type == '2':
                    print('Bot is thinking',end='',flush=True)
                    sleep(0.5)
                    print('.',end='',flush=True)
                    sleep(0.5)
                    print('.',end='',flush=True)
                    sleep(0.5)
                    print('.')
                    sleep(0.5)
                    poschoice = blacks.move() + 1
                    print(poschoice)
                if poschoice == '0':
                    continue
                else:
                    while True:
                        try:
                            int(poschoice)
                            if int(poschoice) == 0:
                                break
                            if int(poschoice) in range(1,len(choice.move_possibilites())+1):
                                poschoice = choice.move_possibilites()[int(poschoice)-1]
                                break
                            else:
                                poschoice = input('Invalid choice, please try again: ')
                        except ValueError:
                            if len(poschoice) == 2 and poschoice[0].isalpha() and poschoice[1].isnumeric():
                                if [letters.index(poschoice[0]),int(poschoice[1])-1] in choice.move_possibilites():
                                    poschoice = [letters.index(poschoice[0]),int(poschoice[1])-1]
                                    break
                                else:
                                    poschoice = input('Invalid choice, please try again: ')
                            else:
                                poschoice = input('Invalid choice, please try again: ')
                    if poschoice in whites_coords:
                        move_event(choice,poschoice,Pieces.whites[whites_coords.index(poschoice)])
                        if type(Pieces.whites[whites_coords.index(poschoice)]) == King:
                            event('Blacks won the game.')
                            end = True
                        Pieces.whites.pop(whites_coords.index(poschoice))
                        Pieces.alives.pop(pieces_coords.index(poschoice))
                        [choice.x,choice.y] = poschoice
                        break
                    elif type(poschoice) == list:
                        move_event(choice,poschoice)
                        [choice.x,choice.y] = poschoice
                        break
                    else:
                        continue
    if end:
        break