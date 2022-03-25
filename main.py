import pygame
from pygame.locals import *

import random
import sys

from settings import *


class Minesweeper:
    def __init__(self):
        pygame.display.set_caption("Minesweeper")
        self.display_surface = pygame.display.set_mode(WINDOW_DIMENSIONS)
        self.clock = pygame.time.Clock()
        self.is_running = False

        self.field = [[random.randint(0, 10) for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]

        self.sprite = pygame.image.load("tiles.jpg").convert()

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick(TARGET_FPS)
            frame_time_s = frame_time_ms / 1000.
            print(f"Frame time: {frame_time_ms} ms    \r", end="")

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.stop()


            self.display_surface.fill("white")
            for x, row in enumerate(self.field):
                for y, cell in enumerate(row):
                    self.display_surface.blit(self.sprite, (x * CELL_SIZE, y * CELL_SIZE), (CELL_SIZE * cell, 0, CELL_SIZE, CELL_SIZE))
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def stop(self):
        self.is_running = False


if __name__ == "__main__":
    Minesweeper().run()

