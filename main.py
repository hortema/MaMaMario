
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

squarex = 0
squarey = 0

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

    def update( self, location ):
        self.box[0] += self.speedx
        self.box[1] += self.speedy
        self.speedx = 0
        self.speedy += location.gv

earth = Planet(bg1, 9.8, "Earth")
moon = Planet(bg2, 1.62, "Moon")
currentLocation = earth

def updatePlayer( player, keys ):
    if keys[player.leftKey] ==True:
        player.speedx = -10
    elif keys[player.rightKey] ==True:
        player.speedx = 10

    if keys[player.upKey] == True and player.box[1] >= 600 - player.box[3]:
        player.speedy = -60

    if player.box[1]<= 0 and player.speedy < 0:
        player.speedy = 0
        player.box[1] = 0
        # if touch sky no go thru
    if player.box[1] >= 600 - player.box[3] and player.speedy > 0:
        player.speedy = 0
        player.box[1] = 600 - player.box[3]
        #IF TOUCH GROUND STAY GROUNDED
    if (player.box[0] + player.box[2]) >= 800 and player.speedx > 0:
        player.speedx = 0
        player.box[0] = 800 - player.box[2]
        #IF U TOUCH DA RIGHT WALL NO MOVE PLS
    if player.box[0] <= 0 and player.speedx < 0:
        player.speedx = 0
        player.box[0] = 0
        #NO DRIVE THRU DA LEFT WALL

def level1():
    global level, squarex, squarey, box, Dead, currentLocation, earth, moon

    player1 = Player(375,250,white, pg.K_w, pg.K_a, pg.K_d)
    player2 = Player(10,250,blue, pg.K_i, pg.K_j, pg.K_l)

    while level == 0:
        pg.event.pump()

        #box[0] += squarex
        #box[1] += squarey
        player1.update(currentLocation)
        player2.update(currentLocation)


        #inputs
        mx,my = pg.mouse.get_pos()
        L,M,R = pg.mouse.get_pressed() #1/0 : 1-pressed
        keys = pg.key.get_pressed()

        #events

        #squarex = 0

        #squarey += currentLocation.gv
        #gravity

        updatePlayer(player1, keys)
        updatePlayer(player2, keys)

        if keys[pg.K_e] ==True:
            currentLocation = earth
        if keys[pg.K_m] ==True:
            currentLocation = moon
        screen.blit(currentLocation.bg, (0,0))
        pg.display.flip


        #pg.draw.rect (screen,Mud, mud)

        pg.draw.rect(screen,player1.colour,player1.box)
        pg.draw.rect(screen,player2.colour,player2.box)
        pg.display.flip()

        clock.tick(30)
while True:
    if level == 0:
        level1()
    if level == 1:
        pass