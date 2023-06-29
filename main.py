import pygame
import random
import os
#test 100 200 300
#test changes
# 게임 환경 설정
pygame.init()
WIDTH, HEIGHT = 1000, 800
BG_COLOR = (0, 0, 0)
BLOCK_SIZE = 30
PLAY_WIDTH, PLAY_HEIGHT = 10 * BLOCK_SIZE, 20 * BLOCK_SIZE
TOP_LEFT_X, TOP_LEFT_Y = (WIDTH - PLAY_WIDTH) // 2, HEIGHT - PLAY_HEIGHT - 50
#test changes2
#test changes3
#test cannges4
# 테트리스 블록 클래스
class Tetromino:
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[1, 1, 0], [0, 1, 1]],  # Z
        [[0, 1, 1], [1, 1, 0]],  # S
        [[1, 1, 1], [0, 0, 1]],  # J
        [[1, 1, 1], [1, 0, 0]],  # L
        [[1, 1, 1], [0, 1, 0]],  # T
    ]
    COLORS = [
        (0, 255, 255),  # I - Cyan
        (255, 255, 0),  # O - Yellow
        (0, 255, 0),  # Z - Green
        (255, 0, 0),  # S - Red
        (0, 0, 255),  # J - Blue
        (255, 165, 0),  # L - Orange
        (128, 0, 128),  # T - Purple
    ]

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(Tetromino.COLORS)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = list(zip(*reversed(self.shape)))

    def draw(self, surface):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    pygame.draw.rect(surface, self.color,
                                     (TOP_LEFT_X + self.x * BLOCK_SIZE + col * BLOCK_SIZE,
                                      TOP_LEFT_Y + self.y * BLOCK_SIZE + row * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    def is_collision(self, grid):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if (
                    self.shape[row][col]
                    and (
                        self.x + col < 0
                        or self.x + col >= 10
                        or self.y + row >= 20
                        or grid[self.y + row][self.x + col] != (0, 0, 0)
                    )
                ):
                    return True
        return False

# 다음 블록 클래스
class NextBlock:
    def __init__(self):
        self.x = 13
        self.y = 3
        self.shape = random.choice(Tetromino.SHAPES)

    def draw(self, surface):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    pygame.draw.rect(surface, (255, 255, 255),
                                     (TOP_LEFT_X + self.x * BLOCK_SIZE + col * BLOCK_SIZE,
                                      TOP_LEFT_Y + self.y * BLOCK_SIZE + row * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

# 게임 화면 초기화
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HaraTetris")

# 게임 노랑색 테두리 표시 함수
def draw_play_area(surface):
    pygame.draw.rect(surface, (255, 255, 0), (TOP_LEFT_X - 2, TOP_LEFT_Y - 2, PLAY_WIDTH + 4, PLAY_HEIGHT + 4), 4)

# 음악 재생 함수
current_path = os.path.dirname(os.path.realpath(__file__))
resource_path = os.path.join(current_path, 'bgm.mp3')

# pygame 초기화 및 음악 로드

def play_music():
    pygame.mixer.music.load(resource_path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

# 게임 루프
def main():
    clock = pygame.time.Clock()
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    tetromino = Tetromino(5, 0, random.choice(Tetromino.SHAPES))
    next_block = NextBlock()
    game_over = False

    
    play_music()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetromino.move(-1, 0)
                    if tetromino.is_collision(grid):
                        tetromino.move(1, 0)
                elif event.key == pygame.K_RIGHT:
                    tetromino.move(1, 0)
                    if tetromino.is_collision(grid):
                        tetromino.move(-1, 0)
                elif event.key == pygame.K_DOWN:
                    tetromino.move(0, 1)
                    if tetromino.is_collision(grid):
                        tetromino.move(0, -1)
                elif event.key == pygame.K_SPACE:
                    tetromino.rotate()

        tetromino.move(0, 1)
        if tetromino.is_collision(grid):
            tetromino.move(0, -1)
            for row in range(len(tetromino.shape)):
                for col in range(len(tetromino.shape[row])):
                    if tetromino.shape[row][col]:
                        grid[tetromino.y + row][tetromino.x + col] = tetromino.color
            tetromino = Tetromino(5, 0, next_block.shape)
            next_block = NextBlock()
            if tetromino.is_collision(grid):
                game_over = True

        win.fill(BG_COLOR)
        draw_play_area(win)
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                pygame.draw.rect(win, grid[row][col],
                                 (TOP_LEFT_X + col * BLOCK_SIZE, TOP_LEFT_Y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        tetromino.draw(win)
        next_block.draw(win)

        if game_over:
            font = pygame.font.Font(None, 60)
            text = font.render("Game Over", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            win.blit(text, text_rect)

        pygame.display.update()
        clock.tick(5)

if __name__ == "__main__":
    main()
