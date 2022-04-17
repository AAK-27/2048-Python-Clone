import random, sys, pygame
import copy
from pygame.locals import *
from random import randint

FPS = 60
XMARGIN = 60
YMARGIN = 50
TOPYMARGIN = 196
BOTTOMYMARGIN = 50
TILESIZE = 107
GAPSIZE = 15
BOARDWIDTH = 4
BOARDHEIGHT = 4
WINDOWWIDTH = ((XMARGIN * 2) + (BOARDWIDTH * GAPSIZE) + (BOARDWIDTH * TILESIZE) + GAPSIZE)
WINDOWHEIGHT = (TOPYMARGIN + BOTTOMYMARGIN + (BOARDHEIGHT * GAPSIZE) + (BOARDHEIGHT * TILESIZE) + GAPSIZE)
SLIDESPEED = 1
SLIDETIME = 5
PADDING = TILESIZE / 2

SCORE = 0

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

FONTSIZE = 55
LARGETILEFONT = 55
MEDIUMTILEFONT = 45
SMALLTILEFONT = 35
TINYTILEFONT = 30
WHITE =      (255, 255, 255)
BLACK =      (  0,   0,   0)
MILKYWHITE = (250, 248, 239)
BEIGE =      (187, 173, 160)
BROWN =      (143, 122, 102)

EMPTY = (205, 193, 180)
TWO = (238, 228, 218)
FOUR = (238, 225, 201)
EIGHT = (243, 178, 122)
SIXTEEN = (246, 150, 100)
THIRTYTWO = (247, 124, 95)
SIXTYFOUR = (247, 95, 59)
ONETWENTYEIGHT = (237, 208, 115)
TWOFIFTYSIX = (237, 204, 98)
FIVETWELVE = (237, 201, 80)
TENTWENTYFOUR = (237, 197, 63)
TWENTYFOURTYEIGHT = (237, 194, 46)
SUPER = (60, 58, 50)

BGCOLOR = MILKYWHITE
BOARDBGCOLOR = BEIGE
LIGHTTEXTCOLOR = (249, 246, 242)
DARKTEXTCOLOR =  (119, 110, 101)
        
def main():
    global FPSCLOCK, DISPLAYSURF, SCORE, SMALLFONT, MEDIUMFONT, LARGEFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('2048')
    SMALLFONT = pygame.font.Font('freesansbold.ttf', 14)
    MEDIUMFONT = pygame.font.Font('freesansbold.ttf', 18)
    LARGEFONT = pygame.font.Font('freesansbold.ttf', 25)
    TILES = generateNewBoard(0)
    SCORE = 0
    RESET_BUTTON = drawScreen(TILES)

    while True:

        slideTo = None
        drawScreen(TILES)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                if RESET_BUTTON.collidepoint(event.pos):
                    TILES, SCORE = newGame(TILES, SCORE)

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s):
                    slideTo = DOWN
                elif event.key == K_r:
                    TILES, SCORE = newGame(TILES, SCORE)

        if slideTo:
            makeMove(TILES, slideTo)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def newGame(tiles, score):
    TILES = generateNewBoard(0)
    score = 0
    return (TILES, score)

def addTile(TILES):
    emptyTiles = checkForEmptyTiles(TILES)
    if emptyTiles != ([] or None ):
        if (emptyTiles.__len__() != 0):
            newTile = randint(0, emptyTiles.__len__() - 1)
            tileValGen = randint(1, 10)
            if (tileValGen == 1):
                newTileVal = 4
            else:
                newTileVal = 2

            newTileX, newTileY = emptyTiles[newTile]

            tileColumn = TILES[newTileX]
            tileColumn[newTileY] = newTileVal
            TILES[newTileX] = tileColumn

            newTileAnimation(newTileX, newTileY, newTileVal, 20)
            drawScreen(TILES)

    return TILES

def drawScreen(TILES):
    DISPLAYSURF.fill(BGCOLOR)
    # Render Title
    titleFont = pygame.font.Font("freesansbold.ttf", 80)
    title = titleFont.render("2048", True, DARKTEXTCOLOR, None)
    titleSurf = title.get_rect(x=(XMARGIN), y=(40))
    DISPLAYSURF.blit(title, titleSurf)
    # Draw Scoreboard
    score = str(SCORE)
    pygame.draw.rect(DISPLAYSURF, BEIGE, (XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH - 256, TOPYMARGIN - 175, 128, 55), 0, 3)
    scoreTextSurf, scoreTextRect = makeText('SCORE', SMALLFONT, LIGHTTEXTCOLOR, None, XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH - 194, TOPYMARGIN - 160)
    DISPLAYSURF.blit(scoreTextSurf, scoreTextRect)
    scoreSurf, scoreRect = makeText(score, LARGEFONT, 'white', None, XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH - 194, TOPYMARGIN - 138)
    DISPLAYSURF.blit(scoreSurf, scoreRect)    
    # Draw High Score
    pygame.draw.rect(DISPLAYSURF, BEIGE, (XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE - 128, TOPYMARGIN - 175, 128, 55), 0, 3)
    bestSurf, bestRect = makeText('BEST', SMALLFONT, LIGHTTEXTCOLOR, None, XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH - 52, TOPYMARGIN - 160)
    DISPLAYSURF.blit(bestSurf, bestRect)
    # Draw New Game Button
    RESET_BUTTON = pygame.draw.rect(DISPLAYSURF, BROWN, (XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE - 128, TOPYMARGIN - 80, 128, 40), 0, 3)
    newGameSurf, newGameRect = makeText("New Game", MEDIUMFONT, LIGHTTEXTCOLOR, None, XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE - 64, TOPYMARGIN - 60)
    DISPLAYSURF.blit(newGameSurf, newGameRect)

    # Draw Board and All of the Tiles
    pygame.draw.rect(DISPLAYSURF, BOARDBGCOLOR, (XMARGIN, TOPYMARGIN, (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE, (GAPSIZE + TILESIZE) * BOARDHEIGHT + GAPSIZE), 0, 6)
    for x in range (BOARDWIDTH):
        for y in range (BOARDHEIGHT):
            column = TILES[x]
            tileVal = column[y]

            if (tileVal > 0):
                value = str(tileVal)
            else:
                value = ""
            
            if tileVal <= 4:
                TEXTCOLOR = DARKTEXTCOLOR
            else:
                TEXTCOLOR = LIGHTTEXTCOLOR
            tileX = x
            tileY = y
            tileColor, tileFont = getTileStyles(tileVal)
            font = pygame.font.Font("freesansbold.ttf", tileFont)
            text = font.render(value, True, TEXTCOLOR, None)
            textRect = text.get_rect(center=(tileX * (TILESIZE + GAPSIZE) + XMARGIN + PADDING + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + PADDING + GAPSIZE))
            pygame.draw.rect(DISPLAYSURF, tileColor, (tileX * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + GAPSIZE, TILESIZE, TILESIZE), 0, 3)
            DISPLAYSURF.blit(text, textRect)

    return RESET_BUTTON

def generateNewBoard(z):
    TILES = []
    if z == 0:
        for x in range(BOARDWIDTH):
            column = []
            for y in range(BOARDHEIGHT):
                column.append(0)
            TILES.append(column)
    else:
        if z == 1:
            column1 = [0, 16, 8, 0]
            column2 = [1024, 32, 4, 0]
            column3 = [512,  64, 2, 0]
            column4 = [256,  128, 2, 0]
        elif z == 2:
            column1 = [4096,  2048, 16, 8]
            column2 = [8192,  1024, 32, 4]
            column3 = [16384, 512,  64, 2]
            column4 = [32768, 256,  128, 2]
        elif z == 3:
            column1 = [2, 2, 0, 0]
            column2 = [0, 0, 0, 0]
            column3 = [0, 0, 0, 0]
            column4 = [0, 0, 0, 0]

        TILES.append(column1)
        TILES.append(column2)
        TILES.append(column3)
        TILES.append(column4)

    drawScreen(TILES)

    addTile(TILES)
    addTile(TILES)

    return TILES

def getTileStyles(argument):
    if argument <= 2048:
        match argument:
            case 0:
                return (EMPTY, SMALLTILEFONT)
            case 2:
                return (TWO, LARGETILEFONT)
            case 4:
                return (FOUR, LARGETILEFONT)
            case 8:
                return (EIGHT, LARGETILEFONT)
            case 16:
                return (SIXTEEN, LARGETILEFONT)
            case 32:
                return (THIRTYTWO, LARGETILEFONT)
            case 64:
                return (SIXTYFOUR, LARGETILEFONT)
            case 128:
                return (ONETWENTYEIGHT, MEDIUMTILEFONT)
            case 256:
                return (TWOFIFTYSIX, MEDIUMTILEFONT)
            case 512:
                return (FIVETWELVE, MEDIUMTILEFONT)
            case 1024:
                return (TENTWENTYFOUR, SMALLTILEFONT)
            case 2048:
                return (TWENTYFOURTYEIGHT, SMALLTILEFONT)
    else:
        return (SUPER, TINYTILEFONT)

def makeMove(TILES, slideTo):
    board = copy.deepcopy(TILES)
    slideTiles(TILES, slideTo)
    if board != TILES:
        drawScreen(TILES)
        addTile(TILES)
    return TILES
            
def checkForEmptyTiles(TILES):
    emptyTiles = []
    if TILES != ([] or None ):
        if (TILES.__len__() != 0):
            x = 0
            for x in range(BOARDWIDTH):
                column = TILES[x]
                y = 0
                for y in range(BOARDHEIGHT):
                    tile = column[y]
                    if tile == 0:
                        emptyTiles.append((x, y))
            if (emptyTiles == []):
                gameLost()
    return emptyTiles

def slideTiles(TILES, slideTo):
    global SCORE
    slides = []
    board = copy.deepcopy(TILES)
    if slideTo in (UP, LEFT):
        increment = 1
        first = 0
        second = 1
        third = 2
    else:
        increment = -1
        first = BOARDHEIGHT - 1
        second = BOARDHEIGHT - 2
        third = BOARDHEIGHT - 3
    if slideTo in (UP, DOWN):
        x = 0
        for x in range(BOARDWIDTH):
            column = TILES[x]
            i = increment
            f = first
            s = second
            t = third
            while (0 <= t < BOARDHEIGHT):
                tile = []
                start = []
                end = []
                tile1 = column[f]
                tile2 = column[s]
                tile3 = column[t]
                if tile1 == 0:
                    if tile2 == 0:
                        if tile3 == 0:
                            t += i
                        else:
                            column[f] = tile3
                            column[t] = 0
                            start = [x, t]
                            end = [x, f]
                            tile = [start, end, tile3]
                            slides.append(tile)
                            t += i
                    else:
                        if tile3 == 0:
                            column[f] = tile2
                            column[s] = 0
                            start = [x, s]
                            end = [x, f]
                            tile = [start, end, tile2]
                            slides.append(tile)
                            t += 1
                        else:
                            if tile2 == tile3:
                                column[f] = tile2 + tile3
                                SCORE += tile2 + tile3
                                column[s] = 0
                                column[t] = 0
                                start = [x, s]
                                end = [x, f]
                                tile = [start, end, tile2]
                                slides.append(tile)
                                start = [x, t]
                                end = [x, f]
                                tile = [start, end, tile3]
                                slides.append(tile)
                                f += i
                                s += i
                                t += i
                            else:
                                column[f] = tile2
                                column[s] = tile3
                                column[t] = 0
                                start = [x, s]
                                end = [x, f]
                                tile = [start, end, tile2]
                                slides.append(tile)
                                start = [x, t]
                                end = [x, f]
                                tile = [start, end, tile3]
                                slides.append(tile)
                                f += i
                                s += i
                                t += i
                else:
                    if tile2 == 0:
                        if tile3 > 0:
                            if tile1 == tile3:
                                column[f] = tile1 + tile3
                                SCORE += tile1 + tile3
                                column[t] = 0
                                start = [x, t]
                                end = [x, f]
                                tile = [start, end, tile3]
                                slides.append(tile)
                                f += i
                                t += i
                            else:
                                column[s] = tile3
                                column[t] = 0
                                start = [x, t]
                                end = [x, s]
                                tile = [start, end, tile3]
                                slides.append(tile)
                                f += i
                                s += i
                                t += i
                        else:
                            t += i
                    else:
                        if tile1 == tile2:
                            column[f] = tile1 + tile2
                            SCORE += tile1 + tile2
                            column[s] = 0
                            start = [x, s]
                            end = [x, f]
                            tile = [start, end, tile2]
                            slides.append(tile)
                            f += i
                            s += i
                            t += i
                        else:
                            if tile3 == 0:
                                f += i
                                s += i
                                t += i
                            else:
                                if tile2 == tile3:
                                    column[s] = tile2 + tile3
                                    SCORE += tile2 + tile3
                                    column[t] = 0
                                    start = [x, t]
                                    end = [x, s]
                                    tile = [start, end, tile3]
                                    slides.append(tile)
                                    f = s + i
                                    s += i
                                    t += i
                                else:
                                    f += i
                                    s += i
                                    t += i
            TILES[x] = column
    elif slideTo in (RIGHT, LEFT):
        y = 0
        for y in range(BOARDHEIGHT):
            x = 0
            row = []
            for x in range(BOARDWIDTH):
                column = TILES[x]
                row.append(column[y])
            i = increment
            f = first
            s = second
            t = third
            while (0 <= t < BOARDWIDTH):
                tile1 = row[f]
                tile2 = row[s]
                tile3 = row[t]
                if tile1 == 0:
                    if tile2 == 0:
                        if tile3 == 0:
                            t += i
                        else:
                            row[f] = tile3
                            row[t] = 0
                            start = [t, y]
                            end = [f, y]
                            tile = [start, end, tile3]
                            slides.append(tile)
                            t += i
                    else:
                        if tile3 == 0:
                            row[f] = tile2
                            row[s] = 0
                            start = [s, y]
                            end = [f, y]
                            tile = [start, end, tile2]
                            slides.append(tile)
                            t += 1
                        else:
                            if tile2 == tile3:
                                row[f] = tile2 + tile3
                                SCORE += tile2 + tile3
                                row[s] = 0
                                row[t] = 0
                                start = [s, y]
                                end = [f, y]
                                tile = [start, end, tile2]
                                slides.append(tile)
                                start = [t, y]
                                tile = [start, end, tile3]
                                slides.append(tile)
                                f += i
                                s += i
                                t += i
                            else:
                                row[f] = tile2
                                row[s] = tile3
                                row[t] = 0
                                start = [s, y]
                                end = [f, y]
                                tile = [start, end, tile2]
                                slides.append(tile)
                                start = [t, y]
                                end = [s, y]
                                tile = [start, end, tile3]
                                f += i
                                s += i
                                t += i
                else:
                    if tile2 == 0:
                        if tile3 > 0:
                            if tile1 == tile3:
                                row[f] = tile1 + tile3
                                SCORE += tile1 + tile3
                                row[t] = 0
                                start = [t, y]
                                end = [f, y]
                                tile = [start, end, tile3]
                                slides.append(tile)
                                f += i
                                t += i
                            else:
                                row[s] = tile3
                                row[t] = 0
                                start = [t, y]
                                end = [s, y]
                                tile = [start, end, tile3]
                                slides.append(tile)
                                f += i
                                s += i
                                t += i
                        else:
                            t += i
                    else:
                        if tile1 == tile2:
                            row[f] = tile1 + tile2
                            SCORE += tile1 + tile2
                            row[s] = 0
                            start = [s, y]
                            end = [f, y]
                            tile = [start, end, tile2]
                            slides.append(tile)
                            f += i
                            s += i
                            t += i
                        else:
                            if tile3 == 0:
                                f += i
                                s += i
                                t += i
                            else:
                                if tile2 == tile3:
                                    row[s] = tile2 + tile3
                                    SCORE += tile2 + tile3
                                    row[t] = 0
                                    start = [t, y]
                                    end = [s, y]
                                    tile = [start, end, tile3]
                                    slides.append(tile)
                                    f = s + i
                                    s += i
                                    t += i
                                else:
                                    f += i
                                    s += i
                                    t += i
            x = 0
            for x in range(BOARDWIDTH):
                column = TILES[x]
                column[y] = row[x]
                TILES[x] = column
    slideAnimation(slides, board)       

def newTileAnimation(newTileX, newTileY, newTileVal, animationSpeed):
    i = 0
    while (i < TILESIZE):
        checkForQuit()
        tileX = newTileX
        tileY = newTileY
        tileColor, tileFont = getTileStyles(newTileVal)
        fontSize = (i / TILESIZE) * tileFont
        font = pygame.font.Font("freesansbold.ttf", int(fontSize))
        if (newTileVal > 0):
            value = str(newTileVal)
        else:
            value = ""
            
        if (newTileVal <= 4):
            TEXTCOLOR = DARKTEXTCOLOR
        else:
            TEXTCOLOR = LIGHTTEXTCOLOR
        text = font.render(value, True, TEXTCOLOR, None)
        pygame.draw.rect(DISPLAYSURF, EMPTY, (tileX * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + GAPSIZE, TILESIZE, TILESIZE), 0, 3)
        textRect = text.get_rect(center=(tileX * (TILESIZE + GAPSIZE) + XMARGIN + PADDING + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + PADDING + GAPSIZE))
        xPad = PADDING - (i / 2)
        yPad = PADDING - (i / 2)
        pygame.draw.rect(DISPLAYSURF, tileColor, (tileX * (TILESIZE + GAPSIZE) + XMARGIN + xPad + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + yPad + GAPSIZE, i, i), 0, 3)
        DISPLAYSURF.blit(text, textRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        i += animationSpeed

def slideAnimation(array, board):
    for f in range(1, SLIDETIME, SLIDESPEED):
        drawScreen(board)
        t = 0
        for t in range(len(array)):
            (start, end, val) = array[t]
            (startX, startY) = start
            (endX, endY) = end
            if startX == endX:
                x = startX
                i = f * (startY - endY) / SLIDETIME
                y = startY - i
            elif startY == endY:
                i = f * (startX - endX) / SLIDETIME
                x = startX - i
                y = startY
            if val == 0:
                value = ''
            else:
                value = str(val)
            if val <= 4:
                fontColor = DARKTEXTCOLOR
            else:
                fontColor = LIGHTTEXTCOLOR
            color, fontSize = getTileStyles(val)
            pygame.draw.rect(DISPLAYSURF, EMPTY, (startX * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE, startY * (TILESIZE + GAPSIZE) + TOPYMARGIN + GAPSIZE, TILESIZE, TILESIZE), 0, 3)
            pygame.draw.rect(DISPLAYSURF, color, (x * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE, y * (TILESIZE + GAPSIZE) + TOPYMARGIN + GAPSIZE, TILESIZE, TILESIZE), 0, 3)
            font = pygame.font.Font('freesansbold.ttf', fontSize)
            textSurf = font.render(value, True, fontColor, None)
            textRect = textSurf.get_rect(center=(x * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE + PADDING, y * (TILESIZE + GAPSIZE) + TOPYMARGIN + GAPSIZE + PADDING))
            DISPLAYSURF.blit(textSurf, textRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
            

def makeText(text, fontStyle, color, bgcolor, x, y):
    # create the Surface and Rect objects for some text.
    font = fontStyle
    textSurf = font.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect(center=(x, y))
    return (textSurf, textRect)

def gameLost():
    print("GAME OVER")

if __name__ == '__main__':
    main()    