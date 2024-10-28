import random
from typing import Optional, List
from PIL import Image
import numpy as np
from tqdm import tqdm

from cells import Cell
from constants import *


class Generator:

    def __init__(self,
                 size_x: int,
                 size_y: int):
        self.size_x = size_x
        self.size_y = size_y
        self.matrix = []

    def generate(self,
                 ) -> List[List[Cell]]:
        self.matrix = self.create_wall()
        self.generate_maze()
        return self.matrix

    def create_wall(self) -> List[List[Cell]]:
        matrix = []
        for y in tqdm(range(self.size_y)):
            x_row = []
            for x in range(self.size_x):
                cell = Cell(x, y)
                if y == 0:
                    cell.down = BORDER
                elif y == self.size_y-1:
                    cell.up = BORDER
                if x == 0:
                    cell.left = BORDER
                elif x == self.size_y-1:
                    cell.right = BORDER
                x_row.append(cell)
            matrix.append(x_row)
       # print(matrix)
        return matrix

    def free_directions(self, cell: Cell) -> Optional[dict]:
        walls = dict(filter(lambda x: x[1] == WALL, cell.status_wall().items()))
        if UP in walls:
            if self.matrix[cell.y + 1][cell.x].is_passed:
                del walls[UP]
        if RIGHT in walls:
            if self.matrix[cell.y][cell.x + 1].is_passed:
                del walls[RIGHT]
        if DOWN in walls:
            if self.matrix[cell.y - 1][cell.x].is_passed:
                del walls[DOWN]
        if LEFT in walls:
            if self.matrix[cell.y][cell.x - 1].is_passed:
                del walls[LEFT]
        if len(walls) == 0:
            return None
        return walls

    def free_go(self, cell: Cell) -> Optional[dict]:
        dirs = dict(filter(lambda x: x[1] == VOID, cell.status_wall().items()))
        if UP in dirs:
            if self.matrix[cell.y + 1][cell.x].is_here:
                del dirs[UP]
        if RIGHT in dirs:
            if self.matrix[cell.y][cell.x + 1].is_here:
                del dirs[RIGHT]
        if DOWN in dirs:
            if self.matrix[cell.y - 1][cell.x].is_here:
                del dirs[DOWN]
        if LEFT in dirs:
            if self.matrix[cell.y][cell.x - 1].is_here:
                del dirs[LEFT]
        if len(dirs) == 0:
            return None
        return dirs

    def get_cell_by_dir(self, cell: Cell, direction: int) -> Cell:
        x_add = 0
        y_add = 0
        if direction == UP:
            y_add = 1
        elif direction == RIGHT:
            x_add = 1
        elif direction == DOWN:
            y_add = -1
        elif direction == LEFT:
            x_add = -1
        return self.matrix[cell.y + y_add][cell.x + x_add]

    def generate_maze(self):
        way_cell = []
        cur_cell: Cell = self.matrix[0][0]
        cur_cell.is_passed = True
        while True:
            free_directions = self.free_directions(cur_cell)
            if free_directions is None:
                if len(way_cell) == 0:
                    break
                else:
                    cur_cell = way_cell.pop(-1)
            else:
                title_dirs = list(free_directions.keys())
                next_dir = title_dirs[random.randint(0, len(title_dirs)-1)]
                cur_cell.set_wall(next_dir, VOID)
                next_cell = self.get_cell_by_dir(cur_cell, next_dir)
                next_cell.set_inverse_wall(next_dir, VOID)
                next_cell.is_passed = True

                way_cell.append(cur_cell)
                cur_cell = next_cell

    def go_maze(self):
        way_cell = []
        cur_cell: Cell = self.matrix[0][0]
        cur_cell.is_here = True
        while True:
            free_go = self.free_go(cur_cell)
            if free_go is None:
                cur_cell = way_cell.pop(-1)
            else:
                title_dirs = list(free_go.keys())
                next_dir = title_dirs[random.randint(0, len(title_dirs)-1)]
                next_cell = self.get_cell_by_dir(cur_cell, next_dir)
                next_cell.is_here = True

                way_cell.append(cur_cell)
                cur_cell = next_cell

                if next_cell.x == self.size_x - 1 and next_cell.y == self.size_y - 1:
                    way_cell.append(next_cell)
                    break

        for cell in way_cell:
            cell.is_success = True

    def get_color(self,
                  cell: Cell,
                  x: int,
                  y: int,
                  size_x: int,
                  size_y: int,
                  add_x: int = 0,
                  add_y: int = 0,
                  direction: Optional[int] = None,
                  is_main: bool = False):
        wall_type = {VOID: (255, 255, 255), WALL: (127, 127, 127), BORDER: (0, 0, 0)}
        cell_go = {"HERE": (0, 0, 255), "SUCCESS": (255, 0, 0)}
        if is_main:
            if cell.is_success:
                return cell_go["SUCCESS"]
            elif cell.is_here:
                return cell_go["HERE"]
            return wall_type[VOID]
        if direction is not None:
            if direction == UP:
                if cell.up == VOID:
                    if cell.is_success:
                        if self.matrix[cell.y + 1][cell.x].is_success:
                            return cell_go["SUCCESS"]
                        elif self.matrix[cell.y + 1][cell.x].is_here:
                            return cell_go["HERE"]
                    elif cell.is_here:
                        if self.matrix[cell.y + 1][cell.x].is_here:
                            return cell_go["HERE"]
                return wall_type[cell.up]
            elif direction == RIGHT:
                if cell.right == VOID:
                    if cell.is_success:
                        if self.matrix[cell.y][cell.x + 1].is_success:
                            return cell_go["SUCCESS"]
                        elif self.matrix[cell.y][cell.x + 1].is_here:
                            return cell_go["HERE"]
                    elif cell.is_here:
                        if self.matrix[cell.y][cell.x + 1].is_here:
                            return cell_go["HERE"]
                return wall_type[cell.right]
            elif direction == DOWN:
                if cell.down == VOID:
                    if cell.is_success:
                        if self.matrix[cell.y - 1][cell.x].is_success:
                            return cell_go["SUCCESS"]
                        elif self.matrix[cell.y - 1][cell.x].is_here:
                            return cell_go["HERE"]
                    elif cell.is_here:
                        if self.matrix[cell.y - 1][cell.x].is_here:
                            return cell_go["HERE"]
                return wall_type[cell.down]
            elif direction == LEFT:
                if cell.left == VOID:
                    if cell.is_success:
                        if self.matrix[cell.y][cell.x - 1].is_success:
                            return cell_go["SUCCESS"]
                        elif self.matrix[cell.y][cell.x - 1].is_here:
                            return cell_go["HERE"]
                    elif cell.is_here:
                        if self.matrix[cell.y][cell.x - 1].is_here:
                            return cell_go["HERE"]
                return wall_type[cell.left]
        else:
            if x+add_x >= size_x-1 or x+add_x < 0 or y+add_y >= size_y-1 or y+add_y < 0:
                return wall_type[BORDER]
            return wall_type[WALL]

    def print_maze(self, filename: str = "image.png"):
        is_invalid_matrix = False
        size_y = len(self.matrix)
        if size_y > 0:
            size_x = len(self.matrix[0])
            if size_x > 0:
                size_cell = 0
                # Размер исходного изображения
                width = size_x * 2 + 1
                height = size_y * 2 + 1

                # Создание пустого изображения
                image = Image.new("RGB", (width, height), "white")

                pixels = np.array(image)

                for y in tqdm(range(size_y)):
                    for x in range(size_x):
                        y_prefix = 2 * (size_y-1-y)
                        x_prefix = 2 * x
                        pixels[y_prefix + 1 + size_cell, x_prefix + 1 + size_cell] = self.get_color(self.matrix[y][x], x, y, size_x, size_y, is_main=True)

                        pixels[y_prefix + size_cell, x_prefix + 1 + size_cell] = self.get_color(self.matrix[y][x], x, y, size_x, size_y, direction=UP)
                        pixels[y_prefix + 1 + size_cell, x_prefix + 2 + size_cell] = self.get_color(self.matrix[y][x], x, y, size_x, size_y, direction=RIGHT)
                        pixels[y_prefix + 2 + size_cell, x_prefix + 1 + size_cell] = self.get_color(self.matrix[y][x], x, y, size_x, size_y, direction=DOWN)
                        pixels[y_prefix + 1 + size_cell, x_prefix + size_cell] = self.get_color(self.matrix[y][x], x, y, size_x, size_y, direction=LEFT)

                        pixels[y_prefix + size_cell, x_prefix + size_cell] = self.get_color(self.matrix[y][x], x, y, size_x, size_y, add_x=-1, add_y=1)
                        pixels[y_prefix + size_cell, x_prefix + 2 + size_cell] = self.get_color(self.matrix[y][x], x, y, size_x, size_y, add_x=1, add_y=1)
                        pixels[y_prefix + 2 + size_cell, x_prefix + size_cell] = self.get_color(self.matrix[y][x], x, y, size_x, size_y, add_x=-1, add_y=-1)
                        pixels[y_prefix + 2 + size_cell, x_prefix + 2 + size_cell] = self.get_color(self.matrix[y][x], x, y, size_x, size_y, add_x=1, add_y=-1)
                image = Image.fromarray(pixels)

                image.save(filename, "PNG")
            else:
                is_invalid_matrix = True
        else:
            is_invalid_matrix = True
        if is_invalid_matrix:
            return "Maze nof found"
