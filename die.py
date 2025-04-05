import pygame
import sys
import random
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DIE DIE DIE")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()

def start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = font.render("Press SPACE to Start", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - title.get_height() // 2))
    pygame.display.flip()

start_screen()
waiting_for_start = True
while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                waiting_for_start = False
                break

player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 10

enemy_size = 40
enemy_list = []
enemy_speed = 4
enemy_spawn_rate = 60
enemy_spawn_timer = 5
enemy_count = 3
for _ in range(enemy_count):
    enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
    enemy_list.append(enemy_pos)
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed

    # Enemy
    for enemy in enemy_list:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            enemy[0] = random.randint(0, WIDTH - enemy_size)
            enemy[1] = 0

    # kil stuff
    for enemy in enemy_list:
        if (enemy[0] < player_pos[0] < enemy[0] + enemy_size or
            enemy[0] < player_pos[0] + player_size < enemy[0] + enemy_size) and \
           (enemy[1] < player_pos[1] < enemy[1] + enemy_size or
            enemy[1] < player_pos[1] + player_size < enemy[1] + enemy_size):
            running = False

    # player and enemy
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
    for enemy in enemy_list:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_rate:
        enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
        enemy_list.append(enemy_pos)
        enemy_spawn_timer = 0
    pygame.display.flip()

    clock.tick(30)
message = pygame.font.Font(None, 74).render("Game Over", True, WHITE)
screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
pygame.display.flip()
pygame.time.delay(2000)
pygame.quit()
sys.exit()