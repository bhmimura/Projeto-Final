# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 17:24:36 2015

@author: marcelotanak
"""

import pygame
from pygame import *
#import pyganim

#=========Display======#
WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30


#=========Game main==#
def main():
    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    timer = pygame.time.Clock()
    currentLevel = 0

    up = down = left = right = running = False


    bg = Surface((32,32))
    #bg = pygame.image.load('BG\BGL1.png').convert()
    bg.fill(Color("#000000"))
    entities = pygame.sprite.Group()
    player = Player(32, 55)




    levels = [[
        "",
        "",
        "",
        "",
        "",
        "SSSSSSSSSSSSSSSS",
        "PPPPPPPPPSSSSSSS          ",
        " ",
        "                                                     

        ],
        [
        "",
        "",
        "",
        "",
        "PPPPPPPPPPPP",
        "PPPPPPPPPPPP"
        ]]


        # Level Generating code 
    def load_level(level):
        platforms = []
        x = y = 0
        for row in levels:
            for col in row:
                if col == "P":
                    p = Platform(x, y)
                    platforms.append(p)
                    entities.add(p)
                if col == "E":
                    e = ExitBlock(x, y)
                    platforms.append(e)
                    entities.add(e)
                if col == "G":
                    g = Platform1(x, y)
                    platforms.append(g)
                    entities.add(g)
                if col == "A":
                    a = Stone(x, y)
                    platforms.append(a)
                    entities.add(a)
                if col == "S":
                    s = Stone0(x, y)
                    platforms.append(s)
                    entities.add(s)
                if col == "H":
                    h = HalfPlaform0(x, y)
                    platforms.append(h)
                    entities.add(h)
                if col == "B":
                    b = StoneBack(x, y)
                    entities.add(b)
                if col == "T":
                    t = Bridge(x,y)
                x += 32
            y += 32
            x = 0
        return platforms, entities

    platforms, entities = load_level(currentLevel)
    load_level(currentLevel)




    total_levels_width  = len(levels[0])*32
    total_levels_height = len(levels)*32
    camera = Camera(complex_camera, total_levels_width, total_levels_height)
    entities.add(player)



    while 1:

        load_level(currentLevel)
        timer.tick(60)


        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit("ESCAPE")
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                running = True
            if e.type == KEYUP and e.key == K_l:
                currentLevel += 1
                load_level(currentLevel)
                print(level)

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False







        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))


        ##Update player, draw everything else##
        ###THE PROBLEM IS HERE I THINK###

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        '''
        BegimoAnim.anchor(anchorPoint = 'east')
        BegimoAnim.blit(screen, (player))
        '''


        camera.update(player)
        pygame.display.update()
        player.update(up, down, left, right, running, platforms)





class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           ## stop scrolling at the left edge##
    #l = max(-(camera.width-WIN_WIDTH), l)   ## stop scrolling at the right edge##
    t = max(-(camera.height-WIN_HEIGHT), t) ## stop scrolling at the bottom##
    t = min(0, t)                           ## stop scrolling at the top##
    return Rect(l, t, w, h)


#============PLAYER===============#
right_standing = pygame.image.load('PlayerModels\Sprites\PlayerStill2.gif')
left_standing = pygame.transform.flip(right_standing, True, False)
animTypes = 'right_walk'.split()

'''
BegimoAnim = pyganim.PygAnimation([
    ('PlayerModels\Sprites\Player_right_walk1.gif', 0.2,),
    ('PlayerModels\Sprites\Player_right_walk2.gif', 0.2,),
                                    ])
'''

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface = right_standing
        self.rect = self.image.get_rect()
    def update(self, up, down, left, right, running, platforms):
        a = 0
        #BegimoAnim.blit(screen, (player))
        if up:
            # Pasokti tik ant zemes
            if self.onGround: self.yvel -= 7
        if down:
            pass
        if running:
            self.xvel = 12
        if left:
            self.xvel = -5
            self.image = left_standing
        if right:
            self.xvel = 5
            self.image = right_standing




            #BegimoAnim.play()

        if not self.onGround:
            # gravitacija + acceleracija
            self.yvel += 0.3
            # Max kritimo greitis
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # Prieaugis X direkcijoje
        self.rect.left += self.xvel
        # daryti X axis collision
        self.collide(self.xvel, 0, platforms)
        # Prieaugis Y direkcijoje
        self.rect.top += self.yvel
        # Ar ore?
        self.onGround = False;
        # daryti Y axis collision
        self.collide(0, self.yvel, platforms)



    def collide(self, xvel, yvel, platforms):
        level = 0
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    currentLevel += 1
                    walls, players, finishes = load_level(currentLevel)
                    print(level)
                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

#=========Platforms, ground
class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface =  pygame.image.load("GroundModels\Ground0.png").convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class Platform1(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface =  pygame.image.load("GroundModels\Ground.png").convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass
#================stone
class Stone(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface = pygame.image.load("GroundModels\Stone.png").convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class Stone0(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface = pygame.image.load("GroundModels\Stone0.png").convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class StoneBack(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface = pygame.image.load("GroundModels\Stone.png").convert()
        self.rect = Rect(x, y, 32, 32)


class Bridge(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)

    def update(self):
        pass
#=================pusblokis zeme
class HalfPlaform0(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface =  pygame.image.load("GroundModels\HalfGround0.png").convert()
        self.rect = Rect(x, y + 16, 32, 16)


    def update(self):
        pass


class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))

if __name__ == "__main__":
    main()