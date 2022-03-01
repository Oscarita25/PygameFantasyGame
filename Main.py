import pygame as pg
import Levels

pg.init()


resolution = (256, 256)
display = pg.display.set_mode(resolution, flags=pg.SCALED | pg.RESIZABLE)

clock = pg.time.Clock()

Levels.init(display, clock)

active_scene = Levels.mainMenu()

while active_scene is not None:

    active_scene.game()
    active_scene = active_scene.next

pg.quit()
