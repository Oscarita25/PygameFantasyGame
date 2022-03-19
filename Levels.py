import pygame as pg

import time

import pygame.image

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

# Map Pixel Size is the Size of the map in pixels
# for ex.  MAP_PIX = 256 -> the map is 256x256
MAP_PIX = (CHUNKSIZE * TILESIZE) * MAPSIZE

# display surface
display = None

# clock for measuring time, ticks,...
# clock for setting time related events
# (update frequency of the loop per second (ups, updates per second))
clock = None

# isDebug is a boolean stating if the Debug Menu should be open.
isDebug = False

# vec is just a way of shortening my time to write code.
# it has a lot of math functions written to calculate different
# types of movements etc.
vec = pygame.math.Vector2

''' Settings '''
MAX_FPS = 0
ASPECT_RATIO = "1:1"
FULLSCREEN = "OFF"

''' Aspect Ratio Muliplicator '''
ASPC_MULT = 1
multiplicator16_9 = (16 / 9)
multiplicator1_1 = 1

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
    '''
    # example dictonary
    map_dict = {
    # "0, 0" -> is the Chunk Cordinate
    # [] <- the Map has to be the size of CHUNKSIZE

        "0, 0":
            [[1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 0, 0, 1, 1, 1]],
    }
    '''

    _rows = 0
    _elements = 0
    # create a map surface (a rectangle) which is the maximum size of the map
    # CHUNKSIZE * TILESIZE = Pixels of 1 Chunk
    # (CHUNKSIZE * TILESIZE) * MAPSIZE = Pixels of 1 MAP
    map_surface = pg.Surface((MAP_PIX, MAP_PIX))

    # go trough every Chunk and add Tiles to map
    # x chunk axis
    for x in range(MAPSIZE):
        # y chunk axis
        for y in range(MAPSIZE):
            if f"{x}, {y}" in map_dict:
                for row in map_dict[f"{x}, {y}"]:
                    # go trough every row in Chunk
                    for element in row:
                        # add tile to map for every     element.
                        map_surface.blit(tiles[element], ((TILESIZE * _elements) + (CHUNKSIZE * TILESIZE) * x,
                                                          (TILESIZE * _rows) + (CHUNKSIZE * TILESIZE) * y))
                        _elements += 1
                        # for element in row -> END
                    _elements = 0
                    _rows += 1
                    # for  row in map_dict[f"{x}, {y}"] -> END
            _rows = 0
            # for y in range(MAPSIZE) -> END
    # for x in range(MAPSIZE) -> END

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


def aspec_change():
    global ASPECT_RATIO
    global ASPC_MULT
    global display
    global FULLSCREEN

    if ASPECT_RATIO == "1:1" and FULLSCREEN == "OFF":
        ASPC_MULT = multiplicator16_9
        display = pg.display.set_mode(
            [256 * ASPC_MULT,
             256 * 1], flags=pg.SCALED | pg.RESIZABLE)
        ASPECT_RATIO = "16:9"
    elif ASPECT_RATIO == "16:9" and FULLSCREEN == "OFF":
        ASPC_MULT = multiplicator1_1
        display = pg.display.set_mode(
            [256,
             256], flags=pg.SCALED | pg.RESIZABLE)
        ASPECT_RATIO = "1:1"
    elif ASPECT_RATIO == "1:1" and FULLSCREEN == "ON":
        ASPC_MULT = multiplicator16_9
        display = pg.display.set_mode(
            [256 * ASPC_MULT,
             256 * 1], flags=pg.SCALED | pg.FULLSCREEN)
        ASPECT_RATIO = "16:9"
    elif ASPECT_RATIO == "16:9" and FULLSCREEN == "ON":
        ASPC_MULT = multiplicator1_1
        display = pg.display.set_mode(
            [256,
             256], flags=pg.SCALED | pg.FULLSCREEN)
        ASPECT_RATIO = "1:1"
    pg.event.post(pg.event.Event(pg.VIDEORESIZE))


def change_fullscreen():
    global FULLSCREEN
    global display

    if FULLSCREEN == "OFF":
        display = pg.display.set_mode(
            [256 * ASPC_MULT,
             256 * 1], flags=pg.SCALED | pg.FULLSCREEN)
        FULLSCREEN = "ON"
    else:
        display = pg.display.set_mode(
            [256 * ASPC_MULT,
             256], flags=pg.SCALED | pg.RESIZABLE)
        FULLSCREEN = "OFF"

    pg.event.post(pg.event.Event(pg.VIDEORESIZE))


class Minimap:
    def __init__(self, game):
        self.game = game

        self.surface = pg.Surface((64, 64))
        self.surface.fill((0, 0, 0))

        self.cam_surf = pg.Surface((CHUNKSIZE * TILESIZE, CHUNKSIZE * TILESIZE))
        self.cam_surf.fill((255, 0, 0))
        self.cam_surf.set_alpha(128)
        self.cam_surf = pg.transform.scale(self.cam_surf, ((CHUNKSIZE * TILESIZE) / 128, (CHUNKSIZE * TILESIZE) / 128))
        self.image = pg.transform.scale(self.game.map_surface, (64, 64))

    def update(self):
        # self.comb_surf.fill((0, 0, 0))
        self.surface.blit(self.image, (0, 0))
        self.surface.blit(self.cam_surf,
                          ((abs(self.game.camera_pos[0]) / 128),
                           (abs(self.game.camera_pos[1]) / 128)))
        pg.draw.rect(self.surface, (255, 255, 255), (0, 0, 64, 64), 2)


class Player(pg.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/textures/Player_Sprite.png")
        self.rect = self.image.get_rect()

        #Position and Direction
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = "DOWN"

    def move_p(self):
        self.pos += self.vel

    def update_p(self):
        pass

    def jump_p(self):
        pass

    def attack_p(self):
        pass


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
        self.font = pg.font.SysFont('Arial', 10)
        self.s_delta = self.font.render(str(self.frametime), 0, (0, 0, 0))
        self.s_fps = self.font.render(str(0), 0, (0, 0, 0))

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
        display.blit(self.s_delta, [display.get_size()[0] - 32, display.get_size()[1] - 20])
        display.blit(self.s_fps, [display.get_size()[0] - 32, display.get_size()[1] - 10])

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
            [Obj.Button(Colors.BLACK, display.get_size()[0] / 2, display.get_size()[1] / 3 + 25, 50, 25,
                        text='Start'),
             Obj.Button(Colors.BLACK, display.get_size()[0] / 2, display.get_size()[1] / 3 + 50, 50, 25,
                        text='Options'),
             Obj.Button(Colors.BLACK, display.get_size()[0] / 2, display.get_size()[1] / 3 + 75, 50, 25,
                        text='Quit')]

        self.selected_btn = None

        self.title = pg.image.load('assets/textures/menu/title.png').convert_alpha()
        self.title = pg.transform.scale(self.title,
                                        (self.title.get_size()[0] * 2, self.title.get_size()[1] * 2)).convert_alpha()
        self.background = pg.image.load('assets/textures/menu/background.png').convert()
        self.background = pg.transform.scale(self.background, display.get_size()).convert()

    def game(self):
        global isDebug
        mouse_pos = pg.mouse.get_pos()

        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.terminate()

            if e.type == pg.KEYDOWN:

                if e.key == pg.K_DOWN:
                    if self.selected_btn is None:
                        self.selected_btn = 0
                        if not (self.selected_btn > len(self.btn_lst)):
                            self.btn_lst[self.selected_btn].isSelected = True

                    else:
                        self.selected_btn += 1
                        if not (self.selected_btn > len(self.btn_lst) - 1):
                            self.btn_lst[self.selected_btn - 1].isSelected = False
                            self.btn_lst[self.selected_btn].isSelected = True
                        else:
                            self.selected_btn -= 1

                if e.key == pg.K_UP:
                    if self.selected_btn is None:
                        self.selected_btn = 0
                        if not (self.selected_btn > len(self.btn_lst)):
                            self.btn_lst[self.selected_btn].isSelected = True
                    elif len(self.btn_lst) == 1:
                        self.btn_lst[self.selected_btn].isSelected = True
                    else:
                        self.selected_btn -= 1
                        if self.selected_btn < 0:
                            self.selected_btn = 0

                        if not (self.selected_btn > len(self.btn_lst) - 1):
                            self.btn_lst[self.selected_btn + 1].isSelected = False
                            self.btn_lst[self.selected_btn].isSelected = True
                        else:
                            self.selected_btn -= 1

                if e.key == pg.K_F1:
                    if isDebug:
                        isDebug = False
                    else:
                        isDebug = True

                if e.key == pg.K_RETURN:
                    if self.btn_lst[0].isHover:
                        self.anim_states["anim_cinematic"] = 1
                    if self.btn_lst[1].isHover:
                        self.next_scene(optionMenu())
                    if self.btn_lst[2].isHover:
                        self.terminate()

            if e.type == pg.MOUSEBUTTONDOWN:
                if self.selected_btn is not None:
                    self.btn_lst[self.selected_btn].isSelected = False
                    self.btn_lst[self.selected_btn].isHover = False
                    self.selected_btn = None

                # if MB Left (1) is clicked ->
                if e.button == 1:
                    if self.btn_lst[0].isHover:
                        self.anim_states["anim_cinematic"] = 1

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
        if self.anim_states["anim_cinematic"] == 2:
            self.next_scene(Level_00())
        pg.display.flip()
        clock.tick(MAX_FPS)
        self.calculatedelta()


class optionMenu(Level):
    def __init__(self):
        Level.__init__(self)
        # list of buttons
        self.btn_lst = \
            [Obj.Button(Colors.BLACK, display.get_size()[0] / 2, display.get_size()[1] / 3 + 25, 50, 25,
                        text='Back'),
             Obj.Button(Colors.BLACK, display.get_size()[0] / 2, display.get_size()[1] / 3 + 50, 50, 25,
                        text=f"Aspect Ratio: {ASPECT_RATIO}"),
             Obj.Button(Colors.BLACK, display.get_size()[0] / 2, display.get_size()[1] / 3 + 75, 50, 25,
                        text=f"Fullscreen: {FULLSCREEN}")]
        self.selected_btn = None

        self.title = pg.image.load('assets/textures/menu/title.png')
        self.title = pg.transform.scale(self.title,
                                        (self.title.get_size()[0] * 2, self.title.get_size()[1] * 2)).convert_alpha()
        self.title_xy = [display.get_size()[0] / 2 - self.title.get_size()[0] / 2,
                         display.get_size()[1] / 4 - self.title.get_size()[1] / 2]
        self.background = pg.image.load('assets/textures/menu/background.png').convert()
        self.background = pg.transform.scale(self.background, display.get_size()).convert()

    def game(self):
        global isDebug
        global display
        global ASPECT_RATIO
        global FULLSCREEN
        global ASPC_MULT

        self.calculatedelta()
        mouse_pos = pg.mouse.get_pos()

        if round(self.frametime, 0) == 0:

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.terminate()

                if e.type == pg.KEYDOWN:

                    if e.key == pg.K_DOWN:
                        if self.selected_btn is None:
                            self.selected_btn = 0
                            if not (self.selected_btn > len(self.btn_lst)):
                                self.btn_lst[self.selected_btn].isSelected = True

                        else:
                            self.selected_btn += 1
                            if not (self.selected_btn > len(self.btn_lst) - 1):
                                self.btn_lst[self.selected_btn - 1].isSelected = False
                                self.btn_lst[self.selected_btn].isSelected = True
                            else:
                                self.selected_btn -= 1

                    if e.key == pg.K_UP:
                        if self.selected_btn is None:
                            self.selected_btn = 0
                            if not (self.selected_btn > len(self.btn_lst)):
                                self.btn_lst[self.selected_btn].isSelected = True
                        elif len(self.btn_lst) == 1:
                            self.btn_lst[self.selected_btn].isSelected = True
                        else:
                            self.selected_btn -= 1
                            if self.selected_btn < 0:
                                self.selected_btn = 0

                            if not (self.selected_btn > len(self.btn_lst) - 1):
                                self.btn_lst[self.selected_btn + 1].isSelected = False
                                self.btn_lst[self.selected_btn].isSelected = True
                            else:
                                self.selected_btn -= 1

                    if e.key == pg.K_F1:
                        if isDebug:
                            isDebug = False
                        else:
                            isDebug = True

                    if e.key == pg.K_ESCAPE:
                        self.next_scene(mainMenu())
                    if e.key == pg.K_RETURN:
                        if self.btn_lst[0].isHover:
                            self.next_scene(mainMenu())
                        if self.btn_lst[1].isHover:
                            aspec_change()
                            self.btn_lst[1].text = f"Aspect Ratio: {ASPECT_RATIO}"

                        if self.btn_lst[2].isHover:
                            change_fullscreen()
                            self.btn_lst[2].text = f"Fullscreen: {FULLSCREEN}"

                if e.type == pg.MOUSEBUTTONDOWN:
                    if self.selected_btn is not None:
                        self.btn_lst[self.selected_btn].isSelected = False
                        self.btn_lst[self.selected_btn].isHover = False
                        self.selected_btn = None

                    # if MB Left (1) is clicked ->
                    if e.button == 1:
                        if self.btn_lst[0].isHover:
                            self.next_scene(mainMenu())
                        if self.btn_lst[1].isHover:
                            aspec_change()
                            self.btn_lst[1].text = f"Aspect Ratio: {ASPECT_RATIO}"
                        if self.btn_lst[2].isHover:
                            change_fullscreen()
                            self.btn_lst[2].text = f"Fullscreen: {FULLSCREEN}"

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
        if ASPECT_RATIO == "1:1":
            self.camera_zoom = MAP_PIX / display.get_size()[1]
        elif ASPECT_RATIO == "16:9":
            self.camera_zoom = MAP_PIX / (display.get_size()[1] * (16 / 9))

        self.map = {
            "16, 16":
                [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 1, 0, 0, 0, 0],
                 [1, 0, 0, 1, 0, 0, 0, 0],
                 [1, 0, 0, 1, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 1, 1, 0, 0, 1, 1, 1]],

            "16, 17":
                [[1, 1, 0, 0, 0, 0, 1, 1],
                 [1, 0, 1, 1, 1, 1, 0, 1],
                 [1, 0, 1, 0, 0, 1, 0, 1],
                 [1, 0, 1, 1, 1, 1, 0, 0],
                 [1, 0, 1, 1, 1, 1, 0, 0],
                 [1, 0, 1, 0, 0, 1, 0, 1],
                 [1, 0, 1, 0, 0, 1, 0, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]],

            "5, 5":
                [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]],
            "5, 4":
                [[1, 1, 1, 0, 0, 1, 1, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [1, 0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 0, 0, 1],
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

        # set cam_pos to center of the map.
        self.camera_pos[0] = -self.scaled_map.get_size()[0] / 2
        self.camera_pos[1] = -self.scaled_map.get_size()[1] / 2

        # list of buttons
        self.btn_lst = \
            [Obj.Button(Colors.BLACK, display.get_size()[0] / 2, display.get_size()[1] / 3 + 25, 50, 25,
                        text='Back')]
        self.btn_lst[0].isVisible = False
        self.selected_btn = None

        self.player = Player(self.scaled_map.get_size()[0] / 2 + 32*4, self.scaled_map.get_size()[1] / 2 + 32*4)

        # mini map
        self.Minimap = Minimap(self)
        self.show_minimap = False

        self.anim_states["anim_cinematic"] = 1

    def game(self):
        global isDebug
        self.calculatedelta()
        mouse_pos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()

        if round(self.frametime, 0) == 0:

            if keys[pg.K_w]:
                self.camera_pos[1] += self.frametime * self.camera_speed
            if keys[pg.K_s]:
                self.camera_pos[1] -= self.frametime * self.camera_speed
            if keys[pg.K_a]:
                self.camera_pos[0] += self.frametime * self.camera_speed
            if keys[pg.K_d]:
                self.camera_pos[0] -= self.frametime * self.camera_speed

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.terminate()

                if e.type == pg.KEYDOWN:

                    if e.key == pg.K_DOWN:
                        if self.selected_btn is None:
                            self.selected_btn = 0
                            if not (self.selected_btn > len(self.btn_lst)):
                                self.btn_lst[self.selected_btn].isSelected = True

                        else:
                            self.selected_btn += 1
                            if not (self.selected_btn > len(self.btn_lst) - 1):
                                self.btn_lst[self.selected_btn - 1].isSelected = False
                                self.btn_lst[self.selected_btn].isSelected = True
                            else:
                                self.selected_btn -= 1

                    if e.key == pg.K_UP:
                        if self.selected_btn is None:
                            self.selected_btn = 0
                            if not (self.selected_btn > len(self.btn_lst)):
                                self.btn_lst[self.selected_btn].isSelected = True

                        elif len(self.btn_lst) == 1:
                            self.btn_lst[self.selected_btn].isSelected = True
                        else:
                            self.selected_btn -= 1
                            if self.selected_btn < 0:
                                self.selected_btn = 0

                            if not (self.selected_btn > len(self.btn_lst) - 1):
                                self.btn_lst[self.selected_btn + 1].isSelected = False
                                self.btn_lst[self.selected_btn].isSelected = True
                            else:
                                self.selected_btn -= 1

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
                    if e.key == pg.K_m:
                        if self.show_minimap:
                            self.show_minimap = False
                        else:
                            self.show_minimap = True

                    if e.key == pg.K_F11:
                        change_fullscreen()

                    if e.key == pg.K_RETURN:
                        if self.btn_lst[0].isHover:
                            self.next_scene(mainMenu())

                if e.type == pg.MOUSEBUTTONDOWN:
                    if self.selected_btn is not None:
                        self.btn_lst[self.selected_btn].isSelected = False
                        self.btn_lst[self.selected_btn].isHover = False
                        self.selected_btn = None

                    # if MB Left (1) is clicked ->
                    if e.button == 1:
                        if self.btn_lst[0].isHover and self.btn_lst[0].isVisible:
                            self.next_scene(mainMenu())

                if e.type == pg.VIDEORESIZE:
                    for button in self.btn_lst:
                        button.x = display.get_size()[0] / 2 - button.width / 2

            self.Minimap.update()

            for button in self.btn_lst:
                button.Hover(mouse_pos, Colors.MAGENTA)

            display.fill(Colors.WHITE)

            display.blit(self.scaled_map, self.camera_pos)

            self.scaled_map.blit(self.player.image, self.player.pos)
            if self.show_minimap:
                display.blit(self.Minimap.surface, (display.get_size()[0] - 64, 0))

            for button in self.btn_lst:
                button.draw(display)

            if isDebug:
                self.drawDebug(Colors.WHITE)

        self.cinematic_change(0.3)
        pg.display.flip()
        clock.tick(MAX_FPS)
