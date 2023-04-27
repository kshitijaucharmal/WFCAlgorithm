import random
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, name, img, w, h):
        self.name = name
        self.image = img
        self.image = pygame.transform.scale(img, (w, h))
        self.rect = self.image.get_rect()
        pass

    def show(self, ds, x, y):
        ds.blit(self.image, (x, y))
        pass
