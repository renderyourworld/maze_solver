import random
import time
from graphics import Window, Cell
from typing import Optional


class Maze:
    def __init__(
            self,
            x1: int,
            y1: int,
            num_rows: int,
            num_cols: int,
            cell_size_x: int,
            cell_size_y: int,
            win: Optional[Window] = None,
            seed: Optional[int] = None
                 ) -> None:
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed :
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break__walls_r(0, 0)
        self._reset_cells_visited()


    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j) 

    def _draw_cell(self, i: int, j: int):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        # time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)
    
    def _break__walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []

            # Determine which cells to visit next
            # up
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append((i, j-1))
            
            # down
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                to_visit.append((i, j+1))
            
            # left
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1, j))
            
            # right
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                to_visit.append((i+1, j))
            
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            # Pick a direction at random
            direction_index = random.randrange(len(to_visit))
            next_cell = to_visit[direction_index]

            # Knockdown walls between this cell and the next cells
            # up
            if next_cell[1] == j-1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False
            # down
            if next_cell[1] == j+1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False
            # left
            if next_cell[0] == i-1:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False
            # right
            if next_cell[0] == i+1:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False
            
            # Visit the next cell
            self._break__walls_r(next_cell[0], next_cell[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True

        # If we are at the end cell then we are done
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        # Determine which cells to visit next
        # up
        if j > 0 and not self._cells[i][j-1].has_bottom_wall and not self._cells[i][j-1].visited:
            # Can go up
            current_cell.draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                current_cell.draw_move(self._cells[i][j-1], undo=True)
        # down
        if j < self._num_rows - 1 and not self._cells[i][j+1].has_top_wall and not self._cells[i][j+1].visited:
            # Can go down
            current_cell.draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                current_cell.draw_move(self._cells[i][j+1], undo=True)
        # left
        if i > 0 and not self._cells[i-1][j].has_right_wall and not self._cells[i-1][j].visited:
            # Can go left
            current_cell.draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            else:
                current_cell.draw_move(self._cells[i-1][j], undo=True)
        # right
        if i < self._num_cols - 1 and not self._cells[i+1][j].has_left_wall and not self._cells[i+1][j].visited:
            # Can go right
            current_cell.draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                current_cell.draw_move(self._cells[i+1][j], undo=True)

        return False

                