import pygame
import random
import sys
import os
import time

fps = 25
width, height = 640, 480

TEMPLATE_O = [['.....',
               '.....',
               '.OO..',
               '.OO..',
               '.....']]

TEMPLATE_I = [['..O..',
               '..O..',
               '..O..',
               '..O..',
               '.....'],
              ['.....',
               '.....',
               'OOOO.',
               '.....',
               '.....']]

TEMPLATE_S = [['.....',
               '.....',
               '..OO.',
               '.OO..',
               '.....'],
              ['.....',
               '..O..',
               '..OO.',
               '...O.',
               '.....']]

TEMPLATE_Z = [['.....',
               '.....',
               '.OO..',
               '..OO.',
               '.....'],
              ['.....',
               '..O..',
               '.OO..',
               '.O...',
               '.....']]

TEMPLATE_L = [['.....',
               '...O.',
               '.OOO.',
               '.....',
               '.....'],
              ['.....',
               '..O..',
               '..O..',
               '..OO.',
               '.....'],
              ['.....',
               '.....',
               '.OOO.',
               '.O...',
               '.....'],
              ['.....',
               '.OO..',
               '..O..',
               '..O..',
               '.....']]

TEMPLATE_J = [['.....',
               '.O...',
               '.OOO.',
               '.....',
               '.....'],
              ['.....',
               '..OO.',
               '..O..',
               '..O..',
               '.....'],
              ['.....',
               '.....',
               '.OOO.',
               '...O.',
               '.....'],
              ['.....',
               '..O..',
               '..O..',
               '.OO..',
               '.....']]

TEMPLATE_T = [['.....',
               '..O..',
               '.OOO.',
               '.....',
               '.....'],
              ['.....',
               '..O..',
               '..OO.',
               '..O..',
               '.....'],
              ['.....',
               '.....',
               '.OOO.',
               '..O..',
               '.....'],
              ['.....',
               '..O..',
               '.OO..',
               '..O..',
               '.....']]

TEMPLATES = {
    'O': TEMPLATE_O,
    'I': TEMPLATE_I,
    'S': TEMPLATE_S,
    'Z': TEMPLATE_Z,
    'L': TEMPLATE_L,
    'J': TEMPLATE_J,
    'T': TEMPLATE_T}


def main():
    global width, height

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    base_font = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Tetris game')
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


class TetrisGame:
    def __init__(self, screen, *board_size):
        global width, height

        # Иницилизация игровых переменных
        self.level = None
        self.fallFreq = None
        self.width = width
        self.height = height
        self.score = 0
        self.calculate_level_and_fall_frequency(self.score)

        # Иницилизация счетчиков времени
        self.lastMoveDownTime = time.time()
        self.lastMoveSidewaysTime = time.time()
        self.lastFallTime = time.time()

        self.surface = screen

        pygame.mixer.music.load('tetris.mp4')

        self.intro_playing()
        self.menu_starting()

        # Иницилизация игрового поля
        self.board = Board(*board_size, self.surface)
        self.board.generate_blank_board()

    def intro_playing(self):
        pass

    def menu_starting(self):
        pass

    def calculate_level_and_fall_frequency(self, score):
        self.level = int(score / 10) + 1
        self.fallFreq = 0.27 - (self.level * 0.02)

    def create_new_figure(self):
        template = random.choice(list(TEMPLATES.keys()))
        shape = {'shape': template,
                 'rotation': random.randint(0, len(TEMPLATES[template]) - 1),
                 'x': int(self.board.width / 2) - int(self.width / 2),
                 'y': -2,
                 'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))}
        return shape


class Board:
    def __init__(self, width, height, screen):
        self.board = None
        self.width = width
        self.height = height
        self.surface = screen

    def generate_blank_board(self):
        self.board = []
        for i in range(self.width):
            self.board.append(['.'] * self.height)


if __name__ == '__main__':
    main()
