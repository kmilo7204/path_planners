import pygame
from pygame.locals import *

# Colors pallete
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (38, 255, 122)
ORANGE = (227,123,52)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
MAJ_BLUE = (82, 86, 243)
PAC_BLUE = (36, 167, 214)
HONEY = (255, 182, 46)

class Display:
    def __init__(self, width, height):
        # This should be move to grid
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(BLACK)
        self.update_display()

    def update_display(self):
        pygame.display.update()

    def draw_box(self, color: tuple, cell: tuple, resolution: int):
        pygame.draw.rect(self.screen, color, (cell[0] * resolution + 1, cell[1] * resolution + 1, resolution - 1, resolution - 1))
        self.update_display()