import pygame, random

pygame.init()

# GAME WINDOW
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock object
clock = pygame.time.Clock()
FPS = 10

# GAME VARIABLES
tile_size = 30
# Create the walls of the level
world_data = []
walls = []
# Create wall group 
wall_group = pygame.sprite.Group()
# Define spawn position for the snake
spawn_position = ()
# Track the player's points
points = 0
# Total time until the game ends
total_time = 60

# COLORS
GREY = (60, 60, 60)
BG = (0, 0, 0)
GREEN = (100, 255, 10)
BLUE = (70, 130, 255)
RED = (255, 0, 0) 
WHITE = (255, 255, 255)

# FONT
FONT = pygame.font.SysFont('Futura', 30)

# FUNCTIONS
def draw_grid(tile_size):
    # Fill screen
    SCREEN.fill(BG)

    # Draw vertical lines
    for x in range(tile_size, SCREEN_WIDTH, tile_size):
        pygame.draw.line(SCREEN, GREY, (x, 0), (x, SCREEN_HEIGHT))

    # Draw horizontal lines
    for y in range(tile_size, SCREEN_HEIGHT, tile_size):
        pygame.draw.line(SCREEN, GREY, (0, y), (SCREEN_WIDTH, y))

def new_collectable_position():
    # generate random collectable position
    pos = [random.randint(1, 18), random.randint(1, 18)]

    # While the position generated coincides with snake or walls
    while pos[0] == snake.rect.x or pos[1] == snake.rect.y or pos in walls:
        # Create new position
        pos = [random.randint(1, 18), random.randint(1, 18)]

    return pos

def display_text(txt, color, font, x, y):
    text = font.render(txt, True, color)
    SCREEN.blit(text, (x, y))

def end_game_screen(score):
    # Fill the screen
    SCREEN.fill(GREY)

    # Display the end game text
    display_text(f'Game over! Score: {score}', WHITE, FONT, 195, 295)

# CLASSES

class Snake:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Attributes for moving
        self.moving = False
        self.velocity = 1
        self.dx = self.velocity
        self.dy = 0

    def update(self):
        # Fill the snake with color
        self.image.fill(self.color)

        # Keep position of snake inside of tiles
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size

        # Draw the snake on the screen
        SCREEN.blit(self.image, self.rect)

    def move(self):
        # Check if snake is moving and snake not colliding with walls
        if self.moving and not self.collision_with_walls():
            self.x += self.dx
            self.y += self.dy

    def collision_with_walls(self):
        # Check for collision with walls
        for wall in wall_group:
            if wall.x == self.x + self.dx and wall.y == self.y + self.dy:
                return True
        return False

class Walls(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()

        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * tile_size
        self.rect.y = self.y * tile_size

class Collectable():
    def __init__(self):
        self.pos = new_collectable_position()
        self.x = self.pos[0] * tile_size
        self.y = self.pos[1] * tile_size
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        SCREEN.blit(self.image, self.rect)

# Open the level file
with open('World.txt', 'r') as world:
    for line in world:
        world_data.append(line)

# Create walls
for row, tiles in enumerate(world_data):
    for col, tile in enumerate(tiles):
        if tile == '1':
            wall = Walls(row, col, BLUE)
            walls.append([row, col])
            wall_group.add(wall)
        elif tile == 'P':
            spawn_position = (row, col)

# Create the snake
snake = Snake(spawn_position[0], spawn_position[1], GREEN)

# Create collectable
collectable = Collectable()

# MAIN LOOP
run = True
while run:
    # Set frame rate
    clock.tick(FPS)

    # Draw grid
    draw_grid(tile_size)

    # Draw snake
    snake.update()
    snake.move()

    # Check for collision with collectable
    if collectable.rect.colliderect(snake.rect):
        points += 1
        collectable = Collectable()

    # Draw collectable
    collectable.draw()

    # Draw walls
    wall_group.draw(SCREEN)

    # Get the current time
    current_time = pygame.time.get_ticks() // 1000

    # Display score and time remaining
    display_text(f'Time remaining {total_time - current_time} seconds', WHITE, FONT, 5, 5)
    display_text(f'Score: {points}', WHITE, FONT, 500, 5)

    # Display end game screen
    if total_time - current_time <= 0:
        end_game_screen(points)

    # Event handler
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            run = False

        # Key presses for moving the snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.moving = True
                snake.dx = -snake.velocity
                snake.dy = 0

            elif event.key == pygame.K_RIGHT:
                snake.moving = True
                snake.dx = snake.velocity
                snake.dy = 0

            elif event.key == pygame.K_UP:
                snake.moving = True
                snake.dy = -snake.velocity
                snake.dx = 0

            elif event.key == pygame.K_DOWN:
                snake.moving = True
                snake.dy = snake.velocity
                snake.dx = 0

        # Key releases
        if event.type == pygame.KEYUP:
            snake.moving = False

    pygame.display.update()

pygame.quit()