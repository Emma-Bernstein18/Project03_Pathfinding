A* Pathfinding Visualization

Overview:
- This project is an interactive visualization of the A* pathfinding algorithm built using Python and Pygame.

- The goal of the project is to show how A* explores a grid while searching for the shortest path, and how different heuristics change the algorithm’s performance.
Users can place a start point, an end point, draw walls, choose between three heuristics, and watch the algorithm run in real time with color-coded states.

This project helped me understand:
- How A* works
- The role of heuristics and why admissibility matters
- How diagonal movement affects path cost
- How to build a visual algorithm demo using Pygame

How to run:

Requirements:
- Python 3.x
- pygame

Installation
- pip install pygame
Run the program
- python main.py

Controls:

- S	Place Start point (green)
- E	Place End point (red)
- W	Draw/erase walls (black)
- 1	Manhattan heuristic (4-direction movement)
- 2	Euclidean heuristic (8-direction movement)
- 3	Octile heuristic (8-direction movement)
- SPACE	Run the A* algorithm
- C	Clear walls & visualization (keeps start/end)
- R	Full reset (removes everything)
- M	Generate random maze (optional if implemented)

Heuristics:

Manhattan Distance:
- Formula: dx + dy
- Only considers up, down, left, right moves
- Used when diagonal movement is disabled
- Very fast but not accurate when diagonals are possible

Euclidean Distance:
- Formula: √(dx² + dy²)
- Straight-line “as the crow flies” distance
- Works when diagonal movement is allowed
- Slightly less accurate, needs to explore more nodes because of straight-line distance.

Octile Distance:
- Formula: max(dx, dy) + (√2 − 1) × min(dx, dy)
- Designed for 8-direction grids
- Accounts for diagonal cost = √2
- Most accurate/tight for this project
- Usually explores the fewest nodes
