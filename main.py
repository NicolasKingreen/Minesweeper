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
        self.rmb_pressed = False
        self.click_cooldown = 100
        self.click_time = 0

        self.init_field()

        self.sprite = pygame.image.load("tiles.jpg").convert()

    def init_field(self):
        self.field = [[0 for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]

        # placing mines
        for _ in range(MINES):
            x = random.randint(0, FIELD_SIZE-1)
            y = random.randint(0, FIELD_SIZE-1)
            self.field[x][y] = 9

        # counting mines around each cell
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

            # winning condition
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

        # converting mouse position to cell coordinates
        mouse_cell_x = mouse_pos[0] // CELL_SIZE
        mouse_cell_y = mouse_pos[1] // CELL_SIZE
        mouse_cell = mouse_cell_x, mouse_cell_y

        mouse_buttons_pressed = pygame.mouse.get_pressed()
        if any(mouse_buttons_pressed) and self.can_click \
                and not (self.lmb_pressed or self.rmb_pressed):
            self.can_click = False
            self.click_time = pygame.time.get_ticks()

            # if LMB pressed
            if mouse_buttons_pressed[0]:
                self.lmb_pressed = True

                # clicking on a mine
                if self.field[mouse_cell_x][mouse_cell_y] == 9:
                    self.end_game(False)

                # clicking on an empty cell (no digits)
                elif self.field[mouse_cell_x][mouse_cell_y] == 0:
                    for x, y \
                    in (self.get_empty_cells_around(mouse_cell_x, mouse_cell_y)):
                        self.uncovered_tiles[x][y] = 0

                # clicking on a digit cell
                else:
                    self.uncovered_tiles[mouse_cell[0]][mouse_cell[1]] = 0 

            # if RMB pressed, placing a flag
            elif mouse_buttons_pressed[2] and \
                self.uncovered_tiles[mouse_cell_x][mouse_cell_y] != 0:
                self.rmb_pressed = True
                if self.uncovered_tiles[mouse_cell_x][mouse_cell_y] == 1:
                    self.uncovered_tiles[mouse_cell_x][mouse_cell_y] = 2
                elif self.uncovered_tiles[mouse_cell_x][mouse_cell_y] == 2:
                    self.uncovered_tiles[mouse_cell_x][mouse_cell_y] = 1

        # controlling single click
        if not mouse_buttons_pressed[0] and self.lmb_pressed:
            self.lmb_pressed = False
        elif not mouse_buttons_pressed[2] and self.rmb_pressed:
            self.rmb_pressed = False 

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

                # if there is a covered mine
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
                tile_x = 0
                if self.uncovered_tiles[x][y] == 0:
                    tile_x = cell
                elif self.uncovered_tiles[x][y] == 1:
                    tile_x = 10
                else:
                    tile_x = 11
                self.display_surface.\
                    blit(self.sprite,
                        (x * CELL_SIZE, y * CELL_SIZE),
                        (CELL_SIZE * tile_x, 0, CELL_SIZE, CELL_SIZE))
        pygame.display.update()


if __name__ == "__main__":
    Minesweeper().run()

