import pygame
import random
import os

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Highway Racer Pro")

GRAY, YELLOW, WHITE, BLACK, RED = (50, 50, 50), (255, 255, 0), (255, 255, 255), (0, 0, 0), (255, 0, 0)

def load_asset(filename, w, h):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)
    try:
        img = pygame.image.load(file_path).convert_alpha()
        return pygame.transform.scale(img, (w, h))
    except:
        surf = pygame.Surface((w, h))
        surf.fill((random.randint(100, 255), 0, 0))
        return surf

car_w, car_h = 50, 100
player_img = load_asset('car.png', car_w, car_h)
ENEMY_IMAGES = [
    load_asset('truck.png', 60, 120),
    load_asset('taxi.png', 50, 100),
    load_asset('van.png', 55, 110)
]

def spawn_enemy(existing_enemies):
    img = random.choice(ENEMY_IMAGES)
    w, h = img.get_size()
    
    attempts = 0
    while attempts < 15: 
        x = random.randint(200, 600 - w)
        y = random.randint(-800, -150)
        new_rect = pygame.Rect(x, y, w, h)
        overlap = False
        for e in existing_enemies:
            if new_rect.inflate(20, 100).colliderect(e["rect"]): 
                overlap = True
                break
        
        if not overlap:
            return {"img": img, "rect": new_rect}
        attempts += 1
    return {"img": img, "rect": pygame.Rect(random.randint(200, 600-w), -200, w, h)}

def draw_road(offset):
    pygame.draw.rect(screen, GRAY, (150, 0, 500, height))
    pygame.draw.rect(screen, (30, 100, 30), (0, 0, 150, height))
    pygame.draw.rect(screen, (30, 100, 30), (650, 0, 150, height))
    for y in range(-100, height, 100):
        pygame.draw.rect(screen, YELLOW, (width // 2 - 5, y + offset, 10, 50))

def start_menu():
    menu_font = pygame.font.SysFont("Arial", 50, bold=True)
    sub_font = pygame.font.SysFont("Arial", 30)
    
    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_road(0)
        
        title = menu_font.render("HIGHWAY RACER", True, WHITE)
        instruction = sub_font.render("Press SPACE to Start", True, YELLOW)
        
        screen.blit(title, (width//2 - title.get_width()//2, height//2 - 50))
        screen.blit(instruction, (width//2 - instruction.get_width()//2, height//2 + 20))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def game_loop():
    player_x = width // 2 - car_w // 2
    player_y = height - car_h - 20
    global_speed = 5
    score = 0
    lane_offset = 0
    enemies = []
    
    for _ in range(3):
        enemies.append(spawn_enemy(enemies))

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30, bold=True)
    running = True

    while running:
        lane_offset = (lane_offset + global_speed) % 100
        draw_road(lane_offset)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 160: player_x -= 7
        if keys[pygame.K_RIGHT] and player_x < 640 - car_w: player_x += 7

        player_rect = pygame.Rect(player_x, player_y, car_w, car_h)
        
        for enemy in enemies[:]:
            enemy["rect"].y += global_speed
            screen.blit(enemy["img"], enemy["rect"])

            if player_rect.colliderect(enemy["rect"]):
                running = False # Crash!

            if enemy["rect"].y > height:
                enemies.remove(enemy)
                enemies.append(spawn_enemy(enemies))
                score += 1
                global_speed += 0.1

        screen.blit(player_img, (player_x, player_y))
        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (20, 20))

        pygame.display.flip()
        clock.tick(60)
    
    return True

while True:
    start_menu()
    game_loop()

pygame.quit()
