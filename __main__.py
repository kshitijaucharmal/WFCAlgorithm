import pygame
import random

from block import Block
from rule import Rule

WIDTH = 400
HEIGHT = 400

grid_size = 20

rows = WIDTH // grid_size

ds = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wave Function Collapse")

selected = [0, 0]

tile_images = {
    'left' : pygame.image.load("sprites/left.png"),
    'up' : pygame.image.load("sprites/up.png"),
    'down' : pygame.image.load("sprites/down.png"),
    'right' : pygame.image.load("sprites/right.png"),
    'blank' : pygame.image.load("sprites/blank.png"),
}

# Should have length/names the same as images
rules = {
    'left' : Rule(),
    'up' : Rule(),
    'down' : Rule(),
    'right' : Rule(),
    'blank' : Rule(),
}

# Setup Rules
# Blank rules
rules['blank'].north = ['up', 'blank']
rules['blank'].south = ['down', 'blank']
rules['blank'].east = ['right', 'blank']
rules['blank'].west = ['left', 'blank']
# Left Rules
rules['left'].north = ['down', 'left', 'right']
rules['left'].south = ['up', 'left', 'right']
rules['left'].east = ['right', 'blank']
rules['left'].west = ['right', 'down', 'up']
# Right Rules
rules['right'].north = ['down', 'left', 'right']
rules['right'].south = ['up', 'left', 'right']
rules['right'].east = ['left', 'down', 'up']
rules['right'].west = ['left', 'blank']
# Up Rules
rules['up'].north = ['down', 'left', 'right']
rules['up'].south = ['down', 'blank']
rules['up'].east = ['up', 'left', 'down']
rules['up'].west = ['right', 'down', 'up']
# Down Rules
rules['down'].north = ['up', 'blank']
rules['down'].south = ['up', 'left', 'right']
rules['down'].east = ['left', 'down', 'up']
rules['down'].west = ['right', 'up', 'down']

board = []
for i in range(rows):
    board.append(list())
    for j in range(rows):
        t = Block(tile_images, grid_size, grid_size)
        board[i].append(t)

def propagate(x, y, depth):
    if depth <= 0:
        return
    # Get selected tiles rules
    tile = board[x][y]
    try:
        tilename = tile.tiles[0].name
    except:
        print("Entropy is high, wrong tiles chosen")
        return
    tilerules = rules[tilename]

    if y > 0:
        north = board[x][y - 1]
        north.reduce_entropy(tilerules.north)
        propagate(x, y-1, depth-1)
    if y < rows-1:
        south = board[x][y + 1]
        south.reduce_entropy(tilerules.south)
        propagate(x, y+1, depth-1)
    if x < rows - 1:
        east = board[x + 1][y]
        east.reduce_entropy(tilerules.east)
        propagate(x+1, y, depth-1)
    if x > 0:
        west = board[x - 1][y]
        west.reduce_entropy(tilerules.west)
        propagate(x-1, y, depth-1)
    pass

def solve():
    # Collapse selected tile
    err = board[selected[0]][selected[1]].collapse()
    # Propagate Changes
    propagate(selected[0], selected[1], depth=8)

def main():
    run = True
    while run:
        ds.fill((11, 11, 11))

        for i in range(rows):
            for j in range(rows):
                chosen = True if i == selected[0] and j == selected[1] else False
                board[i][j].show(ds, i * grid_size, j * grid_size, chosen)

        # Draw grid
        # for i in range(rows):
            # pygame.draw.line(ds, (255, 255, 255), (0, i * grid_size), (WIDTH, i * grid_size), 1)
        # for i in range(rows):
            # pygame.draw.line(ds, (255, 255, 255), (i * grid_size, 0), (i * grid_size, HEIGHT), 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    selected[1] = selected[1] + 1 if selected[1] < rows-1 else 0
                if event.key == pygame.K_k:
                    selected[1] = selected[1] - 1 if selected[1] > 0 else rows-1
                if event.key == pygame.K_h:
                    selected[0] = selected[0] - 1 if selected[0] > 0 else rows-1
                if event.key == pygame.K_l:
                    selected[0] = selected[0] + 1 if selected[0] < rows-1 else 0
                solve()

                if event.key == pygame.K_s:
                    solve()

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
