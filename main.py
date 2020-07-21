#v1.5
import pygame as pg
import sys

from sys import path
from sys import exit
import os

from pygame.locals import QUIT


#my_path = os.path.dirname(os.path.realpath(__file__))
#os.chdir(my_path)
#path.append(my_path)

#Colours
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
cookie = (171,119,36)
Grass = (41,204,109)
Mud = (128,74,52)
LAVABLE = (255,100,0)


#box = pg.Rect(375,250,50,100)
boxColour = (158, 54, 179)
mouse = pg.Rect(100,100,0,0)
mud = pg.Rect(0,550,800,50)

wallSize = 40
screenx = 800
screeny = 600

my_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(my_path)
path.append(my_path)

class Wall(object):
    def __init__(self, pos, color):
        walls.append(self)
        self.rect = pg.Rect(pos[0], pos[1], wallSize, wallSize)
        self.color = color

#Setup

pg.init()
screen = pg.display.set_mode((screenx,screeny)) #set your window size, (x,y)
pg.display.set_caption("Finite State Machines")
clock = pg.time.Clock()

walls = []
L3V3L = []

levelone = [
"S                   ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"       WWWW        E",
]

leveltwo = [
"S                   ",
"                    ",
"                    ",
"                    ",
"                    ",
"            E       ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"       WWWW         ",
"       WWWW         ",
"WWWWWWWWWWWWWWWWWWWW",
]

levelthree = [
"S                   ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                   E",
"WWWWWWWLLLLWWWWWWWWW",
]

levelfour = [
"S                   ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"                    ",
"   WWWWWWWWWWWWWWWWW",
"   W                ",
"   W                ",
"   W                ",
"   WW   WWWWWWWWW   ",
"        WWWWWWWWW   ",
"        WWWWWWWWWW  ",
"WWWWWWWWWWWWWWWWWWEE",
]

levelnone = [
"S W                 ",
"  W                 ",
"  W                 ",
"  W    WWWWW        ",
"  W    W   W        ",
"  W    W E W        ",
"  W    W   W        ",
"  WWWWWWWWWWWWWWWWWW",
"                   W",
"                   W",
"                   W",
"                   W",
"                   W",
"                   W",
"WWWWWWWWWWWWWWWWWWWW",
]

L3V3L.append(levelone)
L3V3L.append(leveltwo)
L3V3L.append(levelthree)
L3V3L.append(levelfour)
L3V3L.append(levelnone)
print(len(L3V3L))
LEVELNum = 0

end_rect = pg.Rect(0, 0, 40, 40)

class Player():
    WIDTH = 50
    HEIGHT = 100
    CROUTCH = 10

    def __init__(self, startX, startY, col, uKey, lKey, rKey, dKey, inSurface):
        self.box = pg.Rect(startX,startY,Player.WIDTH,Player.HEIGHT)
        self.speedx = 0
        self.speedy = 0
        self.colour = col
        self.upKey = uKey
        self.leftKey = lKey
        self.rightKey = rKey
        self.downKey = dKey
        self.showing = False
        self.onGround = False
        self.oldboxsurface = inSurface
        self.crouching = False

    def update( self, planet, keys ):
        if keys[self.leftKey] ==True:
            self.speedx = -10
        elif keys[self.rightKey] ==True:
            self.speedx = 10

        if keys[self.upKey] == True and self.onGround:
            self.speedy = -50

        if keys[self.downKey] == True and self.onGround and self.crouching == False:
            self.box.height = Player.CROUTCH
            self.box.top += Player.HEIGHT-Player.CROUTCH
            self.crouching = True
        elif keys[self.downKey] == False and self.crouching == True:
            self.box.height = Player.HEIGHT
            self.box.top -= Player.HEIGHT-Player.CROUTCH
            self.crouching = False


        self.onGround = False # reset onGround flag

        futureboxX = pg.Rect(self.box)
        futureboxX.x += self.speedx
        futureboxX.union_ip(self.box)
        futureboxY = pg.Rect(self.box)
        futureboxY.y += self.speedy
        futureboxY.union_ip(self.box)

        for wall in walls:
            fXCollided = futureboxX.colliderect(wall.rect)
            fYCollided = futureboxY.colliderect(wall.rect)
            if self.speedx > 0 and fXCollided: # Moving right; Hit the left side of the wall
                self.speedx = 0
                self.box.right = wall.rect.left
            elif self.speedx < 0 and fXCollided: # Moving left; Hit the right side of the wall
                self.speedx = 0
                self.box.left = wall.rect.right
            if self.speedy > 0 and fYCollided: # Moving down; Hit the top side of the wall
                self.speedy = 0
                self.box.bottom = wall.rect.top
                self.onGround = True # on the top of the wall is like on the ground YEET!
            elif self.speedy < 0 and fYCollided: # Moving up; Hit the bottom side of the wall
                self.speedy = 0
                self.box.top = wall.rect.bottom

        if futureboxY.top <= 0 and self.speedy < 0: # if touch sky no go thru
            self.speedy = 0
            self.box.top = 0
        elif futureboxY.bottom >= screeny and self.speedy > 0: #IF TOUCH GROUND STAY GROUNDED
            self.speedy = 0
            self.box.bottom = screeny
            self.onGround = True #yes we are on the ground YEET!!
        if futureboxX.right >= screenx and self.speedx > 0: #IF U TOUCH DA RIGHT WALL NO MOVE PLS
            self.speedx = 0
            self.box.right = screenx
        elif futureboxX.left <= 0 and self.speedx < 0: #NO DRIVE THRU DA LEFT WALL
            self.speedx = 0
            self.box.left = 0

        oldBox = pg.Rect(self.box)
        self.box[0] += self.speedx
        self.box[1] += self.speedy
        if self.onGround:
            self.speedx = 0
        else:
            self.speedy += planet.gv

        if self.showing:
            #pg.draw.rect(screen,(100,100,100),oldBox)
            screen.blit(self.oldboxsurface, (oldBox.x, oldBox.y) )
            pg.draw.rect(screen,self.colour,self.box)
            futureboxY.width -= Player.WIDTH-10
            futureboxY.x += (Player.WIDTH-10)/2
            #pg.draw.rect(screen,(255,200,200),futureboxY)
            futureboxX.height -= Player.HEIGHT-10
            futureboxX.y += (Player.HEIGHT-10)/2
            #pg.draw.rect(screen,(200,255,200),futureboxX)

def ChangeLevel(newlevel):
    global LEVELNum
    if newlevel > len(L3V3L):
        LEVELNum = levelnone
    walls.clear()
    LEVELNum = newlevel

    playerx = 0
    playery = 0

    x = y = 0
    for row in L3V3L[LEVELNum]:
        for col in row:
            if col == "W":
                Wall((x, y), black)
            if col == "M":
                Wall((x, y), Mud)
            if col == "G":
                Wall((x, y), Grass)
            if col == "L":
                Wall((x, y), LAVABLE)
            if col == "S":
                playerx = x
                playery = y
            if col == "E":
                #end_rect = pg.Rect(x, y, 40, 40)
                end_rect.x = x
                end_rect.y = y
            x += wallSize
        y += wallSize
        x = 0
    return(playerx,playery)
ChangeLevel(0)

bg1 = pg.image.load("BG1.jpg")
bg2 = pg.image.load("CMON.png")

class Planet():
    def __init__(self, inBG, inGv, inName):
        self.bg = inBG
        self.gv = inGv
        self.name = inName
level = 0
Dead = 1

Quit = 0

def printBox( box, name ):
    print("{}, x={}, y={}, w={}, h={} t={} b={}".format( name, box.x, box.y, box.w, box.h, box.top, box.bottom ) )

grey = pg.image.load("TransparentGrey30.png")
grey2 = pg.transform.scale(grey, (Player.WIDTH, Player.HEIGHT))

earth = Planet(bg1, 9.8, "Earth")
moon = Planet(bg2, 1.62, "Moon")
currentPlanet = earth

def level1():
    global level, Dead, currentPlanet, earth, moon, Quit, LEVELNum

    player1 = Player(10,250,white, pg.K_UP, pg.K_LEFT, pg.K_RIGHT, pg.K_DOWN, grey2)
    #player2 = Player(10,250,blue, pg.K_i, pg.K_j, pg.K_l, grey2)

    while level == 0:
        pg.event.pump()

        screen.blit(currentPlanet.bg, (0,0))

        #inputs
        mx,my = pg.mouse.get_pos()
        L,M,R = pg.mouse.get_pressed() #1/0 : 1-pressed
        keys = pg.key.get_pressed()

        #events
        for event in pg.event.get():
        #for every event in the list return by pg.event.get()
            if event.type == pg.locals.QUIT:
                Quit = 1
                return

        #gravity

        if keys[pg.K_e] ==True:
            currentPlanet = earth
        if keys[pg.K_m] ==True:
            currentPlanet = moon

        #if keys[pg.K_1] ==True:
        player1.showing = True
        #if keys[pg.K_2] ==True:
        #player2.showing = True
        player1.update(currentPlanet, keys)
        #player2.update(currentPlanet, keys)

        for wall in walls:
            pg.draw.rect(screen, wall.color, wall.rect)
            pg.draw.rect(screen, (255, 0, 0), end_rect)
        #pg.draw.rect (screen,Mud, mud)

        if player1.box.colliderect(end_rect):
            print(LEVELNum)
            player1.box.topleft = ChangeLevel(LEVELNum + 1)


        pg.display.flip()

        clock.tick(30)

while True:

    if level == 0:
        level1()
    if level == 1:
        pass

    if Quit == 1:
        pg.quit()
        break