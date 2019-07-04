#!/usr/bin/python3
# File name   : car_dir.py
# Description : By controlling Servo,the camera can move Up and down,left and right and the Ultrasonic wave can move to left and right.
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12
from __future__ import division
import time

import Adafruit_PCA9685

def replace_num(initial,new_num):   #Call this function to replace data in '.txt' file
    newline=""
    str_num=str(new_num)
    with open("set.txt","r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = initial+"%s" %(str_num+"\n")
            newline += line
    with open("set.txt","w") as f:
        f.writelines(newline)

def num_import_int(initial):        #Call this function to import data from '.txt' file
    with open("set.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=int(snum)
    return n

#import the settings for servos
vtr_mid_orig    = num_import_int('E_C1:')
hoz_mid_orig    = num_import_int('E_C2:')

turn_right_max  = num_import_int('turn_right_max:')
turn_left_max   = num_import_int('turn_left_max:')
turn_middle     = num_import_int('turn_middle:')

look_up_max    = num_import_int('look_up_max:')
look_down_max  = num_import_int('look_down_max:')
look_right_max = num_import_int('look_right_max:')
look_left_max  = num_import_int('look_left_max:')

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

def turn_ang(ang):
    if ang < turn_right_max:
        ang = turn_right_max
    elif ang > turn_left_max:
        ang = turn_left_max
    else:
        pass
    pwm.set_pwm(2,0,ang)

def right():
    pwm.set_pwm(2, 0, turn_right_max)

def left():
    pwm.set_pwm(2, 0, turn_left_max)

def middle():
    pwm.set_pwm(2, 0, turn_middle)

def ultra_turn(hoz_mid):
    pwm.set_pwm(1, 0, hoz_mid)

def camera_turn(vtr_mid):
    pwm.set_pwm(0, 0, vtr_mid)

def ahead():
	pwm.set_pwm(1, 0, hoz_mid_orig)
	pwm.set_pwm(0, 0, vtr_mid_orig)

def set_pwm(channel, deflection):
    # set any PWM channel based on % deflection +/- and min/max position value
    if channel == "0":
        pwm.set_pwm(0, 0, getSteer(look_down_max, vtr_mid_orig, look_up_max, deflection))    
    elif channel == "1":
        pwm.set_pwm(1, 0, getSteer(look_left_max, hoz_mid_orig, look_right_max, deflection))            
    elif channel == "2":
        pwm.set_pwm(2, 0, getSteer(turn_left_max, turn_middle, turn_right_max, deflection))     

def getSteer(min, center, max, deflection):  #Calc PWM value from +/- percetage deflection and min, center and max PWM value
    newPos = center
    deflectionNum = ideflection
    if deflectionNum > 0:  # right/up
        newPos = center - (center - min) * (abs(deflectionNum) / 100)
    elif deflectionNum:  # left/down      
        newPos = center + (max - center) * (abs(deflectionNum) / 100)
    else:
        newPos = center
    return int(newPos)