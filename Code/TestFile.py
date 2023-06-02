from machine import Pin,I2C
from neopixel import NeoPixel
from MX1508 import *
from VL53L0X import *
from tcs34725 import *
from time import sleep_ms,sleep
import uasyncio as asio
import aioespnow
import network

Lt=60
R_W_count,W_count,col_id,col_id_l,direct,di,dist,busy,busy_col,col_sel=0,0,0,0,0,0,500,0,0,5 
color=['Red','Yellow','White','Green','Black','Cyan','Blue','Magenta']
debug=1

def color_det():
    global col_id,col_id_l
    rgb=tcs.read(1)
    r,g,b=rgb[0],rgb[1],rgb[2]
    h,s,v=rgb_to_hsv(r,g,b)
    if 352<h<365:
        col_id_l=col_id
        col_id=0
    if 61<h<120:
        col_id_l=col_id
        col_id=1
    elif 121<h<180:
        if v>1000:
            col_id_l=col_id
            col_id=2
        elif 100<v<800:
            col_id_l=col_id
            col_id=3
        elif v<100:
            col_id_l=col_id
            col_id=4
    elif 181<h<240:
        if v>400:
            col_id_l=col_id
            col_id=5
        else:
            col_id_l=col_id
            col_id=6
    elif 330<h<352:
        col_id_l=col_id
        col_id=7 
    if debug:
        print('Color is {}. R:{} G:{} B:{} H:{:.0f} S:{:.0f} V:{:.0f}'.format(color[col_id],r,g,b,h,s,v)) 
        
def LED_cont():
        if col_id==0:
            np[0]=(Lt,0,0)
        elif col_id==1:
            np[0]=(Lt,Lt,0)
        elif col_id==2:
            np[0]=(Lt,Lt,Lt)
        elif col_id==3:
            np[0]=(0,Lt,0)
        elif col_id==4:
            np[0]=(0,0,0)
            np.write()
            np[0]=(Lt,0,0)
            np.write()
        elif col_id==5:
            np[0]=(0,Lt,Lt)
        elif col_id==6:
            np[0]=(0,0,Lt) 
        elif col_id==7:
            np[0]=(Lt,0,Lt)
        print("Color "+str(col_id) )    
        np.write()
        
dist = 500
speed=1023

i2c_bus = I2C(1,sda=Pin(21), scl=Pin(22))
tcs = TCS34725(i2c_bus)#17 16

tcs.gain(4)#gain must be 1, 4, 16 or 60
tcs.integration_time(80)
i2c_bus1 = I2C(0,sda=Pin(17), scl=Pin(16))

tof = VL53L0X(i2c_bus1)
NUM_OF_LED = 2
np = NeoPixel(Pin(27), NUM_OF_LED)

motor_L = MX1508(33, 32)
motor_R = MX1508(12, 14)

while 1:
    motor_R.reverse(speed)
    motor_L.reverse(speed)

    color_det()
    LED_cont()
    tof.start()
    dist_l=dist
    dist=tof.read()-65
    tof.stop()
    print(dist)


