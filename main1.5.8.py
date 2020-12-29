import pygame
from pygame.locals import *
import copy
import numpy as np
import random as r
import time as t
from sys import exit as systemExit
import math
import tkinter as tk

class Board:

    def __init__(self, size=16):
        #self.board = np.zeros((16, 16), int)
        self.board = np.array([[0]+[-1]*(size-1)]*size, int)
        self.finish = False
        self.winner = None
        self.record = []
        self.size = size

    def put_chess(self, player, row):
        if self.finish == True:
            print('Game finish! player {0} won!'.format(self.winner))
        
        else:
            if player == 1 or player == 2:
                column = list(self.board[row]).index(0)

                self.record.append([player, (row, column)])
                self.board[row][column] = player
                if column < self.size-1:
                    self.board[row][column+1] = 0
            else:
                print('player {0} does not exist'.format(player))
                raise NameError('player \'{0}\' does not exist'.format(player))

            print('Player {0} put a chess in position ({1}, {2})!'.format(player, row, column))
            self.check_win_v2(player, row, column)

    def check_win_v2(self, player, row, column):
        checkList = []

        for each in [-3, -2, -1, 0, 1, 2, 3]:  # horizontal
            try: checkList.append(self.board[row+each][column]) if row+each>=0 else None
            except: None
        checkList.append(-1)

        for each in [-3, -2, -1, 0, 1, 2, 3]:  # positive oblique
            try: checkList.append(self.board[row+each][column+each]) if (row+each>=0 and column+each>=0) else None
            except: None
        checkList.append(-1)

        for each in [-3, -2, -1, 0, 1, 2, 3]:  # negative oblique
            try: checkList.append(self.board[row+each][column-each]) if (row+each>=0 and column-each>=0) else None
            except: None
        checkList.append(-1)

        for each in [-3, -2, -1, 0, 1, 2, 3]:  # vertical
            try: checkList.append(self.board[row][column+each]) if column+each>=0 else None
            except: None

        #print(checkList)
        for i in range(len(checkList)-3):
            if checkList[i:i+4] == [player]*4:
                self.finish = True
                self.winner = player
                print('Game finish! player {0} won!'.format(self.winner))
                break

    def print_board(self):
        for i in range(self.size-1, -1, -1):
            for j in range(self.size):
                if self.board[j][i] == 1:
                    print('●',end='')
                elif self.board[j][i] == 2:
                    print('〇',end='')
                else:
                    print('国',end='')
                #print(int(self.board[i][j]),end=' ')
            print('')

class Chess_AI:

    def __init__(self, player=2):
        self.number = player
        self.competitor_number = 1 if player==2 else 2

    def compute(self, board, player=None, predicting=False):
        BOARD_WIDTH = len(board)
        DATA_WIDTH = BOARD_WIDTH - 1
        player = self.number if player == None else player
        scoreBoard = [0]*BOARD_WIDTH
        competitor = 1 if player == 2 else 2

        for eachRow in range(BOARD_WIDTH):
            if list(board[eachRow]).count(0) == 0:
                scoreBoard[eachRow] = -1000000
            else:
                row = eachRow
                column = list(board[eachRow]).index(0)

                board1 = copy.deepcopy(board)
                board1[row][column] = player
                try: board1[row][column+1] = 0
                except: None

                if not predicting:
                    if max(self.compute(board1, player=competitor, predicting=True)) >= 100000:
                        scoreBoard[eachRow] -= 100000
                        
                checkList = []

                for each in [-3, -2, -1, 0, 1, 2, 3]:  # horizontal
                    try: checkList.append(board1[row+each][column]) if 0<=row+each<=DATA_WIDTH else checkList.append(-1)
                    except: None
                checkList.append(-2)

                for each in [-3, -2, -1, 0, 1, 2, 3]:  # positive oblique
                    try: checkList.append(board1[row+each][column+each]) if (0<=row+each<=DATA_WIDTH and 0<=column+each<=DATA_WIDTH) else checkList.append(-1)
                    except: None
                checkList.append(-2)

                for each in [-3, -2, -1, 0, 1, 2, 3]:  # negative oblique
                    try: checkList.append(board1[row+each][column-each]) if (0<=row+each<=DATA_WIDTH and 0<=column-each<=DATA_WIDTH) else checkList.append(-1)
                    except: None
                checkList.append(-2)

                for each in [-3, -2, -1, 0, 1, 2, 3]:  # vertical
                    try: checkList.append(board1[row][column+each]) if 0<=column+each<=DATA_WIDTH else checkList.append(-1)
                    except: None

                #print(checkList)
                for i in range(len(checkList)-3):
                    if checkList[i:i+4] == [player]*4:
                        scoreBoard[eachRow] += 500000
                    elif sorted(checkList[i:i+4]) in [[player]+[competitor]*3, [competitor]*3+[player]]:
                        scoreBoard[eachRow] += 50000
                    elif sorted(checkList[i:i+4]) in [[0]+[player]*3, [0]+[competitor]*2+[player], [0]+[player]+[competitor]*2]:
                        scoreBoard[eachRow] += 2500
                    elif sorted(checkList[i:i+4]) in [[-1]+[competitor]*2+[player], [-1]+[player]+[competitor]*2]:
                        scoreBoard[eachRow] += 500
                    elif checkList[i:i+4] in [[0, 0, player, player], [0, player, 0, player], [0, player, player, 0], [player, 0, 0, player], [player, 0, player, 0], [player, player, 0, 0]]:
                        scoreBoard[eachRow] += 100
                    elif checkList[i:i+4] in [[player, 0, player, player], [player, player, 0, player]]:
                        scoreBoard[eachRow] += 20

                for i in range(len(checkList)-4):
                    if checkList[i:i+5] == [0]+[player]*3+[0]:
                        scoreBoard[eachRow] += 2500
                    elif checkList[i:i+5] in [[0, 0]+[player]*2+[0], [0]+[player]*2+[0, 0]]:
                        scoreBoard[eachRow] += 100
                    elif checkList[i:i+5] in [[0, 0, player, 0, 0]]:
                        scoreBoard[eachRow] += 20

        #print(scoreBoard) if not predicting else None
        return scoreBoard

    def give_score(self, board, player):
        score = 0
        player = player
        opp_player = self.competitor_number if player==self.number else self.competitor_number

        for j in range(0, len(board)):  # horizontal
            check_array = board[:,j]
            for each_piece in range(len(check_array)-3):
                score += self.get_score(check_array[each_piece:each_piece+4], player, opp_player)

        for i in range(0, len(board)-3):  # positive oblique
            for j in range(0, len(board[0])-3):
                check_array = [board[i+k][j+k] for k in range(4)]
                score += self.get_score(check_array, player, opp_player)

        for i in range(0, len(board)-3):  # negative oblique
            for j in range(3, len(board[0])):
                check_array = [board[i+k][j-k] for k in range(4)]
                score += self.get_score(check_array, player, opp_player)

        for i in range(0, len(board)):  # vertical
            check_array = board[i,:]
            for each_piece in range(len(check_array)-3):
                score += self.get_score(check_array[each_piece:each_piece+4], player, opp_player)

        return score
                
    def get_score(self, array, player, opp_player=None):
        if opp_player == None:
            opp_player = 2 if player == 1 else 1
        array = list(array)
        score = 0
        if array.count(player) == 4:
            score += 100000
        elif array.count(player) == 3 and array.count(0) == 1:
            score += 500
        elif array.count(player) == 2 and array.count(0) == 2:
            score += 200

        if array.count(opp_player) == 3 and array.count(0) == 1:
            score -= 400
        '''if array.count(opp_player) == 2 and array.count(0) == 2:
            score -= 150'''

        return score

    def is_valid_location(self, board, col):
        return list(board[col]).count(0)

    def get_valid_locations(self, board):
        return [i for i in range(len(board)) if self.is_valid_location(board, i)]

    def semi_put_chess(self, board, player, position):
        row, col = position
        board_copy = copy.deepcopy(board)
        board_copy[row][col] = player
        if col<len(board)-1:
            board_copy[row][col+1] = 0
        return board_copy

    def score_position(self, board, piece):
        COLUMN_COUNT = len(board)
        ROW_COUNT = len(board)
        WINDOW_LENGTH = 4
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(ROW_COUNT):
                row_array = [int(i) for i in list(board[r,:])]
                for c in range(COLUMN_COUNT-3):
                        window = row_array[c:c+WINDOW_LENGTH]
                        score += self.get_score(window, piece)

        ## Score Vertical
        for c in range(COLUMN_COUNT):
                col_array = [int(i) for i in list(board[:,c])]
                for r in range(ROW_COUNT-3):
                        window = col_array[r:r+WINDOW_LENGTH]
                        score += self.get_score(window, piece)

        ## Score posiive sloped diagonal
        for r in range(ROW_COUNT-3):
                for c in range(COLUMN_COUNT-3):
                        window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
                        score += self.get_score(window, piece)

        for r in range(ROW_COUNT-3):
                for c in range(COLUMN_COUNT-3):
                        window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                        score += self.get_score(window, piece)

        return score

    def is_winning_move(self, board, piece):
        COLUMN_COUNT = len(board)
        ROW_COUNT = len(board)
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
                for r in range(ROW_COUNT):
                        if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                                return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT-3):
                        if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                                return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
                for r in range(ROW_COUNT-3):
                        if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                                return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
                for r in range(3, ROW_COUNT):
                        if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                                return True  

    def simple(self, scoreBoard):
        BOARD_WIDTH = len(scoreBoard)
        aiScore = scoreBoard
        aiChoose = list(range(BOARD_WIDTH))

        while min(aiScore) != max(aiScore):
            aiChoose.pop(aiScore.index(min(aiScore)))
            aiScore.remove(min(aiScore))

        row = r.choice(aiChoose)

        return row

    def mini_max(self, board, depth, alpha=-math.inf, beta=math.inf, maximizingPlayer=True):
        valid_locations = self.get_valid_locations(board)
        #r.shuffle(valid_locations)

        if self.is_winning_move(board, self.number):  #check if ai win
            return (None, 100000000000000)
        elif self.is_winning_move(board, self.competitor_number):  #check if player win
            return (None, -10000000000000)
        elif len(valid_locations) == 0: # Game is over, no more valid moves
            return (None, 0)
        
        if depth == 0: # Depth is zero
            #print('depth 0')
            return (None, self.score_position(board, self.number))
        
        if maximizingPlayer:
                value = -math.inf
                target_row = r.choice(valid_locations)
                r.shuffle(valid_locations)
                for row in valid_locations:
                        col = list(board[row]).index(0)
                        board_copy = copy.deepcopy(board)
                        board_copy = self.semi_put_chess(board_copy, self.number, (row, col))
                        new_score = self.mini_max(board_copy, depth-1, alpha, beta, False)[1]
                        #print(row, new_score)
                        if new_score > value:
                                value = new_score
                                target_row = row
                        alpha = max(alpha, value)
                        if alpha >= beta:
                                #print('max cut')
                                break
                #print(depth, alpha, beta, maximizingPlayer)
                return target_row, value

        else: # Minimizing player
                value = math.inf
                target_row = r.choice(valid_locations)
                r.shuffle(valid_locations)
                for row in valid_locations:
                        col = list(board[row]).index(0)
                        board_copy = copy.deepcopy(board)
                        board_copy = self.semi_put_chess(board_copy, self.competitor_number, (row, col))
                        new_score = self.mini_max(board_copy, depth-1, alpha, beta, True)[1]
                        #print(row, new_score)
                        if new_score < value:
                                value = new_score
                                target_row = row
                        beta = min(beta, value)
                        if alpha >= beta:
                                #print('min cut')
                                break
                #print(depth, alpha, beta, maximizingPlayer)
                return target_row, value

BOARD_SIZE = 8

def color_rect(screen, color_lib, rect_pos, width=100):

    left_x = rect_pos[0]
    right_x = rect_pos[0]+rect_pos[2]
    top_y = rect_pos[1]
    bottom_y = rect_pos[1]+rect_pos[3]
    
    left_top = [left_x, top_y]
    left_bottom = [left_x, bottom_y]
    right_top = [right_x, top_y]
    right_bottom = [right_x, bottom_y]

    starting_line = ((sum(left_top) // width)) * width
    ending_line = ((sum(right_bottom) // width) + 1) * width
    processing_line = starting_line

    while processing_line != ending_line:
        points = []

        # if left_top is in processing_line
        if ((sum(left_top) // width)) * width == processing_line:
            points.append(left_top)
            
        if left_x < processing_line - top_y < right_x:
            points.append([processing_line-top_y, top_y])
            
        if left_x < processing_line + width - top_y < right_x:
            points.append([processing_line+width-top_y, top_y])
            
        # if right_top is in processing_line
        if ((sum(right_top) // width)) * width == processing_line:
            points.append(right_top)
            
        if top_y < processing_line - right_x < bottom_y:
            points.append([right_x, processing_line-right_x])
            
        if top_y < processing_line + width - right_x < bottom_y:
            points.append([right_x, processing_line+width-right_x])
        
        #if right_bottom is in processing_line
        if ((sum(right_bottom) // width)) * width in (processing_line, processing_line + width):
            points.append(right_bottom)
            
        if left_x < processing_line + width - bottom_y < right_x:
            points.append([processing_line+width-bottom_y, bottom_y])
            
        if left_x < processing_line - bottom_y < right_x:
            points.append([processing_line-bottom_y, bottom_y])
        
        #if left_bottom is in processing_line
        if ((sum(left_bottom) // width)) * width in (processing_line, processing_line + width):
            points.append(left_bottom)
            
        if top_y < processing_line + width - left_x < bottom_y:
            points.append([left_x, processing_line+width-left_x])
            
        if top_y < processing_line - left_x < bottom_y:
            points.append([left_x, processing_line-left_x])

    
        color_pick = (processing_line//width)%len(color_lib)
        if len(points) >= 3:
            pygame.draw.polygon(screen, color_lib[color_pick], points)
        processing_line += width

def draw_background():
    color_rect(screen, color_lib, [0, 0, size[0], size[1]])

def draw_board_background():
    color_rect(screen, light_color_lib, [24, 24, 488, 488])

def draw_board_high_light(size=16):
    if player_round:
        if size == 16:
            mouse_pos = pygame.mouse.get_pos()
            for each in range(16):
                if 30*(each+1) < mouse_pos[0] < 30*(each+1)+26 and 26 < mouse_pos[1] < 510:
                    pygame.draw.rect(screen, dark_gray, (30*(each+1)-2, 28, 30, 480))
        if size == 8:
            mouse_pos = pygame.mouse.get_pos()
            for each in range(8):
                if 60*(each+1)-30 < mouse_pos[0] < 60*(each+1)+26 and 26 < mouse_pos[1] < 510:
                    pygame.draw.rect(screen, dark_gray, (60*(each+1)-30, 28, 60, 480))
    if player_vs_player and (not player_round):
        if size == 16:
            mouse_pos = pygame.mouse.get_pos()
            for each in range(16):
                if 30*(each+1) < mouse_pos[0] < 30*(each+1)+26 and 26 < mouse_pos[1] < 510:
                    pygame.draw.rect(screen, dark_gray, (30*(each+1)-2, 28, 30, 480))

def draw_button(size=16):
    if size == 16:
        for each in range(16):
            pygame.draw.rect(screen, dark_gray, (30*(each+1)-1, 519, 28, 28), 0)
            pygame.draw.rect(screen, light_gray, (30*(each+1), 520, 26, 26), 0)
    if size == 8:
        for each in range(8):
            pygame.draw.rect(screen, dark_gray, (60*(each+1)-31, 519, 56, 56), 0)
            pygame.draw.rect(screen, light_gray, (60*(each+1)-30, 520, 54, 54), 0)

def draw_button_high_light(size=16, player_vs_player=False):
    if player_round:
        if size == 16:
            mouse_pos = pygame.mouse.get_pos()
            for each in range(16):
                if 30*(each+1) < mouse_pos[0] < 30*(each+1)+26 and 520 < mouse_pos[1] < 546:
                    pygame.draw.rect(screen, gray, (30*(each+1), 520, 26, 26), 0)
                    pygame.draw.rect(screen, dark_gray, (30*(each+1)-2, 28, 30, 480))
        if size == 8:
            mouse_pos = pygame.mouse.get_pos()
            for each in range(8):
                if 60*(each+1)-30 < mouse_pos[0] < 60*(each+1)+26 and 520 < mouse_pos[1] < 572:
                    pygame.draw.rect(screen, gray, (60*(each+1)-30, 520, 54, 54), 0)
                    pygame.draw.rect(screen, dark_gray, (60*(each+1)-30, 28, 60, 480))
    if not player_round and player_vs_player:
        if size == 16:
            mouse_pos = pygame.mouse.get_pos()
            for each in range(16):
                if 30*(each+1) < mouse_pos[0] < 30*(each+1)+26 and 520 < mouse_pos[1] < 546:
                    pygame.draw.rect(screen, gray, (30*(each+1), 520, 26, 26), 0)
                    pygame.draw.rect(screen, dark_gray, (30*(each+1)-2, 28, 30, 480))

def draw_board(size=16):
    if size == 16:
        for i in range(16):
            for j in range(16):
                pygame.draw.circle(screen, white, (13+30*(i+1), 13+30*(j+1)), 13, 0)
    if size == 8:
        for i in range(8):
            for j in range(8):
                pygame.draw.circle(screen, white, (60*(i+1), 60*(j+1)), 26, 0)

def draw_chess(size=16):
    if size == 16:
        for i in range(16):
            for j in range(16):
                if b1.board[i][j] == 1:
                    pygame.draw.circle(screen, chess_color[0], (13+30*(i+1), 13+30*(16-j)), 13, 0)
                    pygame.draw.circle(screen, gray, (13+30*(i+1), 13+30*(16-j)), 13, 1)
                if b1.board[i][j] == 2:
                    pygame.draw.circle(screen, chess_color[1], (13+30*(i+1), 13+30*(16-j)), 13, 0)
                    pygame.draw.circle(screen, gray, (13+30*(i+1), 13+30*(16-j)), 13, 1)

    if size == 8:
        for i in range(8):
            for j in range(8):
                if b1.board[i][j] == 1:
                    pygame.draw.circle(screen, chess_color[0], (60*(i+1), 60*(8-j)), 26, 0)
                    pygame.draw.circle(screen, gray, (60*(i+1), 60*(8-j)), 26, 1)
                if b1.board[i][j] == 2:
                    pygame.draw.circle(screen, chess_color[1], (60*(i+1), 60*(8-j)), 26, 0)
                    pygame.draw.circle(screen, gray, (60*(i+1), 60*(8-j)), 26, 1)

def draw_chess_high_light(size=16, player_round=False):
    if player_round:
        if size == 16:
            mouse_pos = pygame.mouse.get_pos()
            for each in range(16):
                try:
                    if 30*(each+1) < mouse_pos[0] < 30*(each+1)+26 and 520 < mouse_pos[1] < 546:
                        pygame.draw.circle(screen,
                                           [chess_color[0][0]+rect_color[0] if 0<chess_color[0][0]+rect_color[0]<255 else 255,
                                            chess_color[0][1]+rect_color[0] if 0<chess_color[0][1]+rect_color[0]<255 else 255,
                                            chess_color[0][2]+rect_color[0] if 0<chess_color[0][2]+rect_color[0]<255 else 255],
                                           (30*(each+1)+13, 30*(16-list(b1.board[each]).index(0))+13), 13)
                except: None
        if size == 8:
            mouse_pos = pygame.mouse.get_pos()
            for each in range(8):
                try:
                    if 60*(each+1)-30 < mouse_pos[0] < 60*(each+1)+26 and 520 < mouse_pos[1] < 572:
                        pygame.draw.circle(screen,
                                           [chess_color[0][0]+rect_color[0] if 0<chess_color[0][0]+rect_color[0]<255 else 255,
                                            chess_color[0][1]+rect_color[0] if 0<chess_color[0][1]+rect_color[0]<255 else 255,
                                            chess_color[0][2]+rect_color[0] if 0<chess_color[0][2]+rect_color[0]<255 else 255],
                                           (60*(each+1), 60*(8-list(b1.board[each]).index(0))), 26)
                except: None
    elif (not player_round) and player_vs_player:
        if size == 16:
            mouse_pos = pygame.mouse.get_pos()
            for each in range(16):
                try:
                    if 30*(each+1) < mouse_pos[0] < 30*(each+1)+26 and 520 < mouse_pos[1] < 546:
                        pygame.draw.circle(screen,
                                           [chess_color[1][0]+rect_color[1] if 0<chess_color[1][0]+rect_color[1]<255 else 255,
                                            chess_color[1][1]+rect_color[1] if 0<chess_color[1][1]+rect_color[1]<255 else 255,
                                            chess_color[1][2]+rect_color[1] if 0<chess_color[1][2]+rect_color[1]<255 else 255],
                                           (30*(each+1)+13, 30*(16-list(b1.board[each]).index(0))+13), 13)
                except: None
                    
def draw_players_rect():
    pygame.draw.rect(screen, [rect_color[0]]*3, (540, 30, 240, 60))
    pygame.draw.rect(screen, [rect_color[1]]*3, (540, 90, 240, 60))
    screen.blit(small_font.render('Player 1', True, black),(540, 30))
    screen.blit(small_font.render('Player 2', True, black),(540, 90))
    pygame.draw.circle(screen, chess_color[0], (720, 60), 20)
    pygame.draw.circle(screen, chess_color[1], (720, 120), 20)

def draw_right_bottom_rect():
    color_rect(screen, light_color_lib, [540, 180, 240, 320])

def draw_right_bottom_button_and_high_light():
    
    color_rect(screen, light_color_lib, [545, 510, 110, 30])
    color_rect(screen, light_color_lib, [665, 510, 110, 30])
    color_rect(screen, light_color_lib, [555, 545, 90, 30])
    color_rect(screen, light_color_lib, [675, 545, 90, 30])
    
    if 545 < mouse_pos[0] < 655 and 510 < mouse_pos[1] < 540:
        pygame.draw.rect(screen, white, [545, 510, 110, 30])
    if 665 < mouse_pos[0] < 775 and 510 < mouse_pos[1] < 540:
        pygame.draw.rect(screen, white, [665, 510, 110, 30])
    if 545 < mouse_pos[0] < 655 and 545 < mouse_pos[1] < 575:
        pygame.draw.rect(screen, white, [555, 545, 90, 30])
    if 665 < mouse_pos[0] < 775 and 545 < mouse_pos[1] < 575:
        pygame.draw.rect(screen, white, [675, 545, 90, 30])

    if b1.finish:
        pygame.draw.rect(screen, dark_gray, [545, 510, 111, 31])

    screen.blit(small_font.render('Retract', True, black), (548, 510))
    screen.blit(small_font.render('Restart', True, black), (668, 510))
    screen.blit(small_font.render('Main', True, black), (568, 545))
    screen.blit(small_font.render('Quit', True, black), (688, 545))

def click_put_chess(size=16, player_round=False):
    if player_round:
        if size == 16:
            for each in range(16):
                if 30*(each+1) < mouse_pos[0] < 30*(each+1)+26 and 520 < mouse_pos[1] < 546:
                    b1.put_chess(1, each)
                    return True
        if size == 8:
            for each in range(8):
                if 60*(each+1)-30 < mouse_pos[0] < 60*(each+1)+26 and 520 < mouse_pos[1] < 572:
                    b1.put_chess(1, each)
                    return True
    if not player_round:
        if size == 16:
            for each in range(16):
                if 30*(each+1) < mouse_pos[0] < 30*(each+1)+26 and 520 < mouse_pos[1] < 546:
                    b1.put_chess(2, each)
                    return True
        if size == 8:
            for each in range(8):
                if 60*(each+1)-30 < mouse_pos[0] < 60*(each+1)+26 and 520 < mouse_pos[1] < 572:
                    b1.put_chess(2, each)
                    return True
    return False

def draw_starting_page_button():
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, white, (170, 300, 250, 50))
    pygame.draw.rect(screen, white, (170, 360, 200, 50))
    pygame.draw.rect(screen, white, (170, 420, 350, 50))
    pygame.draw.rect(screen, white, (170, 480, 80, 50))
    
    color_rect(screen, light_color_lib, (170, 300, 250, 50))
    color_rect(screen, light_color_lib, (170, 360, 200, 50))
    color_rect(screen, light_color_lib, (170, 420, 350, 50))
    color_rect(screen, light_color_lib, (170, 480, 80, 50))

    if 170 < mouse_pos[0] < 420 and 300 < mouse_pos[1] < 300+50:
        pygame.draw.rect(screen, white, (170, 300, 250, 50))
    elif 170 < mouse_pos[0] < 370 and 360 < mouse_pos[1] < 360+50:
        pygame.draw.rect(screen, white, (170, 360, 200, 50))
    elif 170 < mouse_pos[0] < 520 and 420 < mouse_pos[1] < 420+50:
        pygame.draw.rect(screen, white, (170, 420, 350, 50))
    elif 170 < mouse_pos[0] < 250 and 480 < mouse_pos[1] < 480+50:
        pygame.draw.rect(screen, white, (170, 480, 80, 50))
        
    screen.blit(small_font.render('Player vs Player', True, black), (180, 305))
    screen.blit(small_font.render('Player vs AI', True, black), (180, 365))
    screen.blit(small_font.render('Player vs AI(advanced)', True, black), (180, 425))
    screen.blit(small_font.render('Quit', True, black), (180, 488))
    

pygame.init()
size = (810, 580)

#colors
white = (255, 255, 255)
light_gray = (200, 200, 200)
gray = (128, 128, 128)
dark_gray = (96, 96, 96)
purple = (255, 0, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
light_blue = (0, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

color_1 = (254, 67, 101)
color_2 = (252, 157, 154)
color_3 = (249, 205, 173)
color_4 = (200, 200, 169)
color_5 = (131, 175, 155)
color_lib = [color_1,
             color_2,
             color_3,
             color_4,
             color_5]

light_color_1 = (255, 161, 178)
light_color_2 = (254, 206, 205)
light_color_3 = (252, 230, 214)
light_color_4 = (228, 228, 212)
light_color_5 = (193, 215, 205)
light_color_lib = [light_color_1,
                   light_color_2,
                   light_color_3,
                   light_color_4,
                   light_color_5]

rect_color = [128, 128]
rect_color_up = True
screen = pygame.display.set_mode(size, pygame.SRCALPHA)
pygame.display.set_caption('4 - Link')
#rect1 = pygame.image.load('rect1.png').convert_alpha()

clock = pygame.time.Clock()
tiny_font = pygame.font.SysFont('arial', 16)
small_font = pygame.font.SysFont('arial', 32)
big_font = pygame.font.SysFont('arial', 60)

going = True
game_finish = False
b1 = Board(size=BOARD_SIZE)
ai = Chess_AI()
wait_time = 0
player_round = True
change_color = False
chess_color = [red, yellow]
chess_color_selection = [blue, green, purple, light_blue]

starting_page = True
player_vs_player = False

starting_number = 1
starting_number_upper = True
starting_name = 1
starting_name_upper = True
while going:
    
    while starting_page:

        #show game name
        while starting_number:
            starting_number += 1 if starting_number_upper else -1
            screen.fill(black)
            screen.blit(big_font.render('4 - LINK', True, [starting_number]*3),(190, 160))
            if starting_number == 255:
                starting_number_upper = False
            pygame.display.flip()
            clock.tick(120)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    systemExit()
                if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    starting_number = 0
                    break
        #show group name
        while starting_name:
            starting_name += 1 if starting_name_upper else -1
            screen.fill(black)
            screen.blit(small_font.render('presented by Du, Feng, Zhao', True, [starting_name]*3), (280, 230))
            if starting_name == 255:
                starting_name_upper = False
            pygame.display.flip()
            clock.tick(120)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    systemExit()
                if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    starting_name = 0
                    break
        
        draw_background()
        screen.blit(big_font.render('4 - LINK', True, black),(190, 160))
        screen.blit(small_font.render('presented by Du, Feng, Zhao', True, black), (280, 230))

        draw_starting_page_button()
        
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                systemExit()
            if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if 170 < mouse_pos[0] < 420 and 300 < mouse_pos[1] < 350:  # PvP
                    BOARD_SIZE = 16
                    b1 = Board(size=BOARD_SIZE)
                    starting_page = False
                    player_vs_player = True
                if 170 < mouse_pos[0] < 420 and 360 < mouse_pos[1] < 410:  # PvAI
                    BOARD_SIZE = 16
                    b1 = Board(size=BOARD_SIZE)
                    starting_page = False
                if 170 < mouse_pos[0] < 420 and 420 < mouse_pos[1] < 470:  # PvAI(advanced)
                    BOARD_SIZE = 8
                    b1 = Board(size=BOARD_SIZE)
                    starting_page = False
                if 170 < mouse_pos[0] < 250 and 480 < mouse_pos[1] < 530:  # Quit
                    pygame.quit()
                    systemExit()

                    
    if b1.finish and (not game_finish):
        
        game_finish = True
        root = tk.Tk()
        root.title('Game Result')
        root.geometry('300x100')

        if player_vs_player:
            L1 = tk.Label(root, text='Game over, player {0} win!'.format(b1.winner), font=('Arial', 12))
        else:
            L1 = tk.Label(root, text='Game over, you {0}!'.format('win' if b1.winner==1 else 'lost'), font=('Arial', 12))
        L2 = tk.Label(root, text='Click "OK" button to continue', font=('Arial', 12))

        def OK():
            root.destroy()

        B1 = tk.Button(root, text='OK', font=('Arial', 12), command=OK)

        L1.pack()
        L2.pack()
        B1.pack(padx=10, pady=10)

        root.mainloop()
        
    for event in pygame.event.get():
        if event.type == QUIT:
            going = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            going = False

        if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            
            #right bottom button
            if 545 < mouse_pos[0] < 655 and 510 < mouse_pos[1] < 540:  # Retract
                if b1.finish:
                    break
                elif (not player_vs_player) and player_round:
                    for i in range(2):
                        try:
                            b1.board[b1.record[-1][1]] = 0
                            b1.record.pop(-1)
                        except: None
                else:
                    try:
                        b1.board[b1.record[-1][1]] = 0
                        b1.record.pop(-1)
                        player_round = not player_round
                    except: None
                
                break
            if 665 < mouse_pos[0] < 775 and 510 < mouse_pos[1] < 540:  # Restart
                b1 = Board(size=BOARD_SIZE)
                player_round = True
                game_finish = False
                break
            if 555 < mouse_pos[0] < 645 and 545 < mouse_pos[1] < 575:  # Main
                starting_page = True
                player_vs_player = False
                player_round = True
                game_finish = False
                break
            if 675 < mouse_pos[0] < 765 and 510 < mouse_pos[1] < 575:  # Quit
                pygame.quit()
                systemExit()
                break
                
            
            # change chess color
            if ((mouse_pos[0]-720)**2 + (mouse_pos[1]-60)**2)**0.5 < 20:
                pygame.draw.rect(screen, white, (540, 90, 240, 60), border_radius=15)
                for each in range(4):
                    pygame.draw.circle(screen, chess_color_selection[each], ([576, 632, 688, 744][each], 120), 20)
                change_color = True
                change_color_player = 1
            elif ((mouse_pos[0]-720)**2 + (mouse_pos[1]-120)**2)**0.5 < 20:
                pygame.draw.rect(screen, white, (540, 150, 240, 60), border_radius=15)
                for each in range(4):
                    pygame.draw.circle(screen, chess_color_selection[each], ([576, 632, 688, 744][each], 180), 20)
                change_color = True
                change_color_player = 2
                
            while change_color:
                mouse_pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == QUIT: going = False
                    elif event.type == KEYDOWN and event.key == K_ESCAPE: going = False

                    if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        if change_color_player == 1 and 540 < mouse_pos[0] < 780 and 90 < mouse_pos[1] < 150:
                            for each in range(4):
                                if ((mouse_pos[0]-[576,632,688,744][each])**2 + (mouse_pos[1]-120)**2)**0.5 < 20:
                                    temp_color = chess_color[0]
                                    chess_color[0] = chess_color_selection[each]
                                    chess_color_selection.remove(chess_color[0])
                                    chess_color_selection.append(temp_color)
                                    change_color = False
                                    break
                        elif change_color_player == 2 and 540 < mouse_pos[0] < 780 and 150 < mouse_pos[1] < 210:
                            for each in range(4):
                                if ((mouse_pos[0]-[576,632,688,744][each])**2 + (mouse_pos[1]-180)**2)**0.5 < 20:
                                    temp_color = chess_color[1]
                                    chess_color[1] = chess_color_selection[each]
                                    chess_color_selection.remove(chess_color[1])
                                    chess_color_selection.append(temp_color)
                                    change_color = False
                                    break
                        else:
                            change_color = False
                            break

                    pygame.display.flip()
                    clock.tick(60)

                    
                
            if player_round:
                try:
                    if click_put_chess(size=BOARD_SIZE, player_round=player_round):
                        player_round = not player_round
                        wait_time = t.time()
                        rect_color = [128, 128]
                        rect_color_up = True
                        break
                except: None
            if (not player_round) and player_vs_player:
                try:
                    if click_put_chess(size=BOARD_SIZE, player_round=player_round):
                        player_round = not player_round
                        wait_time = t.time()
                        rect_color = [128, 128]
                        rect_color_up = True
                except: None

    if (t.time() - wait_time >= 1) and (not player_round) and player_vs_player==False:
        if BOARD_SIZE == 16:
            aiPutChess = ai.compute(b1.board)
            row_to_put = ai.simple(aiPutChess)
        if BOARD_SIZE == 8:
            row_to_put = ai.mini_max(b1.board, 5)[0]
            
        b1.put_chess(2, row_to_put)
        player_round = not player_round
        rect_color = [128, 128]
        rect_color_up = True
        
    #elif not player_round and player_vs_player:
        


    if player_round:
        rect_color_up = True if rect_color[0]<128 else False if rect_color[0]>200 else rect_color_up
        rect_color[0] += 2 if rect_color_up else -2
    else:
        rect_color_up = True if rect_color[1]<128 else False if rect_color[1]>200 else rect_color_up
        rect_color[1] += 2 if rect_color_up else -2

    mouse_pos = pygame.mouse.get_pos()
        
    #background
    draw_background()

    #board background
    draw_board_background()
        
    #board high light
    draw_board_high_light(size=BOARD_SIZE)
            
    #button
    draw_button(size=BOARD_SIZE)

    #button high light
    draw_button_high_light(size=BOARD_SIZE, player_vs_player=player_vs_player)
                
    #board
    draw_board(size=BOARD_SIZE)

    #chess
    draw_chess(size=BOARD_SIZE)

    #chess high light
    draw_chess_high_light(size=BOARD_SIZE, player_round = player_round)

    #player 1&2 rect
    draw_players_rect()

    #right bottom rect
    draw_right_bottom_rect()

    #right bottom button and high light
    draw_right_bottom_button_and_high_light()
        
    
    #record board
    for each in range(len(b1.record)):
        if (505-len(b1.record)*20+each*20) >= 180 if not b1.finish else (505-len(b1.record)*20+each*20) >= 196:
            screen.blit(tiny_font.render('Player {0} put a chess in ({1}, {2})!'.format(b1.record[each][0], b1.record[each][1][0]+1, b1.record[each][1][1]+1), True, black),
                        (550, (500-len(b1.record)*20+each*20)-20) if b1.finish else (550, (500-len(b1.record)*20+each*20)))
    if b1.finish:
        screen.blit(tiny_font.render('Game over, Player {0} win!'.format(b1.winner), True, black), (550, 480))
    
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
systemExit()
