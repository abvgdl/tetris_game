import pygame
import random
import sys
import os

fps = 25
width, height = 640, 480


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
        self.surface = screen

        pygame.mixer.music.load('tetris.mp4')

        lastMoveDownTime = time.time()
        lastMoveSidewaysTime = time.time()
        lastFallTime = time.time()

        self.intro_playing()
        self.menu_starting()
        self.board = Board(*board_size, self.surface)
        self.board.generate_blank_board()

    def intro_playing(self):
        pass

    def menu_starting(self):
        pass


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
