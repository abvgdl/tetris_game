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
        self.base_font = pygame.font.Font('PressStart2P-vaV7.ttf', 20)
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

        # Иницилизация игрового поля
        self.board = Board(*board_size, self.surface)
        self.board.generate_blank_board()

    def calculate_level_and_fall_frequency(self, score):
        self.level = int(score / 1000) + 1
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
                      (random.randint(0, 220), random.randint(0, 220), random.randint(0, 220)))
        return shape

    @staticmethod
    def add_to_board(board, piece: Shape):
        global blank, TEMPLATES, template_height, template_width

        for x in range(template_width):
            for y in range(template_height):
                if TEMPLATES[piece.get_template()][piece.get_rotation()][y][x] != blank:
                    board.board[x + piece.get_coords()[0]][y + piece.get_coords()[1]] = piece.get_color()

    def check_pos_is_valid(self, board, piece: Shape, adj_x=0, adj_y=0):
        global blank, TEMPLATES, template_height, template_width

        for x in range(template_width):
            for y in range(template_height):
                is_board_on_top = y + piece.get_coords()[1] + adj_y < 0
                if is_board_on_top or TEMPLATES[piece.get_template()][piece.get_rotation()][y][x] == blank:
                    continue
                if not self.is_on_board(x + piece.get_coords()[0] + adj_x, y + piece.get_coords()[1] + adj_y):
                    return False
                if board.board[x + piece.get_coords()[0] + adj_x][y + piece.get_coords()[1] + adj_y] != blank:
                    return False
        return True

    def is_on_board(self, x, y):
        return 0 <= x < self.board.width and y < self.board.height

    def draw_element(self, box_x, box_y, color, x=None, y=None):
        global blank

        if color == blank:
            return
        if x is None and y is None:
            x, y = self.coords_convert(box_x, box_y)
        pygame.draw.rect(self.surface, tuple(map(lambda num: num + 35, color)),
                         (x + 1, y + 1, self.size_field, self.size_field))
        pygame.draw.rect(self.surface, color, (x + 1, y + 1, self.size_field - 4, self.size_field - 4))

    def draw_board(self):
        global blank

        pygame.draw.rect(self.surface, (255, 255, 255),
                         (self.x_lim - 3, self.up_lim - 7, (self.board.width * self.size_field) + 8,
                          (self.board.height * self.size_field) + 8), 5)

        pygame.draw.rect(self.surface, (0, 0, 0), (
            self.x_lim, self.up_lim, self.size_field * self.board.width, self.size_field * self.board.height))
        for x in range(self.board.width):
            for y in range(self.board.height):
                if self.board.board[x][y] != blank:
                    self.draw_element(x, y, (self.board.board[x][y]))
                else:
                    x_, y_ = self.coords_convert(x, y)
                    pygame.draw.rect(self.surface, (150, 150, 150), (x_, y_, self.size_field + 1, self.size_field + 1),
                                     1)

    def draw_status(self):
        score_surf = self.base_font.render(f'Score:{self.score}', True, (255, 255, 255))
        score_rect = score_surf.get_rect()
        score_rect.topleft = (self.width - 175, 75)
        self.surface.blit(score_surf, score_rect)

        level_surf = self.base_font.render(f'Level:{self.level}', True, (255, 255, 255))
        level_rect = level_surf.get_rect()
        level_rect.topleft = (self.width - 175, 125)
        self.surface.blit(level_surf, level_rect)

    def draw_piece(self, piece: Shape, px=None, py=None):
        global TEMPLATES, template_height, template_width

        shape = TEMPLATES[piece.get_template()][piece.get_rotation()]
        if px is None and py is None:
            px, py = self.coords_convert(*piece.get_coords())

        for x in range(template_width):
            for y in range(template_height):
                if shape[y][x] != blank:
                    self.draw_element(None, None, piece.inf['color'], px + (x * self.size_field),
                                      py + (y * self.size_field))

    def draw_next_piece(self, piece):
        next_surf = self.base_font.render('Next:', True, (255, 255, 255))
        next_rect = next_surf.get_rect()
        next_rect.topleft = (self.width - 150, 160)
        self.surface.blit(next_surf, next_rect)
        pygame.draw.rect(self.surface, (0, 0, 220), (width - 175, 185, 130, 130), 1)
        self.draw_piece(piece, px=self.width - 150, py=200)


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

def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def is_line_complete(board, y):
    global blank

    for x in range(board.width):
        if board.board[x][y] == blank:
            return False
    return True


def game_process(screen, clock):
    global width, height

    board_width, board_height = 10, 20

    game = TetrisGame(screen, board_width, board_height)
    falling_piece = game.create_new_figure()
    next_piece = game.create_new_figure()
    while True:
        if falling_piece is None:
            falling_piece = next_piece
            next_piece = game.create_new_figure()
            game.lastFallTime = time.time()

            if not game.check_pos_is_valid(game.board, falling_piece):
                return game.score
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.play(-1, 0.0)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.movingLeft = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.movingRight = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.movingDown = False

            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and game.check_pos_is_valid(game.board,
                                                                                                       falling_piece,
                                                                                                       adj_x=-1):
                    falling_piece.inf['x'] -= 1
                    game.movingLeft = True
                    game.movingRight = False
                    game.lastMoveSidewaysTime = time.time()

                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and game.check_pos_is_valid(
                        game.board,
                        falling_piece,
                        adj_x=1):
                    falling_piece.inf['x'] += 1
                    game.movingRight = True
                    game.movingLeft = False
                    game.lastMoveSidewaysTime = time.time()

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    falling_piece.inf['rotation'] = (falling_piece.get_rotation() + 1) % len(
                        TEMPLATES[falling_piece.get_template()])
                    if not game.check_pos_is_valid(game.board, falling_piece):
                        falling_piece.inf['rotation'] = (falling_piece.get_rotation() - 1) % len(
                            TEMPLATES[falling_piece.get_template()])
                elif event.key == pygame.K_q:
                    falling_piece.inf['rotation'] = (falling_piece.get_rotation() - 1) % len(
                        TEMPLATES[falling_piece.get_template()])
                    if not game.check_pos_is_valid(game.board, falling_piece):
                        falling_piece.inf['rotation'] = (falling_piece.get_rotation() + 1) % len(
                            TEMPLATES[falling_piece.get_template()])

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.movingDown = True
                    if game.check_pos_is_valid(game.board, falling_piece, adj_y=1):
                        falling_piece.inf['y'] += 1
                    game.lastMoveDownTime = time.time()

                elif event.key == pygame.K_SPACE and not(pygame.key.get_mods() & pygame.KMOD_LCTRL):
                    game.movingDown = False
                    game.movingLeft = False
                    game.movingRight = False
                    i = 1
                    for i in range(1, game.board.height):
                        if not game.check_pos_is_valid(game.board, falling_piece, adj_y=i):
                            break
                    falling_piece.inf['y'] += i - 1
        if (game.movingLeft or game.movingRight) and time.time() - game.lastMoveSidewaysTime > 0.15:
            if game.movingLeft and game.check_pos_is_valid(game.board, falling_piece, adj_x=-1):
                falling_piece.inf['x'] -= 1
            elif game.movingRight and game.check_pos_is_valid(game.board, falling_piece, adj_x=1):
                falling_piece.inf['x'] += 1
            game.lastMoveSidewaysTime = time.time()

        if game.movingDown and time.time() - game.lastMoveDownTime > 0.1 and game.check_pos_is_valid(game.board,
                                                                                                     falling_piece,
                                                                                                     adj_y=1):
            falling_piece.inf['y'] += 1
            game.lastMoveDownTime = time.time()
        if time.time() - game.lastFallTime > game.fallFreq:
            if not game.check_pos_is_valid(game.board, falling_piece, adj_y=1):
                game.add_to_board(game.board, falling_piece)
                game.score += 100 * remove_full_lines(game.board)
                game.calculate_level_and_fall_frequency(game.score)
                falling_piece = None
            else:
                falling_piece.inf['y'] += 1
                game.lastFallTime = time.time()
        screen.fill((0, 0, 0))
        game.draw_board()
        game.draw_status()
        game.draw_next_piece(next_piece)
        if falling_piece is not None:
            game.draw_piece(falling_piece)

        pygame.display.update()
        clock.tick(fps)


def main():
    global width, height

    surface = pygame.display.set_mode((width, height + 30))
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('Tetris game')

    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("OIP.jpg")
    sprite.rect = sprite.image.get_rect()
    start_time = pygame.time.get_ticks()

    while True:
        sprite.image = pygame.transform.scale(sprite.image, (clock.tick() // 10,  clock.tick() // 25))
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        if elapsed_time > 5000:
            break
        surface.blit(sprite.image, sprite.rect)
        pygame.display.flip()

    while True:
        score = game_process(surface, clock)
        base_font = pygame.font.Font('PressStart2P-vaV7.ttf', 35)
        base_font_outline = pygame.font.Font('PressStart2P-vaV7.ttf', 35)
        main_text = base_font.render(f'YOUR SCORE {score}', 0, (255, 255, 255))
        main_text_outline = base_font_outline.render(f'YOUR SCORE {score}', 0, (0, 0, 255))

        text_rect = main_text.get_rect()
        text_rect_outline = main_text_outline.get_rect()
        text_rect.center = (int(width // 2), int(height // 2))
        text_rect_outline.center = (int(width // 2) - 3, int(height // 2))

        surface.blit(main_text_outline, text_rect_outline)
        surface.blit(main_text, text_rect)

        sub_font_outline = pygame.font.Font('PressStart2P-vaV7.ttf', 15)
        sub_text_outline = sub_font_outline.render('PRESS CTRL + SPACE TO START NEW GAME', 0, (0, 0, 255))
        sub_text_rect_outline = sub_text_outline.get_rect()
        sub_text_rect_outline.center = (int(width // 2) - 2, int(height // 2) + 40)
        surface.blit(sub_text_outline, sub_text_rect_outline)

        sub_font = pygame.font.Font('PressStart2P-vaV7.ttf', 15)
        sub_text = sub_font.render('PRESS CTRL + SPACE TO START NEW GAME', 0, (255, 255, 255))
        sub_text_rect = sub_text.get_rect()
        sub_text_rect.center = (int(width // 2), int(height // 2) + 40)
        surface.blit(sub_text, sub_text_rect)

        running = True
        while running:
            for event in pygame.event.get([pygame.KEYUP]):
                if event.key == pygame.K_SPACE and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    running = False
                    break
            pygame.display.update()
            clock.tick()


if __name__ == '__main__':
    main()
