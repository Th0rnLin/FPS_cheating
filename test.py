from function import *
from pynput import keyboard

def on_press(key):
    try:
        print('key {0} press'.format(key.char))
        if key.char=='c':
            save_screen_grab()
            test_image = './image.png'
            coorindate=openpose(test_image)
            try:
                x, y=int(coorindate[0][0]), int(coorindate[0][1])
                move_and_click(x, y)
            except: pass
    except AttributeError: print('key {0} press'.format(key))

def on_release(key):
    try:
        print('key {0} release'.format(key.char))    
    except AttributeError: print('key {0} release'.format(key))
    if key==keyboard.Key.esc: return False

if __name__=='__main__':
    print('it\' begin!')
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
