import pygame
import math
from math import cos, sin

TILE = 32
player_x = 2.0 * TILE
player_y = 1.5 * TILE
player_a = 3
fov = math.pi / 3
ray_count = 512
screen_h = 512
view_dist = 500
speed = 2

game_map = [
    "1111111111111111",
    "1000101000001001",
    "1001101111001001",
    "1001001001001011",
    "1011001001011011",
    "1000001001011011",
    "1000000000000001",
    "1000100000100001",
    "1000100110100101",
    "1010000110000101",
    "1010011111001101",
    "1010000000001001",
    "1000111100001001",
    "1000000000011001",
    "1011100000000001",
    "1111111111111111",
]

def is_wall(x, y):
    return game_map[int(y / TILE)][int(x / TILE)] == "1"

def blocked(x, y, size=8):
    return (is_wall(x, y) or
            is_wall(x + size - 1, y) or
            is_wall(x, y + size - 1) or
            is_wall(x + size - 1, y + size - 1))

pygame.init()
screen = pygame.display.set_mode((1024, 512))
# change wall texture here
wall_tex = pygame.image.load("textures/wall_textures/wall_03_64.png").convert()
TEX_W = wall_tex.get_width()
TEX_H = wall_tex.get_height()
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    cos_player = cos(player_a)
    sin_player = sin(player_a)
    dx = 0
    dy = 0
    if keys[pygame.K_w]:
        dx += speed * cos_player
        dy += speed * sin_player
    if keys[pygame.K_s]:
        dx -= speed * cos_player
        dy -= speed * sin_player
    if keys[pygame.K_a]:
        dx -= speed * -sin_player
        dy -= speed * cos_player
    if keys[pygame.K_d]:
        dx += speed * -sin_player
        dy += speed * cos_player

    if not blocked(dx + player_x, player_y):
        player_x += dx
    if not blocked(player_x, player_y + dy):
        player_y += dy

    if keys[pygame.K_q]:
        player_a -= .03
    if keys[pygame.K_e]:
        player_a += .03

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen,(40,40,40),(512, 0, 512, 256))
    pygame.draw.rect(screen,(100,100,110),(512, 256, 512, 256))

    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == "1":
                pygame.draw.rect(screen, (255, 155, 155), (x * TILE, y * TILE, TILE, TILE))

    pygame.draw.rect(screen, (255, 255, 255), (player_x, player_y, 8, 8))

    for i in range(ray_count):
        ray_a = player_a - fov/2 + fov * i/ray_count

        c = 0
        cos_a = cos(ray_a)
        sin_a = sin(ray_a)
        while c < view_dist:
            x = player_x + c*cos_a
            y = player_y + c*sin_a
            if is_wall(x, y):
                break
            else:
                c += 1
        prev_x = player_x + (c-1)*cos_a
        prev_y = player_y + (c-1)*sin_a
        if i % 8 == 0:
            pygame.draw.line(screen,(255,255,255),((player_x + 4),(player_y + 4)), (x,y))
        dist = c*cos(ray_a-player_a)

        col_changed = int(x / TILE) != int(prev_x / TILE)
        row_changed = int(y / TILE) != int(prev_y / TILE)

        if col_changed and row_changed:
            if is_wall(x, prev_y):
                side_shade = 1
                hit_vertical = True
            else:
                side_shade = .8
                hit_vertical = False
        elif col_changed:
           side_shade = 1
           hit_vertical = True
        else:
            side_shade = .8
            hit_vertical = False

        if hit_vertical:
            tex_col = int(((y % TILE)/TILE)*TEX_W)
        else:
            tex_col = int(((x % TILE)/TILE)*TEX_W)

        height = (screen_h * TILE) / max(dist,1)
        height = min(height, screen_h)
        top = (screen_h - height) / 2
        brightness = 1 - dist / view_dist
        brightness = max(0.2, min(1, brightness))
        brightness = brightness * side_shade
        wall_r = int(255 * brightness)
        wall_g = int(155 * brightness)
        wall_b = int(155 * brightness)
        wall_color = wall_r,wall_g,wall_b
        pygame.draw.rect(screen, wall_color, (512 + i, top, 1, height))

        strip = wall_tex.subsurface((tex_col, 0, 1, TEX_H))
        scaled = pygame.transform.scale(strip, (1, max(1, int(height))))
        screen.blit(scaled, (512 + i, int(top)))

    pygame.display.flip()
    clock.tick(60)
    pygame.display.set_caption(f"FPS: {clock.get_fps():.0f}")
pygame.quit()