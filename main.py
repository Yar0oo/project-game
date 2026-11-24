import pygame
import random
from settings import *
import sys

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("Arial", 55, bold=True)
font_medium = pygame.font.SysFont("Arial", 30, bold=True)
font_small = pygame.font.SysFont("Arial", 24)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = (PLAYER_IMAGE)
        self.rect = self.image.get_rect()

        self.rect.centerx = PLAYER_START_X
        self.rect.centery = PLAYER_START_Y

    def update(self, keys, dt):
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED * dt / 1000
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED * dt / 1000
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED * dt / 1000
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED * dt / 1000
        
        self.rect.clamp_ip(screen.get_rect())

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = ENEMY_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(ENEMY_WIDTH // 2, WIDTH - ENEMY_WIDTH // 2)
        self.rect.bottom = 0
        self.speed = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)

    def update(self, dt):
        self.rect.y += self.speed * dt / 1000

        if self.rect.top > HEIGHT:
            self.kill()

player = Player()
enemies = pygame.sprite.Group()

restart_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 60, 240, 55)
        
start_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 60, 240, 55)

menu = True
game_over = False
game_won = False

game_start_time = 0
spawn_timer = 0

spawn_delay = random.randint(ENEMY_SPAWN_MIN, ENEMY_SPAWN_MAX)

def reset_game():
    global game_over, game_won, menu
    global game_start_time, spawn_timer, spawn_delay

    game_over = False
    game_won = False
    menu = False

    player.rect.centerx = PLAYER_START_X
    player.rect.centery = PLAYER_START_Y

    enemies.empty()

    spawn_timer = 0

    spawn_delay = random.randint(ENEMY_SPAWN_MIN, ENEMY_SPAWN_MAX)

    game_start_time = pygame.time.get_ticks()

running = True
while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if menu and start_button.collidepoint(event.pos):
                    reset_game()

                elif (game_over or game_won) and restart_button.collidepoint(event.pos):
                    menu = True
                    game_over = False
                    game_won = False

    if menu:
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        menu_text = font_big.render("Enemy Rain", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(menu_text, menu_rect)
        pygame.draw.rect(screen, (30, 120, 220), start_button, border_radius=10)
        button_text = font_medium.render("Грати", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=start_button.center)
        screen.blit(button_text, button_rect)
        pygame.display.flip()
        continue

    if game_over:
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        lose_text = font_big.render("Ви програли!", True, (255, 0, 0))
        lose_rect = lose_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(lose_text, lose_rect)

        pygame.draw.rect(screen, (30, 120, 220), restart_button, border_radius=10)
        button_text = font_small.render("В меню", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=restart_button.center)
        screen.blit(button_text, button_rect)

        pygame.display.flip()
        continue

    if game_won:
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        win_text = font_big.render("Ви перемогли!", True, (0, 255, 0))
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(win_text, win_rect)

        pygame.draw.rect(screen, (30, 120, 220), restart_button, border_radius=10)
        button_text = font_small.render("В меню", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=restart_button.center)
        screen.blit(button_text, button_rect)

        pygame.display.flip()
        continue

    elapsed_time = (pygame.time.get_ticks() - game_start_time) / 1000
    if elapsed_time >= GAME_DURATION:
        game_won = True

    keys = pygame.key.get_pressed()

    player.update(keys, dt)

    spawn_timer += dt

    if spawn_timer >= spawn_delay:
        enemies.add(Enemy())

        spawn_timer = 0
        spawn_delay = random.randint(ENEMY_SPAWN_MIN, ENEMY_SPAWN_MAX)

    enemies.update(dt)

    if pygame.sprite.spritecollide(player, enemies, False):
        game_over = True

    if game_over:
        continue

    screen.blit(BACKGROUND_IMAGE, (0, 0))
    screen.blit(player.image, player.rect)

    enemies.draw(screen)

    remaining_time = max(0, GAME_DURATION - int(elapsed_time))

    timer_text = font_medium.render(f"Час: {remaining_time}", True, (255, 255, 255))

    screen.blit(timer_text, (20, 20))
    pygame.display.flip()

pygame.quit()
sys.exit()