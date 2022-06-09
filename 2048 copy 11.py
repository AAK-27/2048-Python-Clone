import sys, pygame, os, ctypes, copy
from pygame.locals import *
from random import randint

# Forces windows to load 2048 icon to taskbar by changing the App ID
myappid = '2048v0.10.0' # Arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

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
PADDING = TILESIZE / 2
# Calculates the Animation Speed depending on the FPS
# This way it is the same speed no matter the framerate
ANIMATIONSPEED = 1
ANIMATIONTIME = int(10 * FPS)

SCORE = 0
HIGHSCORE = 0
SCORES = []

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
                # After the player makes a move it will attempt to spawn a new tile
NEWTILE1 = 2    # 9/10 Chance of spawning
NEWTILE2 = 4    # 1/10 Chance of spawning

LARGETFS = 55
MEDIUMTFS = 45
SMALLTFS = 35
TINYTFS = 30

MILKYWHITE = (250, 248, 239)
BEIGE =      (187, 173, 160)
BROWN =      (143, 122, 102)
GREY =       (238, 228, 218, 180)
YELLOW =     (237, 194,  46,  38)

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

MOVES = (K_RIGHT, K_d, K_l, K_UP, K_w, K_k, K_LEFT, K_h, K_d, K_DOWN, K_j, K_s)
WINEVENTS = [2048, 4096, 8192, 16384, 32768, 65536, 131072]
GAMEWON = False

# Gets the directory of the file to load resources using relative path
dirname = os.path.dirname(__file__)
        
def main():
    global FPSCLOCK, DISPLAYSURF, TILES, SCORE, HIGHSCORE, SMALLFONT, MEDIUMFONT, LARGEFONT, GAMEOVER, TITLEFONT, LARGETILEFONT, MEDIUMTILEFONT, SMALLTILEFONT, TINYTILEFONT, RESET_BUTTON, GAMEWON
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    iconfile = os.path.join(dirname, './resources/images/2048.png')
    icon = pygame.image.load(iconfile)
    pygame.display.set_icon(icon)
    pygame.display.set_caption('2048')
    SMALLFONT = pygame.font.Font('freesansbold.ttf', 14)
    MEDIUMFONT = pygame.font.Font('freesansbold.ttf', 18)
    LARGEFONT = pygame.font.Font('freesansbold.ttf', 25)
    TITLEFONT = pygame.font.Font('freesansbold.ttf', 80)
    LARGETILEFONT = pygame.font.Font('freesansbold.ttf', LARGETFS)
    MEDIUMTILEFONT = pygame.font.Font('freesansbold.ttf', MEDIUMTFS)
    SMALLTILEFONT = pygame.font.Font('freesansbold.ttf', SMALLTFS)
    TINYTILEFONT = pygame.font.Font('freesansbold.ttf', TINYTFS)
    getSavedBoard()
    GAMEOVER = False
    RESET_BUTTON = drawScreen(TILES)
    checkForGameOver()

    while True:

        slideTo = None

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                if RESET_BUTTON.collidepoint(event.pos):
                    newGame()

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a, K_h):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d, K_l):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w, K_k):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s, K_j):
                    slideTo = DOWN
                elif event.key == K_r:
                    newGame()
                elif event.key == K_f:
                    gameLost()
                elif event.key == K_v:
                    gameWon()

        if slideTo:
            makeMove(TILES, slideTo)
            checkForGameOver()
            if GAMEWON:
                gameWon()
                GAMEWON = False
                
        drawScreen(TILES)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.display.quit()
    saveGame()
    pygame.quit()
    sys.exit()

def saveGame():
    save = copy.deepcopy(TILES)
    save.append(SCORE)
    save.append(HIGHSCORE)
    saveFile = os.path.join(dirname, './resources/saves/save.txt')
    with open(saveFile, 'w') as file:
        file.write(str(save))

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def newGame():
    global SCORE
    generateNewBoard(0)
    SCORE = 0
    saveGame()

def checkForGameOver():
    s = 0
    for move in (UP, DOWN, LEFT, RIGHT):
        board = copy.deepcopy(TILES)
        slideTiles(board, move, False)
        if board == TILES:
            s += 1
    if s == 4:
        pygame.time.wait(100)
        gameLost()

def addTile(TILES, z):
    emptyTiles = checkForEmptyTiles(TILES)
    if emptyTiles != ([] or None):
        if (emptyTiles.__len__() != 0):
            newTiles = []
            for t in range(z):
                newTile = randint(0, emptyTiles.__len__() - 1)
                tileValGen = randint(1, 10)
                if (tileValGen == 1):
                    newTileVal = NEWTILE2
                else:
                    newTileVal = NEWTILE1

                newTileX, newTileY = emptyTiles[newTile]

                tileColumn = TILES[newTileX]
                tileColumn[newTileY] = newTileVal
                TILES[newTileX] = tileColumn
                newTiles.append( (newTileX, newTileY, newTileVal) )

                del emptyTiles[newTile]

            newTileAnimation(newTiles)
            drawScreen(TILES)
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    return TILES

def drawScreen(TILES):
    DISPLAYSURF.fill(BGCOLOR)
    # Render Title
    title = TITLEFONT.render("2048", True, DARKTEXTCOLOR, None)
    titleSurf = title.get_rect(x=(XMARGIN), y=(40))
    DISPLAYSURF.blit(title, titleSurf)
    # Draw Scoreboard
    score = str(SCORE)
    pygame.draw.rect(DISPLAYSURF, BEIGE, (XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH - 256, TOPYMARGIN - 175, 128, 55), 0, 3)
    scoreTextSurf, scoreTextRect = makeText('SCORE', SMALLFONT, LIGHTTEXTCOLOR, None, XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH - 194, TOPYMARGIN - 160)
    DISPLAYSURF.blit(scoreTextSurf, scoreTextRect)
    scoreSurf, scoreRect = makeText(score, LARGEFONT, 'white', None, XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH - 193, TOPYMARGIN - 138)
    DISPLAYSURF.blit(scoreSurf, scoreRect)    
    # Draw High Score
    highScore = str(HIGHSCORE)
    pygame.draw.rect(DISPLAYSURF, BEIGE, (XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE - 128, TOPYMARGIN - 175, 128, 55), 0, 3)
    bestSurf, bestRect = makeText('BEST', SMALLFONT, LIGHTTEXTCOLOR, None, XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH - 52, TOPYMARGIN - 160)
    DISPLAYSURF.blit(bestSurf, bestRect)
    highScoreSurf, highScoreRect = makeText(highScore, LARGEFONT, 'white', None, XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH - 49, TOPYMARGIN - 138)
    DISPLAYSURF.blit(highScoreSurf, highScoreRect)
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
            tileColor, _, font = getTileStyles(tileVal)
            pygame.draw.rect(DISPLAYSURF, tileColor, (tileX * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + GAPSIZE, TILESIZE, TILESIZE), 0, 3)
            text = font.render(value, True, TEXTCOLOR, None)
            textRect = text.get_rect(center=(tileX * (TILESIZE + GAPSIZE) + XMARGIN + PADDING + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + PADDING + GAPSIZE))
            DISPLAYSURF.blit(text, textRect)
    drawScore(SCORES)
    return RESET_BUTTON

def generateNewBoard(z):
    global TILES
    # 'z' Variable decides what kind of board is generated
    # 0 - Generates empty board
    # 1 - Generates a board so you can combine to 2048
    # 2 - Generates a board to combine to 65536
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
            # [[4096,  2048, 16, 8], [8192,  1024, 32, 4], [16384, 512,  64, 2], [32768, 256,  128, 2], 0, 0]
            column1 = [4096,  2048, 16, 8]
            column2 = [8192,  1024, 32, 4]
            column3 = [16384, 512,  64, 2]
            column4 = [32768, 256,  128, 2]

        TILES.append(column1)
        TILES.append(column2)
        TILES.append(column3)
        TILES.append(column4)

    # Attempts to add two tiles to the board whether it is empty or filled
    addTile(TILES, 2)

def getSavedBoard():
    global TILES, SCORE, HIGHSCORE
    saveFile = os.path.join(dirname, './resources/saves/save.txt')
    with open(saveFile, 'r') as save:
        content = save.read()
        if len(content) > 0:
            content = content.replace('[', '')
            content = content.replace(']', '')
            content = content.replace(',', '')
            tiles = content.split()
            TILES = []
            for x in range (BOARDWIDTH):
                COLUMN = []
                for y in range (BOARDHEIGHT):
                    if x < 1:
                        i = y
                    elif x < 2:
                        i = y + 4
                    elif x < 3:
                        i = y + 8
                    else:
                        i = y + 12
                    tile = tiles[i]
                    TILE = int(tile)
                    COLUMN.append(TILE)
                TILES.append(COLUMN)
            SCORE = int(tiles[BOARDWIDTH * BOARDHEIGHT])
            HIGHSCORE = int(tiles[BOARDWIDTH * BOARDHEIGHT + 1])
        else:
            newGame()

def getTileStyles(val):
    # Returns a color, fontsize, and font depending on the value of the tile
    if val == 0:
        return (EMPTY, LARGETFS, SMALLTILEFONT)
    elif val == 2:
        return (TWO, LARGETFS, LARGETILEFONT)
    elif val == 4:
        return (FOUR, LARGETFS, LARGETILEFONT)
    elif val == 8:
        return (EIGHT, LARGETFS, LARGETILEFONT)
    elif val == 16:
        return (SIXTEEN, LARGETFS, LARGETILEFONT)
    elif val == 32:
        return (THIRTYTWO, LARGETFS, LARGETILEFONT)
    elif val == 64:
        return (SIXTYFOUR, LARGETFS, LARGETILEFONT)
    elif val == 128:
        return (ONETWENTYEIGHT, MEDIUMTFS, MEDIUMTILEFONT)
    elif val == 256:
        return (TWOFIFTYSIX, MEDIUMTFS, MEDIUMTILEFONT)
    elif val == 512:
        return (FIVETWELVE, MEDIUMTFS, MEDIUMTILEFONT)
    elif val == 1024:
        return (TENTWENTYFOUR, SMALLTFS, SMALLTILEFONT)
    elif val == 2048:
        return (TWENTYFOURTYEIGHT, SMALLTFS, SMALLTILEFONT)
    else: 
        return (SUPER, TINYTFS, TINYTILEFONT)

def makeMove(TILES, slideTo):
    board = copy.deepcopy(TILES)
    slideTiles(TILES, slideTo, True)
    if board != TILES:
        addTile(TILES, 1)
    return TILES
            
def checkForEmptyTiles(TILES):
    emptyTiles = []
    if TILES != ([] or None):
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

def slideTiles(TILES, slideTo, updateBoard):
    global SCORE, HIGHSCORE, GAMEWON, SCORES
    slides = []
    scores = 0
    board = copy.deepcopy(TILES)
    if slideTo in (UP, LEFT):
        increment = 1
        first = 0
        second = 1
    else:
        increment = -1
        first = BOARDHEIGHT - 1
        second = BOARDHEIGHT - 2
    if slideTo in (UP, DOWN):
        x = 0
        for x in range(BOARDWIDTH):
            column = TILES[x]
            i = increment
            f = first
            s = second
            while (0 <= s < BOARDHEIGHT):
                tile1 = column[f]
                tile2 = column[s]
                if tile1 == 0:
                    if tile2 == 0:
                        s += i
                    else:
                        column[f] = tile2
                        column[s] = 0
                        start = [x, s]
                        end = [x, f]
                        tile = [start, end, tile2]
                        slides.append( (tile, False) )
                        s += i
                else:
                    if tile2 == 0:
                        s += i
                    else:
                        if tile1 == tile2:
                            tile3 = tile1 + tile2
                            column[f] = tile3
                            column[s] = 0
                            start = [x, s]
                            end = [x, f]
                            tile = [start, end, tile2]
                            slides.append( (tile, True) )
                            if updateBoard:
                                scores += tile3
                                if tile3 >= 2048:
                                    if tile3 in WINEVENTS:
                                        if WINEVENTS[0] == tile3:
                                            del WINEVENTS[0]
                                            GAMEWON = True
                            f += i
                            s += i
                        else:
                            if (f + i) == s:
                                f += i
                                s += i
                            else:
                                column[f + i] = tile2
                                column[s] = 0
                                start = [x, s]
                                end = [x, f + i]
                                tile = [start, end, tile2]
                                slides.append( (tile, False) )
                                f += i
                                s += i
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
            while (0 <= s < BOARDWIDTH):
                tile1 = row[f]
                tile2 = row[s]
                if tile1 == 0:
                    if tile2 == 0:
                        s += i
                    else:
                        row[f] = tile2
                        row[s] = 0
                        start = [s, y]
                        end = [f, y]
                        tile = [start, end, tile2]
                        slides.append( (tile, False) )
                        s += i
                else:
                    if tile2 == 0:
                        s += i
                    else:
                        if tile1 == tile2:
                            tile3 = tile1 + tile2
                            row[f] = tile3
                            row[s] = 0
                            start = [s, y]
                            end = [f, y]
                            tile = [start, end, tile2]
                            slides.append( (tile, True) )
                            if updateBoard:
                                scores += tile3
                                if tile3 >= 2048:
                                    if tile3 in WINEVENTS:
                                        if WINEVENTS[0] == tile3:
                                                del WINEVENTS[0]
                                                GAMEWON = True
                            f += i
                            s += i
                        else:
                            if (f + i) == s:
                                f += i
                                s += i
                            else:
                                row[f + i] = tile2
                                row[s] = 0
                                start = [s, y]
                                end = [f + i, y]
                                tile = [start, end, tile2]
                                slides.append( (tile, False) )
                                f += i
                                s += i
            x = 0
            for x in range(BOARDWIDTH):
                column = TILES[x]
                column[y] = row[x]
                TILES[x] = column
    if updateBoard:
        slideAnimation(slides, board)
        if (scores > 0):
            SCORE += scores
            if SCORE > HIGHSCORE:
                HIGHSCORE = SCORE
            SCORES.append((scores, FPS))

def newTileAnimation(newTiles):
    animation_time = int(ANIMATIONTIME * 0.015)
    for f in range(0, animation_time, ANIMATIONSPEED):
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key in MOVES:
                    pygame.event.post(event)
                    return
        drawScreen(TILES)
        for tile in newTiles:
            tileX, tileY, tileVal = tile
            tileColor, tfs, _ = getTileStyles(tileVal)
            fontSize = f / animation_time * tfs
            font = pygame.font.Font("freesansbold.ttf", int(fontSize))
            if (tileVal > 0):
                value = str(tileVal)
            else:
                value = ""
                
            if (tileVal <= 4):
                TEXTCOLOR = DARKTEXTCOLOR
            else:
                TEXTCOLOR = LIGHTTEXTCOLOR
            text = font.render(value, True, TEXTCOLOR, None)
            pygame.draw.rect(DISPLAYSURF, EMPTY, (tileX * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + GAPSIZE, TILESIZE, TILESIZE), 0, 3)
            textRect = text.get_rect(center=(tileX * (TILESIZE + GAPSIZE) + XMARGIN + PADDING + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + PADDING + GAPSIZE))
            xPad = PADDING - (PADDING * f / animation_time)
            yPad = PADDING - (PADDING * f / animation_time)
            pygame.draw.rect(DISPLAYSURF, tileColor, (tileX * (TILESIZE + GAPSIZE) + XMARGIN + xPad + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + yPad + GAPSIZE, f / animation_time * TILESIZE, f / animation_time * TILESIZE), 0, 3)
            DISPLAYSURF.blit(text, textRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def slideAnimation(slides, board):
    combineTiles = []
    for slide in slides:
        ( (_, end, val), combine) = slide
        if (combine):
            combineTiles.append( (end, val) )
    animation_time = int(ANIMATIONTIME * 0.01)
    for f in range(1, animation_time, ANIMATIONSPEED):
        drawScreen(board)
        for tile in slides:
            ( (start, end, val), _) = tile
            (startX, startY) = start
            (endX, endY) = end
            if startX == endX:
                x = startX
                y = startY - (f * (startY - endY) / animation_time)
            elif startY == endY:
                x = startX - (f * (startX - endX) / animation_time)
                y = startY
            if val == 0:
                value = ''
            else:
                value = str(val)
            if val <= 4:
                fontColor = DARKTEXTCOLOR
            else:
                fontColor = LIGHTTEXTCOLOR
            color, _, font = getTileStyles(val)
            pygame.draw.rect(DISPLAYSURF, EMPTY, (startX * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE, startY * (TILESIZE + GAPSIZE) + TOPYMARGIN + GAPSIZE, TILESIZE, TILESIZE), 0, 3)
            pygame.draw.rect(DISPLAYSURF, color, (x * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE, y * (TILESIZE + GAPSIZE) + TOPYMARGIN + GAPSIZE, TILESIZE, TILESIZE), 0, 3)
            textSurf = font.render(value, True, fontColor, None)
            textRect = textSurf.get_rect(center=(x * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE + PADDING, y * (TILESIZE + GAPSIZE) + TOPYMARGIN + GAPSIZE + PADDING))
            DISPLAYSURF.blit(textSurf, textRect)
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key in MOVES:
                    pygame.event.post(event)
                    return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    combineAnimation(combineTiles)

def combineAnimation(tiles):
    animation_time = int(ANIMATIONTIME * 0.008)
    animation1 = int(animation_time / 4 * 3)
    animation2 = int(animation_time / 4)
    for f in range(0, animation1, ANIMATIONSPEED):
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key in MOVES:
                    pygame.event.post(event)
                    return
        drawScreen(TILES)
        for tile in tiles:
            (pos, val) = tile
            tileVal = val * 2
            (tileX, tileY) = pos
            tileColor, tfs, _ = getTileStyles(tileVal)
            pop = f / animation1 * (GAPSIZE * 2)
            fontSize = tfs + pop
            font = pygame.font.Font("freesansbold.ttf", int(fontSize))
            if (tileVal > 0):
                value = str(tileVal)
            else:
                value = ""
                
            if (tileVal <= 4):
                TEXTCOLOR = DARKTEXTCOLOR
            else:
                TEXTCOLOR = LIGHTTEXTCOLOR
            text = font.render(value, True, TEXTCOLOR, None)
            pygame.draw.rect(DISPLAYSURF, EMPTY, (tileX * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + GAPSIZE, TILESIZE, TILESIZE), 0, 3)
            textRect = text.get_rect(center=(tileX * (TILESIZE + GAPSIZE) + XMARGIN + PADDING + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + PADDING + GAPSIZE))
            pygame.draw.rect(DISPLAYSURF, tileColor, (tileX * (TILESIZE + GAPSIZE) + XMARGIN - (pop / 2) + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN - (pop / 2) + GAPSIZE, TILESIZE + pop, TILESIZE + pop), 0, 3)
            DISPLAYSURF.blit(text, textRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    for f in range(0, animation2, ANIMATIONSPEED):
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key in MOVES:
                    pygame.event.post(event)
                    return
        drawScreen(TILES)
        for tile in tiles:
            (pos, val) = tile
            tileVal = val * 2
            (tileX, tileY) = pos
            tileColor, tfs, _ = getTileStyles(tileVal)
            pop = (GAPSIZE * 2) - (f / animation2 * GAPSIZE * 2)
            fontSize = tfs + pop
            font = pygame.font.Font("freesansbold.ttf", int(fontSize))
            if (tileVal > 0):
                value = str(tileVal)
            else:
                value = ""
                
            if (tileVal <= 4):
                TEXTCOLOR = DARKTEXTCOLOR
            else:
                TEXTCOLOR = LIGHTTEXTCOLOR
            text = font.render(value, True, TEXTCOLOR, None)
            pygame.draw.rect(DISPLAYSURF, EMPTY, (tileX * (TILESIZE + GAPSIZE) + XMARGIN + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + GAPSIZE, TILESIZE, TILESIZE), 0, 3)
            textRect = text.get_rect(center=(tileX * (TILESIZE + GAPSIZE) + XMARGIN + PADDING + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN + PADDING + GAPSIZE))
            pygame.draw.rect(DISPLAYSURF, tileColor, (tileX * (TILESIZE + GAPSIZE) + XMARGIN - (pop / 2) + GAPSIZE, tileY * (TILESIZE + GAPSIZE) + TOPYMARGIN - (pop / 2) + GAPSIZE, TILESIZE + pop, TILESIZE + pop), 0, 3)
            DISPLAYSURF.blit(text, textRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawScore(scores):
    if scores != []:
        dedScores = []
        for s in range(len(scores)):
            score = scores[s]
            val, life = score
            if life == 0:
                dedScores.append(s)
            else:
                y = (life / FPS * 160) - 160
                scoreTxt, scoreSurf = makeText('+' + str(val), LARGEFONT, DARKTEXTCOLOR, None, XMARGIN + (GAPSIZE + TILESIZE) * BOARDWIDTH - 194, TOPYMARGIN - 160 + y)
                alpha = life / FPS * 255
                scoreTxt.set_alpha(alpha)
                life -= 1
                score = val, life
                scores[s] = score
                DISPLAYSURF.blit(scoreTxt, scoreSurf)
        for f in range(len(dedScores)):
            del scores[dedScores[f]]

def makeText(text, fontStyle, color, bgcolor, x, y):
    # create the Surface and Rect objects for some text.
    font = fontStyle
    textSurf = font.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect(center=(x, y))
    return (textSurf, textRect)

def gameLost():
    gameOver = True
    gameOverFont = pygame.font.Font('freesansbold.ttf', 60)
    animation_time = int(ANIMATIONTIME * 0.025)
    for s in range(0, animation_time, ANIMATIONSPEED):
        drawScreen(TILES)
        greyTint = s / animation_time * 186.15
        alpha = s / animation_time * 255
        tintedGrey = (238, 228, 218, greyTint)
        # Draws Transparent Grey Rectange
        shape_surf = pygame.Surface(pygame.Rect(XMARGIN, TOPYMARGIN, (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE, (GAPSIZE + TILESIZE) * BOARDHEIGHT + GAPSIZE).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, tintedGrey, shape_surf.get_rect())
        DISPLAYSURF.blit(shape_surf, (XMARGIN, TOPYMARGIN, (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE, (GAPSIZE + TILESIZE) * BOARDHEIGHT + GAPSIZE))
        # Draws 'Game Over' Text
        gameOverSurf = gameOverFont.render('Game Over!', True, DARKTEXTCOLOR, None)
        gameOverRect = gameOverSurf.get_rect(center=(WINDOWWIDTH / 2, TOPYMARGIN + (TILESIZE + GAPSIZE) * (BOARDHEIGHT / 2) - 30))
        gameOverSurf.set_alpha(alpha)
        DISPLAYSURF.blit(gameOverSurf, gameOverRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    while gameOver:
        drawScreen(TILES)
        # Tinted Grey Rectangle
        shape_surf = pygame.Surface(pygame.Rect(XMARGIN, TOPYMARGIN, (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE, (GAPSIZE + TILESIZE) * BOARDHEIGHT + GAPSIZE).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, (238, 228, 218, 186.15), shape_surf.get_rect())
        DISPLAYSURF.blit(shape_surf, (XMARGIN, TOPYMARGIN, (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE, (GAPSIZE + TILESIZE) * BOARDHEIGHT + GAPSIZE))
        # Game Over Text
        gameOverSurf = gameOverFont.render('Game Over!', True, DARKTEXTCOLOR, None)
        gameOverRect = gameOverSurf.get_rect(center=(WINDOWWIDTH / 2, TOPYMARGIN + (TILESIZE + GAPSIZE) * (BOARDHEIGHT / 2) - 30))
        DISPLAYSURF.blit(gameOverSurf, gameOverRect)
        # 'Try Again' Button
        tryAgainButton = pygame.draw.rect(DISPLAYSURF, BROWN, (WINDOWWIDTH / 2 - 58, TOPYMARGIN + (TILESIZE + GAPSIZE) * (BOARDHEIGHT / 2) + 30, 116, 40), 0, 3)
        tryAgainSurf, tryAgainRect = makeText('Try Again', MEDIUMFONT, 'white', None, WINDOWWIDTH / 2,  TOPYMARGIN + (TILESIZE + GAPSIZE) * (BOARDHEIGHT / 2) + 52)
        DISPLAYSURF.blit(tryAgainSurf, tryAgainRect)
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if tryAgainButton.collidepoint(event.pos):
                    gameOver = False
                    newGame()
                elif RESET_BUTTON.collidepoint(event.pos):
                    gameOver = False
                    newGame()
            elif event.type == KEYUP:
                if event.key in (K_r, K_RETURN):
                    gameOver = False
                    newGame()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def gameWon():
    gameWon = True
    gameWonFont = pygame.font.Font('freesansbold.ttf', 60)
    animation_time = int(ANIMATIONTIME * 0.025)
    for s in range(0, animation_time, ANIMATIONSPEED): # Fade into a Yellow Tint
        drawScreen(TILES)
        yellowTint = s / animation_time * 186.15
        alpha = s / animation_time * 255
        tintedYellow = (237, 194,  46, yellowTint)
        # Draw Transparent Yellow Rectangle
        shape_surf = pygame.Surface(pygame.Rect(XMARGIN, TOPYMARGIN, (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE, (GAPSIZE + TILESIZE) * BOARDHEIGHT + GAPSIZE).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, tintedYellow, shape_surf.get_rect())
        DISPLAYSURF.blit(shape_surf, (XMARGIN, TOPYMARGIN, (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE, (GAPSIZE + TILESIZE) * BOARDHEIGHT + GAPSIZE))
        # Draw 'You Win' Text
        gameWonSurf = gameWonFont.render('You Win!', True, LIGHTTEXTCOLOR, None)
        gameWonRect = gameWonSurf.get_rect(center=(WINDOWWIDTH / 2, TOPYMARGIN + (TILESIZE + GAPSIZE) * (BOARDHEIGHT / 2) - 30))
        gameWonSurf.set_alpha(alpha)
        DISPLAYSURF.blit(gameWonSurf, gameWonRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    while gameWon:
        drawScreen(TILES)
        # Draw Transparent Yellow Rectangle
        shape_surf = pygame.Surface(pygame.Rect(XMARGIN, TOPYMARGIN, (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE, (GAPSIZE + TILESIZE) * BOARDHEIGHT + GAPSIZE).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, tintedYellow, shape_surf.get_rect())
        DISPLAYSURF.blit(shape_surf, (XMARGIN, TOPYMARGIN, (GAPSIZE + TILESIZE) * BOARDWIDTH + GAPSIZE, (GAPSIZE + TILESIZE) * BOARDHEIGHT + GAPSIZE))
        # 'Keep Going' Button
        continueButton = pygame.draw.rect(DISPLAYSURF, BROWN, (WINDOWWIDTH / 2 - 116 - GAPSIZE, TOPYMARGIN + (TILESIZE + GAPSIZE) * (BOARDHEIGHT / 2) + 30, 116, 40), 0, 3)
        continueSurf, continueRect = makeText('Keep Going', MEDIUMFONT, 'white', None, WINDOWWIDTH / 2 - GAPSIZE - 58,  TOPYMARGIN + (TILESIZE + GAPSIZE) * (BOARDHEIGHT / 2) + 52)
        DISPLAYSURF.blit(continueSurf, continueRect)
        # 'Try Again' Button
        tryAgainButton = pygame.draw.rect(DISPLAYSURF, BROWN, (WINDOWWIDTH / 2 + GAPSIZE, TOPYMARGIN + (TILESIZE + GAPSIZE) * (BOARDHEIGHT / 2) + 30, 116, 40), 0, 3)
        tryAgainSurf, tryAgainRect = makeText('Try Again', MEDIUMFONT, 'white', None, WINDOWWIDTH / 2 + GAPSIZE + 58,  TOPYMARGIN + (TILESIZE + GAPSIZE) * (BOARDHEIGHT / 2) + 52)
        DISPLAYSURF.blit(tryAgainSurf, tryAgainRect)
        # You Win! Text
        gameWonSurf = gameWonFont.render('You Win!', True, LIGHTTEXTCOLOR, None)
        gameWonRect = gameWonSurf.get_rect(center=(WINDOWWIDTH / 2, TOPYMARGIN + (TILESIZE + GAPSIZE) * (BOARDHEIGHT / 2) - 30))
        DISPLAYSURF.blit(gameWonSurf, gameWonRect)
        # Event Handler for Game Won Screen
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if continueButton.collidepoint(event.pos):
                    gameWon = False
                elif tryAgainButton.collidepoint(event.pos):
                    gameWon = False
                    newGame()
                elif RESET_BUTTON.collidepoint(event.pos):
                    gameWon = False
                    newGame()
            elif event.type == KEYUP:
                if event.key == (K_r):
                    gameWon = False
                    newGame()
                elif event.key in (K_ESCAPE, K_RETURN):
                    gameWon = False
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()    