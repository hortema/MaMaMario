
import pygame as pg

from sys import path
from sys import exit
import os

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
Grass = (41, 204, 109)
Mud = (128, 74, 52)


#box = pg.Rect(375,250,50,100)
boxColour = (158, 54, 179)
mouse = pg.Rect(100,100,0,0)
mud = pg.Rect(0,550,800,50)

screenx = 800
screeny = 600

my_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(my_path)
path.append(my_path)

#Setup

pg.init()
screen = pg.display.set_mode((screenx,screeny)) #set your window size, (x,y)
pg.display.set_caption("Finite State Machines")
clock = pg.time.Clock()

bg1 = pg.image.load("BG1.jpg")
bg2 = pg.image.load("CMON.png")

class Planet():
    def __init__(self, inBG, inGv, inName):
        self.bg = inBG
        self.gv = inGv
        self.name = inName
level = 0
Dead = 1

class Player():
    def __init__(self, startX, startY, col, uKey, lKey, rKey):
        self.box = pg.Rect(startX,startY,50,100)
        self.speedx = 0
        self.speedy = 0
        self.colour = col
        self.upKey = uKey
        self.leftKey = lKey
        self.rightKey = rKey

    def update( self, planet, keys ):
        self.box[0] += self.speedx
        self.box[1] += self.speedy
        self.speedx = 0
        self.speedy += planet.gv

        if keys[self.leftKey] ==True:
            self.speedx = -10
        elif keys[self.rightKey] ==True:
            self.speedx = 10

        if keys[self.upKey] == True and self.box[1] >= screeny - self.box[3]:
            self.speedy = -60

        if self.box[1]<= 0 and self.speedy < 0:
            self.speedy = 0
            self.box[1] = 0
            # if touch sky no go thru
        if self.box[1] >= screeny - self.box[3] and self.speedy > 0:
            self.speedy = 0
            self.box[1] = screeny - self.box[3]
            #IF TOUCH GROUND STAY GROUNDED
        if (self.box[0] + self.box[2]) >= screenx and self.speedx > 0:
            self.speedx = 0
            self.box[0] = screenx - self.box[2]
            #IF U TOUCH DA RIGHT WALL NO MOVE PLS
        if self.box[0] <= 0 and self.speedx < 0:
            self.speedx = 0
            self.box[0] = 0
            #NO DRIVE THRU DA LEFT WALL

        pg.draw.rect(screen,self.colour,self.box)

earth = Planet(bg1, 9.8, "Earth")
moon = Planet(bg2, 1.62, "Moon")
currentPlanet = earth

def level1():
    global level, Dead, currentPlanet, earth, moon

    player1 = Player(375,250,white, pg.K_w, pg.K_a, pg.K_d)
    player2 = Player(10,250,blue, pg.K_i, pg.K_j, pg.K_l)

    while level == 0:
        pg.event.pump()

        screen.blit(currentPlanet.bg, (0,0))



        #inputs
        mx,my = pg.mouse.get_pos()
        L,M,R = pg.mouse.get_pressed() #1/0 : 1-pressed
        keys = pg.key.get_pressed()

        #events

        #gravity

        player1.update(currentPlanet, keys)
        player2.update(currentPlanet, keys)

        if keys[pg.K_e] ==True:
            currentPlanet = earth
        if keys[pg.K_m] ==True:
            currentPlanet = moon

        #pg.draw.rect (screen,Mud, mud)

        pg.display.flip()

        clock.tick(30)

while True:
    if level == 0:
        level1()
    if level == 1:
        pass