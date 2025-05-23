# Créé par Administrateur, le 23/05/2025 en Python 3.7
import pygame
import random
import sys

# Constants
TILE_SIZE = 32
WORLD_WIDTH = 50
WORLD_HEIGHT = 50
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Colors
GRASS = (106, 190, 48)
WATER = (52, 101, 164)
TREE_TRUNK = (120, 72, 0)
TREE_LEAVES = (34, 177, 76)
COIN = (255, 216, 0)
PLAYER_BODY = (50, 50, 200)
PLAYER_HEAD = (200, 200, 255)
HUD_BG = (30, 30, 60)
HUD_TEXT = (255,255,255)

TILE_TYPES = [0, 1, 2]  # 0: grass, 1: water, 2: tree

pygame.init()
pygame.display.set_caption("Open World Game")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)

# Sound
try:
    coin_sound = pygame.mixer.Sound(pygame.mixer.Sound(file=None))
except:
    coin_sound = None

def draw_text(surface, text, pos, color):
    img = font.render(text, True, color)
    surface.blit(img, pos)

def generate_world():
    world = []
    for y in range(WORLD_HEIGHT):
        row = []
        for x in range(WORLD_WIDTH):
            t = random.choices(TILE_TYPES, weights=[10, 2, 3])[0]
            row.append(t)
        world.append(row)
    return world

def place_coins(world, n):
    coins = set()
    while len(coins) < n:
        x = random.randint(0, WORLD_WIDTH - 1)
        y = random.randint(0, WORLD_HEIGHT - 1)
        if world[y][x] == 0:  # Only on grass
            coins.add((x, y))
    return coins

def main():
    player_x = WORLD_WIDTH // 2
    player_y = WORLD_HEIGHT // 2
    coins_collected = 0
    world = generate_world()
    coins = place_coins(world, 50)

    cam_x = 0
    cam_y = 0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        # --- Input ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_RIGHT]: dx = 1
        if keys[pygame.K_LEFT]: dx = -1
        if keys[pygame.K_DOWN]: dy = 1
        if keys[pygame.K_UP]: dy = -1

        nx = player_x + dx
        ny = player_y + dy

        # Movement with boundaries and not on water
        if 0 <= nx < WORLD_WIDTH and 0 <= ny < WORLD_HEIGHT:
            if world[ny][nx] != 1:
                player_x = nx
                player_y = ny

        # Coin pickup
        if (player_x, player_y) in coins:
            coins.remove((player_x, player_y))
            coins_collected += 1
            if coin_sound:
                coin_sound.play()

        # Camera centering
        cam_x = player_x * TILE_SIZE - SCREEN_WIDTH // 2 + TILE_SIZE // 2
        cam_y = player_y * TILE_SIZE - SCREEN_HEIGHT // 2 + TILE_SIZE // 2
        cam_x = max(0, min(cam_x, WORLD_WIDTH * TILE_SIZE - SCREEN_WIDTH))
        cam_y = max(0, min(cam_y, WORLD_HEIGHT * TILE_SIZE - SCREEN_HEIGHT))

        # --- Draw ---
        screen.fill(GRASS)

        # Tiles
        tile_x0 = max(0, cam_x // TILE_SIZE)
        tile_y0 = max(0, cam_y // TILE_SIZE)
        tile_x1 = min(WORLD_WIDTH, tile_x0 + SCREEN_WIDTH // TILE_SIZE + 2)
        tile_y1 = min(WORLD_HEIGHT, tile_y0 + SCREEN_HEIGHT // TILE_SIZE + 2)

        for y in range(tile_y0, tile_y1):
            for x in range(tile_x0, tile_x1):
                tx = x * TILE_SIZE - cam_x
                ty = y * TILE_SIZE - cam_y
                t = world[y][x]
                if t == 0:
                    pygame.draw.rect(screen, GRASS, (tx, ty, TILE_SIZE, TILE_SIZE))
                elif t == 1:
                    pygame.draw.rect(screen, WATER, (tx, ty, TILE_SIZE, TILE_SIZE))
                elif t == 2:
                    pygame.draw.rect(screen, TREE_TRUNK, (tx + TILE_SIZE//3, ty + TILE_SIZE//2, TILE_SIZE//3, TILE_SIZE//2))
                    pygame.draw.circle(screen, TREE_LEAVES, (tx + TILE_SIZE//2, ty + TILE_SIZE//2), TILE_SIZE//2 - 2)

        # Coins
        for (x, y) in coins:
            tx = x * TILE_SIZE - cam_x
            ty = y * TILE_SIZE - cam_y
            pygame.draw.circle(screen, COIN, (tx + TILE_SIZE // 2, ty + TILE_SIZE // 2), TILE_SIZE // 3)

        # Player
        px = player_x * TILE_SIZE - cam_x
        py = player_y * TILE_SIZE - cam_y
        pygame.draw.rect(screen, PLAYER_BODY, (px + 8, py + 10, 16, 16))
        pygame.draw.circle(screen, PLAYER_HEAD, (int(px + TILE_SIZE//2), int(py + 15)), 8)

        # HUD
        pygame.draw.rect(screen, HUD_BG, (0, 0, SCREEN_WIDTH, 30))
        draw_text(screen, f"Coins: {coins_collected}", (10, 5), HUD_TEXT)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
