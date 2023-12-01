# This file was created by Sean Daly

'''

'''
#Goals
'''
Make the screen move up with the player
Make the level end onces the player reaches the final platform
Add platforms that move vertically as well as horizontally
Make a new level in a new "dimension" with a background and different looking mobs
'''

# This file was created by Sean Daly
# content from kids can code: http://kidscancode.org/blog/
# Mr. Cozort in class
# Teo during free period

'''
Goals: Reach the rainbow platform
Rules: move in the air and don't fall to the bottom of the map
Feedback: can view player hp/points
Freedom: run side to side, jump, drop


When Mobs are hit, players loses a point
Add different platforms
When player has 0 points, the player respawns
Player can't move off the screen: when moving left, player respawns right and visa versa
'''

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
import math


vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

 

class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        # defines the screen and display for the game while the code is running
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        # create a group for all sprites
        # defines the score of the player
        self.score = 10
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_ice_plats = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)

        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
        
        # provides the coordinates for the "ice" platform
        self.ice_plat = Ice(self, 222, 200, 100, 20, "normal")
        self.all_sprites.add(self.ice_plat)
        self.all_platforms.add(self.ice_plat)
        self.all_ice_plats.add(self.ice_plat)

        for m in range(0,5):
            # this generates 5 random "mobs" across the screen
            m = Mob(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
            # gives mobs their own sprite or class
            self.all_sprites.add(m)
            self.all_mobs.add(m)

        self.run()
    

    def run(self):
        # while the program is running, the program is checking for updates across events updates and draw
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #I am changing something sala
        # moves them up when player is in the top 4th of screen
        if self.player.rect.y < HEIGHT/4:
            for p in self.all_platforms:
                p.vel.y = -self.player.vel.y

        # checks on number of plats and adds more if needed (based in killing plats of screen...)
        if len(self.all_platforms) < 6:
            for i in range(1,3):
                plat = Platform(randint(0,WIDTH), 0, 200, 35, "moving", (255,255,255))
                self.all_sprites.add(plat)
                self.all_platforms.add(plat)

        self.all_sprites.update()
        # defines that the game updates if a player collides with a mob
        mhits = pg.sprite.spritecollide(self.player, self.all_mobs, False)
        # if the player hits a mob, they lose 1 point.
        if mhits:
            print('this collision happened in main')
            self.score -= 1
            # if the player's score becomes 0, they respawn at the beginning with 10 points
            if self.score == 0:
                self.player.pos = vec(WIDTH/2, HEIGHT/2)
                self.score = 10

        # these lines of code make the player go from the left side to right side of the screen and visa versa (like pacman or doodlejump)
        if self.player.pos.x < 0:
            self.player.pos.x = WIDTH
        if self.player.pos.x > WIDTH:
            self.player.pos.x = 0
        
        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed*1.5

                    
         # this prevents the player from jumping up through a platform
        elif self.player.vel.y <= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_mobs, False)
            if hits:
                self.player.acc.y = 5
                self.player.vel.y = 0
                print("ouch")
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom
                if self.player.rect.top <= hits[0].rect.top - 1:
                    self.player.rect.bottom = hits[0].rect.bottom
            
        ice_collide  = pg.sprite.collide_rect(self.player, self.ice_plat)
        if ice_collide:
            print("collided....")
            # this makes sure it doesn't register as tagged multiple times
            if self.ice_plat.tagged == False:
                self.ice_plat.cd.event_reset()
                # print("the delta is " + str(self.ice_plat.cd.delta))
                print("tagged...FALSE")
                self.ice_plat.tagged = True
                

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLACK)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/10)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    # this deinfes the text that will appear on the screen in our case for the score
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass



g = Game()
while g.running:
    g.new()
    

