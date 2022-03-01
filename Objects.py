import pygame


class Button:

    def __init__(self, color, x, y, width, height, text=''):
        self.x = x - width/2
        self.y = y
        self.color = color
        self.buffer_c = color
        self.isHover = False
        self.isVisible = True
        self.width = width
        self.height = height
        self.surface = pygame.Surface([self.width, self.height])
        self.surface.fill(self.color)
        self.font = pygame.font.Font('assets/fonts/Pixels.ttf', int(self.width / 1.5))
        self.img = pygame.image.load("assets/textures/menu/cursor.png")
        self.img = pygame.transform.scale(self.img, [128, 128]).convert_alpha()
        self.text = text

    def draw(self, win):

        if not self.isVisible:
            return
        # Call this method to draw the button on the screen
        #self.surface.fill(self.color)
        #win.blit(self.surface, (self.x,  self.y))
        if self.isHover:
            win.blit(self.img, [self.x /2, self.y  ])

        if self.text != '':
            text = self.font.render(self.text, 1, self.color)
            win.blit(text, (
                self.x, self.y))

    def Hover(self, pos, secondary_color):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                self.color = secondary_color
                self.isHover = True
                return

        self.color = self.buffer_c
        self.isHover = False
        return

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                self.isHover = True
                return True
        self.isHover = False
        return False
