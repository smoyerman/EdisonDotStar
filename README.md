# EdisonDotStar
Python Library for Dot Stars and Intel Edison

Requires most up to date mraa library for intel edison. If you've never installed this, do the following (make sure Edison is on the interwebs)

# echo "src mraa-upm http://iotdk.intel.com/repos/1.1/intelgalactic" > /etc/opkg/mraa-upm.conf
# opkg update
# opkg install libmraa0

DotStars must be hooked up over the SPI CLK and MOSI lines for this library to work. There's no bitbanging of SPI here. 

Lots of example usage is shown in the example.py file. 

