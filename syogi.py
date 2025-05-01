import tkinter as tk

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()

import pygame
pygame.init()
boardSize = 9
board = [[0] * boardSize for _ in range(boardSize)]
promotionLine = 3
screenSize = min(width, height) * 7 // 10
pieceSize = screenSize // boardSize
screen = pygame.display.set_mode((screenSize, screenSize + pieceSize*2))
pieceFont = pygame.font.SysFont("meiryo", screenSize*3//40)
quantityFont = pygame.font.SysFont(False, screenSize*3//40)

canMove = (((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)), 
((0, -1), (100, 100)), 
((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (0, 1)), 
((-1, -1), (0, -1), (1, -1), (-1, 1), (1, -1)), 
((-1, -2), (1, -2)), 
(), 
(), 
((-1, -1), (1, -1), (-1, 1), (1, 1)), 
(), 
((0, -1), (-1, 0), (1, 0), (0, 1)))
name = ("王", "歩", "金", "銀", "桂", "香", "飛", "", "角", "")
name_promotion = ("王", "と", "金", "全", "圭", "杏", "龍", "", "馬", "")
#0王 1歩 2金 3銀 4桂馬 (5香車 6飛車 7成飛車 8角 9成角)

def FindCanMove(x, y, list):
    ans = []
    for pos in list:
        if turn == 0:
            findX, findY = x+pos[0], y+pos[1]
        else:
            findX, findY = x-pos[0], y-pos[1]
        if 0 <= findX < boardSize and 0 <= findY < boardSize:
            if board[findY][findX] == 0:
                ans.append([findX, findY])
            elif board[findY][findX].team == (turn+1)%2:
                ans.append([findX, findY])
    return ans

def FindCanMoveLine(x, y, dx, dy):
    ans = []
    findX, findY = x, y
    while True:
        if turn == 0:
            findX += dx
            findY += dy
        else:
            findX -= dx
            findY -= dy
        ok = False
        if 0 <= findX < boardSize and 0 <= findY < boardSize:
            if board[findY][findX] == 0:
                ans.append([findX, findY])
                ok = True
            elif board[findY][findX].team == (turn+1)%2:
                ans.append([findX, findY])
        if ok == False:
            return ans

class Piece():
    def __init__(self, type, team):
        self.typeA = type
        if 1 <= self.typeA <= 5:
            self.typeB = 2
        elif self.typeA == 0:
            self.typeB = 0
        else:
            self.typeB = self.typeA + 1
        self.type = type
        self.team = team
        self.promotion = False
        self.canMove = []

    def Hold(self, x, y):
        self.canMove = []
        if self.type == 7 or self.type == 9:
            self.canMove += FindCanMove(x, y, canMove[self.type])
        if self.type <= 4:
            self.canMove += FindCanMove(x, y, canMove[self.type])
        else:
            if self.type == 5 or self.type == 6 or self.type == 7:
                self.canMove += FindCanMoveLine(x, y, 0, -1)
            if self.type == 6 or self.type == 7:
                self.canMove += FindCanMoveLine(x, y, -1, 0)
                self.canMove += FindCanMoveLine(x, y, 1, 0)
                self.canMove += FindCanMoveLine(x, y, 0, 1)
            if self.type == 8 or self.type == 9:
                self.canMove += FindCanMoveLine(x, y, -1, -1)
                self.canMove += FindCanMoveLine(x, y, 1, -1)
                self.canMove += FindCanMoveLine(x, y, -1, 1)
                self.canMove += FindCanMoveLine(x, y, 1, 1)

    def Move(self, bx, by, gx, gy):
        if board[gy][gx] != 0:
            holdPiece[turn].append(board[gy][gx].typeA)
        board[gy][gx] = board[by][bx]
        board[by][bx] = 0
        if self.promotion == False:
            if self.team == 0 and gy < promotionLine:
                self.type = self.typeB
                self.promotion = True
            elif self.team == 1 and boardSize - promotionLine <= gy:
                self.type = self.typeB
                self.promotion = True

def Start():
    if boardSize == 9:
        for i in range(4):
            CreatePiece(i, 0, 5-i, 1)
            CreatePiece(i, 8, 5-i, 0)
        CreatePiece(4, 0, 0, 1)
        CreatePiece(4, 8, 0, 0)
        for i in range(8, 4, -1):
            CreatePiece(i, 0, i-3, 1)
            CreatePiece(i, 8, i-3, 0)
        CreatePiece(1, 1, 6, 1)
        CreatePiece(7, 1, 8, 1)
        CreatePiece(1, 7, 8, 0)
        CreatePiece(7, 7, 6, 0)
        for i in range(9):
            CreatePiece(i, 2, 1, 1)
            CreatePiece(i, 6, 1, 0)

def Click(x, y, hold, holdType, turn):
    global holdPiece
    x, y = x//pieceSize, y//pieceSize
    if 1 <= y <= 9:
        y -= 1
        if holdType == 0:
            nowHoldPiece = board[hold[1]][hold[0]]
            for canMoveNow in nowHoldPiece.canMove:
                if [x, y] == canMoveNow:
                    nowHoldPiece.Move(hold[0], hold[1], x, y)
                    turn = (turn+1)%2
                    return None, None, turn
        elif holdType == 1:
            CreatePiece(x, y, hold, turn)
            del(holdPiece[turn])
            turn = (turn+1)%2
            return None, None, turn
        else:
            selectPiece = board[y][x]
            if selectPiece != 0:
                if selectPiece.team == turn:
                    selectPiece.Hold(x, y)
                    (selectPiece.canMove)
                    return (x, y), 0, turn
    else:
        if turn == 0:
            pieceIndex = x
        else:
            pieceIndex = 8-x
        if pieceIndex < len(set(holdPiece[turn])):
            pieceIndex = holdPiece.index(sorted(list(set(holdPiece[0])))[pieceIndex])
            return pieceIndex, 1, turn
    return None, None, turn

def CreatePiece(x, y, type, team):
    board[y][x] = Piece(type, team)

def DrawQuantityText(t, x, y, team):
    text = quantityFont.render(str(t), True, (255, 255, 255))
    if team == 0:
        text_rect = text.get_rect(center=(x*pieceSize + pieceSize//2 + pieceSize//3, y*pieceSize + pieceSize//2 + pieceSize//3))
    else:
        text_rect = text.get_rect(center=(x*pieceSize + pieceSize//2 - pieceSize//3, y*pieceSize + pieceSize//2 - pieceSize//3))
    if team == 1:
        text = pygame.transform.flip(text, True, True)
    screen.blit(text, text_rect)

def DrawText(t, team, x, y, r=0, g=0, b=0):
    text = pieceFont.render(str(t), True, (r, g, b))
    text_rect = text.get_rect(center=(x*pieceSize + pieceSize//2, y*pieceSize + pieceSize//2))
    if team == 1:
        text = pygame.transform.flip(text, True, True)
    screen.blit(text, text_rect)

def DrawHoldPiece(i, piece, team):
    if team == 0:
        x = i
        y = 10
    else:
        x = 8-i
        y = 0
    pygame.draw.circle(screen, (214, 198, 175), (x*pieceSize + pieceSize//2, y*pieceSize + pieceSize//2), pieceSize//2)
    DrawText(name[piece], team, x, y)
    DrawQuantityText(holdPiece[team].count(piece), x, y, team)

def DrawPiece(x, y, piece):
    y += 1
    pygame.draw.circle(screen, (214, 198, 175), (x*pieceSize + pieceSize//2, y*pieceSize + pieceSize//2), pieceSize//2)
    if piece.promotion:
        if piece.typeA == 0 or piece.typeA == 2:
            DrawText(name_promotion[piece.typeA], piece.team, x, y)
        else:
            DrawText(name_promotion[piece.typeA], piece.team, x, y, 255, 0, 0)
    else:
        DrawText(name[piece.typeA], piece.team, x, y)

def DrawCanMove(x, y):
    pygame.draw.rect(screen, (0, 255, 0), (x*pieceSize, y*pieceSize + pieceSize, pieceSize, pieceSize))


def Draw(hold, holdType):
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (230, 180, 34), (0, pieceSize, screenSize, pieceSize*boardSize))
    if hold != None:
        if holdType == 0:
            for canMoveNow in board[hold[1]][hold[0]].canMove:
                DrawCanMove(canMoveNow[0], canMoveNow[1])
    for y in range(boardSize):
        for x in range(boardSize):
            if board[y][x] != 0:
                DrawPiece(x, y, board[y][x])
    for i, piece in enumerate(sorted(list(set(holdPiece[0])))):
        DrawHoldPiece(i, piece, 0)
    for i, piece in enumerate(sorted(list(set(holdPiece[1])))):
        DrawHoldPiece(i, piece, 1)
    pygame.display.flip()

Start()
loop = True
hold = None
holdPiece = [[], []]
turn = 0
holdType = None
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            hold, holdType, turn = Click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], hold, holdType, turn)
    Draw(hold, holdType)
pygame.quit()
