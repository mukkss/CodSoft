import copy
import sys
import pygame
import random
import numpy as np

from constants import *

# --- PYGAME SETUP ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

# --- CLASSES ---

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
        @return 0 if there is no win yet
        @return 1 if player 1 wins
        @return 2 if player 2 wins
        '''
        # Check for vertical, horizontal, and diagonal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    self.draw_line((20, row * SQSIZE + SQSIZE // 2), (WIDTH - 20, row * SQSIZE + SQSIZE // 2), self.squares[row][0])
                return self.squares[row][0]

        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    self.draw_line((col * SQSIZE + SQSIZE // 2, 20), (col * SQSIZE + SQSIZE // 2, HEIGHT - 20), self.squares[0][col])
                return self.squares[0][col]

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                self.draw_line((20, 20), (WIDTH - 20, HEIGHT - 20), self.squares[1][1], CROSS_WIDTH)
            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                self.draw_line((20, HEIGHT - 20), (WIDTH - 20, 20), self.squares[1][1], CROSS_WIDTH)
            return self.squares[1][1]

        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        return [(row, col) for row in range(ROWS) for col in range(COLS) if self.empty_sqr(row, col)]

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

    def draw_line(self, start, end, player, width=CROSS_WIDTH):
        color = CIRC_COLOR if player == 2 else CROSS_COLOR
        pygame.draw.line(screen, color, start, end, width)

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        return random.choice(board.get_empty_sqrs())

    def minimax(self, board, maximizing):
        case = board.final_state()

        if case == 1:
            return 1, None  # eval, move
        if case == 2:
            return -1, None
        if board.isfull():
            return 0, None

        best_move = None
        empty_sqrs = board.get_empty_sqrs()
        if maximizing:
            max_eval = -100
            for row, col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move

        else:
            min_eval = 100
            for row, col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            return self.rnd(main_board)  # Random choice
        else:
            eval, move = self.minimax(main_board, False)
            print(f'AI chose {move} with eval {eval}')
            return move

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   # 1-cross 2-circle
        self.gamemode = 'ai'  # pvp or ai
        self.running = True
        self.show_lines()

    def show_lines(self):
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            self.draw_cross(row, col)
        elif self.player == 2:
            self.draw_circle(row, col)

    def draw_cross(self, row, col):
        start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
        end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
        pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
        start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
        end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
        pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

    def draw_circle(self, row, col):
        center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
        pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    game.change_gamemode()
                if event.key == pygame.K_r:
                    game.reset()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row, col = pos[1] // SQSIZE, pos[0] // SQSIZE
                if game.board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                    if game.isover():
                        game.running = False

        if game.gamemode == 'ai' and game.player == game.ai.player and game.running:
            pygame.display.update()
            row, col = game.ai.eval(game.board)
            game.make_move(row, col)
            if game.isover():
                game.running = False

        pygame.display.update()

main()
