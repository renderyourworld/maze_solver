from tkinter import Tk, BOTH, Canvas
from typing import TYPE_CHECKING, Optional

class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )


class Window:
    def __init__(self, width, height) -> None:
        self.__root = Tk()
        self.__root.title("Maze Sovler")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed...")

    def draw_line(self, line: Line, fill_color: str = "black"):
        line.draw(self.__canvas, fill_color)

    def close(self):
        self.__running = False


class Cell:
    def __init__(self, window: Optional[Window] = None) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = window
    
    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        left_wall_line = Line(Point(x1, y2), Point(x1, y1))
        top_wall_line = Line(Point(x1, y1), Point(x2, y1))
        right_wall_line = Line(Point(x2, y1), Point(x2, y2))
        bottom_wall_line = Line(Point(x2, y2), Point(x1, y2))
        if self.has_left_wall:
            self._win.draw_line(left_wall_line)
        else:
            self._win.draw_line(left_wall_line, "white")
        if self.has_top_wall:
            self._win.draw_line(top_wall_line)
        else:
            self._win.draw_line(top_wall_line, "white")
        if self.has_right_wall:
            self._win.draw_line(right_wall_line)
        else:
            self._win.draw_line(right_wall_line, "white")
        if self.has_bottom_wall:
            self._win.draw_line(bottom_wall_line)
        else:
            self._win.draw_line(bottom_wall_line, "white")

    def draw_move(self, to_cell: 'Cell', undo: bool = False):
        color = "red"
        if undo:
            color = "gray"
        
        # Draw the line from self to to_cell center position
        c1_center = Point((self._x2 + self._x1) / 2, (self._y2 + self._y1) / 2)
        c2_center = Point((to_cell._x2 + to_cell._x1) / 2, (to_cell._y2 + to_cell._y1) / 2)

        self._win.draw_line(Line(c1_center, c2_center), color)