# The main program for the Cosmic Ray detection / GM logging application
# v0.1
# Set the GPIOs and the defaults in settings.py 
# 
# (c) 2014 Mihaly Vadai 
# Cosmic ray datalogging software is licensed under a 
# Creative Commons Attribution-ShareAlike 4.0 International License.
# Please use this link as a reference when using any parts of this code:
# http://mihalysprojects.weebly.com/blog/geiger-muller-cosmic-ray-datalogger-program-for-raspberry-pi-in-python 
# Thank you.
# This is free software and comes with absolutely no warranty to the extent permitted by applicable law.


import RPi.GPIO as GPIO
from time import time, gmtime, sleep, strftime
from COUNTER import COUNTER
import sys
from settings import *

GM1 = int(GM1)
GM2 = int(GM2)
GM3 = int(GM3)
COSMIC = int(COSMIC)
CPS_to_mR_gm1 = int(CPS_to_mR_gm1)
CPS_to_mR_gm2 = int(CPS_to_mR_gm2)
CPS_to_mR_gm3 = int(CPS_to_mR_gm3)
CPS_to_mR_cosmic = int(CPS_to_mR_cosmic)
CPStomR_gm1 = float(CPStomR_gm1)
CPStomR_gm2 = float(CPStomR_gm2)
CPStomR_gm3 = float(CPStomR_gm3)
CPStomR_cosmic = float(CPStomR_cosmic)
logging_time = int(logging_time)
refresh_rate = int(refresh)

#checking settings
if trigger_type_gm1 != 'FALLING' and trigger_type_gm1 != 'RISING':
	raise ValueError('Invalid trigger setting for GM1 in settings.py. Must be either FALLING or RISING. Exiting.')
	
if GM1 < 1 or GM1 > 28:
	raise ValueError('Invalid GM1 GPIO. Check settings.py. Must be >= 1 and <= 27. Exiting.')

if GM2 < 0 or GM2 > 28:
	raise ValueError('Invalid GM2 GPIO. Check settings.py. Must be >= 0 and <= 27. Exiting.')

if GM3 < 0 or GM3 > 28:
	raise ValueError('Invalid GM2 GPIO. Check settings.py. Must be >= 0 and <= 27. Exiting.')

if COSMIC < 0 or COSMIC > 28:
	raise ValueError('Invalid COSMIC GPIO. Check settings.py. Must be >= 0 and <= 27. Exiting.')

if trigger_type_gm2 != 'FALLING' and trigger_type_gm2 != 'RISING' and GM2 != 0:
	raise ValueError('Invalid trigger setting for GM2 in settings.py. Must be either FALLING or RISING. Exiting.')

if trigger_type_gm3 != 'FALLING' and trigger_type_gm3 != 'RISING' and GM3 != 0:
	raise ValueError('Invalid trigger setting for GM2 in settings.py. Must be either FALLING or RISING. Exiting.')

if trigger_type_cosmic != 'FALLING' and trigger_type_cosmic != 'RISING' and COSMIC != 0:
	raise ValueError('Invalid trigger setting for COSMIC in settings.py. Must be either FALLING or RISING. Exiting.')


if CPS_to_mR_gm1 < 1:
	print('Warning: invalid dose conversion GM1. Check settings.py.')
	print('Assuming you use SBM 20 at 24 CPM / 1 mR/h')
	CPS_to_mR_gm1 = 24

if CPS_to_mR_gm2 < 1 and GM2 != 0:
	print('Warning: invalid dose conversion GM2. Check settings.py.')
	print('Assuming you use SBM 20 at 24 CPM / 1 mR/h')
	CPS_to_mR_gm2 = 24

if CPS_to_mR_gm3 < 1 and GM3 != 0:
	print('Warning: invalid dose conversion GM2. Check settings.py.')
	print('Assuming you use SBM 20 at 24 CPM / 1 mR/h')
	CPS_to_mR_gm3 = 24
	
if CPS_to_mR_cosmic < 1  and COSMIC != 0:
	print('Warning: invalid dose conversion COSMIC. Check settings.py.')
	print('Assuming you use SBM 20 at 24 CPM / 1 mR/h')
	CPS_to_mR_cosmic = 24

	
if logging_time < 1:
	print('Warning: default logging time not valid. Check settings.py.')
	print('Continuing for 60 seconds.')
	logging_time = 60

if len(sys.argv) == 2:
	logging_time = int(sys.argv[1])

if logging_time < 1:
	print('Warning: logging time not valid. Check your terminal input.')
	print('Continuing for 60 seconds.')
	logging_time = 60

#starting	
start_time = time()

sys.stderr.write("\x1b[2J\x1b[H")
GPIO.setmode(GPIO.BCM)
GPIO.setup(GM1, GPIO.IN)
GM1_COUNTER = COUNTER(GM1, CPS_to_mR_gm1, CPStomR_gm1) 
if GM2 != 0:
	GPIO.setup(GM2, GPIO.IN)
	GM2_COUNTER = COUNTER(GM2, CPS_to_mR_gm2, CPStomR_gm2)
if GM3 != 0:
	GPIO.setup(GM3, GPIO.IN)
	GM3_COUNTER = COUNTER(GM3, CPS_to_mR_gm3, CPStomR_gm3)
if COSMIC != 0:
	GPIO.setup(COSMIC, GPIO.IN)
	COSMIC_COUNTER = COUNTER(COSMIC, CPS_to_mR_cosmic, CPStomR_cosmic)

start = strftime("%a, %d %b %Y %H:%M:%S", gmtime())

def print_output():
	sys.stderr.write("\x1b[2J\x1b[H")
	print 'Cosmic Ray / GM logger\n'.center(72)
	print '{0:8}{1:12}{2:7}{3:14}{4:12}{5}'.format('Setup', 'Signal', 'GPIO', 'CPS to mR/h', 'mR to uGy', 'Trigger')
	print '{0:8}{1:12}{2:4d}{3:14d}{4:12.3f}   {5}'.format('', 'GM1', GM1, CPS_to_mR_gm1, CPStomR_gm1, trigger_type_gm1)
	if GM2 != 0:
		print '{0:8}{1:12}{2:4d}{3:14d}{4:12.3f}   {5}'.format('', 'GM2', GM2, CPS_to_mR_gm2, CPStomR_gm2, trigger_type_gm2)
	if GM3 != 0:
		print '{0:8}{1:12}{2:4d}{3:14d}{4:12.3f}   {5}'.format('', 'GM3', GM3, CPS_to_mR_gm3, CPStomR_gm3, trigger_type_gm3)
	if COSMIC != 0:
		print '{0:8}{1:12}{2:4d}{3:14d}{4:12.3f}   {5}'.format('', 'COSMIC', COSMIC, CPS_to_mR_cosmic, CPStomR_cosmic, trigger_type_cosmic)
	print '\nDatalogging started: {0}\n'.format(start)
	print '{0:9}{1:15}{2:8}{3:10}{4:15}{5:15}'.format('Signal','Total counts','CPM','Av. CPM', 'Dose uGy/h', 'Av. Dose uGy/h')
	print '{0:9}{1:12d}   {2:3d}     {3:7d}   {4:10.3f}     {5:14.3f}\n'.format('GM1',GM1_COUNTER.CNT, GM1_COUNTER.cpm(), GM1_COUNTER.av_cpm(), GM1_COUNTER.dose(), GM1_COUNTER.av_dose())
	if GM2 != 0:
		print '{0:9}{1:12d}   {2:3d}     {3:7d}   {4:10.3f}     {5:14.3f}\n'.format('GM2',GM2_COUNTER.CNT, GM2_COUNTER.cpm(), GM2_COUNTER.av_cpm(), GM2_COUNTER.dose(), GM2_COUNTER.av_dose())
	if GM3 != 0:
		print '{0:9}{1:12d}   {2:3d}     {3:7d}   {4:10.3f}     {5:14.3f}\n'.format('GM3',GM3_COUNTER.CNT, GM3_COUNTER.cpm(), GM3_COUNTER.av_cpm(), GM3_COUNTER.dose(), GM3_COUNTER.av_dose())
	if COSMIC != 0:
		print '{0:9}{1:15}{2:8}{3:10}{4:15}{5:15}'.format('Signal','Total counts','CPH','Av. CPH', 'Dose uGy/h', 'Av. Dose uGy/h')
		print '{0:9}{1:12d}   {2:3d}     {3:7d}   {4:10.4f}     {5:14.4f}\n'.format('COSMIC',COSMIC_COUNTER.CNT, COSMIC_COUNTER.cph(), COSMIC_COUNTER.av_cph(), COSMIC_COUNTER.doseh(), COSMIC_COUNTER.av_doseh())
	print 'Time remaining: {0:d} s\n'.format(int(round(logging_time - (time() - start_time))))
	print '(c) 2014 Mihaly Vadai'
	print 'For more information visit:\nhttp://mihalysprojects.weebly.com/blog/category/cosmic-ray'

# The GM Event detections run as a separate thread
# hence this helper function - classes are declared in main.

def add_detection(channel):
	if channel == GM1:
		GM1_COUNTER.update()
	if channel == GM2 and GM2 != 0:
		GM2_COUNTER.update()
	if channel == GM3 and GM3 != 0:
		GM3_COUNTER.update()
	if channel == COSMIC and COSMIC != 0:
		COSMIC_COUNTER.update()
		
if trigger_type_gm1 == 'FALLING':
	GPIO.add_event_detect(GM1, GPIO.FALLING, callback=add_detection)
else:
	GPIO.add_event_detect(GM1, GPIO.RISING, callback=add_detection)

if GM2 != 0:
	if trigger_type_gm2 == 'FALLING':
		GPIO.add_event_detect(GM2, GPIO.FALLING, callback=add_detection)
	else:
		GPIO.add_event_detect(GM2, GPIO.RISING, callback=add_detection)

if GM3 != 0:
	if trigger_type_gm3 == 'FALLING':
		GPIO.add_event_detect(GM3, GPIO.FALLING, callback=add_detection)
	else:
		GPIO.add_event_detect(GM3, GPIO.RISING, callback=add_detection)
		
if COSMIC != 0:
	if trigger_type_cosmic == 'FALLING':
		GPIO.add_event_detect(COSMIC, GPIO.FALLING, callback=add_detection)
	else:
		GPIO.add_event_detect(COSMIC, GPIO.RISING, callback=add_detection)
	

# Updating the display
	
while time() < start_time + logging_time:
	print_output()
	sleep(refresh_rate)

# writing raw data
print 'Calculating statistics and wiring data to files. This can take considerable time.\n'
GM1_COUNTER.csv_write()
print '{0:25}{1}'.format('GM1 Raw:',GM1_COUNTER.filename)
GM1_COUNTER.exponential()
print '{0:25}{1}\n'.format('GM1 Exponential:', GM1_COUNTER.expfilename)

if GM2 != 0:
	GM2_COUNTER.csv_write()
	print '{0:25}{1}'.format('GM2 Raw:',GM2_COUNTER.filename)
	GM2_COUNTER.exponential()
	print '{0:25}{1}\n'.format('GM2 Exponential:', GM2_COUNTER.expfilename)
	
if GM3 != 0:
	GM3_COUNTER.csv_write()
	print '{0:25}{1}'.format('GM3 Raw:',GM3_COUNTER.filename)
	GM3_COUNTER.exponential()
	print '{0:25}{1}\n'.format('GM3 Exponential:', GM3_COUNTER.expfilename)
	
if COSMIC != 0:
	COSMIC_COUNTER.csv_write()
	print '{0:25}{1}'.format('COSMIC Raw:',COSMIC_COUNTER.filename)
	COSMIC_COUNTER.exponential()
	print '{0:25}{1}'.format('COSMIC Exponential:', COSMIC_COUNTER.expfilename)

GPIO.cleanup()
