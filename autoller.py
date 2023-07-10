import keyboard
import mouse
import time
import threading
import random
# import random

inputs_list = []
inputs = []
RECORDING_KEY = 'f11'
PLAY_KEY = 'f10'
EXIT_KEY = 'f12'
CANCEL_CURR_RECORDING_KEY = 'f9'

curr_down_keys = {}

curr_time = time.time()

is_recording = False
is_playing = False
    
print("Miko's bot program\n")

print("F12 to end the program")
print("F11 to record and to end recording")
print("F10 to play and to stop")
print('F9 to cancel current recording')

def key_upped(target_key, input):
    return input.name == target_key and input.event_type == 'up'

class Keyboard_Action:
    def __init__ (self, device, keyboard_key, key_state, delay):
        self.device = device
        self.keyboard_key = keyboard_key
        self.key_state = key_state
        self.delay = delay

def do_keyboard_action(input):
      time.sleep(input.delay * random.randrange(80, 120, 1)/100)
      if input.key_state == 'down':
          keyboard.press(input.keyboard_key)
          curr_down_keys[input.keyboard_key] = True
      else:
          keyboard.release(input.keyboard_key)
          del curr_down_keys[input.keyboard_key]

class Mouse_Action:
    def __init__ (self, device, click_button, x, y, delay):
        self.device = device
        self.click_button = click_button
        self.x = x
        self.y = y
        self.delay = delay

def do_mouse_action(input):
    time.sleep(input.delay)
    mouse.move(input.x + random.randrange(-3,3), input.y+random.randrange(-3,3))
    mouse.click('left')

def keyboard_cb(input):
    global inputs
    global inputs_list
    global RECORDING_KEY
    global PLAY_KEY
    global CANCEL_CURR_RECORDING_KEY
    global curr_time
    global is_recording
    global is_playing

    #KEYBOARD

    #recording
    if key_upped(RECORDING_KEY, input):
        is_recording = not is_recording
        if is_recording and not is_playing:
            print(f'recording #{len(inputs_list) + 1} start')
        elif not is_recording:
            print(f'recording #{len(inputs_list) + 1} end')
            inputs_list.append(inputs)
            inputs = []

    if not is_playing and is_recording:
        if input.name == RECORDING_KEY or input.name == PLAY_KEY:
            curr_time = time.time()
            pass
        elif input.name == CANCEL_CURR_RECORDING_KEY:
            is_recording = False
            inputs = []
            print(f'current recording #{len(inputs_list) + 1} canceled')
        else:
            now_time = time.time()
            elapsed_time = now_time - curr_time
            curr_time = now_time
            inputs.append(Keyboard_Action('keyboard', input.name, input.event_type, elapsed_time))        
    
    #play
    if not is_recording and key_upped(PLAY_KEY, input):
        is_playing = not is_playing
        if not is_playing:
            print('playing has stopped')
            for keys in curr_down_keys.keys():
                keyboard.release(keys)
        threading.Thread(target = play_recording, daemon=True).start()

def play_recording():
    global inputs_list
    global is_playing
    if len(inputs_list) == 0:
        print('no recordings available')
        return
    while(is_playing):
        index = random.randrange(0, len(inputs_list))
        inputs = inputs_list[index]
        print(f'recording #{index + 1} is playing')
        for input in inputs:
            if not is_playing:
                break
            elif input.device == 'keyboard':
                do_keyboard_action(input)
            else:
                do_mouse_action(input)

          

  
keyboard.hook(keyboard_cb)

def mouse_cb():
    global is_recording
    global curr_time

    if is_recording:
        now_time = time.time()
        elapsed_time = now_time - curr_time
        curr_time = now_time
        (x,y) = mouse.get_position()
        inputs.append(Mouse_Action('mouse', 'primary', x, y, elapsed_time))


  

mouse.on_click(mouse_cb)

while True:
    if keyboard.is_pressed(EXIT_KEY):
        break
    time.sleep(0.025)