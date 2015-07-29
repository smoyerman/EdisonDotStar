import DotStar
import time

# Initiate DotStar Object, must always call setup function
DS = DotStar.DotStar(8)  # set nLEDs here
DS.setup()

# Play with the lights - all red
DS.AllRed()
time.sleep(1)
DS.TurnAllOff()

# Play with the lights - all red but dimmer
DS.AllRed(0.5)  # Half intensity, specify a value between 0 and 1
time.sleep(1)
DS.TurnAllOff()

# Similar for green and blue 
DS.AllGreen(0.1)  # Specify intensity
time.sleep(1)
DS.TurnAllOff()
DS.AllBlue(0.8)  # Specify intensity
time.sleep(1)
DS.TurnAllOff()

# Set them all to a nice purple at brightest intensity
R = 100     # Values between 0-255
G = 50
B = 180
intensity = 0.4 
DS.AllColor(R, G, B, intensity)  # Can leave intensity unspecified for default of 1
time.sleep(1)
DS.TurnAllOff()

# Toggle RGB colors
R = [255,0,0,255,0,0,255,0]
G = [0,255,0,0,255,0,0,255]
B = [0,0,255,0,0,255,0,0]
intensity = [1,1,1,0.6,0.6,0.6,0.3,0.3]  
DS.Rainbow(R, G, B, intensity)
time.sleep(1)
DS.TurnAllOff()

# And something kind of cute - march the rainbow
for i in range(20):
    DS.Rainbow(R, G, B, intensity)
    endofR = R[-1]
    R = R[:-1]
    R.insert(0,endofR)
    endofG = G[-1]
    G = G[:-1]
    G.insert(0,endofG)
    endofB = B[-1]
    B = B[:-1]
    B.insert(0,endofB)
    time.sleep(0.5)

DS.TurnAllOff()

