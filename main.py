import pygame
import random
import sys
import os
import time

fps = 25
width, height = 640, 480

blank = '.'
template_width, template_height = 5, 5
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


class Shape:
    def __init__(self, templates, rotation, x, y, color):
        self.inf = {'shape': templates,
                    'rotation': rotation,
                    'x': x,
                    'y': y,
                    'color': color}

    def get_template(self):
        return self.inf['shape']

    def get_rotation(self):
        return self.inf['rotation']

    def get_coords(self):
        return (self.inf['x'], self.inf['y'])

    def get_color(self):
        return self.inf['color']


class TetrisGame:
    def __init__(self, screen, *board_size):
        self.base_font = pygame.font.Font('freesansbold.ttf', 18)
        global width, height

        # Иницилизация игровых переменных
        self.level = None
        self.fallFreq = None
        self.width = width
        self.height = height
        self.size_field = 20
        self.x_lim = int((self.width - board_size[0] * self.size_field) / 2)
        self.up_lim = self.height - (board_size[1] * self.size_field) - 5
        self.score = 0
        self.calculate_level_and_fall_frequency(self.score)

        # Иницилизация счетчиков времени
        self.lastMoveDownTime = time.time()
        self.lastMoveSidewaysTime = time.time()
        self.lastFallTime = time.time()

        # Направление движения фигур:
        self.movingDown = False
        self.movingRight = False
        self.movingLeft = False
        self.movingUP = False

        # Иницилизация цветов

        self.surface = screen

        # pygame.mixer.music.load('tetris.mp4')

        self.intro_playing()
        self.menu_starting()

        # Иницилизация игрового поля
        self.board = Board(*board_size, self.surface)
        self.board.generate_blank_board()

    def intro_playing(self):
        pass

    def menu_starting(self):
        pass

    def pause_game(self):
        DISPLAYSURF.fill(BGCOLOR)
        self.show_text('Paused')
        self.lastFallTime = time.time()
        self.lastMoveDownTime = time.time()
        self.lastMoveSidewaysTime = time.time()

    def calculate_level_and_fall_frequency(self, score):
        self.level = int(score / 10) + 1
        self.fallFreq = 0.27 - (self.level * 0.02)

    def coords_convert(self, x, y):
        return (self.x_lim + (x * self.size_field)), (self.up_lim + (y * self.size_field))

    def create_new_figure(self):
        global template_width

        template = random.choice(list(TEMPLATES.keys()))
        shape = Shape(template,
                      random.randint(0, len(TEMPLATES[template]) - 1),
                      int(self.board.width / 2) - int(template_width / 2),
                      -2,
                      (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        return shape

    def add_to_board(self, board, piece: Shape):
        global blank, TEMPLATES, template_height, template_width

        for x in range(template_width):
            for y in range(template_height):
                if TEMPLATES[piece.get_template()][piece.get_rotation()][y][x] != blank:
                    board.board[x + piece.get_coords()[0]][y + piece.get_coords()[1]] = piece.get_color()

    def check_pos_is_valid(self, board, piece: Shape, adjX=0, adjY=0):
        global blank, TEMPLATES, template_height, template_width

        for x in range(template_width):
            for y in range(template_height):
                is_board_on_top = y + piece.get_coords()[1] + adjY < 0
                if is_board_on_top or TEMPLATES[piece.get_template()][piece.get_rotation()][y][x] == blank:
                    continue
                if not self.is_on_board(x + piece.get_coords()[0] + adjX, y + piece.get_coords()[1] + adjY):
                    return False
                if board.board[x + piece.get_coords()[0] + adjX][y + piece.get_coords()[1] + adjY] != blank:
                    return False
        return True

    def is_on_board(self, x, y):
        # print(x, self.board.width, y, self.board.height)
        # print(len(self.board.board), len(self.board.board[0]))
        # print(x >= 0 and x < self.board.width and y < self.board.height)
        return 0 <= x < self.board.width and y < self.board.height

    def drawBox(self, box_x, box_y, color, x=None, y=None):
        global blank

        if color == blank:
            return
        if x is None and y is None:
            x, y = self.coords_convert(box_x, box_y)
        pygame.draw.rect(self.surface, color, (x + 1, y + 1, self.size_field - 4, self.size_field - 4))

    def drawBoard(self):
        pygame.draw.rect(self.surface, (255, 255, 255),
                         (self.x_lim - 3, self.up_lim - 7, (self.board.width * self.size_field) + 8,
                          (self.board.height * self.size_field) + 8), 5)

        pygame.draw.rect(self.surface, (0, 0, 0), (
            self.x_lim, self.up_lim, self.size_field * self.board.width, self.size_field * self.board.height))
        for x in range(self.board.width):
            for y in range(self.board.height):
                self.drawBox(x, y, self.board.board[x][y])

    def drawStatus(self):
        score_surf = self.base_font.render('Score: %s' % self.score, True, (255, 255, 255))
        score_rect = score_surf.get_rect()
        score_rect.topleft = (self.width - 150, 20)
        self.surface.blit(score_surf, score_rect)

        level_surf = self.base_font.render('Level: %s' % self.level, True, (0, 0, 0))
        level_rect = level_surf.get_rect()
        level_rect.topleft = (self.width - 150, 50)
        self.surface.blit(level_surf, level_rect)

    def drawPiece(self, piece: Shape, px=None, py=None):
        global TEMPLATES, template_height, template_width

        shape = TEMPLATES[piece.get_template()][piece.get_rotation()]
        if px is None and py is None:
            px, py = self.coords_convert(*piece.get_coords())

        # draw each of the boxes that make up the piece
        for x in range(template_width):
            for y in range(template_height):
                if shape[y][x] != blank:
                    self.drawBox(None, None, piece.inf['color'], px + (x * self.size_field), py + (y * self.size_field))

    def drawNextPiece(self, piece):
        nextSurf = self.base_font.render('Next:', True, (255, 255, 255))
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (self.width - 120, 80)
        self.surface.blit(nextSurf, nextRect)
        self.drawPiece(piece, px=self.width - 120, py=100)


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

    def get_board(self):
        return self.board


def remove_full_lines(board):
    global blank

    count_removes_lines = 0
    y = board.height - 1
    while y >= 0:
        if is_line_complete(board, y):
            for pullDownY in range(y, 0, -1):
                for x in range(board.width):
                    board.board[x][pullDownY] = board.board[x][pullDownY - 1]
            for x in range(board.width):
                board.board[x][0] = blank
            count_removes_lines += 1
        else:
            y -= 1
    return count_removes_lines


def is_line_complete(board, y):
    global blank

    for x in range(board.width):
        if board.board[x][y] == blank:
            return False
    return True


def main():
    global width, height

    board_width, board_height = 10, 20
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Tetris game')
    running = True

    game = TetrisGame(screen, board_width, board_height)
    fallingPiece = game.create_new_figure()
    nextPiece = game.create_new_figure()

    while running:
        if fallingPiece is None:
            fallingPiece = nextPiece
            nextPiece = game.create_new_figure()
            game.lastFallTime = time.time()

            if not game.check_pos_is_valid(game.board, fallingPiece):
                return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.play(-1, 0.0)
                    game.pause_game()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.movingLeft = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.movingRight = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.movingDown = False

            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and game.check_pos_is_valid(game.board,
                                                                                                       fallingPiece,
                                                                                                       adjX=-1):
                    fallingPiece.inf['x'] -= 1
                    game.movingLeft = True
                    game.movingRight = False
                    game.lastMoveSidewaysTime = time.time()

                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and game.check_pos_is_valid(game.board,
                                                                                                          fallingPiece,
                                                                                                          adjX=1):
                    fallingPiece.inf['x'] += 1
                    game.movingRight = True
                    game.movingLeft = False
                    game.lastMoveSidewaysTime = time.time()

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    fallingPiece.inf['rotation'] = (fallingPiece.get_rotation() + 1) % len(
                        TEMPLATES[fallingPiece.get_template()])
                    if not game.check_pos_is_valid(game.board, fallingPiece):
                        fallingPiece.inf['rotation'] = (fallingPiece.get_rotation() - 1) % len(
                            TEMPLATES[fallingPiece.get_template()])
                elif event.key == pygame.K_q:
                    fallingPiece.inf['rotation'] = (fallingPiece.get_rotation() - 1) % len(
                        TEMPLATES[fallingPiece.get_template()])
                    if not game.check_pos_is_valid(game.board, fallingPiece):
                        fallingPiece.inf['rotation'] = (fallingPiece.get_rotation() + 1) % len(
                            TEMPLATES[fallingPiece.get_template()])

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.movingDown = True
                    if game.check_pos_is_valid(game.board, fallingPiece, adjY=1):
                        fallingPiece.inf['y'] += 1
                    game.lastMoveDownTime = time.time()

                elif event.key == pygame.K_SPACE:
                    game.movingDown = False
                    game.movingLeft = False
                    game.movingRight = False
                    i = 1
                    for i in range(1, game.board.height):
                        if not game.check_pos_is_valid(game.board, fallingPiece, adjY=i):
                            break
                    fallingPiece.inf['y'] += i - 1
        if (game.movingLeft or game.movingRight) and time.time() - game.lastMoveSidewaysTime > 0.15:
            if game.movingLeft and game.check_pos_is_valid(game.board, fallingPiece, adjX=-1):
                fallingPiece.inf['x'] -= 1
            elif game.movingRight and game.check_pos_is_valid(game.board, fallingPiece, adjX=1):
                fallingPiece.inf['x'] += 1
            game.lastMoveSidewaysTime = time.time()

        if game.movingDown and time.time() - game.lastMoveDownTime > 0.1 and game.check_pos_is_valid(game.board,
                                                                                                     fallingPiece,
                                                                                                     adjY=1):
            fallingPiece.inf['y'] += 1
            game.lastMoveDownTime = time.time()
        if time.time() - game.lastFallTime > game.fallFreq:
            if not game.check_pos_is_valid(game.board, fallingPiece, adjY=1):
                game.add_to_board(game.board, fallingPiece)
                game.score += remove_full_lines(game.board)
                game.calculate_level_and_fall_frequency(game.score)
                fallingPiece = None
            else:
                fallingPiece.inf['y'] += 1
                game.lastFallTime = time.time()
        print(fps, game.lastFallTime, game.lastMoveDownTime, game.lastMoveSidewaysTime, game.fallFreq)
        screen.fill((0, 0, 0))
        game.drawBoard()
        game.drawStatus()
        game.drawNextPiece(nextPiece)
        if fallingPiece is not None:
            print(121212121)
            game.drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(fps)


if __name__ == '__main__':
    main()
