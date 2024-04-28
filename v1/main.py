
import pygame
import sys
from pygame.locals import *
from pydub import AudioSegment
from pydub.playback import play
import serial

## serial config ##
DEVICE_NAME = '/dev/ttyACM0'
if sys.argv[1] == 'windows':
    DEVICE_NAME = 'COM3'
serial_port =  serial.Serial(DEVICE_NAME, 9600),


def terminate():
    pygame.quit()
    sys.exit()
    
    

# init pygame
audioSettings = {"frequency": 44100, "size": -16, "channels": 2, "buffer": 256}
system_fps = 120.0
pygame.mixer.pre_init(
    audioSettings["frequency"],
    audioSettings["size"],
    audioSettings["channels"],
    audioSettings["buffer"],
)
pygame.mixer.init()
pygame.init()
pygame.display.set_caption("cj_v74cl_hacks v1")
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode(
    (640, 480)
)

# vars 2
font = pygame.font.SysFont(None, 23)
bg_color = (255, 255, 255)
text_color = (10, 10, 10)
s_ki = pygame.mixer.Sound("sounds/ki.wav")
s_rim = pygame.mixer.Sound("sounds/rim.wav")
s_hi = pygame.mixer.Sound("sounds/hi.wav")
s_m = [pygame.mixer.Sound(f"sounds/m{i}.wav") for i in range(1, 6)]
pad_colors = {
    "ki": (255, 0, 0),
    "hi": (0, 255, 0),
    "rim": (0, 0, 255),
    "m": [
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
        (100, 0, 255),
        (0, 0, 0)
    ]
}
pad_value_max = 255
pad_values = {
    "ki": pad_value_max,
    "hi": pad_value_max,
    "rim": pad_value_max,
    "m": [pad_value_max, pad_value_max, pad_value_max, pad_value_max, pad_value_max]   
}

def on_parse_keys(event, que):
    if event.key == K_1:
        que["m"]["1"] = True
    if event.key == K_2:
        que["m"]["2"] = True
    if event.key == K_3:
        que["m"]["3"] = True
    if event.key == K_4:
        que["m"]["4"] = True
    if event.key == K_5:
        que["m"]["5"] = True
    if event.key == K_a:
        que["ki"] = True
    if event.key == K_s:
        que["hi"] = True
    if event.key == K_d:
        que["rim"] = True
    return que

def player(que):
    if que["ki"]:
        s_ki.play()
    if que["hi"]:
        s_hi.play()
    if que["rim"]:
        s_rim.play()
    for i in range(1, 6):
        if que["m"][str(i)]:
            s_m[i-1].play()

def update_value(que):
    # if key pressed, set value to max. each frame, reduce value by 1
    if que["ki"]:
        pad_values["ki"] = pad_value_max
    if que["hi"]:
        pad_values["hi"] = pad_value_max
    if que["rim"]:
        pad_values["rim"] = pad_value_max
    for i in range(1, 6):
        if que["m"][str(i)]:
            pad_values["m"][i-1] = pad_value_max


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def gen_rbga(color, alpha):
    return (color[0], color[1], color[2], alpha)

def update_ui():
    block_size = 50
    draw_rect_alpha(window_surface, gen_rbga(pad_colors["ki"], pad_values["ki"]), (0, 0, block_size, block_size))
    draw_rect_alpha(window_surface, gen_rbga(pad_colors["hi"], pad_values["hi"]), (block_size, 0, block_size, block_size))
    draw_rect_alpha(window_surface, gen_rbga(pad_colors["rim"], pad_values["rim"]), (block_size*2, 0, block_size, block_size))
    for i in range(0, 5):
        draw_rect_alpha(window_surface, gen_rbga(pad_colors["m"][i], pad_values["m"][i]), (block_size*(i), block_size, block_size, block_size))
    
        
    # reduce value by n
    n = 3
    for i in range(1, 6):
        pad_values["m"][i-1] = pad_values["m"][i-1] - n
        if pad_values["m"][i-1] < 0:
            pad_values["m"][i-1] = 0
    pad_values["ki"] = pad_values["ki"] - n
    if pad_values["ki"] < 0:
        pad_values["ki"] = 0
    pad_values["hi"] = pad_values["hi"] - n
    if pad_values["hi"] < 0:
        pad_values["hi"] = 0
    pad_values["rim"] = pad_values["rim"] - n
    if pad_values["rim"] < 0:
        pad_values["rim"] = 0
def read_serial(que):


               

while True:
    window_surface.fill(bg_color)
    text = font.render("Press 1-5, a, s, d to play sound", True, text_color)
    window_surface.blit(text, (10, 120))

    que = {
        "ki": False,
        "hi": False,
        "rim": False,
        "m": {
            "1": False,
            "2": False,
            "3": False,
            "4": False,
            "5": False,
        }
    }

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()


        # from keyboard        
        if event.type == KEYDOWN:
            que = on_parse_keys(event, que)
                
        # from arduino
        

    # update ui based on que
    update_value(que)
    # player
    player(que)

    update_ui()

    pygame.display.update()
    main_clock.tick(system_fps)
