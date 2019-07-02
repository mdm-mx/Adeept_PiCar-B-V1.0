"""Simple example showing how to get gamepad events."""
from __future__ import print_function
from inputs import get_gamepad
import time
import math
import client

def read():
    """Just print out some event infomation when the gamepad is used."""
    while 1:
        events = get_gamepad()
        for event in events:
            if event.ev_type == "Absolute":
                if event.code == "ABS_X":
                    printIfNotZero("Steer",calcPercentDeflection(event.state))
                elif event.code == "ABS_Y":
                    printIfNotZero("Motor",calcPercentDeflection(event.state))
                elif event.code == "ABS_RY":
                    printIfNotZero("Camera Tilt",calcPercentDeflection(event.state))                            
                elif event.code == "ABS_RX":
                    printIfNotZero("Camera Pan",calcPercentDeflection(event.state))
                elif event.code == "ABS_HAT0X":
                    print(event.code, event.state)                      
                elif event.code == "ABS_HAT0Y":
                    print(event.code, event.state)                                             
            elif (event.ev_type == "Key" and event.state==1):  # ignoring button up, so this is a momentary switch
                if event.code == "BTN_WEST":
                    print("X")
                    client.scan(event)
                elif event.code == "BTN_EAST":
                    print("B")
                elif event.code == "BTN_NORTH":
                    print("Y")
                elif event.code == "BTN_SOUTH":
                    print("A")
                elif event.code == "BTN_TL":
                    print("Button-Top-Left")    
                    #lights_ON(event)
                elif event.code == "BTN_TR":
                    print("Button-Top-Right")                                                                                        
                elif event.code == "BTN_START":
                    print("Button-Start")    
                elif event.code == "BTN_SELECT":
                    print("Button-Select")                                            

def printIfNotZero(command,perct):
    if perct != 0:
        print(command,perct) 

def calcPercentDeflection(value):
    # return percentage deflection +/-, ignoring small deflections!
    min_deflection = 5000
    perct = 0
    if (value < (min_deflection * -1)):
        perct =  ((value + min_deflection) * 100) / (32768- min_deflection)
    elif (value > min_deflection):
        perct = ((value - min_deflection) * 100) / (32767 - min_deflection)
    else:        
        perct= 0
    return round(perct,0)

if __name__ == "__main__":
    read()
#read()