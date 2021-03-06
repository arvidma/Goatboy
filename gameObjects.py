'''
@author: mikael
@author: arvid
'''

import pygame, random, gameLogic, mapLogic, math

class GameObject(pygame.sprite.Sprite):
    x, y = 0, 0
    filename = 'door.bmp'
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = gameLogic.load_image(self.filename, -1)
    def setposition(self, x, y): # Satt blockets startposition
        self.x, self.y = x, y
    def setimage(self, imagename, colorkey):
        self.filename = imagename
        self.image, self.rect = gameLogic.load_image(imagename, colorkey)

class Goatboy(GameObject):
    '''
    This is Goatboy
    '''
    x = 300
    y = 150
    onGround = True    # Star goatboy pa marken?
    turnedRight = True # Ar goatboy vand at hoger?
    rightDown = False  # Ar hogerknappen nedtryckt?
    leftDown = False   # Ar vansterknappen nedtryckt?
    maxspeed = 10 # maxhastighet
    jumpheight = 20 # Hopphojd
    topscroll = 300
    bottomscroll = 400
    leftscroll = 400
    rightscroll = 600
    shooting = False
    weapon = 1
    usedUpSuperShots = 1        # Must start at 1 to avoid DIV/0
    prevMapUsedUpSuperShots = 1 #

    dx = 0    # Goatboys momentana hastighet i x-led
    dy = 0    # -"- y-led
    ddx = 0 # Goatboys acceleration i x-led
    boneRect = pygame.Rect(x + 30, y + 74, 22, 1)    # Bonerect is his feets that are collition tested againts ground later on

    def __init__(self, gameState):            # Initiera goatboy
        pygame.sprite.Sprite.__init__(self)             # Ladda en sprite
        self.image, self.rect = gameLogic.load_image('goatboy.bmp', -1)     # Ladda bilden pa goatboy

    def update(self, gameState):            #  
        gs = gameState
        
        # Testa goatboys ben mot alla block
        if gs.thor.boneRect.collidelist(gs.map.blocks) != -1:
            if gs.thor.dy > 0:             # Om man nuddar ett block pa vagen ner,
                gs.thor.dy = 0             # faller man inte langre nedat
                gs.thor.onGround = True    # och har fotterna pa fast mark.
        else:
            gs.thor.onGround = False       # nuddar man inget block, star man inte pa marken
    
        # Om ens sprite krockar med en elakings, dor man
        if gs.thor.rect.collidelist(gs.map.enemies) != -1:
            gs.thor.die(gs)
        
        # Om man inte krockat med en fiende, men med en dorr, sa beamas man till nasta level
        elif gs.thor.rect.collidelist(gs.map.doors) != -1:
            gs.map.doors[gs.thor.rect.collidelist(gs.map.doors)].open(gs) # Oppna dorren
        
        self.x = self.x + self.dx    # Flytta goatboy i hans horisontella hastighet
        if self.dx < self.maxspeed and self.dx > -self.maxspeed: # Om goatboys maxhastiget inte ar mott,
            self.dx = self.dx + self.ddx             # oka hans hastighet med hans acceleration
            
        self.y = self.y + self.dy    # Flytta goatboy i hans vertikala hastighet
        if self.dy > 100:        # Om goatboy faller fortare an 100
            self.die(gs)           # sa dor han!
            
        if self.shooting:
            if random.randint(1, 2) == 2:
                shot = Shot(gs)
                shot.limit = self.weapon
                shot.dy = random.randint(-self.weapon, self.weapon)
                if shot.dy < 0:
                    shot.ddy = -1
                else:
                    shot.ddy = 1
                gs.map.addShot(shot)
            gameLogic.loadvisible(gs)
            
        # -- This is the frame of goatboys scroll :
        if self.y > self.bottomscroll:
            gs.scrolly = gs.scrolly + (self.bottomscroll - self.y)
            self.y = self.bottomscroll
        elif self.y < self.topscroll:
            gs.scrolly = gs.scrolly - (self.y - self.topscroll)
            self.y = self.topscroll
        if self.x > self.rightscroll:
            gs.scrollx = gs.scrollx + (self.rightscroll - self.x)
            self.x = self.rightscroll
        elif self.x < self.leftscroll:
            gs.scrollx = gs.scrollx - (self.x - self.leftscroll)
            self.x = self.leftscroll
            
        # If goatboy doesn't stand on the ground, he will fall down
        if not self.onGround:
            self.dy = self.dy + 1
        
        #If goatboy is on a moving block, he should be moving along with it
        if self.onGround:
            pass    
        
        self.rect.topleft = self.x, self.y # Satt goatboys sprite till hans nya koordinater
        self.boneRect = pygame.Rect(self.x + 30, self.y + 74, 22, 1)    # Flytta fotterna efter de nya koordinaterna

    def die(self, gameState):
        gameLogic.reset(gameState)

    def move_right(self):
        self.ddx = 1 # Nar goatboy flyttar at hoger ar hans acceleration positiv
        self.rightDown = True     # Hogerknappen ar nedtryckt
        if not self.turnedRight:                    # Om goatboy inte ar vand at hoger, 
            self.image = pygame.transform.flip(self.image, 1, 0)     # vand pa hans bild
            self.turnedRight = True                    # och sag att han e vand at hoger

    def move_left(self):
        self.ddx = -1         # Nar goatboy flyttar at vanster ar hans acceleration negativ
        self.leftDown = True     # vansterknappen ar nedtryckt
        if self.turnedRight:     # Om goatboy ar vand at hoger,
            self.image = pygame.transform.flip(self.image, 1, 0) # vand pa hans bild
            self.turnedRight = False    # goatboy ar inte langre vand at hoger

    def move_up(self):
        if self.onGround:             # Om goatboy star pa marken,
            self.dy = self.dy - self.jumpheight # Hoppa!
            self.onGround = False         # Goatboy star inte langre pa marken

    def move_down(self):
        self.dy = self.dy + 1

    def stop(self):                      # stop() kallas da man slapper hoger eller vanster.
        if self.rightDown and self.ddx == -1: # Om goatboy ar pa vag at vanster men trycker at hoger,
            self.dx = self.dx / 2          # halvera goatboys hastighet.
            self.rightDown = False          # Goatboy slutar trycka
        elif self.leftDown and self.ddx == 1: # Vice versa.
            self.dx = self.dx / 2
            self.leftDown = False
        else:
            self.dx = 0    # Goatboys hastighet ar noll
            self.ddx = 0    # Goatboys acceleration ar noll
            self.rightDown = False # hoger ar inte nedtryckt
            self.leftDown = False  # vanster ar inte nedtryckt

    def get_x(self):
        return self.x

    def changeweapon(self):
        self.weapon = (self.weapon + 2) % 16

    def get_y(self):
        return self.y
    
    def superShot(self, gameState):
        if (gameState.scoore / self.usedUpSuperShots) < 10:
            return
        
        self.usedUpSuperShots += 1
        
        for i in range(1,36):
            shot = FancyShot(gameState=gameState, angle=( 2*math.pi ) * i/36 )
            gameState.map.addShot(shot)


class Flamenemy(GameObject):
    '''
    Flamenemy-classen
    '''
    x = 0
    y = 0
    kind = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = gameLogic.load_image('flamenemy.bmp', -1) # Ladda default-bild
        self.dx, self.dy = random.randint(-10, 10), random.randint(-5, 5)
        self.ddx, self.ddy = 1, -1

    def update(self, gameState):
        self.x = self.x + self.dx
        self.dx = self.dx + self.ddx
        self.y = self.y + self.dy
        self.dy = self.dy + self.ddy
        if self.dx > 20 or self.dx < -20: # Om blocket ar utanfor vandpunkterna,
            self.ddx = -self.ddx
            self.image = pygame.transform.flip(self.image, 1, 0)                  # byt hall.
        if self.dy > 10 or self.dy < -10: # Om blocket ar utanfor vandpunkterna,
            self.ddy = -self.ddy    
        self.rect.topleft = self.x + gameState.scrollx, self.y + gameState.scrolly # Flytta blockets sprite i forhallande till scrollen

    def reset(self):
        self.dx, self.dy, self.ddx, self.ddy = random.randint(-10, 10), random.randint(-5, 5), 1, -1 #random.randint(-1,1),random.randint(-1,1)

    def die(self, gameState):
        gameState.scoore = gameState.scoore + 1
        gameState.map.enemies.remove(self)

class Flameboy(GameObject):
    '''
    Flameboy
    '''
    kind = 1
    filename = 'flameboy.bmp'
    onGround = False
    range = 400
    life = 20
    limit = random.randint(4, 7)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = gameLogic.load_image(self.filename, -1) 
        self.dx, self.ddx, self.dy, self.ddy = 1, -1, 1, 0

    def update(self, gameState):
        gs = gameState
        
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.dx = self.dx + self.ddx
        if not self.onGround:
            self.dy = self.dy + 1
        if self.dx > self.limit or self.dx < -self.limit:
            self.ddx = -self.ddx
            self.limit = random.randint(4, 7)
            if self.onGround:
                self.dy = -random.randint(5, 15)
                if self.x + gs.scrollx < gs.thor.x + self.range and self.x + gs.scrollx > gs.thor.x - self.range and self.y + gs.scrolly < gs.thor.y + self.range and self.y + gs.scrolly > gs.thor.y - self.range:
                    enemy = Flamenemy()
                    enemy.setposition(self.x - 100, self.y)
                    gs.map.addEnemy(enemy)
                    gameLogic.loadvisible(gs)
        if self.dy > 100:
            print "flameboy fell down"
            gs.map.enemies.remove(self)
            gameLogic.loadvisible(gs)
        if self.rect.collidelist(gs.map.blocks) != -1:
            if self.dy > 0:
                self.dy, self.ddy = 0, 0
                self.onGround = True
        else:
            self.onGround = False
        self.rect.topleft = self.x + gs.scrollx, self.y + gs.scrolly

    def reset(self):
        self.dx, self.dy, self.ddx, self.ddy = 1, -1, 1, 0
        self.onGround = False

    def die(self, gameState):
        self.life = self.life - 1
        if self.life < 1:
            gameState.scoore = gameState.scoore + 1
            gameState.map.enemies.remove(self)
            gameLogic.loadvisible(gameState)
        else:
            self.dy = -10


class Block(GameObject):
    '''
    Block-classen
    '''
    x = 0
    y = 0
    rightlimit = 1000000    # Default-varde for blockets hogra vandpunkt da det ar rorligt
    leftlimit = -1000000    # -"- vanstra -"-
    dx = 0
    filename = 'blockgrass.bmp'
    gs = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = gameLogic.load_image(self.filename, -1) # Ladda default-bild
        self.dx = 0

    def update(self, gameState):
        self.x = self.x + self.dx
        if self.rect.w + self.x > self.rightlimit or self.x < self.leftlimit: # Om blocket ar utanfor vandpunkterna,
            self.dx = -self.dx                          # byt hall.
        self.rect.topleft = self.x + gameState.scrollx, self.y + gameState.scrolly # Flytta blockets sprite i forhallande till scrollen

    def setdx(self, dx):
        self.dx = dx # Blockets horisontella hastighet

    def setlimits(self, leftlimit, rightlimit): # Satt blockets vandpunkter
        self.leftlimit = leftlimit
        self.rightlimit = rightlimit


class Shot(GameObject):
    '''
    Shot classen .. d e ett skott
    '''
    filenames = ['shot.bmp', 'oldshot.bmp']
    images = []
    imagenr = 0
    range = 400

    def __init__(self, gameState):
        gs = gameState
        pygame.sprite.Sprite.__init__(self)
        for filename in self.filenames:
            image, self.rect = gameLogic.load_image(filename, -1)
            self.images.append(image)
        self.image = self.images[0]
        self.x, self.y = gs.thor.x - gs.scrollx, gs.thor.y + 30 - gs.scrolly
        self.dy, self.ddy = random.randint(-6, 6), random.randint(-1, 1)
        if gs.thor.turnedRight:
            self.dx = 15
            self.x = self.x + 40
        else:
            self.dx = -15

    def update(self, gameState):
        gs = gameState

        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.dy = self.dy + self.ddy
        self.imagenr = (self.imagenr + 1) % len(self.filenames)
        self.image = self.images[self.imagenr]    
        if self.dy > self.limit or self.dy < -self.limit:
            
            self.ddy = -self.ddy
        self.rect.topleft = self.x + gs.scrollx, self.y + gs.scrolly
        if self.x + gs.scrollx > gs.thor.x + self.range  or self.x + gs.scrollx < gs.thor.x - self.range:
            gs.map.shots.remove(self) # ta bort skottet fran listan i kartan o hopppas garbagecollectorn fixar biffen
            gameLogic.loadvisible(gs)
        elif self.rect.collidelist(gs.map.enemies) != -1:
            gs.map.shots.remove(self)
            gs.map.enemies[self.rect.collidelist(gs.map.enemies)].die(gs)
            gameLogic.loadvisible(gs)

class FancyShot(GameObject):
    gameState = None
    angle = None
    velocity = None
    timeToLive = None   # Antal frames som skottet ar vid liv. Range ar ttl*velocity
    filenames = ['shot.bmp', 'oldshot.bmp']
    images = []
    imagenumber = 0    
    x = 0
    y = 0
    dx = 0
    dy = 0
    
    def __init__(self, gameState, angle=0.25, velocity=15, timeToLive=30):
        pygame.sprite.Sprite.__init__(self)
        self.gameState = gameState
        self.angle = angle
        self.velocity = velocity        
        self.timeToLive = timeToLive

        for filename in self.filenames:
            image, self.rect = gameLogic.load_image(filename, -1)
            self.images.append(image)
        self.image = self.images[0]
        
        self.x = self.gameState.thor.x - self.gameState.scrollx
        self.y = self.gameState.thor.y + 30 - self.gameState.scrolly
        
        self.dx = int( math.cos(self.angle) * self.velocity )
        self.dy = int( math.sin(self.angle) * self.velocity )
        
    def update(self, knarg=None):
        if self.timeToLive == 0:
            self.gameState.map.shots.remove(self)
            return
        
        if self.rect.collidelist(self.gameState.map.enemies) != -1:
            self.gameState.map.shots.remove(self)
            self.gameState.map.enemies[self.rect.collidelist(self.gameState.map.enemies)].die(self.gameState)

        self.image = self.images[ (self.imagenumber) % ( len(self.images) ) ]
        self.imagenumber += 1
        
        self.x += self.dx
        self.y += self.dy    
        self.timeToLive -= 1

        self.rect.topleft = (self.x + self.gameState.scrollx, self.y + self.gameState.scrolly)

class Door(GameObject):
    '''
    Door class
    '''
    filename = 'door.bmp'
    targetMap = None

    def __init__(self, targetMap=None):
        GameObject.__init__(self)

        if self.targetMap == None:
            self.targetMap = 'map' + str( gameLogic.getHighestMapNumber() ) + '.map'
        else:
            self.targetMap = targetMap

    def update(self, gameState):
        self.rect.topleft = self.x + gameState.scrollx, self.y + gameState.scrolly

    def open(self, gameState):
        gameState.scoreFromPreviousLevel = gameState.scoore
        gameState.thor.prevMapUsedUpSuperShots = gameState.thor.usedUpSuperShots        
        gameState.map = mapLogic.Map()
        gameState.map.loadmap(self.targetMap)
        gameState.mapname = self.targetMap
        gameLogic.reset(gameState)

    def setTargetDoor(self, targetNum):
        self.targetMap = 'map' + str( targetNum ) + '.map'


