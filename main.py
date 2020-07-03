
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
levelone = [
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
"         GGG        ",
"                    ",
"            MM      ",
"       WWWW         ",
]


x = y = 0
for row in levelone:
    for col in row:
        if col == "W":
            Wall((x, y), black)
        if col == "M":
            Wall((x, y), Mud)
        if col == "G":
            Wall((x, y), Grass)
        #if col == "E":
            #end_rect = pygame.Rect(x, y, 20, 20)
        x += wallSize
    y += wallSize
    x = 0

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

class Player():
    def __init__(self, startX, startY, col, uKey, lKey, rKey):
        self.box = pg.Rect(startX,startY,50,100)
        self.speedx = 0
        self.speedy = 0
        self.colour = col
        self.upKey = uKey
        self.leftKey = lKey
        self.rightKey = rKey
        self.showing = False
        self.onGround = False

    def update( self, planet, keys ):
        self.box[0] += self.speedx
        self.box[1] += self.speedy
        self.speedx = 0
        self.speedy += planet.gv

        if keys[self.leftKey] ==True:
            self.speedx = -9
        elif keys[self.rightKey] ==True:
            self.speedx = 9

        if keys[self.upKey] == True and self.onGround:
            self.speedy = -40

        self.onGround = False # reset onGround flag

        if self.box.top <= 0 and self.speedy < 0: # if touch sky no go thru
            self.speedy = 0
            self.box.top = 0
        if self.box.bottom >= screeny and self.speedy > 0: #IF TOUCH GROUND STAY GROUNDED
            self.speedy = 0
            self.box.bottom = screeny
            self.onGround = True #yes we are on the ground YEET!!
        if self.box.right >= screenx and self.speedx > 0: #IF U TOUCH DA RIGHT WALL NO MOVE PLS
            self.speedx = 0
            self.box.right = screenx
        if self.box.left <= 0 and self.speedx < 0: #NO DRIVE THRU DA LEFT WALL
            self.speedx = 0
            self.box.left = 0

        futurebox = self.box
        futurebox.x += self.speedx
        futurebox.y += self.speedy
        for wall in walls:
            alreadyCollided = self.box.colliderect(wall.rect)
            if futurebox.colliderect(wall.rect):
                if self.speedx > 0: # Moving right; Hit the left side of the wall
                    self.speedx = 0
                    if alreadyCollided:
                        self.box.right = wall.rect.left - 1
                elif self.speedx < 0: # Moving left; Hit the right side of the wall
                    self.speedx = 0
                    if alreadyCollided:
                        self.box.left = wall.rect.right + 1
                if self.speedy > 0: # Moving down; Hit the top side of the wall
                    self.speedy = 0
                    if alreadyCollided:
                        self.box.bottom = wall.rect.top - 1
                        self.onGround = True # on the top of the wall is like on the ground YEET!
                elif self.speedy < 0: # Moving up; Hit the bottom side of the wall
                    self.speedy = 0
                    if alreadyCollided:
                        self.box.top = wall.rect.bottom + 1

        #for wall in walls:
            #if self.box.colliderect(wall.rect):
                #if self.speedx > 0: # Moving right; Hit the left side of the wall
                    #self.box.right = wall.rect.left
                #if self.speedx < 0: # Moving left; Hit the right side of the wall
                    #self.box.left = wall.rect.right
                #if self.speedy > 0: # Moving down; Hit the top side of the wall
                    #self.box.bottom = wall.rect.top
                #if self.speedy < 0: # Moving up; Hit the bottom side of the wall
                    #self.box.top = wall.rect.bottom

        print ( "self {},{}".format( self.box.left , self.box.right ) )

        if self.showing:
            pg.draw.rect(screen,self.colour,self.box)

earth = Planet(bg1, 9.8, "Earth")
moon = Planet(bg2, 1.62, "Moon")
currentPlanet = earth

def level1():
    global level, Dead, currentPlanet, earth, moon, Quit

    player1 = Player(10,250,white, pg.K_UP, pg.K_LEFT, pg.K_RIGHT)
    #player2 = Player(10,250,blue, pg.K_i, pg.K_j, pg.K_l)

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
        #pg.draw.rect(screen, (255, 0, 0), end_rect)
        #pg.draw.rect (screen,Mud, mud)

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