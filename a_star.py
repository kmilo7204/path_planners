# Path planning algorithms implementation
import pygame
import display
import math
import time
from rich import print
from pygame.locals import *

import grid

# Initialization
pygame.init()

class AStar:
    def __init__(self, grid: list):
        # Reference nodes
        self.start = []
        self.end = []

        # Searching grid
        self.grid = grid

        # Open or search list
        self.open_ls = []

    def set_grid(self, grid: list):
        """
        Set the grid for the searching algorithm

        Keyword arguments:
        grid -- the new grid for the searching algorithm
        """

        self.grid = []
        self.grid = grid

    def get_start(self):
        """Return the position of the start node"""

        return self.start

    def get_end(self):
        """Return the position of the end node"""
        return self.end 

    def set_start(self, start: list):
        """
        Set the desired start node

        Keyword arguments:
        start -- the desired start node
        """
        self.start = start

    def set_end(self, end: list):
        """
        Set the desired end node

        Keyword arguments:
        end -- the desired end node
        """
        self.end = end

    def init_open(self):
        """
        Initialize the open list with the initial position or
        start node
        """
        g_cost = 0 
        distance = self.calculate_distance(self.start)
        f_cost = g_cost + distance  

        # Cleaning the open list 
        self.open_ls = []

        # Initial node appending -> [g_cost, f_cost, X , Y]
        self.open_ls.append([g_cost, f_cost, self.start[0], self.start[1]])

    def get_element(self, search_ls: list):
        """Return the second element of the given list (For sorting)"""
        return search_ls[1]

    def calculate_distance(self, cell: list):
        """
        Return the distance between the desired cell to the goal
        
        Keyword arguments:
        cell -- desired cell for ditance calculation
        """
        return abs(cell[0] - self.end[0]) + abs(cell[1] - self.end[1])

    def get_neighbors(self, cell: list):
        """
        Return the neighbor's position of the given cell (In X and Y positions)

        Keyword arguments:
        cell -- desired cell for finding the neighbors
        """
        x = cell[2] 
        y = cell[3] 

        # Create a list of the desire movements
        neighbors_ls = [
            [x, y + 1], # Right
            [x, y - 1],  # Left 
            [x - 1, y], # Up
            [x + 1, y] # Down
        ]
        return neighbors_ls    

    def reconstruct_path(self, path_set: set, current: tuple):
        """
        Reconstructs the path from the end position to the start 

        The incoming set, contains the relation of the current node 
        and the prior one, the key and values are mapped to get the
        corresponding trajectory

        Keyword arguments:
        path_set -- set containing the relation between cells
        current -- value from where searching in the path_set will start 
        """

        path_ls = []
        # Saving the end cell
        path_ls.append([current[0], current[1]])

        while current in path_set:
            """
            As soon as we enter in the set we extract the key of the current node
            (It means we extract the node which expanded the current one) and 
            re-assing this one to keep looking until we reach the start node
            """
            # Get the preceding node of the current one 
            current = path_set[current]
            path_ls.append([current[0], current[1]])

        return path_ls

    def search_astar(self):
        """
        Pseudocode of the A Star search algorithm
            # Initialization
                1. Add the initial node to the open list
                2. Initialize the prior_set (Will store the path)
                3. Initialize the G-Score and the F-Score
            # Loop
                1. Select the node with the lowest F-Score
                2. Remove the current node from the open list (Open set)
                3. For each neighbor of current
                4. Calculate a tentative G-Score 
                5. If tentative G-Score is better than the previous one:
                    Update the new path (As we find and optimal one)
                    Calculae the new G value and the F value
                    5.1 If the node has not been visited:
                        Add it to the open set
        """
        self.init_open()

        close_ls = [[0 for i in range(len(self.grid[0]))] for j in range(len(self.grid))]

        f_score = [[float("inf") for i in range(len(self.grid))] for j in range(len(self.grid[0]))]
        g_score = [[float("inf") for i in range(len(self.grid))] for j in range(len(self.grid[0]))]

        # Set contianing the path
        prior_set = {}

        # List for the visited nodes
        visited_ls = []
        visited_ls.append(self.start)

        # Initial G and F scores considering the heuristics
        g_score[self.start[0]][self.start[1]] = 0
        f_score[self.start[0]][self.start[1]] = g_score[self.start[0]][self.start[1]] + self.calculate_distance(self.start)

        # Updating the visited nodes grid
        close_ls[self.start[0]][self.start[1]] = 1


        while True:
            if (len(self.open_ls) == 0):
                print("[bold red]XXXXX Unable to find path, change conditions XXXXX[/bold red]")

                return [[], []]

            else:
                # Step 1: The node with the lowest F value will be expanded
                self.open_ls.sort(key=self.get_element, reverse=True)
                
                # Step 2: Delete the select node from the open list
                current = self.open_ls.pop() 
                
                # Stop condition for when the goal was found
                if ((current[2] == self.end[0]) and (current[3] == self.end[1])):
                    print("[bold green]===> Path was found at: {}, {} <===[/bold green]".format(current[2], current[3]))

                    # print("Path was found at: {}, {}".format(current[2], current[3]))                    
                    path_ls = self.reconstruct_path(prior_set, (self.end[0], self.end[1]))
                    return [path_ls, visited_ls]

                # Step 3: For each neighbor of the current cell evaluate the conditions 
                neighbors_ls = self.get_neighbors(current)                
                for action in neighbors_ls:
                    # Extract the new cell position 
                    new_x = action[0]
                    new_y = action[1]

                    # Grid dimensions assertion and free obstacle checking
                    if ((new_x >= 0) and (new_x < len(self.grid)) and (new_y >= 0) and (new_y < len(self.grid[0])) and (self.grid[new_x][new_y] == 0)):
                        # Step 4: Calculate a tentative G-Score (Cost of the motion)
                        prov_g = current[0] + 1

                        visited_ls.append([new_x, new_y])
                        # Step 5: If tentative G-Score is better than the previous one
                        if (prov_g < g_score[new_x][new_y]):
                            # Update the corresponding set and lists
                            prior_set[(new_x, new_y)] = (current[2], current[3])
                            g_score[new_x][new_y] = prov_g
                            f_score[new_x][new_y] = g_score[new_x][new_y] + self.calculate_distance([new_x, new_y]) 

                            # If the node or cell has not been visited, then add it to the open list
                            if (close_ls[new_x][new_y] == 0):
                                self.open_ls.append([g_score[new_x][new_y], f_score[new_x][new_y], new_x, new_y])
                                close_ls[new_x][new_y] = 1

def main():
    # Main loop
    grid_game = grid.Grid(800, 800, 10)
    planner = AStar(grid_game.get_grid())

    redraw = False
    running = True
    action = 0
    while running:
        # Check for events in the game
        for event in pygame.event.get():
            # Quit event just happened
            if event.type == QUIT:
                running = False

            # Mouse event
            if event.type == MOUSEBUTTONDOWN:
                # Left click
                if (pygame.mouse.get_pressed()[0]):
                    position = pygame.mouse.get_pos()
                    if (action == 0):
                        # Set and draw the initial position
                        action = 1
                        start_cell = grid_game.get_cell(position)
                        grid_game.draw_start(start_cell)

                        # Planner start position
                        planner.set_start(start_cell)

                    elif (action == 1):
                        # Set and draw the final position
                        action = 2
                        end_cell = grid_game.get_cell(position)
                        grid_game.draw_end(end_cell)

                        # Planner end position
                        planner.set_end(end_cell)

                    elif (action == 2):
                        # Draw an obstacle
                        grid_game.set_obstacle(position)
                        planner.set_grid(grid_game.get_grid())

                # Right click
                elif (pygame.mouse.get_pressed()[2]):
                    grid_game.restart_grid()
                    action = 0
                    redraw = False

            # Keys interaction
            if event.type == KEYDOWN:
                if event.key == K_h:
                    help_msg = {
                        "1st Left click: Set the start position",
                        "2nd Left click: Set the final position",
                        "From 3rd Left click: Draw obstacles",
                        "Spacebar: Start the searching algorithm"
                    }

                    print("[blue]{}[/blue]".format(help_msg))
                   
                elif event.key == K_SPACE and action == 2:
                    # We we try to draw with different obstacles
                    if (planner.get_start() and planner.get_end() and redraw):
                        grid_game.clean_path()
                        grid_game.draw_obstacles()
                        # Drawing start and end location
                        grid_game.draw_start(grid_game.get_start())
                        grid_game.draw_end(grid_game.get_end())
                    
                    planner.set_grid(grid_game.get_grid())
                    # Space will start the searching algorithm
                    print("[bold yellow]||===========================||[/bold yellow]")
                    print("[bold yellow]|| Starting search algorithm ||[/bold yellow]")
                    print("[bold yellow]||===========================||[/bold yellow]")

                    path_ls, explored_ls = planner.search_astar()

                    # We will try to reuse the grid_game to draw once again the path
                    grid_game.draw_path(path_ls, explored_ls)
                    redraw = True

if __name__ == "__main__":
    main()

