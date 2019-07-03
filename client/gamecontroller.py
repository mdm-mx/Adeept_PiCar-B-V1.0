"""Simple example showing how to get gamepad events."""
from __future__ import print_function
from inputs import get_gamepad
import time
import math

last_motorSetting = 0
last_PWMSetting = [0,0,0,0,0,0,0,0,0,0,0,0]  #12 channels

def getPWM_Command(channel, event_state ):
    global last_PWMSetting
    command = ""
    deflection = calcPercentDeflection(event_state)
    if deflection != last_PWMSetting[channel]:
        command = "pwm_set:" + str(channel) + ":" + str(deflection)
        last_PWMSetting[channel] = deflection
    return command

def read(cb):
    """Just print out some event infomation when the gamepad is used."""
    try:
        events = get_gamepad()  #test game pad exists
    except:
        print("Unable to connect to gamepad.  Use WASD controls instead.")
        return
        
    while 1:
        events = get_gamepad()
        for event in events:
            if event.ev_type == "Absolute":
                if event.code == "ABS_X":
                    # STEERING channel 2
                    cmd = getPWM_Command(2, event.state)
                    if cmd != "":
                        cb(cmd)  # call back
                elif event.code == "ABS_Y":
                    global last_motorSetting
                    motorSetting = calcPercentDeflection(event.state)
                    if motorSetting != last_motorSetting:
                        cmd = "motor_set:" + str(motorSetting)
                        last_motorSetting = motorSetting
                        cb(cmd)  # call back           
                elif event.code == "ABS_RY":
                    # Camera TILT channel 0
                    cmd = getPWM_Command(0, event.state)
                    if cmd != "":
                        cb(cmd)  # call back                    
                elif event.code == "ABS_RX":
                    # Camera PAN channel 1
                    cmd = getPWM_Command(1, event.state)
                    if cmd != "":
                        cb(cmd)  # call back       
                elif event.code == "ABS_HAT0X":
                    print(event.code, event.state)                      
                elif event.code == "ABS_HAT0Y":
                    print(event.code, event.state)                                             
            elif (event.ev_type == "Key" and event.state==1):  # ignoring button up, so this is a momentary switch
                if event.code == "BTN_WEST":
                    print("X")
                    cb("scan")
                elif event.code == "BTN_EAST":
                    cb("stop")
                elif event.code == "BTN_NORTH":
                    print("Y")
                elif event.code == "BTN_SOUTH":
                    print("A")
                elif event.code == "BTN_TL":
                    cb("lights_ON")  # call back      
                elif event.code == "BTN_TR":
                    print("Button-Top-Right")                                                                                        
                elif event.code == "BTN_START":
                    cb("middle") 
                elif event.code == "BTN_SELECT":
                    cb("ahead")                                        

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
    return int(float(perct))

def writeoutput(cmd):  #testing stub for callback function; just print command.
    print(cmd)

if __name__ == "__main__":
    read(writeoutput)