import pygame
boardSize = 9
board = [[0] * boardSize for _ in range(boardSize)]

canMove = (((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)), 
((0, -1)), 
((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (0, 1)), 
((-1, -1), (0, -1), (1, -1), (-1, 1), (1, -1)), 
((-1, -2), (1, -2)))
#0王 1歩 2金 3銀 4桂馬 (5香車 6飛車 7成飛車 8角 9成角)

def FindCanMove(x, y, list):
    ans = []
    for pos in list:
        findX, findY = x+pos[0], y+pos[1]
        if board[findY][findX] == 0 and 0 <= findX < boardSize and 0 <= findY < boardSize:
            ans.append([findX, findY])
    return ans

def FindCanMoveLine(x, y, dx, dy):
    ans = []
    findX, findY = x, y
    while True:
        findX, findY += dx, dy
        if board[findY][findX] == 0 and 0 <= findX < boardSize and 0 <= findY < boardSize:
            ans.append([findX, findY])
        else:
            break
    return ans

class Piece():
    def __init__(self, type, team):
        self.typeA = type
        self.type = type
        self.team = team
        self.canMove = []
    def Hold(self, x, y):
        self.canMove = []
        if self.type == 7 or self.type == 9:
            self.canMove.append(FindCanMove(x, y, canMove[0]))
        if self.type <= 4:
            self.canMove.append(FindCanMove(x, y, canMove[self.type]))
        else:
            if self.type == 5 or self.type == 6 or self.type == 7:
                self.canMove.append(FindCanMoveLine(x, y, 0, -1))
            if self.type == 6 or self.type == 7:
                self.canMove.append(FindCanMoveLine(x, y, -1, 0))
                self.canMove.append(FindCanMoveLine(x, y, 1, 0))
                self.canMove.append(FindCanMoveLine(x, y, 0, -1))
            if self.type == 8 or self.type == 9:
                self.canMove.append(FindCanMoveLine(x, y, -1, -1))
                self.canMove.append(FindCanMoveLine(x, y, 1, -1))
                self.canMove.append(FindCanMoveLine(x, y, -1, 1))
                self.canMove.append(FindCanMoveLine(x, y, 1, 1))

                
    def Move(self, bx, by, gx, gy):
        board[by][bx], board[gy][gx] = board[gy][gx], board[by][bx]
        

def CreatePiece(x, y, type, team):
    board[y][x] = Piece(type, team)