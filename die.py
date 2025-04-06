import pygame # type: ignore
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

bullet_size = 10
bullet_speed = 15
bullet_color = (255, 255, 0)
bullet_list = []

player_size = 50
player_speed = 10

enemy_size = 40
enemy_speed = 4
enemy_spawn_rate = 60
enemy_count = 3

score = 0
font = pygame.font.Font(None, 36)

def start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = font.render("Press SPACE to Start", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - title.get_height() // 2))
    pygame.display.flip()

def game_loop():
    global score, enemy_list, bullet_list, player_pos

    score = 0
    player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
    enemy_list = []
    bullet_list = []

    for _ in range(enemy_count):
        enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
        enemy_list.append(enemy_pos)

    clock = pygame.time.Clock()
    enemy_spawn_timer = 0

    running = True
    while running:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            bullet_pos = [player_pos[0] + player_size // 2 - bullet_size // 2, player_pos[1]]
            bullet_list.append(bullet_pos)

        for bullet in bullet_list[:]:
            for enemy in enemy_list[:]:
                is_golden = enemy[2] if len(enemy) > 2 else False
                if (enemy[0] < bullet[0] < enemy[0] + enemy_size or
                    enemy[0] < bullet[0] + bullet_size < enemy[0] + enemy_size) and \
                   (enemy[1] < bullet[1] < enemy[1] + enemy_size or
                    enemy[1] < bullet[1] + bullet_size < enemy[1] + enemy_size):
                    bullet_list.remove(bullet)
                    enemy_list.remove(enemy)
                    score += 5 if is_golden else 1
                    break

        game_over = False

        screen.fill(BLACK)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                running = False

        # player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed

        # Enemy
        for enemy in enemy_list:
            enemy[1] += enemy_speed * (2 if len(enemy) > 2 and enemy[2] else 1)
            if enemy[1] > HEIGHT:
                enemy[0] = random.randint(0, WIDTH - enemy_size)
                enemy[1] = 0

        for enemy in enemy_list:
            if (enemy[0] < player_pos[0] < enemy[0] + enemy_size or
                enemy[0] < player_pos[0] + player_size < enemy[0] + enemy_size) and \
               (enemy[1] < player_pos[1] < enemy[1] + enemy_size or
                enemy[1] < player_pos[1] + player_size < enemy[1] + enemy_size):
                game_over = True

        for bullet in bullet_list[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullet_list.remove(bullet)
            else:
                pygame.draw.circle(screen, bullet_color, (bullet[0] + bullet_size // 2, bullet[1] + bullet_size // 2), bullet_size // 2)

        pygame.draw.ellipse(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
        for enemy in enemy_list:
            color = (255, 215, 0) if len(enemy) > 2 and enemy[2] else RED
            pygame.draw.rect(screen, color, (enemy[0], enemy[1], enemy_size, enemy_size), border_radius=5)

        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_rate:
            enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
            enemy_list.append(enemy_pos)
            enemy_spawn_timer = 0
            if random.random() < 0.05:  # 5% chance
                golden_enemy_pos = [random.randint(0, WIDTH - enemy_size), 0, True]
                enemy_list.append(golden_enemy_pos)

        pygame.display.flip()
        clock.tick(30)

        if game_over:
            break

    # Game Over screen
    screen.fill(BLACK)
    message = pygame.font.Font(None, 74).render("Game Over", True, WHITE)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
    score_message = pygame.font.Font(None, 48).render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_message, (WIDTH // 2 - score_message.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    pygame.time.delay(2000)

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
                game_loop()
                break

pygame.quit()
sys.exit()