import display
import time

import pygame
from pygame.locals import *

class Grid:
    def __init__(self, width, height, cells):
        # Note, I can set the number of cells depending on the dimensions
        self.width = width
        self.height = height
        self.cells = cells
        self.resolution = width // cells

        self.start = []
        self.end = []

        # Creating rows
        self.grid = [[0 for i in range(self.cells)] for j in range(self.cells)]

        # Display object
        self.game_display = display.Display(width, height)

        # Drawing grid lines
        self.draw_divisions()

    """Form a complex number.

    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)
    """
    def get_grid(self):
        """Return the console's grid"""

        return self.grid

    def draw_divisions(self):
        """Draw the grid lines on the screen"""

        for i in range(self.cells):
            pygame.draw.line(self.game_display.screen, display.GRAY, (0, i * self.resolution), (self.width, i * self.resolution))
            pygame.draw.line(self.game_display.screen, display.GRAY, (i * self.resolution, 0), (i * self.resolution, self.height))

        self.game_display.update_display()

    def get_cell(self, position: tuple):
        """
        Return the corresponding cell for the screen click
        
        Keyword arguments:
        position -- screen pixel
        """

        cell_x = position[0] // self.resolution
        cell_y = position[1] // self.resolution
        return (cell_x, cell_y)

    def get_start(self):
        """Return the start cell of the grid"""
        return self.start

    def get_end(self):
        """Return the end cell of the grid"""
        return self.end

    def draw_rectangle(self, cell: tuple, color: tuple):
        """
        Draw and colour the given cell with the given color
        
        Keyword arguments:
        cell -- the cell to be drawn
        color -- the desired color
        """

        self.game_display.draw_box(color, cell, self.resolution)
        self.game_display.update_display()

    def set_obstacle(self, position: tuple):
        """
        Draw and colour the given cell as an obstacle, this function
        updates the grid inmediately
        
        Keyword arguments:
        position -- screen pixel
        """

        cell = self.get_cell(position)
        
        # Empty
        if (self.grid[cell[0]][cell[1]] == 0):
            self.grid[cell[0]][cell[1]] = 1
            self.draw_rectangle(cell, display.GRAY)

        # Obstacle
        else:
            self.grid[cell[0]][cell[1]] = 0
            self.draw_rectangle(cell, display.BLACK)
    
    def draw_obstacles(self):
        """
        Draw the desired obstacles, this is mainly used when
        the redrawn function is called
        """
        for i in range(len(self.grid[0])):
            for j in range(len(self.grid)):
                if (self.grid[i][j] == 0):
                    self.draw_rectangle((i, j), display.BLACK)

                else:
                    self.draw_rectangle((i, j), display.GRAY)

    
    def draw_start(self, cell: tuple):
        """
        Draw and colour the start cell with honey colour
        
        Keyword arguments:
        cell -- the cell to be drawn
        """
        self.start = [cell[0], cell[1]]
        self.draw_rectangle(cell, display.HONEY)

    def draw_end(self, cell: tuple):
        """
        Draw and colour the end cell with blue colour
        
        Keyword arguments:
        cell -- the cell to be drawn
        """
        self.end = [cell[0], cell[1]]
        self.draw_rectangle(cell, display.MAJ_BLUE)

    def draw_path(self, path_ls: list, explored_ls: list):
        """
        Draw the path from the end to the goal
        
        Keyword arguments:
        path_ls -- the list with the desired path
        explored_ls -- the list with the explored cells
        """
        for cell in explored_ls:
            if ((cell[0] == self.start[0]) and (cell[1] == self.start[1]) or (cell[0] == self.end[0]) and (cell[1] == self.end[1])):
                continue
            org_cell = [cell[0], cell[1]]
            self.draw_rectangle(org_cell, display.PAC_BLUE)
            time.sleep(0.02)

        # self.draw_start(self.get_start())
        # self.draw_end(self.get_end())

        print(self.start, self.end)
        for cell in path_ls:
            if ((cell[0] == self.end[0]) and (cell[1] == self.end[1]) or (cell[0] == self.start[0]) and (cell[1] == self.start[1])):
                continue

            org_cell = [cell[0], cell[1]]
            self.draw_rectangle(org_cell, display.GREEN)
            time.sleep(0.07)


    def clean_path(self):
        """Clean the grid and prepare it to be used"""
        # Black screen drawing
        self.game_display.screen.fill(display.BLACK)
        # Drawing grid lines
        self.draw_divisions()


    def restart_grid(self):
        """Clean and restart the grid to start a new searching"""
        # Restarting grid and desired nodes
        self.grid = []
        self.grid = [[0 for i in range(self.cells)] for j in range(self.cells)]
        self.start = []
        self.end = []

        # Clean the grid
        self.clean_path()
