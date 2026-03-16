from typing import List, Optional, Dict
import random

WIDTH = 10
HEIGHT = 20

# Tetromino block shapes as list of coordinates for each rotation
PIECES = {
    "I": [
        [(0,0),(1,0),(2,0),(3,0)],
        [(1,-1),(1,0),(1,1),(1,2)],
    ],
    "O": [
        [(0,0),(1,0),(0,1),(1,1)],
    ],
    "T": [
        [(1,0),(0,1),(1,1),(2,1)],
        [(1,0),(1,1),(2,1),(1,2)],
        [(0,1),(1,1),(2,1),(1,2)],
        [(1,0),(0,1),(1,1),(1,2)],
    ],
    "L": [
        [(0,0),(0,1),(0,2),(1,2)],
        [(0,1),(1,1),(2,1),(2,0)],
        [(0,0),(1,0),(1,1),(1,2)],
        [(0,1),(1,1),(2,1),(0,2)],
    ],
    "J": [
        [(1,0),(1,1),(1,2),(0,2)],
        [(0,0),(0,1),(1,1),(2,1)],
        [(0,0),(1,0),(0,1),(0,2)],
        [(0,0),(1,0),(2,0),(2,1)],
    ],
    "S": [
        [(1,0),(2,0),(0,1),(1,1)],
        [(1,0),(1,1),(2,1),(2,2)],
    ],
    "Z": [
        [(0,0),(1,0),(1,1),(2,1)],
        [(2,0),(1,1),(2,1),(1,2)],
    ],
}
COLORS = {"I": 1, "O": 2, "T": 3, "L": 4, "J": 5, "S": 6, "Z": 7}

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False
        self.current_piece = None
        self.piece_x = 3
        self.piece_y = 0
        self.rotation = 0
        self.next_piece = random.choice(list(PIECES.keys()))
        self.spawn_piece()

    def spawn_piece(self):
        if self.game_over:
            return
        self.current_piece = self.next_piece
        self.next_piece = random.choice(list(PIECES.keys()))
        self.piece_x = 3
        self.piece_y = 0
        self.rotation = 0
        if self._collides(self.piece_x, self.piece_y, self.rotation):
            self.game_over = True

    def _shape(self, piece: str, rotation: int):
        rotations = PIECES[piece]
        return rotations[rotation % len(rotations)]

    def _collides(self, x: int, y: int, rotation: int):
        for dx, dy in self._shape(self.current_piece, rotation):
            gx = x + dx
            gy = y + dy
            if gx < 0 or gx >= WIDTH or gy < 0 or gy >= HEIGHT:
                return True
            if self.grid[gy][gx] != 0:
                return True
        return False

    def _lock_piece(self):
        color = COLORS[self.current_piece]
        for dx, dy in self._shape(self.current_piece, self.rotation):
            gx = self.piece_x + dx
            gy = self.piece_y + dy
            if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
                self.grid[gy][gx] = color
        self._clear_lines()
        self.spawn_piece()

    def _clear_lines(self):
        new_grid = []
        cleared = 0
        for row in self.grid:
            if all(cell != 0 for cell in row):
                cleared += 1
            else:
                new_grid.append(row)
        while len(new_grid) < HEIGHT:
            new_grid.insert(0, [0] * WIDTH)
        self.grid = new_grid
        if cleared > 0:
            self.lines += cleared
            self.score += (cleared * 100)
            self.level = 1 + self.lines // 10

    def move(self, dx: int, dy: int):
        if self.game_over:
            return
        if not self._collides(self.piece_x + dx, self.piece_y + dy, self.rotation):
            self.piece_x += dx
            self.piece_y += dy
            return True
        if dy > 0:
            self._lock_piece()
        return False

    def rotate(self):
        if self.game_over:
            return
        new_rot = (self.rotation + 1) % len(PIECES[self.current_piece])
        if not self._collides(self.piece_x, self.piece_y, new_rot):
            self.rotation = new_rot

    def hard_drop(self):
        if self.game_over:
            return
        while not self._collides(self.piece_x, self.piece_y + 1, self.rotation):
            self.piece_y += 1
        self._lock_piece()

    def tick(self):
        if self.game_over:
            return
        self.move(0, 1)

    def get_state(self):
        board = [row.copy() for row in self.grid]
        if self.current_piece and not self.game_over:
            for dx, dy in self._shape(self.current_piece, self.rotation):
                gx = self.piece_x + dx
                gy = self.piece_y + dy
                if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
                    board[gy][gx] = COLORS[self.current_piece]
        return {
            "grid": board,
            "score": self.score,
            "lines": self.lines,
            "level": self.level,
            "gameOver": self.game_over,
            "nextPiece": self.next_piece,
            "width": WIDTH,
            "height": HEIGHT,
        }
