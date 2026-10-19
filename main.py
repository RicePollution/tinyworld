import pygame
import math
from math import cos, sin

TILE = 32
player_x = 2.0 * TILE
player_y = 1.5 * TILE
player_a = 3
fov = math.pi / 3

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
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if not blocked(player_x, player_y - 2):
            player_y -= 2
    if keys[pygame.K_s]:
        if not blocked(player_x, player_y + 2):
            player_y += 2
    if keys[pygame.K_a]:
        if not blocked(player_x - 2, player_y):
            player_x -= 2
    if keys[pygame.K_d]:
        if not blocked(player_x + 2, player_y):
            player_x += 2
    if keys[pygame.K_q]:
        player_a -= .03
    if keys[pygame.K_e]:
        player_a += .03

    screen.fill((0, 0, 0))

    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == "1":
                pygame.draw.rect(screen, (255, 155, 155), (x * TILE, y * TILE, TILE, TILE))

    pygame.draw.rect(screen, (255, 255, 255), (player_x, player_y, 8, 8))

    for i in range(512):
        ray_a = player_a - fov/2 + fov * i/512

        c = 0
        while c < 500:
            x = player_x + c*cos(ray_a)
            y = player_y + c*sin(ray_a)
            if is_wall(x, y):
                break
            else:
                c += 2
        pygame.draw.line(screen,(255,255,255),((player_x + 4),(player_y + 4)), (x,y))

    pygame.display.flip()
    clock.tick(60)
    print(clock.get_fps())

pygame.quit()