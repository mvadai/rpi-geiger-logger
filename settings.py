# settings.py for the Cosmic Ray detection / GM logging application
# v0.1
#
# (c) 2014 Mihaly Vadai 
# Cosmic ray datalogging software is licensed under a 
# Creative Commons Attribution-ShareAlike 4.0 International License.
# Please use this link as a reference when using any parts of this code: 
# http://mihalysprojects.weebly.com/blog/geiger-muller-cosmic-ray-datalogger-program-for-raspberry-pi-in-python
# Thank you.
# This is free software and comes with absolutely no warranty to the extent permitted by applicable law.

#Set the default logging time below
logging_time = 60

#Set the GPIOs you connect to the 3V pulse from the GM tubes and the coincidence detector below.
#To disable a pin set it to 0.
#This is BCM numbering. In other words this is the Broadcom SOC channel number. see: http://pi.gadgetoid.com/pinout
GM1 = 22
GM2 = 24
GM3 = 0

#Coincidence input GPIO
COSMIC = 25

#Set the trigger type here it's either FALLING or RISING. Default is FALLING.
#For some GM counters this might be rising.
trigger_type_gm1 = 'FALLING'
#trigger_type_gm1 = 'RISING'
trigger_type_gm2 = 'FALLING'
#trigger_type_gm2 = 'RISING'
trigger_type_gm3 = 'FALLING'
#trigger_type_gm3 = 'RISING'
trigger_type_cosmic = 'FALLING'
#trigger_type_cosmic = 'RISING'

# Set the CPS_to_mR for the type of GM tube you're using
# For SBM20 it's between 22 CPS (Co-60) and 29 CPS (Ra-226) for 1 mR/h.
# This can be any unit provided it is consistent with the conversion
# rate to uGy.

CPS_to_mR_gm1 = 24
CPS_to_mR_gm2 = 24
CPS_to_mR_gm3 = 24
CPS_to_mR_cosmic = 24

#Set the conversion rate between mR or chosen unit and microGy (or microSv)
#if the tube you're using is calibrated for uGy, use 1 here.

CPStomR_gm1 = 8.77
CPStomR_gm2 = 8.77
CPStomR_gm3 = 8.77
CPStomR_cosmic = 8.77

# Set the screen refresh rate in seconds.
refresh = 1
