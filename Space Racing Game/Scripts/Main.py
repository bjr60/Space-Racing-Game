import pygame, sys, random, math, pickle
from collections import deque
class User:
    def __init__(self, x, y):
        self.position = pygame.Vector2()
        self.position.xy = x,y
        self.direction = pygame.Vector2()
        self.direction.xy = x,y
        self.size = pygame.Vector2()
        self.size.xy = 50,50
        self.playerRect = pygame.Rect(self.position.x,self.position.y,self.size.x,self.size.y)
    def updateUserMovement(self,playerVel, wallCollision):
        self.direction.x = 0
        self.direction.y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.position.x > 0 and wallCollision != "Left Hit":
            self.direction.x = -1
        if keys[pygame.K_RIGHT]  and self.position.x < width-self.size.x and wallCollision != "Right Hit":
            self.direction.x = 1
        if keys[pygame.K_UP] and self.position.y > 0 and wallCollision != "Top Hit":
            self.direction.y = -1
        if keys[pygame.K_DOWN] and self.position.y < height-self.size.y and wallCollision != "Bottom Hit":
            self.direction.y = 1
        self.position.xy = (self.position.x + self.direction.x*playerVel, self.position.y + self.direction.y*playerVel)
    def drawPlayer(self):
        self.playerRect = pygame.Rect(self.position.x,self.position.y,self.size.x,self.size.y)
        screen.blit(bebop,self.playerRect)
        #pygame.draw.rect(screen, [255,255,255], self.playerRect)
    def checkWallCollision(self,wallList):
        for walls in wallList:
            if self.playerRect.colliderect(walls.topWall):
                hit = self.renderWallCollision(1, walls)
                return hit
            if self.playerRect.colliderect(walls.bottomWall):
                hit = self.renderWallCollision(2, walls)
                return hit
        return False
    def renderWallCollision(self, wallNum, walls):
        #An interesting attempt worth keeping
        """
        wallCorners = [[0,0],[0,0],[0,0],[0,0]]
        if wallNum == 1:
            wallCorners[0] = walls.position1.x,walls.position1.y
            wallCorners[1] = walls.position1.x+walls.size1.x,walls.position1.y
            wallCorners[2] = walls.position1.x,walls.position1.y+walls.size1.y
            wallCorners[3] = walls.position1.x+walls.size1.x,walls.position1.y+walls.size1.y
        if wallNum == 2:
            wallCorners[0] = walls.position2.x,walls.position2.y
            wallCorners[1] = walls.position2.x+walls.size2.x,walls.position2.y
            wallCorners[2] = walls.position2.x,walls.position2.y+walls.size2.y
            wallCorners[3] = walls.position2.x+walls.size2.x,walls.position2.y+walls.size2.y
        """
        overlaps = [0,0,0,0] #TopOverlap,RightOverlap,LeftOverlap,BottomOverlap
        if wallNum == 1:
            wallPosX = walls.position1.x
            wallPosY = walls.position1.y
            wallSizeX = walls.size1.x
            wallSizeY = walls.size1.y
        else:
            wallPosX = walls.position2.x
            wallPosY = walls.position2.y
            wallSizeX = walls.size2.x
            wallSizeY = walls.size2.y
        overlaps[0] = wallPosY - (self.position.y+self.size.y) #top-bottom will neg
        overlaps[1] = (wallPosX + wallSizeX) - self.position.x #right-left will pos
        overlaps[2] = wallPosX - (self.position.x+self.size.x) #left-right will neg
        overlaps[3] = (wallPosY + wallSizeY) - self.position.y #bottom-top will pos
        #top of wall collision (bottom of object)
        if overlaps[0] <= 0 and abs(overlaps[0])<wallSizeY:
            if overlaps[1] >= 0 and abs(overlaps[1]) < wallSizeX:
                if abs(overlaps[1])>=abs(overlaps[0]):
                    return "Bottom Hit"
                elif abs(overlaps[1])<=abs(overlaps[0]):
                    return "Left Hit"
            elif overlaps[2] <= 0 and abs(overlaps[2]) < wallSizeX:
                if abs(overlaps[2])>=abs(overlaps[0]):
                    return "Bottom Hit"
                elif abs(overlaps[2])<=abs(overlaps[0]):
                    return "Right Hit"
            else:
                return "Bottom Hit"
        if overlaps[3] >= 0 and abs(overlaps[3])<wallSizeY:
            if overlaps[1] >= 0 and abs(overlaps[1]) < wallSizeX:
                if abs(overlaps[1])>=abs(overlaps[3]):
                    return "Top Hit"
                elif abs(overlaps[1])<=abs(overlaps[3]):
                    return "Left Hit"
            elif overlaps[2] <= 0 and abs(overlaps[2]) < wallSizeX:
                if abs(overlaps[2])>=abs(overlaps[3]):
                    return "Top Hit"
                elif abs(overlaps[2])<=abs(overlaps[3]):
                    return "Right Hit"
            else:
                return "Top Hit"
        """
        playerCorners = [[0,0],[0,0],[0,0],[0,0]]
        playerCorners[0] = self.position.x,self.position.y
        playerCorners[1] = self.position.x+self.size.x,self.position.y
        playerCorners[2] = self.position.x,self.position.y+self.size.y
        playerCorners[3] = self.position.x+self.size.x,self.position.y+self.size.y
        """
    def checkDeath(self, gapEnemyList, normEnemyList, enemyProjectileList):
        for enemies in gapEnemyList:
            if self.playerRect.colliderect(enemies.gapEnemyRect):
                return True
        for enemies in normEnemyList:
            if self.playerRect.colliderect(enemies.normEnemyRect):
                return True
        for projectiles in enemyProjectileList:
            if self.playerRect.colliderect(projectiles.projectileRect):
                return True
        return False
        
class wall:
    def __init__(self, lengthList):
        lengthOpen = random.choice(lengthList)
        self.size1 = pygame.Vector2()
        self.size1.xy = 100,random.randint(0,height-lengthOpen)
        self.size2 = pygame.Vector2()
        self.size2.xy = 100, height-(self.size1.y+lengthOpen)
        self.position1 = pygame.Vector2()
        self.position1.xy = 800, 0
        self.position2 = pygame.Vector2()
        self.position2.xy = 800, self.size1.y+lengthOpen
        self.pointGiven = False
        self.wallSurface = asteroidSurface
        self.topWall = pygame.Rect(self.position1.x,self.size1.y-800,self.size1.x,800)
        self.bottomWall = pygame.Rect(self.position2.x,self.position2.y,self.size2.x,800)
    def updateWall(self,screenVel):
        self.position1.x = self.position1.x-screenVel
        self.position2.x = self.position2.x-screenVel
    def drawWall(self):
        self.topWall = pygame.Rect(self.position1.x,self.size1.y-800,self.size1.x,800)
        self.bottomWall = pygame.Rect(self.position2.x,self.position2.y,self.size2.x,800)
        screen.blit(self.wallSurface,self.topWall)
        screen.blit(self.wallSurface,self.bottomWall)
        #pygame.draw.rect(screen, [255,255,255], self.topWall)
        #pygame.draw.rect(screen, [255,255,255], self.bottomWall)
        
class Projectile:
    def __init__(self, x, y, dx, dy, projVel):
        self.position = pygame.Vector2()
        self.position.xy = x,y
        self.direction = pygame.Vector2()
        self.direction.xy = dx,dy
        self.size = pygame.Vector2()
        self.size.xy = 10,10
        self.projectileVel = projVel
        self.projectileRect = pygame.Rect(self.position.x,self.position.y,self.size.x,self.size.y)
    def updateProjectile(self):
        self.position.xy = (self.position.x + self.direction.x*self.projectileVel, self.position.y + self.direction.y*self.projectileVel)
    def drawProjectile(self):
        self.projectileRect = pygame.Rect(self.position.x,self.position.y,self.size.x,self.size.y)
        pygame.draw.rect(screen, [255,0,0], self.projectileRect)
    def wallCollision(self, wallList):
        for walls in wallList:
            if self.projectileRect.colliderect(walls.topWall):
                return True
            if self.projectileRect.colliderect(walls.bottomWall):
                return True
        return False
class gapEnemy:
    def __init__(self, x, y):
        self.position = pygame.Vector2()
        self.position.xy = x,y
        self.direction = pygame.Vector2()
        self.direction.xy = x,y
        self.size = pygame.Vector2()
        self.size.xy = 40,40
        self.gapEnemySurf = random.choice(evilShips)
        self.gapEnemyRect = pygame.Rect(self.position.x,self.position.y,self.size.x,self.size.y)
    def updateGapEnemy(self, screenVel):
        self.direction.x = -1
        self.direction.y = 0
        self.position.xy = (self.position.x + self.direction.x*screenVel, self.position.y)
    def drawGapEnemy(self):
        self.gapEnemyRect = pygame.Rect(self.position.x,self.position.y,self.size.x,self.size.y)
        screen.blit(self.gapEnemySurf,self.gapEnemyRect)
        #pygame.draw.rect(screen, [255,255,0], self.gapEnemyRect)
    def projectileCollision(self, projectileList):
        for projectiles in projectileList:
            if self.gapEnemyRect.colliderect(projectiles.projectileRect):
                return True, projectiles
        return False, None
    def shootProjectile(self):
        dx = player.position.x-self.position.x
        dy = player.position.y-self.position.y
        dxNorm = dx/(((dx**2)+(dy**2))**(1/2))
        dyNorm = dy/(((dx**2)+(dy**2))**(1/2))
        enemyProjectileList.append(Projectile(self.position.x+15,self.position.y+15,dxNorm,dyNorm,enemyProjVel))
class normEnemy:
    def __init__(self, x, y):
        self.position = pygame.Vector2()
        self.position.xy = x,random.choice([200,350,500])
        self.direction = pygame.Vector2()
        self.direction.xy = x,y
        self.moved = 0
        self.setMoves = [random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400]),random.choice([75,150,200,300,400])]
        self.firstDirection = random.randint(0,1)
        if self.firstDirection == 1:
            self.setDirections = [1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1]
        else:
            self.setDirections = [-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1]
        self.counter = 0
        self.enemyVel = random.randint(2, 6)
        self.size = pygame.Vector2()
        self.size.xy = 75,75
        self.normEnemySurf = random.choice(evilNormEnemyShips)
        self.normEnemyRect = pygame.Rect(self.position.x,self.position.y,self.size.x,self.size.y)
    def updateNormEnemy(self, screenVel):
        self.direction.x = -1
        self.direction.y = self.directionChange()
        self.position.xy = (self.position.x + self.direction.x*screenVel, self.position.y + self.direction.y*self.enemyVel)
        self.moved=self.moved+abs(self.direction.y*self.enemyVel)
    def directionChange(self):
        if self.counter >= 13:
            return 0
        if self.moved >= self.setMoves[self.counter]:
            self.counter = self.counter+1
            self.moved = 0
        if self.counter >= 13:
            return 0
        return self.setDirections[self.counter]
    def drawNormEnemy(self):
        self.normEnemyRect = pygame.Rect(self.position.x,self.position.y,self.size.x,self.size.y)
        screen.blit(self.normEnemySurf,self.normEnemyRect)
        #pygame.draw.rect(screen, [255,255,0], self.normEnemyRect)
    def projectileCollision(self, projectileList):
        for projectiles in projectileList:
            if self.normEnemyRect.colliderect(projectiles.projectileRect):
                return True, projectiles
        return False, None
    def shootProjectile(self):
        dx = player.position.x-self.position.x
        dy = player.position.y-self.position.y
        dxNorm = dx/(((dx**2)+(dy**2))**(1/2))
        dyNorm = dy/(((dx**2)+(dy**2))**(1/2))
        enemyProjectileList.append(Projectile(self.position.x+25,self.position.y+25,dxNorm,dyNorm,self.enemyVel*random.choice([1,1.5])))

def bg():
    screen.blit(bg_surface,(bgX + width,0))
    screen.blit(bg_surface,(bgX,0))
#Turn this into a class  
"""  
def lootbox():
    loot = random.randint(1,100)
    
    if loot <=10:
        pygame.draw.rect(screen, [0,255,0], ammoRect)
    elif loot <=20:
        pygame.draw.rect(screen, [0,0,255], gasRect)
    elif loot <=30:
        pygame.draw.rect(screen, [0,255,255], cowRect)
"""
class Lootbox:
    def __init__(self, x, loot):
        self.position = pygame.Vector2()
        self.position.xy = x,random.choice([50,100,200,350,400,525,625,675])
        self.size = pygame.Vector2()
        self.loot = loot
        self.lootType = ""
        if self.loot <=10:
            self.lootType = "Ammo"
            self.lootSurface = ammoSurface
        elif self.loot <=20:
            self.lootType = "Gas"
            self.lootSurface = gasSurface
        elif self.loot <=30:
            self.lootType = "Cow"
            self.lootSurface = random.choice(cowSurfaces)
        self.size.xy = 50,50
        self.lootRect = pygame.Rect(self.position.x,self.position.y,self.size.x,self.size.y)
    def updateLoot(self, screenVel):
        self.position.x = self.position.x - screenVel
    def drawLoot(self):
        self.lootRect = pygame.Rect(self.position.x,self.position.y,self.size.x,self.size.y)
        screen.blit(self.lootSurface,self.lootRect)
        #pygame.draw.rect(screen, [0,255,0], self.lootRect)
        #pygame.draw.rect(screen, [0,0,255], self.lootRect)
        #pygame.draw.rect(screen, [0,255,255], self.lootRect)
    def userLootCollision(self):
        if self.lootRect.colliderect(player.playerRect):
            return True
        return False
    def projectileCollision(self, projectileList):
        for projectiles in projectileList:
            if self.lootRect.colliderect(projectiles.projectileRect):
                return True, projectiles
        return False, None


def mainGame(dt,bgX, gamePlay, deathMenu, ammo, gasToScreen, rawScore, cows, gas):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and ammo>0:
            ammo = ammo-1
            playerProjectileList.append(Projectile(player.position.x+player.size.x,player.position.y+(.5*player.size.y),1,0, playerProjVel))
    #Game Paramaters
    screenVel = dt/10+1
    playerVel = 5
    wallCollision = player.checkWallCollision(wallList)
    if wallCollision == "Right Hit":
        dt = 0
        screenVel = 0
        playerVel = 2
    #Move background
    bgX -= screenVel
    bg()
    #Randomize Game Events like enemies and loot based on background location
    if bgX <= -750:
        wallList.append(wall(lengthOpenings))
        if random.randint(1,2) == 1:
            temp = (wallList[-1].position2.y - (wallList[-1].position1.y+wallList[-1].size1.y))/2
            gapEnemyList.append(gapEnemy(wallList[-1].position2.x+35, wallList[-1].position2.y - temp - 15))
        if random.randint(1,5) == 1:
            normEnemyList.append(normEnemy(max(random.randint(wallList[-1].position2.x+150,wallList[-1].position2.x+700),random.randint(wallList[-1].position2.x+150,wallList[-1].position2.x+700)),375))
        loot = random.randint(1,100)
        if loot <= 30:
            lootList.append(Lootbox(random.randint(wallList[-1].position2.x+150,wallList[-1].position2.x+700),loot))
        bgX = 0
    dt = dt+(1/120)
    
    #Create Player
    player.updateUserMovement(playerVel, wallCollision)
    player.drawPlayer()
    deathMenu = player.checkDeath(gapEnemyList, normEnemyList, enemyProjectileList)
    if gas == 0:
        deathMenu = True
    if deathMenu == True:
        gamePlay = False
    
    #Create our Projectiles
    for projectiles in playerProjectileList:
        projectiles.updateProjectile()
        projectiles.drawProjectile()
        if projectiles.position.x >= 750:
            playerProjectileList.remove(projectiles)
            continue
        if projectiles.wallCollision(wallList) == True:
            playerProjectileList.remove(projectiles)
            continue
        
    #Create Loot
    for loots in lootList:  
        loots.updateLoot(screenVel)
        loots.drawLoot()
        if loots.position.x<=-150:
            lootList.remove(loots)
            continue
        if loots.userLootCollision()==True:
            if loots.lootType == "Ammo":
                ammo = ammo + 10
            elif loots.lootType == "Gas":
                gas = gas+6000
            elif loots.lootType == "Cow":
                cows = cows+1
            lootList.remove(loots)
            continue
        lootHit, projectileUsed = loots.projectileCollision(playerProjectileList)
        if lootHit:
            lootList.remove(loots)
            playerProjectileList.remove(projectiles)
            continue
    
    #Create Gap Enemies
    for gapEnemies in gapEnemyList:
        gapEnemies.updateGapEnemy(screenVel)
        gapEnemies.drawGapEnemy()
        if gapEnemies.position.x<=-150:
            gapEnemyList.remove(gapEnemies)
            continue
        gapEnemyHit, projectileUsed = gapEnemies.projectileCollision(playerProjectileList)
        if gapEnemyHit:
            gapEnemyList.remove(gapEnemies)
            playerProjectileList.remove(projectiles)
            continue
        if random.randint(1,50) == 1:
            gapEnemies.shootProjectile()
    
    #Create normal Enemies
    for normEnemies in normEnemyList:
        normEnemies.updateNormEnemy(screenVel)
        normEnemies.drawNormEnemy()
        if normEnemies.position.x<=-150:
            normEnemyList.remove(normEnemies)
            continue
        normEnemyHit, projectileUsed = normEnemies.projectileCollision(playerProjectileList)
        if normEnemyHit:
            normEnemyList.remove(normEnemies)
            playerProjectileList.remove(projectiles)
            continue
        if random.randint(1,30) == 1:
            normEnemies.shootProjectile()
    
    #Create Enemy Projectiles
    for projectiles in enemyProjectileList:
        projectiles.updateProjectile()
        projectiles.drawProjectile()
        if projectiles.position.x <= 0 or projectiles.position.x >= 750:
            enemyProjectileList.remove(projectiles)
            continue
        if projectiles.position.y <= 0 or projectiles.position.y >= 750:
            enemyProjectileList.remove(projectiles)
            continue
        if projectiles.wallCollision(wallList) == True:
            enemyProjectileList.remove(projectiles)
            continue
    
    #Create astroid belt
    dequeNumber = 0
    for walls in wallList:
        walls.updateWall(screenVel)
        if walls.position1.x<player.position.x and walls.pointGiven == False:
            rawScore+=1
            walls.pointGiven = True
        if walls.position1.x<=-150:
            dequeNumber += 1
        walls.drawWall()
    for i in range(0,dequeNumber):
        wallList.popleft()
        
    #print game variables
    font = pygame.font.SysFont('arial',15)
    text = font.render("Score: " + str(rawScore) + " x " + str(cows+1),True,[255,255,255])
    textRect = text.get_rect()
    textRect.topleft = (5,5)
    screen.blit(text, textRect)
    font = pygame.font.SysFont('arial',15)
    text = font.render("Gas: " + str(gasToScreen),True,[255,255,255])
    textRect = text.get_rect()
    textRect.topleft = (5,20)
    screen.blit(text, textRect)    
    font = pygame.font.SysFont('arial',15)
    text = font.render("Ammo: " + str(ammo),True,[255,255,255])
    textRect = text.get_rect()
    textRect.topleft = (5,35)
    screen.blit(text, textRect)
        
    return dt, bgX, gamePlay, deathMenu, ammo, cows, gas, rawScore

def menuScreen(mainMenu,gamePlay,bgX):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            mainMenu = False
            gamePlay = True
    bgX -= 1
    bg()
    if bgX <= -750:
        bgX=0
    font = pygame.font.SysFont('arial',100)
    text = font.render("Main Menu",True,[255,255,255])
    textRect = text.get_rect()
    textRect.center = (375,375)
    screen.blit(text, textRect)
    font = pygame.font.SysFont('arial',40)
    text = font.render("Press Space to Start",True,[255,255,255])
    textRect = text.get_rect()
    textRect.center = (375,425)
    screen.blit(text, textRect)
    return mainMenu,gamePlay, bgX

def deathScreen(deathMenu,mainMenu,bgX, totalScore):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            deathMenu = False
            mainMenu = True
    bgX -= 1
    bg()
    #Randomize Game Events like enemies and loot based on background location
    if bgX <= -750:
        bgX=0
    font = pygame.font.SysFont('arial',30)
    text = font.render("...Goodbye Space Cowboy",True,[255,255,255])
    textRect = text.get_rect()
    textRect.center = (500,675)
    screen.blit(text, textRect)
    font = pygame.font.SysFont('arial',30)
    text = font.render("Final Score: " + str(totalScore),True,[255,255,255])
    textRect = text.get_rect()
    textRect.center = (375,375)
    screen.blit(text, textRect)
    with open('../HighScore.pkl', 'rb') as file:
        highScore = pickle.load(file)
    text = font.render("High Score: " + str(highScore),True,[255,255,255])
    textRect = text.get_rect()
    textRect.center = (375,425)
    screen.blit(text, textRect)
    if highScore<totalScore:
        pickle.dump(totalScore, open('../HighScore.pkl','wb'))
    return deathMenu,mainMenu, bgX
    

pygame.init()
width,height = 750,750
screen = pygame.display.set_mode((width,height)) #Size of game screen
#frame rate limit set up
clock = pygame.time.Clock()

#surfaces
bg_surface = pygame.transform.scale(pygame.image.load('../assets/stars-colored-orange.png').convert(),[width,height])
asteroidSurface = pygame.image.load('../assets/asteroids.png').convert_alpha()
evilShip1 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('../assets/evilShip1.png').convert_alpha(),[50,50]),90)
evilShip2 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('../assets/evilShip2.png').convert_alpha(),[50,50]),90)
evilShip3 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('../assets/evilShip3.png').convert_alpha(),[50,50]),-90)
evilShips = [evilShip1,evilShip2,evilShip3]
bebop = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('../assets/bebop.png').convert_alpha(),[50,50]),-90)
evilNormShip1 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('../assets/evilNormShip1.png').convert_alpha(),[100,100]),-90)
evilNormShip2 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('../assets/evilNormShip2.png').convert_alpha(),[100,100]),-90)
evilNormShip3 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('../assets/evilNormShip3.png').convert_alpha(),[100,100]),-90)
evilNormEnemyShips = [evilNormShip1,evilNormShip2,evilNormShip3]
coolCow = pygame.transform.scale(pygame.image.load('../assets/coolCow.png').convert_alpha(),[75,75])
machineGunCow = pygame.transform.flip(pygame.transform.scale(pygame.image.load('../assets/machineGunCow.png').convert_alpha(),[75,75]),True,False)
gattlingGunCow = pygame.transform.scale(pygame.image.load('../assets/cowgattling gun.png').convert_alpha(),[100,100])
cowSurfaces = [coolCow,machineGunCow,gattlingGunCow]
ammoSurface = pygame.transform.scale(pygame.image.load('../assets/ammo.png').convert_alpha(),[75,75])
gasSurface = pygame.transform.scale(pygame.image.load('../assets/gas.png').convert_alpha(),[75,75])

#Screens
mainMenu = True
gamePlay = False
deathMenu = False


#Game Variables
playerVel = 5
playerProjVel = 15
enemyProjVel = 5
screenVel = 1
bgX = 0
dt = 0
ammo = 20
gas = 6000
gasToScreen = round(gas/120)
cowsCollected = 0
rawScore = 0
totalScore = 0

#Main Blocks
player = User(375,375)
wallList = deque()
lengthOpenings = [75,100,150,200]
playerProjectileList = []
gapEnemyList = []
normEnemyList = []
enemyProjectileList = []
lootList = []

while True:
    if mainMenu:
        mainMenu,gamePlay,bgX = menuScreen(mainMenu,gamePlay,bgX)
    if gamePlay:
        dt,bgX,gamePlay,deathMenu, ammo, cowsCollected,gas, rawScore = mainGame(dt,bgX,gamePlay,deathMenu, ammo, gasToScreen, rawScore, cowsCollected,gas)
        gas -= 1
        gasToScreen = round(gas/120)
        totalScore = rawScore*(cowsCollected+1)
    if deathMenu:
        player = User(375,375)
        dt = 0
        wallList = deque()
        playerProjectileList = []
        gapEnemyList = []
        normEnemyList = []
        enemyProjectileList = []
        lootList = []
        ammo = 20
        gas = 6000
        gasToScreen = round(gas/120)
        rawScore = 0
        cowsCollected = 0
        deathMenu,mainMenu,bgX = deathScreen(deathMenu,mainMenu,bgX, totalScore)
        
    pygame.display.update()
    clock.tick(120)