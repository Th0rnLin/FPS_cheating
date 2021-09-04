import win32gui
import pyscreenshot
import pyautogui
import sys
import cv2
import os
import argparse
from sys import platform

def save_window_grab(name='FPS_cheating'):
    handle=win32gui.FindWindow(0, name) # find window
    x1, y1, x2, y2=win32gui.GetWindowRect(handle) # get position
    img=pyscreenshot.grab(bbox=(x1, y1, x2, y2)) # screen shot
    img.save('./image.png')

def save_screen_grab():
    img = pyscreenshot.grab()
    img.save('./image.png')

def move_and_click(x, y, t=2):
    pyautogui.click(x=x, y=y, duration=0.1, clicks=t, interval=0.1)

def openpose(image_name="./image.png"):
    try:
        # Import Openpose (Windows/Ubuntu/OSX)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + './bin/python/openpose/Release');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + './bin;'
            import pyopenpose as op
        except ImportError as e:
            print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e

        # Flags
        parser = argparse.ArgumentParser()
        parser.add_argument("--image_path", default=image_name, help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
        args = parser.parse_known_args()

        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = "./models/"

        # Add others in path?
        for i in range(0, len(args[1])):
            curr_item = args[1][i]
            if i != len(args[1])-1: next_item = args[1][i+1]
            else: next_item = "1"
            if "--" in curr_item and "--" in next_item:
                key = curr_item.replace('-','')
                if key not in params:  params[key] = "1"
            elif "--" in curr_item and "--" not in next_item:
                key = curr_item.replace('-','')
                if key not in params: params[key] = next_item

        # Construct it from system arguments
        # op.init_argv(args[1])
        # oppython = op.OpenposePython()

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        # Process Image
        datum = op.Datum()
        imageToProcess = cv2.imread(args[0].image_path)
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))

        # Display Image
        #print("Body keypoints: \n" + str(datum.poseKeypoints))
        #cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
        #cv2.waitKey(0)

        #print(datum.poseKeypoints[0])
        return datum.poseKeypoints[0]
        
    except Exception as e: pass
