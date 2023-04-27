import random
import pygame
from tile import Tile

class Block:
    def __init__(self, images, w, h):
        self.w = w
        self.h = h

        self.images = images
        self.tiles = []
        for key, value in self.images.items():
            self.tiles.append(Tile(key, value, w/3, h/3))

        # entropy is the number of options a tile has
        self.entropy = len(self.tiles)
        pass

    def show(self, ds, x, y, selected=False):
        if selected:
            pygame.draw.rect(ds, (255, 0, 0), (x, y, self.w, self.h), 4)
        if len(self.tiles) == 1:
            full_img = pygame.transform.scale(self.tiles[0].image, (self.w, self.h))
            ds.blit(full_img, (x, y))
            return
        ctr = 0
        for i in range(3):
            for j in range(3):
                if ctr >= len(self.tiles):
                    return
                
                self.tiles[ctr].show(ds, x + i * (self.w/3), y + j * (self.h/3))
                ctr += 1
        pass

    def collapse(self):
        # Can't collapse now that only one option remains
        if self.entropy == 1:
            return -1

        # Collapse this tile to a random tile
        tile = random.choice(self.tiles)
        self.tiles.clear()
        self.tiles.append(tile)

        # Set Entropy at last
        self.entropy = 1
        pass

    def reduce_entropy(self, rules):
        if self.entropy == 1:
            return -1

        newtiles = []
        for t in self.tiles:
            if t.name in rules:
                newtiles.append(t)

        self.tiles = newtiles
        self.entropy = len(self.tiles)
        pass
