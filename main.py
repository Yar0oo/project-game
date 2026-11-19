import pygame
import random
from settings import *

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("Arial", 55, bold=True)
font_medium = pygame.font.SysFont("Arial", 30, bold=True)
font_small = pygame.font.SysFont("Arial", 24)

player_rect = PLAYER_IMAGE.get_rect()
player_rect.centerx = PLAYER_START_X
player_rect.centery = PLAYER_START_Y

enemies = []

def create_enemy():
    enemy_rect = ENEMY_IMAGE.get_rect()
    enemy_rect.centerx = random.randint(ENEMY_WIDTH // 2, WIDTH - ENEMY_WIDTH // 2)
    enemy_rect.bottom = 0
    speed_speed = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
    return [enemy_rect, speed_speed]

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
    player_rect.centerx = PLAYER_START_X
    player_rect.centery = PLAYER_START_Y
    enemies.clear()
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
        menu_text = font_big.render("Потужноліт", True, (255, 255, 255))
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
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_rect.x -= PLAYER_SPEED * dt / 1000
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_rect.x += PLAYER_SPEED * dt / 1000
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_rect.y -= PLAYER_SPEED * dt / 1000
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_rect.y += PLAYER_SPEED * dt / 1000
    player_rect.clamp_ip(screen.get_rect())
    
    spawn_timer += dt
    if spawn_timer >= spawn_delay:
        enemies.append(create_enemy())
        spawn_timer = 0
        spawn_delay = random.randint(ENEMY_SPAWN_MIN, ENEMY_SPAWN_MAX)

    for enemy in enemies[:]:
        enemy_rect, enemy_speed = enemy
        enemy_rect.y += enemy_speed * dt / 1000
        if enemy_rect.top > HEIGHT:
            enemies.remove(enemy)

    for enemy in enemies:
        enemy_rect, enemy_speed = enemy

        if player_rect.colliderect(enemy_rect):
            game_over = True

    if game_over:
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        pygame.display.flip()
        continue

    

    screen.blit(BACKGROUND_IMAGE, (0, 0))
    screen.blit(PLAYER_IMAGE, player_rect)
    for enemy in enemies:
        enemy_rect, enemy_speed = enemy
        screen.blit(ENEMY_IMAGE, enemy_rect)

    remaining_time = max(0, GAME_DURATION - int(elapsed_time))
    timer_text = font_medium.render(f"Час: {remaining_time}", True, (255, 255, 255))
    screen.blit(timer_text, (20, 20))
    pygame.display.flip()

pygame.quit()
sys.exit()