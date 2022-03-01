import pygame as pg

import time

import Colors
import Objects as Obj

''' global variables used by every scene '''
# Tiles are by default 32x32
# can be changed if you wish to change textures
# (you have to change every single texture)
TILESIZE = 32

# a Map is by default 32x32 Chunks
MAPSIZE = 32

# a Chunk is by default 8x8 Tiles
# The Chunksize determines how many Tiles fit in one Chunk
# of the map (divided into chunks for performance)
CHUNKSIZE = 8

# display surface
display = None

# clock for measuring time, ticks,...
# clock for setting time related events
# (update frequency of the loop per second (ups, updates per second))
clock = None

isDebug = False

''' Settings '''
MAX_FPS = 0

'''Saved Data across scenes'''
data = {

}

''' Tileset '''
tiles = {
}


def init(surface, clck):
    global display
    global clock
    global tiles
    display = surface
    clock = clck

    tiles = {
        0: pg.image.load("assets/textures/tiles/grass.png").convert(),
        1: pg.image.load("assets/textures/tiles/stone.png").convert()
    }


def gen_mapsurf(map_dict):
    _rows = 0
    _elements = 0
    map_surface = pg.Surface(((CHUNKSIZE * TILESIZE) * MAPSIZE, (CHUNKSIZE * TILESIZE) * MAPSIZE))
    for x in range(MAPSIZE):
        for y in range(MAPSIZE):
            if f"{x}, {y}" in map_dict:
                for row in map_dict[f"{x}, {y}"]:
                    for element in row:
                        map_surface.blit(tiles[element], ((TILESIZE * _elements) + (CHUNKSIZE * TILESIZE) * x,
                                                          (TILESIZE * _rows) + (CHUNKSIZE * TILESIZE) * y))
                        _elements += 1
                    _elements = 0
                    _rows += 1
                _rows = 0
    return map_surface.convert()


def scale_map(surface, zoom):
    if display.get_size()[0] < display.get_size()[1]:
        return pg.transform.scale(surface,
                                  (display.get_size()[1] * zoom,
                                   display.get_size()[1] * zoom))
    elif display.get_size()[0] > display.get_size()[1]:
        return pg.transform.scale(surface,
                                  (display.get_size()[0] * zoom,
                                   display.get_size()[0] * zoom))
    else:
        return pg.transform.scale(surface,
                                  (display.get_size()[0] * zoom,
                                   display.get_size()[0] * zoom))


class Level:

    def __init__(self):

        self.anim_states = {
            "anim_cinematic": 0
        }

        self.counters = {
            "anim_cinematic_00": 0,
            "anim_cinematic_01": 0
        }
        self.next = self
        self.ticksLastFrame = 0
        self.frametime = 0
        self.fps = 0
        self.font = pg.font.SysFont('Arial', 50)
        self.s_delta = self.font.render(str(self.frametime), 1, (0, 0, 0))
        self.s_fps = self.font.render(str(0), 1, (0, 0, 0))

    def calculatedelta(self):
        ticks = time.time_ns()
        self.fps = clock.get_fps()

        # update game values
        self.frametime = (time.time_ns() - self.ticksLastFrame) / 1000000000
        self.ticksLastFrame = ticks

    def drawDebug(self, color=Colors.BLACK):
        # draw the values fps and delta time
        # on the bottom right corner
        # update surface values
        self.s_delta = self.font.render(str(int(self.frametime * 1000)) + " ms", 0, color)
        self.s_fps = self.font.render(str(int(self.fps)) + " fps", 0, color)
        display.blit(self.s_delta, [display.get_size()[0] - 200, display.get_size()[1] - 200])
        display.blit(self.s_fps, [display.get_size()[0] - 200, display.get_size()[1] - 100])

    def cinematic_change(self, duration=1):
        # function for changing scenes cinematicly
        # Fade to Black -> stay for set amount of time black -> Fade out again

        # anim_states["anim_cinematic"] -> state of animation
        # counters["anim_cinematic_00"] -> lenght period of the animation (how long the screen is black)
        # counters["anim_cinematic_01"] -> 0 -> 255 value of the alpha of the Black

        if self.anim_states["anim_cinematic"] == 0:
            # state 0
            # Animation has not started

            return
        elif self.anim_states["anim_cinematic"] == 1:
            # state 1
            # Transparent -> Black

            # increase black till 255
            if not (self.counters["anim_cinematic_01"] + self.frametime * 340 >= 255):
                self.counters["anim_cinematic_01"] += self.frametime * 340

            # change to state 2
            else:
                self.anim_states["anim_cinematic"] = 2

        elif self.anim_states["anim_cinematic"] == 2:
            # state 2
            # Black -> Transparent

            # wait a specific amount of time
            # amount of seconds -> default 1

            if self.counters["anim_cinematic_00"] + self.frametime <= duration:
                self.counters["anim_cinematic_00"] += self.frametime
                self.counters["anim_cinematic_01"] = 255

            # decrease black till 0
            elif not (self.counters["anim_cinematic_01"] - self.frametime * 340 <= 0):
                self.counters["anim_cinematic_01"] -= self.frametime * 340

            # change to state 0
            else:
                self.counters["anim_cinematic_01"] = 0
                self.anim_states["anim_cinematic"] = 0
                self.counters["anim_cinematic_00"] = 0

        s = pg.Surface(display.get_size())
        s.fill(Colors.BLACK)
        s.set_alpha(self.counters["anim_cinematic_01"])
        display.blit(s, (0, 0))

    def game(self):
        raise Exception('[ERROR] Not Overwriting "Level" ')

    def next_scene(self, next_scene):
        self.next = next_scene
        del self

    def terminate(self):
        self.next_scene(None)


class mainMenu(Level):
    def __init__(self):
        Level.__init__(self)
        # list of buttons
        self.btn_lst = \
            [Obj.Button(Colors.BLACK, display.get_size()[0] / 2, display.get_size()[1] / 3 + 100, 200, 100,
                        text='Start'),
             Obj.Button(Colors.BLACK, display.get_size()[0] / 2, display.get_size()[1] / 3 + 200, 200, 100,
                        text='Options'),
             Obj.Button(Colors.BLACK, display.get_size()[0] / 2, display.get_size()[1] / 3 + 300, 200, 100,
                        text='Quit')]
        self.title = pg.image.load('assets/textures/menu/title.png')
        self.title = pg.transform.scale(self.title, (768, 192)).convert_alpha()
        self.background = pg.image.load('assets/textures/menu/background.png').convert()
        self.background = pg.transform.scale(self.background, display.get_size()).convert()

    def game(self):
        global isDebug
        mouse_pos = pg.mouse.get_pos()

        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.terminate()

            if e.type == pg.KEYDOWN:

                if e.key == pg.K_F1:
                    if isDebug:
                        isDebug = False
                    else:
                        isDebug = True

            if e.type == pg.MOUSEBUTTONDOWN:
                # if MB Left (1) is clicked ->
                if e.button == 1:
                    if self.btn_lst[0].isHover:
                        self.anim_states["anim_cinematic"] = 1
                        self.next_scene(Level_00())
                    if self.btn_lst[1].isHover:
                        self.next_scene(optionMenu())
                    if self.btn_lst[2].isHover:
                        self.terminate()

            if e.type == pg.VIDEORESIZE:
                for button in self.btn_lst:
                    button.x = display.get_size()[0] / 2 - button.width / 2
                    self.background = pg.transform.scale(self.background, display.get_size()).convert()

        for button in self.btn_lst:
            button.Hover(mouse_pos, Colors.MAGENTA)

        display.fill(Colors.BLUE)

        display.blit(self.background, [0, 0])

        display.blit(self.title, [display.get_size()[0] / 2 - self.title.get_size()[0] / 2,
                                  display.get_size()[1] / 4 - self.title.get_size()[1] / 2])

        for button in self.btn_lst:
            button.draw(display)

        if isDebug:
            self.drawDebug()

        self.cinematic_change()
        pg.display.flip()
        clock.tick(MAX_FPS)
        self.calculatedelta()


class optionMenu(Level):
    def __init__(self):
        Level.__init__(self)
        # list of buttons
        self.btn_lst = \
            [Obj.Button(Colors.BLACK, display.get_size()[0] / 2, display.get_size()[1] / 3 + 100, 200, 100,
                        text='Back')]
        self.title = pg.image.load('assets/textures/menu/title.png')
        self.title = pg.transform.scale(self.title, (768, 192)).convert_alpha()
        self.title_xy = [display.get_size()[0] / 2 - self.title.get_size()[0] / 2,
                         display.get_size()[1] / 4 - self.title.get_size()[1] / 2]
        self.background = pg.image.load('assets/textures/menu/background.png').convert()
        self.background = pg.transform.scale(self.background, display.get_size()).convert()

    def game(self):
        global isDebug
        self.calculatedelta()
        mouse_pos = pg.mouse.get_pos()

        if round(self.frametime, 0) == 0:

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.terminate()

                if e.type == pg.KEYDOWN:

                    if e.key == pg.K_F1:
                        if isDebug:
                            isDebug = False
                        else:
                            isDebug = True

                    if e.key == pg.K_ESCAPE:
                        self.next_scene(mainMenu())

                if e.type == pg.MOUSEBUTTONDOWN:
                    # if MB Left (1) is clicked ->
                    if e.button == 1:
                        if self.btn_lst[0].isHover:
                            self.next_scene(mainMenu())

                if e.type == pg.VIDEORESIZE:
                    for button in self.btn_lst:
                        button.x = display.get_size()[0] / 2 - button.width / 2
                        self.background = pg.transform.scale(self.background, display.get_size()).convert()
                        self.title_xy = [display.get_size()[0] / 2 - self.title.get_size()[0] / 2, self.title_xy[1]]

            for button in self.btn_lst:
                button.Hover(mouse_pos, Colors.MAGENTA)

            display.fill(Colors.BLUE)

            display.blit(self.background, [0, 0])

            display.blit(self.title, self.title_xy)

            for button in self.btn_lst:
                button.draw(display)

            if isDebug:
                self.drawDebug()

        pg.display.flip()
        clock.tick(MAX_FPS)


class Level_00(Level):
    def __init__(self):
        Level.__init__(self)

        # setup camera
        self.camera_pos = [0, 0]
        self.camera_speed = 250
        self.camera_zoom = 20

        self.map = {
            "16, 16":
                [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]],

            "16, 17":
                [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]],

            "17, 17":
                [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]]

        }

        # generate map
        self.map_surface = gen_mapsurf(self.map)

        # scale map_surface (keep it seperate so we can resize it at all times)
        # if check to keep aspect ratio
        # (map is a square, not a rectangle, so keep it as one)
        self.scaled_map = scale_map(self.map_surface, self.camera_zoom)

        self.camera_pos[0] = -self.scaled_map.get_size()[0] / 2
        self.camera_pos[1] = -self.scaled_map.get_size()[1] / 2

        # list of buttons
        self.btn_lst = \
            [Obj.Button(Colors.BLACK, display.get_size()[0] / 2, display.get_size()[1] / 3 + 100, 200, 100,
                        text='Back')]
        self.btn_lst[0].isVisible = False

        self.anim_states["anim_cinematic"] = 1

    def game(self):
        global isDebug
        self.calculatedelta()
        mouse_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()

        if round(self.frametime, 0) == 0:

            if keys[pg.K_w]:
                self.camera_pos[1] += self.frametime * self.camera_speed
            elif keys[pg.K_s]:
                self.camera_pos[1] -= self.frametime * self.camera_speed
            elif keys[pg.K_a]:
                self.camera_pos[0] += self.frametime * self.camera_speed
            elif keys[pg.K_d]:
                self.camera_pos[0] -= self.frametime * self.camera_speed

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.terminate()

                if e.type == pg.KEYDOWN:

                    if e.key == pg.K_F1:
                        if isDebug:
                            isDebug = False
                        else:
                            isDebug = True

                    if e.key == pg.K_ESCAPE:
                        if self.btn_lst[0].isVisible:
                            self.btn_lst[0].isVisible = False
                        else:
                            self.btn_lst[0].isVisible = True

                if e.type == pg.MOUSEBUTTONDOWN:
                    # if MB Left (1) is clicked ->
                    if e.button == 1:
                        if self.btn_lst[0].isHover and self.btn_lst[0].isVisible:
                            self.next_scene(mainMenu())

                if e.type == pg.VIDEORESIZE:
                    for button in self.btn_lst:
                        button.x = display.get_size()[0] / 2 - button.width / 2

            for button in self.btn_lst:
                button.Hover(mouse_pos, Colors.MAGENTA)

            display.fill(Colors.WHITE)

            display.blit(self.scaled_map, self.camera_pos)

            for button in self.btn_lst:
                button.draw(display)

            if isDebug:
                self.drawDebug(Colors.WHITE)

        self.cinematic_change(0.3)
        pg.display.flip()
        clock.tick(MAX_FPS)
