# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 14:14:48 2020

@author: 612754070
"""


import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
import pygame_menu

pygame.init()

pygame.display.set_caption("Charlotte's Snake Game") #Names the game in the pop up window

from pygame import mixer

mixer.music.load('pacman.wav')

mixer.music.play(-1) #-1 means that the sound plays continuously


class cube(object): #This class defines the 'snake' head/body as an object
    rows = 20
    w = 700
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,255)): #This makes my snakes body purple. Maps the starting position
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,255,0), circleMiddle, radius) #Draws eye 1
            pygame.draw.circle(surface, (0,255,0), circleMiddle2, radius) #Draws eye 2
        



class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos) #shape of head is a cube and this defines the front of the head
        self.body.append(self.head)
        self.dirnx = 0 #Direction the snake is moving for X axis
        self.dirny = 1 #Direction the snake is moving for Y axis

    def move(self):
        for event in pygame.event.get():#creates a list of all the events happen - all the movements of the player e.g. keyboard press
            if event.type == pygame.QUIT:#This checks all the events that happens and if the player clicks exit.
                pygame.quit()
# This loop means we can run the game at this stage and the pop up box wont close until the player clicks the red exit button

            keys = pygame.key.get_pressed()  #makes note of what key has been pressed in the game
#Below shows what direction the shape needs to move on the grid when differet keys are pressed.
            for key in keys:
                if keys[pygame.K_a]:#Left direction
                    self.dirnx = -1 #Change direction according to what key is pressed
                    self.dirny = 0 #0 so we only move one direction. X axis doesnt move
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] #We have a new turn at position, and this is the direction to move

                elif keys[pygame.K_d]: #Right direction
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_w]:#Up direction
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_s]:#Down direction
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
#elif makes sure that the player can only use one key at a time
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
               if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
               elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
               elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
               elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
               else: c.move(c.dirnx,c.dirny) # If we haven't reached the edge just move in our current direction
        

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        tail = self.body[-1] #Finds the last cube in the list
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:#Checks the direction of the last cube to work out where to place the next, new one.
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:#Draws eyes if it's the first cube
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows #Distance between the lines

    x = 0 #Keeps track of the X
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w)) #Draws 2 white lines every loop in the for loop
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
        

def redrawWindow(surface):
    global rows, width, s, food
    surface.fill((0,0,0)) #Makes the screen display black
    s.draw(surface)
    food.draw(surface)
    drawGrid(width,rows, surface)
    pygame.display.update()


def randomFood(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, food
    width = 700
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,255), (10,10))
    food = cube(randomFood(rows, s), color=(255,200,0))
    flag = True

    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(55) #delays prgramme by 55miliseconds so doesn't run too fast
        clock.tick(11)#means game doesn't run more than 10fps. Slows the snake
        s.move()
        if s.body[0].pos == food.pos:
            s.addCube()#Adds a new cube if there is a collision with the food
            food = cube(randomFood(rows, s), color=(255,200,0))

        for x in range(len(s.body)):#Makes sure that if the snake hits itself the game ends
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('Oh no, You Lost!', 'Try again...')
                s.reset((10,10))
                break

            
        redrawWindow(win)


      
main()
