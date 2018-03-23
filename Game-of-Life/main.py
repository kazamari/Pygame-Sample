import pygame, sys
from pygame.locals import *
from random import randint

# Number of frames per second
FPS = 5

### Sets size of grid
WINDOWWIDTH = 300
WINDOWHEIGHT = 200
CELLSIZE = 10

# Check to see if the width and height are multiples of the cell size.
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"

# Determine number of cells in horizonatl and vertical plane
CELLWIDTH = WINDOWWIDTH // CELLSIZE # number of cells wide
CELLHEIGHT = WINDOWHEIGHT // CELLSIZE # Number of cells high

# set up the colours
BLACK = (0,  0,  0)
WHITE = (255, 255, 255)
DARKGRAY = (245, 245, 245)

# Draws the grid lines
def draw_grid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

# Colours the cells green for life and white for no life
def colourGrid(lifeDict):
    for item in lifeDict:
        y = item[1] * CELLSIZE  # translates array into grid size
        x = item[0] * CELLSIZE  # translates array into grid size
        pygame.draw.rect(DISPLAYSURF, WHITE if lifeDict[item] == 0 else BLACK, (x, y, CELLSIZE, CELLSIZE))
    return None

# Creates an dictionary of all the cells
# Sets all cells as dead (0)
def blankGrid():
    gridDict = {}
    # creates dictionary for all cells
    for y in range(CELLHEIGHT):
        for x in range(CELLWIDTH):
            gridDict[x,y] = 0
    return gridDict

# Assigns a 0 or a 1 to all cells
def startingGridRandom(lifeDict):
    for item in lifeDict:
        lifeDict[item] = randint(0,1)
    return lifeDict

# determines the next generation by running a 'tick'
def tick(lifeDict):
    # Determines how many alive neighbours there are around each cell
    def getNeighbours(item, lifeDict):
        neighbours = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if not (x == 0 and y == 0):
                    neighbours += bool(lifeDict[((item[0] + x) % CELLWIDTH, (item[1] + y) % CELLHEIGHT)])
        return neighbours

    newTick = {}
    for item in lifeDict:
        # get number of neighbours for that item
        numberNeighbours = getNeighbours(item, lifeDict)
        newTick[item] = bool((lifeDict[item] == 0 and numberNeighbours == 3) or (lifeDict[item] == 1 and numberNeighbours in [2, 3]))
    return newTick

# main function
def main():
    pygame.init()
    global DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # размер окна
    pygame.display.set_caption('Game of Life') # заголовок окна

    DISPLAYSURF.fill(WHITE)  # fills the screen white

    lifeDict = blankGrid()  # creates library and populates to match blank grid
    lifeDict = startingGridRandom(lifeDict)  # Assign random life

    # Colours the live cells, blanks the dead
    colourGrid(lifeDict)

    draw_grid()
    pygame.display.update()

    while True: #main game loop
        for event in pygame.event.get(): # Обрабатываем события
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # runs a tick
        lifeDict = tick(lifeDict)

        # Colours the live cells, blanks the dead
        colourGrid(lifeDict)

        draw_grid()
        pygame.display.update() # обновление и вывод всех изменений на экран
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
