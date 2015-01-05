# The COUNTER.py class for the the Cosmic Ray detection / GM logging 
# application # v0.1
#
# (c) 2014 Mihaly Vadai 
# Cosmic ray datalogging software is licensed under a 
# Creative Commons Attribution-ShareAlike 4.0 International License.
# Please use this link as a reference when using any parts of this code: 
# http://mihalysprojects.weebly.com/blog/geiger-muller-cosmic-ray-datalogger-program-for-raspberry-pi-in-python
# Thank you.
# This is free software and comes with absolutely no warranty to the extent permitted by applicable law.

import csv
import gc
from time import time, gmtime, strftime
from math import log

class COUNTER:
	def __init__(self, pin, CPStomR, mRtouGy):
		self.PIN = pin
		self.CPStomR = CPStomR
		self.mRtouGy = mRtouGy
		self.START_TIME = time()
		self.CNT = 0
		self.TIMES = []
		self.DOSES = []
		self.CPMS = []
	
	def update(self):
		self.CNT += 1
		self.TIMES.append(time() - self.START_TIME)
		self.DOSES.append(self.dose())
		self.CPMS.append(self.cpm())

	#returns the average CPM for the whole time period
	def av_cpm(self):
		mfloat = (time() - self.START_TIME)/60
		if mfloat == 0:
			return 0
		else:
			return int(float(self.CNT)/mfloat)
	
	#returns the average CPH for the whole time period
	def av_cph(self):
		hfloat = (time() - self.START_TIME)/3600
		if hfloat == 0:
			return 0
		else:
			return int(float(self.CNT)/hfloat)
	
	#returns the average absorbed dose in uGy
	def av_dose(self):
		mR = (float(self.av_cpm())/60)/self.CPStomR
		return mR*self.mRtouGy
	
	#returns the average dose calculated from the cph in mR	
	def av_doseh(self):
		mR = (float(self.av_cph())/3600)/self.CPStomR
		return mR*self.mRtouGy

	#returns the estimated cpm for times less than a minute and
	#the cpm above one minute	
	def cpm(self):
		last_minute = time() - 60
		if last_minute < self.START_TIME:
			return self.av_cpm()
		else:
			t = list(self.TIMES)
			i = len(t)
			cnt = 0
			while i > 0 and t[i-1] > last_minute - self.START_TIME:
				i -= 1
				cnt += 1
			return cnt
			
	#returns the estimated cph for times less than an hour and
	#the cph above one hour
	def cph(self):
		last_hour = time() - 3600
		if last_hour < self.START_TIME:
			return self.av_cph()
		else:
			t = list(self.TIMES)
			i = len(t)
			cnt = 0
			while i > 0 and t[i-1] > last_hour - self.START_TIME:
				i -= 1
				cnt += 1
			return cnt
			
	#returns the actual dose in uGy
	def dose(self):
		mR = (float(self.cpm())/60)/self.CPStomR
		return mR*self.mRtouGy
	
	#returns the actual calculated from the CPH dose in uGy
	def doseh(self):
		mR = (float(self.cph())/3600)/self.CPStomR
		return mR*self.mRtouGy
		
	# Calculates the statistics on GM hit times and writes it to a csv file.
	def exponential(self):
		self.expfilename = 'GPIO%d-exp-%s.csv' % (self.PIN, strftime("%d-%b-%Y-%H-%M-%S", gmtime()))
		
		# calculationg time differences
		i = 0
		t = []
		while i < len(self.TIMES)-2:
			t.append(self.TIMES[i+1] - self.TIMES[i])
			i += 1
		t.sort()
		
		# Calculating optimal time interval lengths
		length = len(t)
		if length > 0:
			num_boxes = int(log(length, 2))
		else:
			num_boxes = 1

		if num_boxes < 1:
			time_interval = float(t[length-1])/1
		elif length > 0:
			time_interval = float(t[length-1])/num_boxes
		else:
			time_interval = 1
		
		with open(self.expfilename, 'wb') as csvfile:
			expwriter = csv.writer(csvfile, delimiter=',')
			expwriter.writerow(['Time interval end (s)', 'Number of hits in time interval'])
			interval = time_interval
			cnt = 0
			for tm in t:
				#since t is sorted there's no need to check for the low boundary
				if tm <= interval:
					cnt += 1
				else:
					expwriter.writerow([interval, cnt])
					interval += time_interval
					cnt = 1
		del t
		gc.collect()
		
	def csv_write(self):
		self.filename = 'GPIO%d-%s.csv' % (self.PIN, strftime("%d-%b-%Y-%H-%M-%S", gmtime()))
		with open(self.filename, 'wb') as csvfile:
			 gmwriter = csv.writer(csvfile, delimiter=',')
			 gmwriter.writerow(['Average cpm:', self.av_cpm(), 'Average dose:', self.av_dose()])
			 gmwriter.writerow(['Count', self.CNT])
			 gmwriter.writerow(['Times (s)', 'Actual doses (uGy/h)', 'Actual CPMs'])
			 i = 0
			 while i < len(self.TIMES):
				 gmwriter.writerow([self.TIMES[i], self.DOSES[i], self.CPMS[i]])
				 i += 1
