import pygame as pg
import Levels

pg.init()


resolution = (1000, 1000)
display = pg.display.set_mode(resolution, flags=pg.RESIZABLE)

clock = pg.time.Clock()

Levels.init(display, clock)

active_scene = Levels.mainMenu()

while active_scene is not None:

    active_scene.game()
    active_scene = active_scene.next

pg.quit()
