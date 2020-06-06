
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


box = pg.Rect(375,250,50,100)
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

earth = Planet(bg1, 9.8, "Earth")
moon = Planet(bg2, 1.62, "Moon")
currentLocation = earth

def level1():
    global level, squarex, squarey, box, Dead, currentLocation, earth, moon

    while level == 0:
        pg.event.pump()

        box[0] += squarex
        box[1] += squarey

        #inputs
        mx,my = pg.mouse.get_pos()
        L,M,R = pg.mouse.get_pressed() #1/0 : 1-pressed
        keys = pg.key.get_pressed()

        #events

        squarex = 0

        squarey += currentLocation.gv
        #gravity

        if keys[pg.K_a] ==True:
            squarex = -10
        elif keys[pg.K_d] ==True:
            squarex = 10
        #elif keys[pg.K_s] == True:
            #squarey = 10
        if keys[pg.K_w] == True and box[1] >= 600 - box[3]:
            squarey = -60

        if box[1]<= 0 and squarey < 0:
            squarey = 0
            box[1] = 0
            # if touch sky no go thru
        if box[1] >= 600 - box[3] and squarey > 0:
            squarey = 0
            box[1] = 600 - box[3]
            #IF TOUCH GROUND STAY GROUNDED
        if (box[0] + box[2]) >= 800 and squarex > 0:
            squarex = 0
            box[0] = 800 - box[2]
            #IF U TOUCH DA RIGHT WALL NO MOVE PLS
        if box[0] <= 0 and squarex < 0:
            squarex = 0
            box[0] = 0
            #NO DRIVE THRU DA LEFT WALL

        #else:
            #squarex = 0
            #squarey = 20
            #boxColour = (158, 54, 179)

        if keys[pg.K_e] ==True:
            currentLocation = earth
        if keys[pg.K_m] ==True:
            currentLocation = moon
        screen.blit(currentLocation.bg, (0,0))
        pg.display.flip


        #pg.draw.rect (screen,Mud, mud)

        pg.draw.rect(screen,white,box)

        pg.display.flip()

        clock.tick(30)
while True:
    if level == 0:
        level1()
    if level == 1:
        pass