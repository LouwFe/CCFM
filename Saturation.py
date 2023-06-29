# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 15:21:49 2020

@author: grundch

The program requires to be at the surface of sample
"""

import numpy as np
from matplotlib import pyplot as plt
import asc500_base as asc
import Laser_DLL as iBeam
import time
import pandas as pd
import os
import AMC


date = time.strftime("%Y-%m-%d", time.gmtime())
SAVE_PATH = os.path.join('Data_Saturation', date)
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)
time_now = time.strftime("%H-%M-%S", time.localtime())
SAVE_PATH = os.path.join(SAVE_PATH, time_now)
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

#%% Config Plot
SAVE_FIGURE = True
SAVE_FORMAT = 'png'
FSIZE = (11. / 2.54, 9. / 2.54)

#%% Config Scan Parameters
Pos_x = 15 #in um
Pos_y = 15 #in um

#z_pos = [0,10, 20, 30,40,50]
#z_pos = [0, 5 ,8, 11, 14, 17, 20] #in um
#z_pos = [18,20,22, 28, 30, 32] #in um
z_pos = [30]
#area = (str(Area_x) + 'x' + str(Area_y))

#%% Config ASC
expTime = 1e-3
sampTime = 1e-3
average = 0
chnNo = 0
bufSize = 163

binPath = "Installer\\ASC500CL-V2.7.6\\"
dllPath = "64bit_lib\\ASC500CL-LIB-WIN64-V2.7.6\\daisybase\\lib\\"
asc500 = asc.ASC500Base(binPath, dllPath)
asc500.startServer()
#asc500.sendProfile('Installer\\ASC500CL-V2.7.6\\afm.ngp')
asc500.setDataEnable(1)
asc500.configureChannel(chnNo,
                        asc500.getConst('CHANCONN_PERMANENT'),
                        asc500.getConst('CHANADC_COUNTER'),
                        average,
                        sampTime)
print(asc500.getChannelConfig(chnNo))
asc500.configureDataBuffering(chnNo, bufSize)
asc500.setCounterExposureTime(expTime)
print("Exposure time ", asc500.getCounterExposureTime())

#%% Config Laser
laser_pow = np.arange(0, 70, .5)#in mW, TODO: is float needs to be converted into str

laser = iBeam.iBeam()
laser.connect('COM4')
laser.setLaserPowerIn_mW('1', '0')
laser.setLaserPowerIn_mW('2', '0')

#Turn Laser ON
laser.setLaserON()
time.sleep(1)
#time.sleep(75)


#%% Define Measuring Routine
def do_meas(chnNo, bufSize):
    all_counts_init = []
    means_init = []
    time_init = []
    #print('Starting init measurement')
    while True:
        # Wait until buffer is full
        if asc500.waitForFullBuffer(chnNo) != 0:
            break
    out = asc500.getDataBuffer(chnNo, 0, bufSize)
    counts= np.asarray(out[3][:])
    sum_counts = sum(counts)
    #print('Duration: ' + str(time_end) + ' s')
    return sum_counts, counts

#%%initialize the size of the heatmap (and other stuff)
all_counts = []
counts = []
#%% Start saturation loop
timer_all = round(time.perf_counter(),2)
for val in laser_pow:
    dump = do_meas(chnNo,bufSize)[0]
    laser.setLaserPowerIn_mW('2', str(round(val,1)))
    time.sleep(0.5)
    counts.append(do_meas(chnNo,bufSize)[0]/bufSize * 1000)
    print('laser power: ' + str(round(val,1)))

print('Duration of measurement: ' + str(round(time.perf_counter(),2) - timer_all))

np.save(os.path.join(SAVE_PATH,
                     ('Saturation_' + str(round(laser_pow[0])) + ' to ' + str(round(laser_pow[-1])) + ' mW_counts')),
        counts)

laser.setLaserPowerIn_mW('2', '2.5')

#%% Print heatmap for every z-layer
fig = plt.figure(1)
plt.plot(laser_pow, counts)
plt.xlabel('Laser Power [mW]')
plt.ylabel('counts')

fig.savefig(os.path.join(SAVE_PATH,
                          ('Saturation_' + str(round(laser_pow[0])) + ' to ' + str(round(laser_pow[-1])) + ' mW_counts'
                           + '.' + SAVE_FORMAT)),
            format = SAVE_FORMAT, dpi=1200, bbox_inches='tight')


#%% Close devices
asc500.setCounterExposureTime(163e-3)
asc500.stopServer()
laser.disconnect()
