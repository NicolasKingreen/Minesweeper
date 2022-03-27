import pygame
from pygame.locals import *

import random
import sys
import time

from settings import *


class Minesweeper:
    def __init__(self):
        pygame.display.set_caption("Minesweeper")
        self.display_surface = pygame.display.set_mode(WINDOW_DIMENSIONS)
        self.clock = pygame.time.Clock()
        self.is_running = False

        self.can_click = True
        self.lmb_pressed = False 
        self.click_cooldown = 100
        self.click_time = 0

        self.init_field()

        self.sprite = pygame.image.load("tiles.jpg").convert()

    def init_field(self):
        self.field = [[0 for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]
        for _ in range(MINES):
            x = random.randint(0, FIELD_SIZE-1)
            y = random.randint(0, FIELD_SIZE-1)
            self.field[x][y] = 9

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                if self.field[i][j] == 9:
                    continue
                total_mines_around = 0
                for x in range(i-1, i+2):
                    if x < 0 or x >= FIELD_SIZE:
                        continue
                    for y in range(j-1, j+2):
                        if y < 0 or y >= FIELD_SIZE:
                            continue
                        if self.field[x][y] == 9:
                            total_mines_around += 1

                self.field[i][j] = total_mines_around

        self.uncovered_tiles = [[1 for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick(TARGET_FPS)
            frame_time_s = frame_time_ms / 1000.
            #print(f"Frame time: {frame_time_ms} ms    \r", end="")

            self.handle_events()
            self.process_click()
            self.update_cooldowns()
            self.draw()

            if self.is_running and self.check_win_condition():
                self.end_game(True)

        pygame.quit()
        sys.exit()

    def stop(self):
        self.is_running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stop()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.stop()

    def process_click(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_cell = mouse_pos[0] // CELL_SIZE, mouse_pos[1] // CELL_SIZE
        mouse_buttons_pressed = pygame.mouse.get_pressed()
        if any(mouse_buttons_pressed) and self.can_click and not self.lmb_pressed:
            self.can_click = False
            self.lmb_pressed = True
            self.click_time = pygame.time.get_ticks()
            if mouse_buttons_pressed[0]:
                if self.field[mouse_cell[0]][mouse_cell[1]] == 9:
                    self.end_game(False)
                elif self.field[mouse_cell[0]][mouse_cell[1]] == 0:
                    for x, y in (self.get_empty_cells_around(mouse_cell[0], mouse_cell[1])):
                        self.uncovered_tiles[x][y] = 0
                else:
                    self.uncovered_tiles[mouse_cell[0]][mouse_cell[1]] = 0 
            elif mouse_buttons_pressed[2] and self.uncovered_tiles[mouse_cell[0]][mouse_cell[1]] != 0:
                self.uncovered_tiles[mouse_cell[0]][mouse_cell[1]] = 2

        if not mouse_buttons_pressed[0] and self.lmb_pressed:
            self.lmb_pressed = False

    def update_cooldowns(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.click_time > self.click_cooldown:
            self.can_click = True

    def get_empty_cells_around(self, x, y, empty_cells=[]): 
        if self.field[x][y] == 0 and (x, y) not in empty_cells:
            empty_cells.append((x, y))
        for i in range(x-1, x+2):
            if i < 0 or i >= FIELD_SIZE:
                continue
            for j in range(y-1, y+2):
                if j < 0 or j >= FIELD_SIZE:
                    continue
                if self.field[i][j] == 0 and (i, j) not in empty_cells:
                    self.get_empty_cells_around(i, j, empty_cells)
                elif 0 < self.field[i][j] < 9:
                    if (i, j) not in empty_cells:
                        empty_cells.append((i, j))
        return empty_cells

    def uncover_field(self):
        for x in range(FIELD_SIZE):
            for y in range(FIELD_SIZE):
                self.uncovered_tiles[x][y] = 0

    def check_win_condition(self):
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                if self.field[i][j] != 9 and self.uncovered_tiles[i][j] != 0:
                    return False
        return True

    def end_game(self, has_won):
        if has_won:
            print("You Won!")
        else:
            print("You Lost!")
        self.uncover_field()
        self.draw()
        time.sleep(2)
        self.stop()

    def draw(self):
        self.display_surface.fill("white")
        for x, row in enumerate(self.field):
            for y, cell in enumerate(row):
                if self.uncovered_tiles[x][y] == 0:
                    self.display_surface.blit(self.sprite, 
                                              (x * CELL_SIZE, y * CELL_SIZE), 
                                              (CELL_SIZE * cell, 0, CELL_SIZE, CELL_SIZE))
                elif self.uncovered_tiles[x][y] == 2:
                    self.display_surface.blit(self.sprite,
                                              (x * CELL_SIZE, y * CELL_SIZE),
                                              (CELL_SIZE * 11, 0, CELL_SIZE, CELL_SIZE))
                else:
                    self.display_surface.blit(self.sprite,
                                              (x * CELL_SIZE, y * CELL_SIZE),
                                              (CELL_SIZE * 10, 0, CELL_SIZE, CELL_SIZE))
        pygame.display.update()


if __name__ == "__main__":
    Minesweeper().run()

