import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player settings
PLAYER_SIZE = 50
player_surface = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)  # Create a surface with alpha channel
player_rect = player_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - PLAYER_SIZE // 2))
player_speed = 5

# Draw a triangle on the player surface
pygame.draw.polygon(player_surface, BLACK, [(0, PLAYER_SIZE), (PLAYER_SIZE // 2, 0), (PLAYER_SIZE, PLAYER_SIZE)])

# Bullet settings
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
bullet_image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
bullet_image.fill(RED)
bullet_speed = 7
bullets = []

# Alien settings
ALIEN_WIDTH = 50
ALIEN_HEIGHT = 50
alien_image = pygame.image.load("alien.jpg").convert_alpha()  # Load custom alien image with transparency
alien_image = pygame.transform.scale(alien_image, (ALIEN_WIDTH, ALIEN_HEIGHT))  # Scale the image to match the size
alien_speed = 2
aliens = []

# Scoring
score = 0
font = pygame.font.SysFont(None, 36)

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    window.blit(text_surface, text_rect)

# Function to spawn alien
def spawn_alien():
    alien_x = random.randint(0, WINDOW_WIDTH - ALIEN_WIDTH)
    alien_y = random.randint(-500, -ALIEN_HEIGHT)
    alien_rect = alien_image.get_rect(topleft=(alien_x, alien_y))
    aliens.append(alien_rect)

def move_aliens():
    for alien_rect in aliens:
        alien_rect.y += alien_speed
        if alien_rect.top > WINDOW_HEIGHT:
            aliens.remove(alien_rect)

def shoot_bullet():
    bullet_rect = bullet_image.get_rect(midtop=(player_rect.centerx, player_rect.top))
    bullets.append(bullet_rect)

def draw_window():
    window.fill(WHITE)
    window.blit(player_surface, player_rect)
    for bullet_rect in bullets:
        window.blit(bullet_image, bullet_rect)
    for alien_rect in aliens:
        window.blit(alien_image, alien_rect)
    draw_text(f"Score: {score}", BLACK, 70, 30)

def check_collisions():
    global score
    for bullet_rect in bullets:
        for alien_rect in aliens:
            if bullet_rect.colliderect(alien_rect):
                bullets.remove(bullet_rect)
                aliens.remove(alien_rect)
                score += 10

    for alien_rect in aliens:
        if alien_rect.colliderect(player_rect):
            return True
    return False

# Game state
game_over = False

# Game loop
clock = pygame.time.Clock()
SPAWN_ALIEN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ALIEN_EVENT, 1000)
while True:
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_bullet()
            elif event.type == SPAWN_ALIEN_EVENT:
                spawn_alien()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed

        move_aliens()

        for bullet_rect in bullets:
            bullet_rect.y -= bullet_speed
            if bullet_rect.bottom < 0:
                bullets.remove(bullet_rect)

        draw_window()
        if check_collisions():
            game_over = True
            draw_text("Game Over. Press any key to restart.", RED, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        pygame.display.update()
        clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_over:
                # Reset game variables
                player_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - PLAYER_SIZE // 2)
                bullets.clear()
                aliens.clear()
                score = 0
                game_over = False
