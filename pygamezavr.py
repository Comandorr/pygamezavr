from pygame import*
from random import*

display.init()
clock = time.Clock()
font.init()
mixer.init()
window = None
win_w = 0; win_h = 0
center_x = 0; center_y = 0
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)
dark_gray = (150, 150, 150)
joystick.init()
pads = joystick.get_count()
if pads:
    j1 = joystick.Joystick(0)
    j1.init()
    gamepad_connected = True
else:
    gamepad_connected = False


# return chance (percentage)
def chance(x, max = 101):
    return (x >= randint(1, max))


# creates a window using width and height
def create_window(w=0, h=0):
    global window, win_w, win_h, center_x, center_y
    window = display.set_mode((w, h),  vsync = 1) #FULLSCREEN, OPENGL,
    return window


# checks for player trying to quit the game, requires a variable to run
# designed to use as a condition for a main while cycle of the game
def run_game(run):
    for x in event.get():
        if x.type == QUIT:
            run = False
    return run


# func for loading simple images with path to image and size
# loads and converts the image, also transforms if size is written
def Image(i, size = None):
    img = image.load(i).convert_alpha()
    if size:
        img = transform.scale(img, (size[0], size[1]))
    return img


# fills the game window with color
def fill_window(color):
    display.get_surface().fill(color)


# method for keyboard movement control
# designed to use inside player's class
def keyboard_control(self):
    keys = key.get_pressed()
    if keys[K_d]:
        self.right()
    if keys[K_a]:
        self.left()
    if keys[K_w]:
        self.up()
    if keys[K_s]:
        self.down()


# method for gamepad movement control
# designed to use inside player's class
def gamepad_control(self):
    if j1.get_axis(0) > 0.5:
        self.right()
    if j1.get_axis(0) < -0.5:
        self.left()
    if j1.get_axis(1) > 0.5:
        self.down()
    if j1.get_axis(1) < -0.5:
        self.up()


def combined_control(self):
    keyboard_control(self)
    gamepad_control(self)


# custom Group class, can reset itself
class Group(sprite.Group):
    def reset(self):
        for s in self.sprites():
            s.reset()


# class for simple sprites, containing image (path, size) and coordinates
# reset = blit image into the game window
# move = replace sprite to new coordinates
class SimpleSprite(sprite.Sprite):
    def __init__(self, img, pos):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.x , self.y = pos
        self.screen = display.get_surface()
    def replace(self, pos):
        self.x, self.y = pos
    def reset(self):
        self.rect.topleft = (self.x, self.y)
        self.screen.blit(self.image, (self.rect.topleft))


# class for text sprites with font size, coordinates, color and background
# setText - sets text, reset - resets
class SimpleText(sprite.Sprite):
    def __init__(self, text, size, x, y, color = black, background = None):
        super().__init__()
        self.image = font.Font(None, size).render(text, 1, color, background)
        self.position = [x, y]
        self.size = size
        self.color = color
        self.background = background
        self.rect = self.image.get_rect()
        self.screen = display.get_surface()
    def setText(self, text):
        self.image = font.Font(None, self.size).render(text, 1, self.color, self.background)
        self.rect = self.image.get_rect()
    def reset(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.screen.blit(self.image, self.position)


def stop_game():
    global run
    run = False


create_window()
FRAMES = 0
run = True
start_time = time.get_ticks()
time_passed = 0
def run_game(func):
    global run, FRAMES, start_time, time_passed
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
        func()
        display.update()
        FRAMES += 1
        clock.tick(60)
        time_passed = time.get_ticks() - start_time
