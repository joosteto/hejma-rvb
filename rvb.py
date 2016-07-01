#!/usr/bin/python
# Example using a character LCD plate.
import time
import sys
sys.path.append("../ws2812-spi")
import ws2812
import time
import Adafruit_CharLCD as LCD
import spidev
import numpy

nLED=30

def rvb(spi, nLED, intencity):
    ws2812.write2812(spi, [(intencity/3, intencity, intencity/9)]*nLED)
    
def white(spi, nLED, intencity):
    ws2812.write2812(spi, [(intencity, intencity, intencity)]*nLED)
    
wave_indices=4*numpy.array(range(nLED), dtype=numpy.uint32)*numpy.pi/nLED
wave_period0=2
wave_period1=2.1
wave_period2=2.2
wave_tStart=time.time()
def wave(spi, nLED, intencity):
    t=wave_tStart-time.time()
    #t=1.1
    f=numpy.zeros((nLED,3))
    f[:,0]=numpy.sin(2*numpy.pi*t/wave_period0+wave_indices)
    f[:,1]=numpy.sin(2*numpy.pi*t/wave_period1+wave_indices)
    f[:,2]=numpy.sin(2*numpy.pi*t/wave_period2+wave_indices)
    f=(intencity)*((f+1.0)/2.0)
    fi=numpy.array(f, dtype=numpy.uint8)
    #print fi[0]
    #time_write2812(spi, fi)
    ws2812.write2812(spi, fi)
    time.sleep(0.01)
    


spi = spidev.SpiDev()
spi.open(0,0)

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()
lcd.set_color(0.0, 0.0, 0.0)

# Make list of button value, text, and backlight color.
buttons = ( (LCD.SELECT, 'Select', (1,1,1)),
            (LCD.LEFT,   'Left'  , (1,0,0)),
            (LCD.UP,     'Up'    , (0,0,1)),
            (LCD.DOWN,   'Down'  , (0,1,0)),
            (LCD.RIGHT,  'Right' , (1,0,1)) )

modes=[("White", white, [10]),
       ("RVB",   rvb, [10,10,10]),
       ("Wave",  wave, [10,10,10]),
]
imode=2
intencity=20
prevSelect=False
lastAction=0
lcd.clear()
lcd.message(modes[imode][0])
while True:
    didAction=False
    modes[imode][1](spi, nLED, intencity)
    # Loop through each button and check if it is pressed.
    #print imode, intencity
    if lcd.is_pressed(LCD.SELECT):
        if not prevSelect:
            imode = (imode+1) % len(modes)
            didAction=True
        prevSelect=True
    else:
        prevSelect=False
    if lastAction<time.time()-0.05:
        if lcd.is_pressed(LCD.DOWN):
            intencity=max(0,(intencity*97)/100-1)
            didAction=True
        elif lcd.is_pressed(LCD.UP):
            intencity=min(255,(intencity*100)/97+1)
            didAction=True
    if didAction:
        lcd.clear()
        lcd.message(modes[imode][0]+'\n'+str(intencity))
        lastAction=time.time()
            
