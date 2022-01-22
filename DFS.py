import pygame
import math
import random
from collections import deque

WIDTH = 896
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Depth First Search Planner")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

total_cells = 16384                                     # 128*128
obstacle_cells = 0                                      # as we are creating random obstacles for specified density we need to keep track.
iterations = 0                                          # to keep track the no. of iterations

queue = deque()                                          # to store the neighbouring grids that can be visited.
visited = []                                              # to keep the track of visited grids.
action = [[-1 for col in range(128)] for row in range(128)] # to trace back the path from end to start.
final_path = []                                                 # to store the final path.


# To built pygame environment.
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row 
        self.col = col 
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE

    def make_closed(self):
        self.color = RED
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color =ORANGE
    
    def make_end(self):
        self.color = TURQUOISE 

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x , self.y, self.width, self.width))

    def __lt__(self, other):
        return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    
    return grid

def draw_grid(win, row, width):
    gap = width / row
    for i in range(row):
        pygame.draw.line(win, GREY, (0 , i*gap), (width, i*gap))
        for j in range(row):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

def DFS(draw, grid):
    queue.append(grid[0][0].get_pos())                    # adding starting position of the robot to the queue
    visited.append(grid[0][0].get_pos())                  # adding starting position of the robot as visited.
    found = False                                         # variable to know if the path is found
    resign = False                                        # variable to know if there is no path between start and end.
    
    movement = [[0, -1],    # UP                           MOVEMENTS (Can be 4 Connectivity or 8 conectivity)
                [-1,-1],    # UP LEFT                      I have considered 8 connectivity in this case.
                [-1, 0],    # LEFT
                [-1, 1],    # DOWN LEFT
                [0, 1],     # DOWN
                [1, 1],     # DOWN RIGHT
                [1, 0]]     # RIGHT
    
    while found == False and resign == False:
        global iterations
        if len(queue) == 0:                                 # length of the queue will be 0 only if there is no path from start to end.
            resign = True
            print("No possible path !!!")
        
        else:
            next = queue.pop()                              # As this is DFS, it works as Lat In First Out(FIFO). so we will be removing last element of the queue.
            x = next[0]
            y = next[1]
            grid[x][y].make_closed()
            iterations += 1
            #draw()
    
            if x == 127 and y == 127:                       # if our search reaches at x=127 and y=127, we have reached our goal location. As the problem statement has given fixed goal I have hardcoded it. It can be changed as per user requirement.
                found = True
                print("Robot reached the destinantion in {} iterations.".format(iterations))
            
            else:
                for i in range(len(movement)):               # This loop will check all the neighbour of current grid
                    x2 = x + movement[i][0]
                    y2 = y + movement[i][1]
                    if x2 >= 0 and x2 < 128 and y2 >= 0 and y2 < 128:       # check if the new grid position lies within the boundary
                        if grid[x2][y2].is_barrier() == False and grid[x2][y2].get_pos() not in visited:  # check if its not an obstacle and is not visited before.
                            queue.append(grid[x2][y2].get_pos())                # append to the queue so we will be looking at that grid.
                            visited.append(grid[x2][y2].get_pos())              # we will ne adding that to visited. so we will not look at that grid even if it will be neighbour of other grid as we have already added it in our queue.
                            action[x2][y2] = i
                            
                            
                
    if resign == False:                          # If there is a path.
        x_ = 127    
        y_ = 127
        final_path.append(grid[x_][y_].get_pos())           # last grid of the path appended.
        while x_ != 0 or y_ != 0:                            # while we dont reach till starting grid. This loop will run.
            x2_ = x_ - movement[action[x_][y_]][0]          # Back tracing the path.
            y2_ = y_ - movement[action[x_][y_]][1] 
            final_path.append(grid[x2_][y2_].get_pos())
            x_ = x2_
            y_ = y2_

        final_path.reverse()                        # The path in the final_path will be from end to start to we will reverse it.
        for n in final_path:
            grid[n[0]][n[1]].make_path()            # We will color the path will purple.

def tetrominoes_obstacle_1(grid, i,j):              # Obstacle type 1
    grid[i][j].make_barrier()
    grid[i][j+1].make_barrier()
    grid[i][j+2].make_barrier()
    grid[i][j+3].make_barrier()

def tetrominoes_obstacle_2(grid, i,j):              # Obstacle type 2
    grid[i][j].make_barrier()
    grid[i+1][j].make_barrier()
    grid[i+1][j+1].make_barrier()
    grid[i+1][j+2].make_barrier()

def tetrominoes_obstacle_3(grid, i,j):              # Obstacle type 3
    grid[i][j].make_barrier()   
    grid[i][j+1].make_barrier()
    grid[i+1][j+1].make_barrier()
    grid[i+1][j+2].make_barrier()

def main(win, width):   
    ROWS = 128                                      # no. of rows
    grid = make_grid(ROWS,width)                     # This will make the gris using pygame library.
    grid[0][0].make_start()                         # Coloring the first grid as orange
    grid[127][127].make_end()                        # Coloring the last gris with turqouise
    start = (0,0)
    end = (127, 127)

    percentage_to_be_filled = 25                     # percentage of the total grids that needs to be filled with obstcale.
    global obstacle_cells
    while obstacle_cells < total_cells*percentage_to_be_filled/100:         # The loop will fill the obstacles till this condition is satisfied.
        x = random.randint(0,124)                                           # We will choose random x and y values of the gris to place the obstacle
        y = random.randint(0,124)
        obstacle = random.randint(1,3)                                      # This will randomly choose the obstacle.

        if obstacle == 1:
            if grid[x][y].is_barrier != True and grid[x][y].is_start != True :
                if grid[x+1][y].is_barrier != True and grid[x+2][y].is_barrier != True and grid[x+3][y].is_barrier != True:
                    tetrominoes_obstacle_1(grid, x,y)
                    obstacle_cells += 4                                             # Considering an obstacle occupies 4 cells. (Understanding from figure in assignment)

        elif obstacle == 2:
            if grid[x][y].is_barrier != True and grid[x][y].is_start != True:
                if grid[x][y+1].is_barrier != True and grid[x+1][y+1].is_barrier != True and grid[x+1][y+2].is_barrier != True:
                    tetrominoes_obstacle_2(grid, x,y)
                    obstacle_cells += 4

        elif obstacle == 3:
            if grid[x][y].is_barrier != True and grid[x][y].is_start != True:
                if grid[x+1][y].is_barrier != True and grid[x+1][y+1].is_barrier != True and grid[x+2][y+1].is_barrier != True:
                    tetrominoes_obstacle_3(grid, x,y)
                    obstacle_cells += 4

    run = True 
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:               # to close the pygame terminal if we press close on the right top.
                run = False

        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:         # press space bar to start the search.
                    print("started")
                    DFS(lambda: draw(win, grid, ROWS, width), grid)

    pygame.quit()

main(WIN, WIDTH)