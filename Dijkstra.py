import pygame
import math
import random
from collections import deque
import heapq                        # to represent Priority Queue

WIDTH = 896
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Dijkstra's Planner")

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
obstacle_cells = 0  
iterations = 0

queue = []
visited = []
action = [[-1 for col in range(128)] for row in range(128)]
cost_list = [[float('inf') for col in range(128)] for row in range(128)]
final_path = []

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

    def is_end(self):
        return self.color == TURQUOISE

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

def Dijkstra(draw, grid):
    cost_list[grid[0][0].get_pos()[0]][grid[0][0].get_pos()[1]] = 0
    heapq.heappush(queue, (cost_list[grid[0][0].get_pos()[0]][grid[0][0].get_pos()[1]], grid[0][0].get_pos()))  # This will append the element according to its priority. Which in our case is the cost to reachto that element.
    visited.append(grid[0][0].get_pos())
    
    found = False
    resign = False

    movement = [[0, -1],    # UP
                [-1,-1],    # UP LEFT
                [-1, 0],    # LEFT
                [-1, 1],    # DOWN LEFT
                [0, 1],     # DOWN
                [1, 1],     # DOWN RIGHT
                [1, 0]]     # RIGHT
    
    while found == False and resign == False:
        global iterations
        if len(queue) == 0:
            resign = True
            print("No possible path !!!")
        
        else:
            next = heapq.heappop(queue)
            g = next[0]
            x = next[1][0]
            y = next[1][1]
            grid[x][y].make_closed()
            iterations += 1
            #draw()

            if x == 127 and y == 127:
                found = True
                print("Robot reached the destinantion in {} iterations and the cost to reach the destination is {}.".format(iterations,cost_list[x][y]))
                break
            
            else:
                for i in range(len(movement)):
                    x2 = x + movement[i][0]
                    y2 = y + movement[i][1]
                    if x2 >= 0 and x2 < 128 and y2 >= 0 and y2 < 128:
                        if grid[x2][y2].is_barrier() == False:
                            cost_to_move = math.sqrt((x2-x)**2 +(y2-y)**2)      # we will measure the cost to travel between two neighbour grid by its distance.
                            if(cost_list[grid[x][y].get_pos()[0]][grid[x][y].get_pos()[1]] + cost_to_move < cost_list[grid[x2][y2].get_pos()[0]][grid[x2][y2].get_pos()[1]]): # if the new cost will be less than the previous cost, we will update the cost
                                cost_list[grid[x2][y2].get_pos()[0]][grid[x2][y2].get_pos()[1]] = cost_list[grid[x][y].get_pos()[0]][grid[x][y].get_pos()[1]] + cost_to_move
                                heapq.heappush(queue, (cost_list[grid[x2][y2].get_pos()[0]][grid[x2][y2].get_pos()[1]], grid[x2][y2].get_pos()))
                                action[x2][y2] = i
    
               
    if resign == False:            
        x_ = 127    
        y_ = 127
        final_path.append(grid[x_][y_].get_pos())
        while x_ != 0 or y_ != 0:
            x2_ = x_ - movement[action[x_][y_]][0]
            y2_ = y_ - movement[action[x_][y_]][1] 
            final_path.append(grid[x2_][y2_].get_pos())
            x_ = x2_
            y_ = y2_

        final_path.reverse()
        for n in final_path:
            grid[n[0]][n[1]].make_path()


def tetrominoes_obstacle_1(grid, i,j):
    grid[i][j].make_barrier()
    grid[i][j+1].make_barrier()
    grid[i][j+2].make_barrier()
    grid[i][j+3].make_barrier()

def tetrominoes_obstacle_2(grid, i,j):
    grid[i][j].make_barrier()
    grid[i+1][j].make_barrier()
    grid[i+1][j+1].make_barrier()
    grid[i+1][j+2].make_barrier()

def tetrominoes_obstacle_3(grid, i,j):
    grid[i][j].make_barrier()
    grid[i][j+1].make_barrier()
    grid[i+1][j+1].make_barrier()
    grid[i+1][j+2].make_barrier()

def main(win, width):
    ROWS = 128
    grid = make_grid(ROWS,width)
    grid[0][0].make_start()
    grid[127][127].make_end()
    start = (0,0)
    end = (127, 127)

    percentage_to_be_filled = 25
    global obstacle_cells
    while obstacle_cells < total_cells*percentage_to_be_filled/100:
        x = random.randint(0,124)
        y = random.randint(0,124)
        obstacle = random.randint(1,3)

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
            if event.type == pygame.QUIT:
                run = False

        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("started")
                    Dijkstra(lambda: draw(win, grid, ROWS, width), grid)

    pygame.quit()

main(WIN, WIDTH)