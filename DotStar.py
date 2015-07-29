""" Library for controlling dotstar LEDs

Stephanie Moyerman

April 16, 2015

Note, this library only controls the DotStars over the SPI interface and relies on intel's mraa library 

"""

import mraa as m

# Check to make sure intensity is within accepted range
def checkIntensity(intensity):
    if intensity > 1:
        print "Intensity should be a value between 0 and 1. Setting to max intensity of 1."
        intensity = 1
    if intensity < 0:
        print "Intensity should be a value between 0 and 1. Setting to min intensity of 0."
        intensity = 0
    return intensity


# Check to make sure intensity is within accepted range
def checkColor(R, G, B):
    if R > 255:
        print "Colors should be in the range 0-255. Setting red to max of 255."
        R = 255
    if R < 0:
        print "Colors should be in the range 0-255. Setting red to min of 0."
        R = 0
    if G > 255:
        print "Colors should be in the range 0-255. Setting green to max of 255."
        G = 255
    if G < 0:
        print "Colors should be in the range 0-255. Setting green to min of 0."
        G = 0
    if B > 255:
        print "Colors should be in the range 0-255. Setting blue to max of 255."
        B = 255
    if B < 0:
        print "Colors should be in the range 0-255. Setting blue to min of 0."
        B = 0
    return R, G, B


# Check to make sure intensity array is within accepted range
def checkIntensityArray(intensity):
    for i,j in enumerate(intensity):
        if j > 1:
            print "Intensity should be a value between 0 and 1. Setting to max intensity of 1."
            intensity[i] = 1
        if j < 0:
            print "Intensity should be a value between 0 and 1. Setting to min intensity of 0."
            intensity[i] = 0
        return intensity


# Check to make sure intensity is within accepted range
def checkColorArray(R, G, B):
    for i,j in enumerate(R):
        if j > 255:
            print "Colors should be in the range 0-255. Setting red to max of 255."
            R[i] = 255
        if j < 0:
            print "Colors should be in the range 0-255. Setting red to min of 0."
            R[i] = 0
    for i,j in enumerate(G):
        if j > 255:
            print "Colors should be in the range 0-255. Setting green to max of 255."
            G[i] = 255
        if j < 0:
            print "Colors should be in the range 0-255. Setting green to min of 0."
            G[i] = 0
    for i,j in enumerate(B):
        if j > 255:
            print "Colors should be in the range 0-255. Setting blue to max of 255."
            B[i] = 255
        if j < 0:
            print "Colors should be in the range 0-255. Setting blue to min of 0."
            B[i] = 0
    return R, G, B


# Software SPI write
def sw_spi_out(n,clockPin,dataPin):
    for i in range(8,0,-1):
        n = (n << 1) 
        if (n & 0x80):
            dataPin.write(1)
        else:
            dataPin.write(0)
        clockPin.write(1)
        clockPin.write(0)

# Dotstar class for controlling the DotStar lights
class DotStar():
    nLEDs = 1
    # Pin mapping in mraa library
    mode = 'SPI'
    def __init__(self, nlights):
        self.nLEDs = nlights
    """def SoftwareSPI(self, MOSI, CLK):
        self.mode = 'BB'
        self.MOSI = self.pinmapping[MOSI]
        self.CLK = self.pinmapping[CLK] """
    def setup(self):
        self.header = bytearray(4)
        self.header[0] = 0
        self.header[1] = 0 
        self.header[2] = 0
        self.header[3] = 0        
        self.footer = bytearray(4)
        self.footer[0] = 255
        self.footer[1] = 255
        self.footer[2] = 255
        self.footer[3] = 255
        self.data = bytearray(4)
        self.data[0] = 255  # indicator, do not change
        self.data[1] = 0    # green
        self.data[2] = 0    # blue
        self.data[3] = 0    # red
        # Init SPI using mraa library
        if self.mode == 'SPI':
            self.dev = m.Spi(0)
            self.dev.mode(m.SPI_MODE0)  # mode 0
        elif self.mode == 'BB':
            # Check on GPIO mapping
            self.dataPin = m.Gpio(self.MOSI)
            self.clockPin = m.Gpio(self.CLK)
            self.dataPin.dir(m.DIR_OUT)
            self.dataPin.write(0)
            self.clockPin.dir(m.DIR_OUT)
            self.clockPin.write(0)
        else:
            print "Error on init. Set mode to either 'SPI' or 'BB'" 
    def TurnAllOff(self):
        if self.mode == 'SPI':
            self.dev.write(self.header)
            self.dev.mode(m.SPI_MODE0)
            for i in range(self.nLEDs):
                self.data[1] = 0
                self.data[2] = 0
                self.data[3] = 0
                self.dev.write(self.data)
            self.dev.write(self.footer)
        elif self.mode == 'BB':
            for i in range(4):
                sw_spi_out(0,self.clockPin,self.dataPin)
            for i in range(self.nLEDs):
                for i in range(4):
                    sw_spi_out(0,self.clockPin,self.dataPin)
            for i in range(4):
                sw_spi_out(255,self.clockPin,self.dataPin)
    def AllRed(self, intensity=1): 
        intensity = checkIntensity(intensity)
        if self.mode == 'SPI':
            self.dev.write(self.header)
            for i in range(self.nLEDs):
                self.data[1] = 0
                self.data[2] = 0
                self.data[3] = int(255*intensity)
                self.dev.write(self.data)
            self.dev.write(self.footer)
        elif self.mode == 'BB':
            red = [255, 0, 0, 255]
            for i in range(4):
                sw_spi_out(0,self.clockPin,self.dataPin)
            for i in range(self.nLEDs):
                for j in red:
                    sw_spi_out(j,self.clockPin,self.dataPin)
            for i in range(4):
                sw_spi_out(255,self.clockPin,self.dataPin)
    def AllBlue(self, intensity=1): 
        intensity = checkIntensity(intensity)
        if self.mode == 'SPI':
            self.dev.write(self.header)
            for i in range(self.nLEDs):
                self.data[1] = 0
                self.data[2] = int(255*intensity)
                self.data[3] = 0
                self.dev.write(self.data)
            self.dev.write(self.footer)
    def AllGreen(self, intensity=1): 
        intensity = checkIntensity(intensity)
        if self.mode == 'SPI':
            self.dev.write(self.header)
            for i in range(self.nLEDs):
                self.data[1] = int(255*intensity)
                self.data[2] = 0
                self.data[3] = 0
                self.dev.write(self.data)
            self.dev.write(self.footer)
    def AllColor(self, R, G, B, intensity=1): 
        intensity = checkIntensity(intensity)
        R, G, B = checkColor(R, G, B)
        if self.mode == 'SPI':
            self.dev.write(self.header)
            for i in range(self.nLEDs):
                self.data[1] = int(G*intensity)
                self.data[2] = int(B*intensity)
                self.data[3] = int(R*intensity)
                self.dev.write(self.data)
            self.dev.write(self.footer)
    def Rainbow(self, R, G, B, intensity = [1]):
        if (len(R) == len(G) == len(B) == 1) or (len(R) == len(G) == len(B) == self.nLEDs):
            if (len(intensity) == 1) or (len(intensity) == self.nLEDs):
                intensity = checkIntensityArray(intensity)
                R, G, B = checkColorArray(R, G, B)
                if self.mode == 'SPI':
                    self.dev.write(self.header)
                    for i in range(self.nLEDs):
                        if (len(G) == 1) and (len(intensity) == 1):
                            self.data[1] = int(G[0]*intensity[0])
                            self.data[2] = int(B[0]*intensity[0])
                            self.data[3] = int(R[0]*intensity[0])
                        elif (len(G) == 1) and (len(intensity) > 1):
                            self.data[1] = int(G[0]*intensity[i])
                            self.data[2] = int(B[0]*intensity[i])
                            self.data[3] = int(R[0]*intensity[i])
                        elif (len(G) > 1) and (len(intensity) == 1):
                            self.data[1] = int(G[i]*intensity[0])
                            self.data[2] = int(B[i]*intensity[0])
                            self.data[3] = int(R[i]*intensity[0])
                        elif (len(G) > 1) and (len(intensity) > 1):
                            self.data[1] = int(G[i]*intensity[i])
                            self.data[2] = int(B[i]*intensity[i])
                            self.data[3] = int(R[i]*intensity[i])
                        self.dev.write(self.data)
                    self.dev.write(self.footer)
            else:
                print "Intensity must be an array of length 1 or of length nPixels" 
        else: 
            print "R, G, and B must all be single valued arrays or arrays of length nPixels."







