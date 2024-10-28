from typing import Optional

from constants import *


class Cell:

    def __init__(self,
                 x: int,
                 y: int,
                 ) -> None:

        self.x = x
        self.y = y

        self.up = WALL
        self.right = WALL
        self.down = WALL
        self.left = WALL

        self.is_passed = False
        self.is_here = False
        self.is_success = False

    def status_wall(self) -> dict:
        return {UP: self.up, RIGHT: self.right, DOWN: self.down, LEFT: self.left}

    def set_wall(self,
                 direction: int,
                 value: int
                 ) -> None:
        if direction == UP:
            self.up = value
        elif direction == RIGHT:
            self.right = value
        elif direction == DOWN:
            self.down = value
        elif direction == LEFT:
            self.left = value

    def set_inverse_wall(self,
                         direction: int,
                         value: int
                         ) -> None:
        if direction == UP:
            self.down = value
        elif direction == RIGHT:
            self.left = value
        elif direction == DOWN:
            self.up = value
        elif direction == LEFT:
            self.right = value

