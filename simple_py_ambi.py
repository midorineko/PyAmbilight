from rgb_cie import Converter
from PIL import ImageGrab
import httplib2
import time
from qhue import Bridge

setting_device = 'yourappid'
setting_bridge = 'yourbridgeip'
setting_light_count = 4
b = Bridge(setting_bridge, setting_device)

globvar = 0

def set_globvar_one(x):
    global globvar    # Needed to modify global copy of globvar
    globvar = x
set_globvar_one(0)
def set_globvar_two(x):
    global globvar_two    # Needed to modify global copy of globvar
    globvar_two = x
set_globvar_two(0)
def mainLoop():

    while True:
        start()

def start():
    x, y = getPixels()
    changeLight(x,y)
    time.sleep(.05)

def changeLight(x, y):
    x = round(x, 2)
    y = round(y, 2)
    if globvar - .01 < x < globvar + .01:
        x = globvar
    set_globvar_one(x)
    if globvar_two - .01 < y < globvar_two + .01:
        y = globvar_two
    set_globvar_two(y)

    for t in range(1,setting_light_count+1):
        b.lights(t, 'state', bri=255, on=True, xy=[x, y])

def getPixels():
        #grab screenshot and get the size
        image = ImageGrab.grab()
        im = image.load()
        maxX, maxY = image.size
        step = 100
        #loop through pixels for rgb data
        data = []
        for y in range(0, maxY, step):
            for x in range(0, maxX, step):
                pixel = im[x,y]
                data.append(pixel)

        #loop and check for white/black to exclude from averaging
        r = 0
        g = 0
        b = 0
        threshMin = 60
        threshMax = 200
        counter = 0
        for z in range(len(data)):
            rP, gP, bP, brightness = data[z]
            if rP > threshMax and gP > threshMax and bP > threshMax or rP < threshMin and gP < threshMin and bP < threshMin:
                pass
            else:
                r+= rP
                g+= gP
                b+= bP
                counter+= 1
        if counter > 0:
            rAvg = r/counter
            gAvg = g/counter
            bAvg = b/counter

            converter = Converter()
            hueColor = converter.rgbToCIE1931(rAvg, gAvg, bAvg)
            return hueColor
        else:
            print('problem')
            return (0,0)

mainLoop()
