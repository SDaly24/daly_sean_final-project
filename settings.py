# This file was created by: Chris Cozort
# Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0 

from random import randint
import math

# game settings 
WIDTH = 1024
HEIGHT = 768
FPS = 30

# player settings
PLAYER_JUMP = 30
PLAYER_GRAV = 1.5
PLAYER_FRIC = 0.2

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# gives the coordinates for the platforms and their platform "type"
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40, "normal"),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20,"normal"),
                 (125, HEIGHT - 350, 100, 20, "moving"),
                 #(222, 200, 100, 20, "normal"),
                 (175, 100, 50, 20, "normal")]

# Add new lists for the platforms, ice platforms, and mobs in the "new level"
PLATFORM_LIST_NEW_LEVEL = [(0, HEIGHT - 40, WIDTH, 40, "normal"),
                           (WIDTH / 3 - 50, HEIGHT * 2 / 4, 100, 20,"normal"),
                           (130, HEIGHT - 200, 100, 20, "moving"),
                           #(222, 200, 100, 20, "normal"),
                           (300, 50, 50, 20, "normal")]

ICE_PLATFORM_LIST_NEW_LEVEL = [(222, 200, 100, 20, "normal")]

MOB_LIST_NEW_LEVEL = [(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")]

