
# This file runs Save112! and requires cmu_cs3_graphics and "112.png"

from cmu_cs3_graphics import *
import random
import math
from PIL import Image
# Name: Krutika Kumar 
# AndrewID: krutikak
# Section: 3C

# creates a cell object used in maze generation
class Cell(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.up = True
        self.down = True
        self.left = True
        self.right = True
        
    def __repr__(self):
        return f'({self.row}, {self.col}, {self.up}, {self.down}, {self.left}, {self.right})'
        
# controller function that initializes all app variables
def onAppStart(app):
    app.r = 20
    app.cx = app.r
    app.cy = app.height - app.r
    app.jump = 2*app.r
    app.rows = app.height // 40
    app.cols = app.width // 40
    app.visitedCells = []
    app.ticks = 0
    app.titleScreen = True
    app.mazeList = []
    app.visited = []
    app.coinList = []
    app.maxCoins = 3
    app.score = 0
    app.endLevel = False
    app.difficulty = True
    app.diffLevel = 0
    app.directions = False
    app.lock = True
    app.enemies = []
    app.pathList = []
    app.ouch = (False, 0, 0)
    app.clicks = 0
    app.j = 0
    app.DUBS = False
    app.D = False
    app.U = False
    app.B = False
    app.S = False
    app.reset = False
    app.freddy = False
    app.flag = False
    app.cd = False
    app.power = False

# creates an empty maze list    
def formMazeList(app):
    for row in range(app.rows):
        rowList = []
        for col in range(app.cols):
            cell = Cell(row, col)
            rowList.append(cell)
        app.mazeList.append(rowList)
            
            
# CITE: DFS Algorithm from https://en.wikipedia.org/wiki/Maze_generation_algorithm            
def createMaze(app, row, col):
    if(row == len(app.mazeList) -1 and col == len(app.mazeList[0]) -1 
        and len(app.visited) == len(app.mazeList)):
        return app.mazeList
    else:
        app.visited.append(app.mazeList[row][col])
        potentialCells = {'down' : (row+1, col), 'up' : (row-1, col), 
                    'right' : (row, col+1), 'left' : (row, col-1)}
        potentialCellNames = ['down', 'up', 'right', 'left']
        
        while(len(potentialCells) > 0):
            randIndex = random.randrange(len(potentialCellNames))
            randDir = potentialCellNames[randIndex]
            
            newRow, newCol = potentialCells[randDir]
            
            potentialCellNames.pop(randIndex)
            potentialCells.pop(randDir)
            
            if isValid(app, newRow, newCol):
                
                if randDir == 'up':
                    app.mazeList[row][col].up = False
                    app.mazeList[newRow][newCol].down = False
                    
                elif randDir == 'down':
                    app.mazeList[row][col].down = False
                    app.mazeList[newRow][newCol].up = False
                    
                elif randDir == 'left':
                    app.mazeList[row][col].left = False
                    app.mazeList[newRow][newCol].right = False
                    
                else:
                    app.mazeList[row][col].right = False
                    app.mazeList[newRow][newCol].left = False
                    
                potentialSolution = createMaze(app, newRow, newCol)
                if potentialSolution != None:
                    return potentialSolution
                    
        return None

# helper to create maze; checks if row, col pair is acceptable                
def isValid(app, row, col):
    if row >= len(app.mazeList) or row < 0:
        return False
    elif col >= len(app.mazeList[0]) or col < 0:
        return False
    elif app.mazeList[row][col] in app.visited:
        return False
    else: return True
    
# creates the max coins depending on difficulty
def setMaxCoins(app):
    if app.diffLevel == 1:
        app.maxCoins = 7
    elif app.diffLevel == 2:
        app.maxCoins = 10
        
# places the enemy(s) on the maze depending on difficulty          
def placeEnemies(app):
    if app.diffLevel > 0:
        app.enemies.append((app.rows-1, app.cols-1))
    if app.diffLevel > 1:
        app.enemies.append((0, 0))

# CITE: food algorithm from CMU 112 Website (similar to snake)    
def addCoins(app):
    while True:
        coinRow = random.randrange(app.rows)
        coinCol = random.randrange(app.cols)
        
        playerRow, playerCol = getPlayerRowCol(app)
        if((playerRow != coinRow and playerCol != coinCol) or
            (coinRow != 0 and coinCol != app.rows-1)):
            coinPlace = (coinRow, coinCol)
            app.coinList.append(coinPlace)
            return

# returns the player row, col using app.cx, app.cy           
def getPlayerRowCol(app):
    cellWidth = app.width / app.cols
    cellHeight = app.height / app.rows
    rangex1 = 0
    rangey1 = 0
    rangex2 = cellWidth
    rangey2 = cellHeight
    for row in range(app.rows):
        for col in range(app.cols):
            if( rangex1 <= app.cx and rangex2 >= app.cx and
                rangey1 <= app.cy and rangey2 >= app.cy):
                    return row, col
            rangex1 += cellWidth
            rangex2 += cellWidth
        rangex1 = 0
        rangex2 = cellWidth
        rangey1 += cellHeight
        rangey2 += cellHeight

# takes the result from path finding algo and makes it a working list of 
# the path that the enemy is supposed to take         
def enemyAttacks(app):
    pathList = []
    playerRow, playerCol = getPlayerRowCol(app)
    for enemyRow, enemyCol in app.enemies:
        result = []
        temp = (pathFind(app, enemyRow, enemyCol, playerRow, playerCol))
        node = (playerRow, playerCol)
        while(node != (enemyRow, enemyCol)):
            result.insert(0, node)
            node = temp[node]
        pathList.append(result)
    return pathList

# CITE: Pathfinding BFS Algorithm (https://www.cs.cmu.edu/~112/notes/student-tp-guides/Pathfinding.pdf)        
def pathFind(app, row1, col1, row2, col2):
    Q = [(row1, col1)]
    V = {(row1, col1)}
    path = {}
    while len(Q) != 0:
        node = Q.pop(0)
        if node == (row2, col2):
            return path
        neighbors = [(node[0] + 1,node[1]), (node[0] - 1,node[1]), 
                    (node[0],node[1] + 1), (node[0],node[1] - 1)]
        neighborNames = ['down', 'up', 'right', 'left']
        while len(neighbors) > 0:
            N = neighbors[0]
            direction = neighborNames[0]
            neighbors.pop(0)
            neighborNames.pop(0)
            if inMaze(app, node, N, direction):
                if N not in V:
                    V.add(N)
                    Q.append(N)
                    path[N] = node
    return path

# helper for pathfinding, returns whether a neighbor is in the maze AND
# if the neighbor can be accessed by the node     
def inMaze(app, node, N, direction):
    row, col = N[0], N[1]
    if row >= len(app.mazeList) or row < 0:
        return False
    elif col >= len(app.mazeList[0]) or col < 0:
        return False
    else:
        cell = app.mazeList[node[0]][node[1]]
        if direction == 'up':
            if cell.up != False: return False
            return True
        elif direction == 'down':
            if cell.down != False: return False
            return True
        elif direction == 'left':
            if cell.left != False: return False
            return True
        elif direction == 'right':
            if cell.right != False: return False
            return True
        
# gets repeatedly called to make the coins generate, ouch disappear, 
# enemy move, and check if the player wants to reset            
def onStep(app):
    app.ticks+=1
    if app.ticks % 50 == 0 and len(app.coinList) < app.maxCoins:
        addCoins(app)
    elif app.ouch[0] == True and app.ticks % 50 == 49:
        app.ouch = (False, 0, 0)
    elif app.ticks % 10 == 9:
        if(app.pathList) != []:
            app.clicks += 1
            for i in range(len(app.enemies)):
                app.enemies[i] = app.pathList[i][app.j]
                enemyCheckList = createCheckList(app)
                hurtPlayer(app, enemyCheckList)
            if app.clicks % 3 == 2:
                app.j += 1
    if app.reset == True:
        onAppStart(app)

# draws the title screen    
def drawTitle(app):
    midX = app.width // 2
    midY = app.height // 2
    drawRect(midX // 4, 0, 3*app.width//4, app.height, fill = 'lightBlue')
    drawRect(midX // 2, 3*midY //4, midX, midY//2, fill = 'midnightBlue')
    drawRect(2*midX // 3, 11*midY//8, 2*midX//3, midY//4, 
                fill = 'midnightBlue')
    drawLabel('Save112!', midX, midY - 170, size = 80, bold = True, 
                border = 'midnightBlue', fill = 'aliceBlue')            
    drawLabel('START', midX, midY, size = 60, font = 'orbitron', bold = True, 
                fill = 'aliceBlue')
    drawLabel('HELP', midX, 3*midY//2, size = 30, font = 'orbitron', 
                bold = True, fill = 'aliceBlue')

# draws the maze                 
def drawMaze(app):
    for row in range(len(app.mazeList)):
        for col in range(len(app.mazeList[0])):
            cell = app.mazeList[row][col]
            drawCell(app, cell.row, cell.col, cell.up, cell.down, 
                        cell.left, cell.right)

# helper for drawing the maze; draws each individual cell                        
def drawCell(app, row, col, drawUp, drawDown, drawLeft, drawRight):
    left, top, width, height = getCellBounds(app, row, col)
    right = left + width
    bottom = top + height
    
    if drawUp == True:
        drawLine(left, top, right, top)
        
    if drawDown == True:
        drawLine(left, bottom, right, bottom)
        
    if drawLeft == True:
        drawLine(left, top, left, bottom)
        
    if drawRight == True:
        drawLine(right, top, right, bottom)
            
# draws gridlines that show where the player can move
# CITE: similar to my "hw5 game" Homework fuction "drawGrid"    
def drawGridlines(app):
    for row in range(app.rows):
        for col in range(app.cols):
            
            left, top, width, height = getCellBounds(app, row, col)
            
            drawRect(left, top, width, height, fill=None, border='lightBlue', 
            borderWidth=1)

# "modelToView" function taken from the 112 website notes: "Part 2: Case Studies"
def getCellBounds(app, row, col):
    cellWidth = app.width / app.cols
    cellHeight = app.height / app.rows
    
    left = cellWidth * col 
    top = cellHeight * row
    
    return left, top, cellWidth, cellHeight

# unlocks the end once score is high enough    
def lockedEnd(app):
    if app.score >= app.maxCoins:
        app.lock = False

# checks if power up is available
def powerUp(app):
    if app.score >= app.maxCoins // 2:
        app.power = True


# controller function that changes out of title screen    
def onMousePress(app, mouseX, mouseY):
    midX = app.width // 2
    midY = app.height // 2

    if app.titleScreen == True:
        if mouseX >= midX // 2 and mouseX <= 3 * midX // 2:
            if mouseY >= 3*midY //4 and mouseY <= 5*midY //4:
                formMazeList(app)
                createMaze(app, 0, 0)
                app.titleScreen = False
    
        if mouseX >= 2*midX // 3 and mouseX <= 4*midX // 3:
            if mouseY >= 11*midY//8 and mouseY <= 13*midY//8:
                app.directions = True
    elif app.titleScreen == False and app.difficulty == True:
        if mouseX >= midX // 2 and mouseX <= 3 * midX // 2:
            if mouseY >= midY //3 and mouseY <= 2*midY //3:
                app.diffLevel = 0
                app.difficulty = False
            elif mouseY >= 5*midY//6 and mouseY <= 7*midY//6:
                app.diffLevel = 1
                app.difficulty = False
            elif mouseY >= 8*midY//6 and mouseY <= 5*midY//3:
                app.diffLevel = 2
                app.difficulty = False
            setMaxCoins(app)
            placeEnemies(app)
            app.pathList = enemyAttacks(app)

# creates an enemy checklist of all the enemies cx, cy, row, col            
def createCheckList(app):
    enemyCheckList = []
    for row, col in app.enemies:
            left, top, width, height = getCellBounds(app, row, col)
            enemyCx = left + width // 2
            enemyCy = top + height // 2
            enemyCheckList.append((enemyCx, enemyCy, row, col))
    return enemyCheckList

# controller function that moves player and includes surprises if correct
# key is pressed   
def onKeyPress(app, event):
    if app.directions == True:
        app.directions = False
    elif app.titleScreen == False:
        coinCheckList = []
        enemyCheckList = createCheckList(app)
        for row, col in app.coinList:
            left, top, width, height = getCellBounds(app, row, col)
            coinCx = left + width // 2
            coinCy = top + height // 2
            coinCheckList.append((coinCx, coinCy, row, col))
        
        pRow, pCol = getPlayerRowCol(app)
        cell = app.mazeList[pRow][pCol]
        
        if event == 'space':
            if cell.up == False:
                if isLegal(app, 0, -app.jump):
                    app.cy -= app.jump
                    eatCoins(app, coinCheckList)
                    hurtPlayer(app, enemyCheckList)
                    app.pathList = enemyAttacks(app)
                    app.j = 0
                
        elif event == 'left':
            if cell.left == False:
                if isLegal(app, -app.jump, 0):
                    app.cx -= app.jump
                    eatCoins(app, coinCheckList)
                    hurtPlayer(app, enemyCheckList)
                    app.pathList = enemyAttacks(app)
                    app.j = 0
                
        elif event == 'right':
            if cell.right == False:
                if isLegal(app, app.jump, 0):
                    app.cx += app.jump
                    eatCoins(app, coinCheckList)
                    hurtPlayer(app, enemyCheckList)
                    app.pathList = enemyAttacks(app)
                    app.j = 0
                
        elif event == 'up':
            if cell.up == False:
                if isLegal(app, 0, -app.jump):
                    app.cy -= app.jump
                    eatCoins(app, coinCheckList)
                    hurtPlayer(app, enemyCheckList)
                    app.pathList = enemyAttacks(app)
                    app.j = 0
                
        elif event == 'down':
            if cell.down == False:
                if isLegal(app, 0, app.jump):
                    app.cy += app.jump
                    eatCoins(app, coinCheckList)
                    hurtPlayer(app, enemyCheckList)
                    app.pathList = enemyAttacks(app)
                    app.j = 0
                            
        elif event == 'h':
            app.score += 1
            
        elif event == 'e':
            app.DUBS = True
            
        lockedEnd(app)
        powerUp(app)

        if app.power == True:
            if event == 'p':
                changeRandEnemy(app)
                app.score -= app.maxCoins // 2
                app.power = False

        # all for the end screen
        checkDUBS(app)
        if app.DUBS == True:
            if event == 'r': # resets app only at the end
                app.reset = True
            if event == '5':
                if(app.D == True and app.U == True and app.B == True and 
                app.S == True and app.freddy == True and app.flag == True):
                    app.D = False
                    app.U = False
                    app.B = False
                    app.S = False
                    app.freddy = False
                    app.flag = False
                    app.cd = True
            
            if event == 'f': 
                if(app.D == True and app.U == True and app.B == True 
                and app.S == True and app.freddy == True):
                    app.flag = True
                elif(app.D == True and app.U == True and app.B == True 
                and app.S == True):
                    app.freddy = True
            elif app.D == True and app.U == True and app.B == True:
                app.S = True
            elif app.D == True and app.U == True:
                app.B = True
            elif app.D == True:
                app.U = True
            else:
                app.D = True

# changes the location of a random enemy
# CITE: uses food algorithm from CMU 112 Website (similar to snake) 
def changeRandEnemy(app):
    index = 0
    if len(app.enemies) > 1:
        index = random.randrange(len(app.enemies))
    while True:
        randRow = random.randrange(app.rows)
        randCol = random.randrange(app.cols)
        
        playerRow, playerCol = getPlayerRowCol(app)
        if(playerRow != randRow and playerCol != randCol):
            app.enemies[index] = (randRow, randCol)
            app.pathList = enemyAttacks(app)
            app.j = 0
            return
        
# checks if you made it to the end            
def checkDUBS(app):
    pRow, pCol = getPlayerRowCol(app)
    if pRow == 0 and pCol == app.cols - 1:
        app.DUBS = True

# when a player gets on the same row and col as a coin, it eats it
# CITE: eating food algorithm from CMU 112 Website (similar to snake)         
def eatCoins(app, coinCheckList):
    for cx, cy, row, col in coinCheckList:
        if app.cx == cx and app.cy == cy:
            app.coinList.remove((row, col))
            app.score += 1       

# when a player gets on the same row and col as an enemy, it gets hurts and 
# the enemy dies
# CITE: eating food algorithm from CMU 112 Website (similar to snake)              
def hurtPlayer(app, enemyCheckList):
    for cx, cy, row, col in enemyCheckList:
        if app.cx == cx and app.cy == cy:
            app.enemies.remove((row, col))
            app.score //= 2 
            app.score -= app.maxCoins
            app.ouch = (True, row, col)

# checks whether a move by the player is allowed        
def isLegal(app, changeX, changeY):
    newX = app.cx + changeX 
    newY = app.cy + changeY
    endLeft, endTop, endWidth, endHeight = getCellBounds(app, 0, app.cols-1)
    
    if(newX < app.r or newX > app.width - app.r or newY < app.r or 
        newY > app.height - app.r):
        return False
    elif app.lock == True:
        if(newX < endLeft + endWidth and newX > endLeft 
            and newY < endTop + endHeight and newY > endTop):
            return False
    return True

# draws the coins on the maze 
def drawCoin(app, row, col):
    left, top, width, height = getCellBounds(app, row, col)
    coinCx = left + width // 2
    coinCy = top + height // 2
    radius = width // 3
    drawCircle(coinCx, coinCy, radius, fill = 'lightSalmon')

# draws the enemies on the maze    
def drawEnemy(app, row, col):
    left, top, width, height = getCellBounds(app, row, col)
    enemyCx = left + width // 2
    enemyCy = top + height // 2
    radius = width //2 
    drawCircle(enemyCx, enemyCy, radius, fill = 'fuchsia')

# draws the diffulty screen
def drawDifficulty(app):
    midX = app.width // 2
    midY = app.height // 2
    drawRect(midX // 4, 0, 3*app.width//4, app.height, fill = 'lightBlue')
    drawRect(midX // 2, midY //3, midX, midY//3, fill = 'darkGreen')
    drawRect(midX // 2, 5*midY//6, midX, midY//3, fill = 'gold')
    drawRect(midX // 2, 8*midY//6, midX, midY//3, fill = 'darkRed')
    drawLabel('EASY', midX, midY//2, size = 40, bold = True, 
                fill = 'floralWhite', border = rgb(2, 66, 19))
    drawLabel('MEDIUM', midX, midY, size = 40, bold = True, 
                fill = 'floralWhite', border = rgb(168, 157, 3))
    drawLabel('HARD', midX, 3*midY//2, size = 40, bold = True, 
                fill = 'floralWhite', border = rgb(69, 1, 7))

# draws the direction screen             
def drawDirections(app):
    midX = app.width // 2
    midY = app.height // 2
    drawRect(0, 0, app.width, app.height, fill = 'midnightBlue')
    drawLabel("Directions",midX, midY - 175, size = 30, fill = 'floralWhite',
                bold = True)
    drawLabel("Use the up/space, down, left, right keys to move",midX, 
                midY - 100, size = 20, fill = 'floralWhite', bold = True)
    drawLabel("Collect enough coins so that you unlock 112 lecture!",midX, 
                midY - 50, size = 20, fill = 'floralWhite', bold = True)
    drawLabel("Be wary of enemies who will chase you down",midX, midY, 
                size = 20, fill = 'floralWhite', bold = True)
    drawLabel("and steal your coins!",midX, midY + 50, size = 20, 
                fill = 'floralWhite', bold = True)
    drawLabel("A gold circle will indicate you unlocked your power up!",midX, 
                midY + 100, size = 20, fill = 'floralWhite', bold = True)
    drawLabel("Click 'p' when an enemy is too close!", midX, midY + 150, 
                size = 20, fill = 'floralWhite', bold = True)
    drawLabel("press any key to go back", midX, midY + 250, 
                size = 15, fill = 'floralWhite', bold = True)

# draws the locked cell fill
def drawLockedCell(app):
    endLeft, endTop, endWidth, endHeight = getCellBounds(app, 0, app.cols-1)
    drawRect(endLeft, endTop, endWidth, endHeight, fill = 'red', opacity = 50)
    drawLabel(app.maxCoins - app.score, endLeft + endWidth//2, 
            endTop + endHeight//2, size = 20)

# draws the power up when available
def drawPower(app):
    drawCircle(app.cx, app.cy, app.r//2, fill = 'gold')

# draws the red OUCH!
def drawOuch(app, row, col):
    left, top, width, height = getCellBounds(app, row, col)
    enemyCx = left + width // 2
    enemyCy = top + height // 2
    radius = width //2 
    drawCircle(enemyCx, enemyCy, radius, fill = 'red')
    drawLabel("OUCH", enemyCx, enemyCy, size = 12, fill = "white", bold = True)
    
# CITE: my code from "drawFlagOfTheEU Homework"
def drawFlagOfTheEU(x, y, width, height):
    drawRect(x, y, width, height, fill='mediumBlue') 
    (cx, cy, r) = (x + width/2, y + height/2, min(width, height)/3) 
    # creates the circle of stars in the flag
    for star in range(12):
        starAngle = math.pi/2 - (2*math.pi)*(star/12)
        hourX = cx + r * math.cos(starAngle)
        hourY = cy - r * math.sin(starAngle)
        drawCircle(hourX, hourY, height//25, fill='gold')
    # adds a label, with size and distance depending on flag size
    fontSize = width*height//(height*10)
    drawLabel('European Union', x + width/2, y - fontSize, size = fontSize)
    
    
# CITE: my code from "Freddy Fractal Viewer Homework"    
def drawFreddy(cx, cy, radius):
    border = radius / 10
    dotRadius = radius / 7
    # draws head base
    drawCircle(cx, cy, radius, border = 'black', fill = 'brown', 
                borderWidth = border)
    # draws eyes
    drawCircle(cx - radius / 3, cy - radius/3, dotRadius)
    drawCircle(cx + radius / 3, cy - radius/3, dotRadius)
    # draws snout
    snoutRadius = radius / 2.2
    drawCircle(cx, cy + radius/3, snoutRadius, fill = 'tan', 
                border = 'black', borderWidth = border / 2)
    # draws nose
    drawCircle(cx, cy + dotRadius, dotRadius)
    # draws mouth
    arcWidth = dotRadius * 2
    arcHeight = dotRadius / 2
    drawArc(cx - snoutRadius / 4, cy + radius/4 + dotRadius, dotRadius * 2, 
            dotRadius * 2.5, 90, 180)
    drawArc(cx + snoutRadius / 4, cy + radius/4 + dotRadius, dotRadius * 2, 
            dotRadius * 2.5, 90, 180)
    drawArc(cx - snoutRadius / 4, cy + radius/4 + dotRadius*.9, dotRadius*1.3, 
            dotRadius*2, 90, 180, fill = 'tan')
    drawArc(cx + snoutRadius / 4, cy + radius/4 + dotRadius*.9, dotRadius*1.3, 
            dotRadius*2, 90, 180, fill = 'tan')

# draws the background for dubs
def drawDUBS(app):
    midX = app.width // 2
    midY = app.height // 2
    drawRect(midX // 4, 0, 3*app.width//4, app.height, fill = 'lightBlue')
    drawLabel("press any key to continue", midX, app.height - 40, size = 30)
    drawLabel("press 'r' to reset!", midX, app.height - 10, size = 15)

# draws the D    
def drawD(app):
    drawLabel('D', 150, 120, size = 100, bold = True, fill = 'purple')
    
# draws the U    
def drawU(app):
    drawLabel('U', 250, 220, size = 100, bold = True, fill = 'blue')

# draws the B    
def drawB(app):
    drawLabel('B', 350, 320, size = 100, bold = True, fill = 'green')

# draws the S    
def drawS(app):
    drawLabel('S', 450, 420, size = 100, bold = True, fill = 'red')

# draws Carpe Diem!    
def drawCarpeDiem(app):
    midX = app.width // 2
    midY = app.height // 2
    drawLabel("press 'r' to reset", midX, app.height - 40, size = 50, 
            fill = 'white', border = 'black', bold = True)
    drawLabel("CARPE", midX, midY + 50, size = 100, fill = 'white', 
            border = 'black', bold = True)
    drawLabel("DIEM!!", midX, midY + 150, size = 100, fill = 'white', 
            border = 'black', bold = True)

# the view function
def redrawAll(app):
    if app.titleScreen == True:
        if app.directions == False:
            drawTitle(app)
        else:
            drawDirections(app)
    elif app.difficulty == True:
        drawDifficulty(app)
    elif app.DUBS == True:
        drawDUBS(app)
        if app.D == True:
            drawD(app)
        if app.U == True:
            drawU(app)
        if app.B == True:
            drawB(app)
        if app.S == True:
            drawS(app)
        if app.freddy == True:
            drawFreddy(450, 120, 50)
            drawFreddy(180, 420, 50)
        if app.flag == True:
            drawFlagOfTheEU(100, 70, 200, 100)
            drawFlagOfTheEU(300, 385, 200, 100)
        if app.cd == True:
            image = Image.open("112.png")
            drawImage("112.png", 0, 0, width=app.width, height=app.height)
            drawCarpeDiem(app)
            
    else: 
        drawCircle(app.cx, app.cy, app.r)
        drawGridlines(app)
        drawMaze(app)
        for coinRow, coinCol in app.coinList:
            drawCoin(app, coinRow, coinCol)
        for enemyRow, enemyCol in app.enemies:
            drawEnemy(app, enemyRow, enemyCol)
        if app.lock == True:
            drawLockedCell(app)
        if app.ouch[0] == True:
            drawOuch(app, app.ouch[1], app.ouch[2])
        if app.power == True:
            drawPower(app)
        

def main():
    runApp(width=600, height=600)

main()

