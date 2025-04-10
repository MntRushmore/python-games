import pygame
import random
import math
import colorsys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balls")

clock = pygame.time.Clock()

# Circle
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 380

# Physics
gravity = 0.3
bounciness = 1.05
spawn_timer = 0

bg_hue = 0

class Ball:
    def __init__(self):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, RADIUS - 20)
        self.x = CENTER[0] + math.cos(angle) * distance
        self.y = CENTER[1] + math.sin(angle) * distance
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        hue = random.random()
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)
        self.color = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        self.radius = 10
        self.trail = []
        self.trail.append((self.x, self.y))
        self.hue = random.random()

    def update(self):
        self.vy += gravity
        self.hue = (self.hue + 0.01) % 1
        rgb = colorsys.hsv_to_rgb(self.hue, 1, 1)
        self.color = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        self.x += self.vx
        self.y += self.vy

        dx = self.x - CENTER[0]
        dy = self.y - CENTER[1]
        distance = math.hypot(dx, dy)

        if distance + self.radius > RADIUS:
            nx = dx / distance
            ny = dy / distance
            dot = self.vx * nx + self.vy * ny
            self.vx -= 2 * dot * nx
            self.vy -= 2 * dot * ny
            self.vx *= bounciness
            self.vy *= bounciness
            overlap = (distance + self.radius) - RADIUS
            self.x -= nx * overlap
            self.y -= ny * overlap

        self.trail.append((self.x, self.y))
        if len(self.trail) > 15:
            self.trail.pop(0)

    def draw(self):
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            trail_color = (self.color[0], self.color[1], self.color[2], alpha)
            s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, trail_color, (self.radius, self.radius), self.radius)
            screen.blit(s, (pos[0] - self.radius, pos[1] - self.radius))
        # Draw the ball
        ball_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(ball_surf, self.color, (self.radius, self.radius), self.radius)
        screen.blit(ball_surf, (self.x - self.radius, self.y - self.radius))


balls = [Ball() for _ in range(30)]

running = True
while running:
    clock.tick(60)
    spawn_timer += 1
    if spawn_timer > 15:
        balls.append(Ball())
        spawn_timer = 0

    # neon background
    bg_hue = (bg_hue + 0.5) % 360
    bg_rgb = colorsys.hsv_to_rgb(bg_hue / 360, 0.6, 0.1)
    bg_color = (int(bg_rgb[0] * 255), int(bg_rgb[1] * 255), int(bg_rgb[2] * 255))
    screen.fill(bg_color)

    # main circle
    pygame.draw.circle(screen, (255, 255, 0), CENTER, RADIUS, 2)

    # make it glow
    for glow_radius in range(RADIUS, RADIUS + 40, 8):
        glow_alpha = max(0, 100 - (glow_radius - RADIUS) * 2)
        glow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 255, 0, glow_alpha), CENTER, glow_radius, 2)
        screen.blit(glow_surf, (0, 0))

    for ball in balls:
        ball.update()
        ball.draw()

    pygame.display.flip()

    if len(balls) > 50:
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        screen.scroll(offset_x, offset_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(f"Total Balls Spawned: {len(balls)}")
            running = False

pygame.quit()