# This file was created by Sean Daly

'''

'''
#Goals
'''
Make the screen move up with the player
Make the level end onces the player reaches the final platform
Add platforms that move vertically as well as horizontally
Make a new level in a new "dimension" with a background
'''

# This file was created by Sean Daly
# content from kids can code: http://kidscancode.org/blog/
# Mr. Cozort in class
# Teo LeClaire
# Alex Aguerria
# https://www.youtube.com/watch?v=j9yMFG3D7fg
# chat.gpt

'''
Goals: Reach the rainbow platform 
Rules: move in the air and don't fall to the bottom of the map
Feedback: can view player hp/points
Freedom: run side to side, jump, drop


When Mobs are hit, players loses a point
Add different platforms
When player has 0 points, the player respawns
Player can't move off the screen: when moving left, player respawns right and visa versa
Player can move up on the screen

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
        # instantiate a level counter
        self.current_level = 1
        
    
    def new_level(self):
        print("Entering new level")
        # Code to initialize a new level
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_ice_plats = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()

        # Instantiate classes and add instances to groups for the new level
        self.player = Player(self)
        self.player.update_level(self.current_level)
        self.all_sprites.add(self.player)

        # Create platforms for the new level
        for p in PLATFORM_LIST_NEW_LEVEL:
            plat = Platform(*p)
            # Sets up the current_level for each platform
            plat.current_level = self.current_level
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        # Create ice platforms for the new level
        for i in ICE_PLATFORM_LIST_NEW_LEVEL:
            ice = Ice(self, *i)
            # Sets up the current_level for each ice platform
            ice.current_level = self.current_level
            self.all_sprites.add(ice)
            self.all_platforms.add(ice)
            self.all_ice_plats.add(ice)

        # Create mobs for the new level
        for m in MOB_LIST_NEW_LEVEL:
            mob = Mob(*m)
            # Sets up the current_level for each mob
            mob.current_level = self.current_level
            self.all_sprites.add(mob)
            self.all_mobs.add(mob)

        #Update the player's level
        self.player.update_level(self.current_level)

        # adds 1 to the current level
        self.current_level += 1

        print("exiting new level" )
        self.run()


        

    def new(self):
        # create a group for all sprites
        # defines the score of the player
        self.background_stars = pg.image.load(os.path.join(img_folder, 'stars.jpg')).convert()
        self.background_earth = pg.image.load(os.path.join(img_folder, 'earth.jpg')).convert()
        #self.background_rect = self.background.get_rect()
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

        for m in range(0,8):
            # this generates 8 random "mobs" across the screen
            m = Mob(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
            # gives mobs their own sprite or class
            self.all_sprites.add(m)
            self.all_mobs.add(m)
        for m in range (0,7):
            # this generates 7 random mobs above the y-intercept from the original screen
            m = Mob(randint(0, WIDTH), randint(-math.floor(HEIGHT/2),0), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)

        self.run()
    

    def run(self):
        print("Current Level:", self.current_level)
        # while the program is running, the program is checking for updates across events updates and draw
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            
            # fill the screen yellow for the second level
            if self.current_level == 2:
                self.screen.fill(BLACK)
                self.screen.blit(self.background_earth, (0,0))
            elif self.current_level == 1:
                self.screen.fill(BLACK)
                self.screen.blit(self.background_stars, (0,0))
            
            self.update()
            
            self.all_sprites.draw(self.screen)
            self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/10)
            
            # Displays "You Win" once the third level is reached
            if self.current_level == 3:
                self.draw_text("You Win!", 100, WHITE, WIDTH/2, HEIGHT/2)
                self.draw_text("Exit to play again!", 50, WHITE, WIDTH/2, HEIGHT/2 + 200)

                #pg.time.delay(2000)
                #self.playing = False
        
            pg.display.flip()

    def update(self):
        # moves them up when player is in the top 4th of screen
        if self.player.rect.top <= HEIGHT / 4:
            # changes the y value of the player to become the absolute Y value.
            self.player.pos.y += abs(self.player.vel.y)
            # this adjusts the y positions of the platforms to keep them down
            for plat in self.all_platforms:
                plat.rect.y += abs(self.player.vel.y)
            # this adjusts the y positions of the mobs to keep them down
            for mob in self.all_mobs:
                mob.rect.y += abs(self.player.vel.y)
        
        # Check if the player hits the platform with the category "new level"
        new_level_hit = pg.sprite.spritecollide(self.player, self.all_platforms, False, pg.sprite.collide_rect)
        if new_level_hit:
            #print("Collided with platform:", new_level_hit[0].category)
            if new_level_hit[0].category == "new level":
                self.new_level()
                print("Entering new level")
                self.current_level += 1
        

        # checks on number of plats and adds more if needed (based in killing plats of screen...)
        if len(self.all_platforms) < 6:
            for i in range(1):
                plat = Platform(randint(0,WIDTH-10),-10, 50, 20, "moving",)
                self.all_sprites.add(plat)
                self.all_platforms.add(plat)
            for i in range(1):
                plat = Platform(randint(0,WIDTH-10), -200, 50, 20, "new level")
                self.all_sprites.add(plat)
                self.all_platforms.add(plat)
            # adds an additional ice platform
            for i in range(1):
                ice = Ice(self, randint(0, WIDTH-10), -100, 50, 20, "moving",)
                self.all_sprites.add(ice)
                self.all_platforms.add(ice)
        if len(self.all_mobs) < 6:
            for i in range(0,15):
                m = Mob(randint(0, WIDTH), randint(-(HEIGHT/2),0), 20, 20, "normal")
                # gives mobs their own sprite or class
                self.all_sprites.add(m)
                self.all_mobs.add(m)

            

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
        #self.screen.fill(BLACK)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/10)
        # displays the level for the player
        self.draw_text("Level:" + str(self.current_level), 22, WHITE, WIDTH/2, (HEIGHT/10)+50)
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
    

