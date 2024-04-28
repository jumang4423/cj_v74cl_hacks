
import pygame
import sys
import random
from pygame.locals import *
from pydub import AudioSegment
from pydub.playback import play
import serial

## serial config ##
DEVICE_NAME = ''
serial_port = None
if len(sys.argv) > 1:
    if sys.argv[1] == 'windows':
        DEVICE_NAME = 'COM3'
    if sys.argv[1] == 'mac':
        DEVICE_NAME = '/dev/tty.usbmodem11101'
if DEVICE_NAME != '':
    serial_port =  serial.Serial(DEVICE_NAME, 9600)


def terminate():
    pygame.quit()
    sys.exit()
    
    

# init pygame
pad_arr_size = 12
block_size = 100
max_col = 6
audioSettings = {"frequency": 44100, "size": -16, "channels": 2, "buffer": 64}
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
    (block_size * max_col, block_size * (pad_arr_size // max_col) + 50)
)

# vars 2
font = pygame.font.SysFont(None, 30)
bg_color = (255, 255, 255)
text_color = (10, 10, 10)
# 0,1,2,3,4,5,6,7,8,9,*,#
def load_sounds():
    arr = []
    for i in range(pad_arr_size):
        # check if file exists
        try:
            s = pygame.mixer.Sound(f"sounds/{i}.wav")
            arr.append(s)
        except:
            arr.append(None)
            print(f"Error: sounds/m{i}.wav not found")
    return arr

s_m = load_sounds()
pad_value_max = 255
pad_values = [pad_value_max for i in range(pad_arr_size)]

def on_parse_keys(event, que):
    if event.key == K_1:
        que[1] = True
    if event.key == K_2:
        que[2] = True
    if event.key == K_3:
        que[3] = True
    if event.key == K_4:
        que[4] = True
    if event.key == K_5:
        que[5] = True
    if event.key == K_6:
        que[6] = True
    if event.key == K_7:
        que[7] = True
    if event.key == K_8:
        que[8] = True
    if event.key == K_9:
        que[9] = True
    if event.key == K_a:
        que[10] = True
    if event.key == K_s:
        que[0] = True
    if event.key == K_d:
        que[11] = True
    return que

def player(que):
    for i in range(pad_arr_size):
        if que[i] and s_m[i]:
            s_m[i].play()

def update_value(que):
    for i in range(pad_arr_size):
        if que[i] and s_m[i]:
            pad_values[i] = pad_value_max


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def gen_rbga(color, alpha):
    return (color[0], color[1], color[2], alpha)

def update_ui():
    for i in range(pad_arr_size // max_col):
        for j in range(max_col):
            idx = i * max_col + j
            draw_rect_alpha(window_surface, gen_rbga(text_color, pad_values[idx]), (j * block_size, i * block_size, block_size, block_size))
        
    # reduce value by n
    n = 8
    for i in range(pad_arr_size):
        pad_values[i] = pad_values[i] - n
        if pad_values[i] < 0:
            pad_values[i] = 0

def ard2que(ard):
    # ard: 1,2,3,4,5,6,7,8,9,*,0,#
    # que: 0,1,2,3,4,5,6,7,8,9,*,#
    que = [False for i in range(pad_arr_size)]
    que[1] = ard[0]
    que[2] = ard[1]
    que[3] = ard[2]
    que[4] = ard[3]
    que[5] = ard[4]
    que[6] = ard[5]
    que[7] = ard[6]
    que[8] = ard[7]
    que[9] = ard[8]
    que[10] = ard[9]
    que[0] = ard[10]
    que[11] = ard[11]
    return que

    

last_serial_data = [0 for i in range(pad_arr_size)]
def update_serial_data(que):
    now_serial_data = ard2que([int(x) for x in serial_port.readline().decode('utf-8').strip().split(',')])
    for i in range(pad_arr_size):
        if now_serial_data[i] == 1 and last_serial_data[i] == 0:
            que[i] = True
        last_serial_data[i] = now_serial_data[i]
        

while True:
    window_surface.fill(bg_color)
    text = font.render("Press 1-9, a, s, d to play sound", False, text_color, bg_color)
    window_surface.blit(text, (10, block_size * (pad_arr_size // max_col) + 15))

    que = [False for i in range(pad_arr_size)]

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()


        # from keyboard        
        if event.type == KEYDOWN:
            que = on_parse_keys(event, que)
                
    if serial_port:
        update_serial_data(que)
    update_value(que)
    player(que)
    update_ui()

    pygame.display.update()
    main_clock.tick(system_fps)
