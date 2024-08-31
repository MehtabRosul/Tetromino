import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and constants
WIDTH, HEIGHT = 300, 600
CELL_SIZE = 30
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_COLOR = (128, 128, 128)

# Define colors for tetrominoes
TETROMINO_COLORS = [
    (0, 255, 255),  # I shape (Cyan)
    (255, 255, 0),  # O shape (Yellow)
    (128, 0, 128),  # T shape (Purple)
    (0, 255, 0),    # S shape (Green)
    (255, 0, 0),    # Z shape (Red)
    (0, 0, 255),    # J shape (Blue)
    (255, 165, 0)   # L shape (Orange)
]

# Define tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 1, 0], [0, 1, 1]],  # S shape
    [[0, 1, 1], [1, 1, 0]],  # Z shape
    [[1, 0, 0], [1, 1, 1]],  # J shape
    [[0, 0, 1], [1, 1, 1]]  # L shape
]

# Tetromino class
class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(TETROMINO_COLORS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.locked = False

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self, screen):
        for i, row in enumerate(self.shape):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, self.color, pygame.Rect((self.x + j) * CELL_SIZE, (self.y + i) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Game class
class Game:
    def __init__(self):
        self.grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
        self.current_tetromino = Tetromino()
        self.running = True
        self.game_over = False
        self.game_over_time = 0
        self.game_over_duration = 3000  # 3 seconds

    def draw_grid(self, screen):
        for y in range(ROWS):
            for x in range(COLS):
                pygame.draw.rect(screen, GRID_COLOR, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def draw(self, screen):
        screen.fill(BLACK)
        self.draw_grid(screen)
        self.current_tetromino.draw(screen)
        for y in range(ROWS):
            for x in range(COLS):
                if self.grid[y][x] != BLACK:
                    pygame.draw.rect(screen, self.grid[y][x], pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if self.game_over:
            self.draw_game_over(screen)
        pygame.display.flip()

    def draw_game_over(self, screen):
        font = pygame.font.Font(None, 54)
        text = font.render('Game Over', True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    def check_collision(self):
        shape = self.current_tetromino.shape
        for i, row in enumerate(shape):
            for j, val in enumerate(row):
                if val:
                    if (self.current_tetromino.y + i >= ROWS or
                        self.current_tetromino.x + j < 0 or
                        self.current_tetromino.x + j >= COLS or
                        self.grid[self.current_tetromino.y + i][self.current_tetromino.x + j] != BLACK):
                        return True
        return False

    def place_tetromino(self):
        shape = self.current_tetromino.shape
        for i, row in enumerate(shape):
            for j, val in enumerate(row):
                if val:
                    self.grid[self.current_tetromino.y + i][self.current_tetromino.x + j] = self.current_tetromino.color
        self.clear_lines()
        self.current_tetromino = Tetromino()
        if self.check_collision():
            self.game_over = True
            self.game_over_time = pygame.time.get_ticks()  # Record the time when the game is over

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        for _ in range(ROWS - len(new_grid)):
            new_grid.insert(0, [BLACK] * COLS)
        self.grid = new_grid

    def run(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        drop_time = 500
        drop_event = pygame.USEREVENT + 1
        pygame.time.set_timer(drop_event, drop_time)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_LEFT:
                        self.current_tetromino.x -= 1
                        if self.check_collision():
                            self.current_tetromino.x += 1
                    if event.key == pygame.K_RIGHT:
                        self.current_tetromino.x += 1
                        if self.check_collision():
                            self.current_tetromino.x -= 1
                    if event.key == pygame.K_DOWN:
                        self.current_tetromino.y += 1
                        if self.check_collision():
                            self.current_tetromino.y -= 1
                            self.place_tetromino()
                    if event.key == pygame.K_UP:
                        self.current_tetromino.rotate()
                        if self.check_collision():
                            self.current_tetromino.rotate()
                            self.current_tetromino.rotate()
                            self.current_tetromino.rotate()
                if event.type == drop_event and not self.game_over:
                    self.current_tetromino.y += 1
                    if self.check_collision():
                        self.current_tetromino.y -= 1
                        self.place_tetromino()

            self.draw(screen)

            if self.game_over:
                if pygame.time.get_ticks() - self.game_over_time > self.game_over_duration:
                    self.running = False

            clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    Game().run()
