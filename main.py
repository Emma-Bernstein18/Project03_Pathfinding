import pygame
import sys
import time
import random

pygame.init()

#set up settings for graph
WIDTH = 800
HEIGHT = 800
ROWS = 20
COLS = 20
CELL_SIZE = WIDTH // COLS
INFO_PANEL_HEIGHT = 100  #space at top for instructions/stats

WIN = pygame.display.set_mode((WIDTH, HEIGHT + INFO_PANEL_HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization")

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 191, 255)
DARK_BLUE = (0, 0, 139)
GRAY = (220, 220, 220)

#Font
FONT = pygame.font.SysFont("Arial", 20)

#Cell class
class Cell:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size + INFO_PANEL_HEIGHT  # shift down for panel
        self.size = size

        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.is_path = False
        self.is_open = False
        self.is_closed = False
        self.neighbors = []

    def draw(self, win):
        if self.is_start:
            color = GREEN
        elif self.is_end:
            color = RED
        elif self.is_path:
            color = PURPLE
        elif self.is_closed:
            color = DARK_BLUE
        elif self.is_open:
            color = BLUE
        elif self.is_wall:
            color = BLACK
        else:
            color = WHITE

        pygame.draw.rect(win, color, (self.x, self.y, self.size, self.size))

    def update_neighbors(self, grid, allow_diagonals: bool):
        self.neighbors = []
        rows = len(grid)
        cols = len(grid[0])

        # Straight moves
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall:
            self.neighbors.append((grid[self.row - 1][self.col], 1))
        if self.row < rows - 1 and not grid[self.row + 1][self.col].is_wall:
            self.neighbors.append((grid[self.row + 1][self.col], 1))
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall:
            self.neighbors.append((grid[self.row][self.col - 1], 1))
        if self.col < cols - 1 and not grid[self.row][self.col + 1].is_wall:
            self.neighbors.append((grid[self.row][self.col + 1], 1))

        # Diagonal moves
        if allow_diagonals:
            diag_cost = 1.41421
            if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_wall:
                self.neighbors.append((grid[self.row - 1][self.col - 1], diag_cost))
            if self.row > 0 and self.col < cols - 1 and not grid[self.row - 1][self.col + 1].is_wall:
                self.neighbors.append((grid[self.row - 1][self.col + 1], diag_cost))
            if self.row < rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_wall:
                self.neighbors.append((grid[self.row + 1][self.col - 1], diag_cost))
            if self.row < rows - 1 and self.col < cols - 1 and not grid[self.row + 1][self.col + 1].is_wall:
                self.neighbors.append((grid[self.row + 1][self.col + 1], diag_cost))


#Grid functions
def make_grid(rows, cols, cell_size):
    return [[Cell(r, c, cell_size) for c in range(cols)] for r in range(rows)]


def draw_grid(win, rows, cols, cell_size):
    for x in range(0, WIDTH, cell_size):
        pygame.draw.line(win, BLACK, (x, INFO_PANEL_HEIGHT), (x, HEIGHT + INFO_PANEL_HEIGHT))
    for y in range(INFO_PANEL_HEIGHT, HEIGHT + INFO_PANEL_HEIGHT, cell_size):
        pygame.draw.line(win, BLACK, (0, y), (WIDTH, y))


def redraw(win, grid, mode, heuristic_name, nodes_explored=0, path_length=0, elapsed_time=0.0):
    win.fill(WHITE)
    #draw_info_panel(win, mode, heuristic_name, nodes_explored, path_length, elapsed_time)
    for row in grid:
        for cell in row:
            cell.draw(win)
    draw_grid(win, ROWS, COLS, CELL_SIZE)
    pygame.display.update()


#heuristics
def manhattan(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)


def euclidean(a, b):
    return ((a.row - b.row) ** 2 + (a.col - b.col) ** 2) ** 0.5


def octile(a, b):
    dx = abs(a.row - b.row)
    dy = abs(a.col - b.col)
    return max(dx, dy) + (1.41421 - 1) * min(dx, dy)


#path recognition
def retrace_path(came_from, current, grid, win, mode, heuristic_name):
    while current in came_from:
        current = came_from[current]
        if not current.is_start and not current.is_end:
            current.is_path = True
        redraw(win, grid, mode, heuristic_name)
        pygame.time.delay(20)


#A* algorithm
def a_star(start, end, grid, win, heuristic_function, heuristic_name, mode):
    open_set = [start]
    came_from = {}

    # Reset states
    for row in grid:
        for cell in row:
            cell.is_open = False
            cell.is_closed = False
            cell.is_path = False

    start.is_open = True

    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0.0

    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = heuristic_function(start, end)

    nodes_explored = 0
    start_time = time.time()
    path_length = 0

    while open_set:
        current = min(open_set, key=lambda cell: f_score[cell])

        if current == end:
            total_time = time.time() - start_time
            temp = end
            path = []
            while temp in came_from:
                path.append(temp)
                temp = came_from[temp]
            path_length = len(path)

            print("----- A* Results -----")
            print(f"Heuristic: {heuristic_name}")
            print(f"Nodes explored: {nodes_explored}")
            print(f"Path length: {path_length}")
            print(f"Time taken: {total_time:.4f} seconds")
            print("----------------------")

            retrace_path(came_from, end, grid, win, mode, heuristic_name)
            return True

        open_set.remove(current)
        current.is_open = False
        current.is_closed = True
        nodes_explored += 1

        for neighbor, move_cost in current.neighbors:
            temp_g = g_score[current] + move_cost
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + heuristic_function(neighbor, end)
                if neighbor not in open_set:
                    open_set.append(neighbor)
                    neighbor.is_open = True

        redraw(win, grid, mode, heuristic_name, nodes_explored, path_length, time.time() - start_time)
        pygame.time.delay(20)

    print("No path found.")
    return False


#Generate a randome maze for it to find the optimal path between
def generate_random_maze(grid, start_cell, end_cell, density=0.3):
    for row in grid:
        for cell in row:
            if not (cell == start_cell or cell == end_cell):
                cell.is_wall = random.random() < density


#Main loop
def main():
    clock = pygame.time.Clock()
    grid = make_grid(ROWS, COLS, CELL_SIZE)

    mode = "wall"  # "start", "end", "wall"
    start_cell = None
    end_cell = None

    current_heuristic = manhattan
    heuristic_name = "Manhattan"
    allow_diagonals = False

    nodes_explored = 0
    path_length = 0
    elapsed_time = 0.0

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            #keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    mode = "start"
                    print("Mode: Place START")
                elif event.key == pygame.K_e:
                    mode = "end"
                    print("Mode: Place END")
                elif event.key == pygame.K_w:
                    mode = "wall"
                    print("Mode: Place WALLS")
                elif event.key == pygame.K_1:
                    current_heuristic = manhattan
                    heuristic_name = "Manhattan"
                    allow_diagonals = False
                    print("Heuristic selected: Manhattan (4-direction movement)")
                elif event.key == pygame.K_2:
                    current_heuristic = euclidean
                    heuristic_name = "Euclidean"
                    allow_diagonals = True
                    print("Heuristic selected: Euclidean (8-direction movement)")
                elif event.key == pygame.K_3:
                    current_heuristic = octile
                    heuristic_name = "Octile"
                    allow_diagonals = True
                    print("Heuristic selected: Octile (8-direction movement)")
                elif event.key == pygame.K_SPACE:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid, allow_diagonals)
                    if start_cell and end_cell:
                        a_star(start_cell, end_cell, grid, WIN, current_heuristic, heuristic_name, mode)
                elif event.key == pygame.K_c:
                    for row in grid:
                        for cell in row:
                            cell.is_wall = False
                            cell.is_open = False
                            cell.is_closed = False
                            cell.is_path = False
                    print("Grid cleared (walls removed).")
                elif event.key == pygame.K_r:
                    start_cell = None
                    end_cell = None
                    for row in grid:
                        for cell in row:
                            cell.is_wall = False
                            cell.is_start = False
                            cell.is_end = False
                            cell.is_open = False
                            cell.is_closed = False
                            cell.is_path = False
                    print("Full reset complete.")
                elif event.key == pygame.K_m:
                    if start_cell and end_cell:
                        generate_random_maze(grid, start_cell, end_cell)
                        print("Random maze generated.")

            #clicking on the keyboard
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = (y - INFO_PANEL_HEIGHT) // CELL_SIZE
                col = x // CELL_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS:
                    cell = grid[row][col]
                    if mode == "start":
                        if start_cell:
                            start_cell.is_start = False
                        cell.is_wall = False
                        cell.is_start = True
                        start_cell = cell
                    elif mode == "end":
                        if end_cell:
                            end_cell.is_end = False
                        cell.is_wall = False
                        cell.is_end = True
                        end_cell = cell
                    elif mode == "wall":
                        if not cell.is_start and not cell.is_end:
                            cell.is_wall = not cell.is_wall

        redraw(WIN, grid, mode, heuristic_name, nodes_explored, path_length, elapsed_time)


if __name__ == "__main__":
    main()
