import pygame, sys
from pygame.locals import *
from random import randint

### Sets size of grid
WINDOWWIDTH = 500
WINDOWHEIGHT = 400
CELLSIZE = 20

# Check to see if the width and height are multiples of the cell size.
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"

# Determine number of cells in horizonatl and vertical plane
CELLWIDTH = WINDOWWIDTH // CELLSIZE # number of cells wide
CELLHEIGHT = WINDOWHEIGHT // CELLSIZE # Number of cells high

# set up the colours
COLORS = {0: (255, 255, 255), 1: (234, 0, 7), 2: (45, 198, 45), 3: (255, 204, 0), 4: (0, 0, 255)}

BLACK = (0,  0,  0)
WHITE = (255, 255, 255)
DARKGRAY = (245, 245, 245)
score = 0

def init_box():
    return [[randint(1, 4) for y in range(CELLHEIGHT)] for x in range(CELLWIDTH)]

def draw_box(box):
    for x in range(CELLWIDTH):
        for y in range(CELLHEIGHT):
            yy = (CELLHEIGHT - y - 1) * CELLSIZE  # translates array into grid size
            xx = x * CELLSIZE  # translates array into grid size
            pygame.draw.rect(DISPLAYSURF, COLORS[box[x][y]], (xx, yy, CELLSIZE-1, CELLSIZE-1))
    return None

def remove(pos, box):
    global score
    x = pos[0] // CELLSIZE
    y = CELLHEIGHT - pos[1] // CELLSIZE - 1
    c = box[x][y]
    if c == 0:
        return score
    cells = [(x, y)]
    count = 0
    minx = maxx = x
    while len(cells) > 0:
        cur = cells.pop()
        count += 1
        box[cur[0]][cur[1]] = 0
        minx = min(minx, cur[0])
        maxx = max(maxx, cur[0])
        if cur[0] > 0 and box[cur[0] - 1][cur[1]] == c:
            cells.append((cur[0] - 1, cur[1]))
        if cur[1] > 0 and box[cur[0]][cur[1] - 1] == c:
            cells.append((cur[0], cur[1] - 1))
        if cur[0] < CELLWIDTH - 1 and box[cur[0] + 1][cur[1]] == c:
            cells.append((cur[0] + 1, cur[1]))
        if cur[1] < CELLHEIGHT - 1 and box[cur[0]][cur[1] + 1] == c:
            cells.append((cur[0], cur[1] + 1))
    for x in range(minx, maxx+1):
        col = []
        for y in range(CELLHEIGHT):
            c = box[x][y]
            if c > 0:
                col.append(c)
        while len(col) < CELLHEIGHT:
            col.append(0)
        box[x] = col
    for xx in range(CELLWIDTH - 1, -1, -1):
        if box[xx][0] == 0:
            col = box[xx]
            box.pop(xx)
            box.append(col)
    score += count * (count + 1) // 2
    return score

# main function
def main():
    pygame.init()
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # размер окна
    pygame.display.set_caption('Color Blocks') # заголовок окна

    DISPLAYSURF.fill(WHITE)  # fills the screen white

    # Fonts
    Font = pygame.font.SysFont("Trebuchet MS", 25)

    box = init_box()
    draw_box(box)
    pygame.display.update()

    while True: #main game loop
        for event in pygame.event.get(): # Обрабатываем события
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                remove(pygame.mouse.get_pos(), box)
                draw_box(box)
                if box[0][0] == 0:
                    label = Font.render(str(score), 1, BLACK)
                    DISPLAYSURF.blit(label, (100, 100))

        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__=='__main__':
    main()