# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 15:21:49 2020

@author: grundch

The program requires to be at the surface of sample.
"""

import time
import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from ASClib import ASC500

sys.path.append('AMClib')
from AMClib import AMC

#%% Create directories for saving data

date = time.strftime('%Y-%m-%d', time.gmtime())
SAVE_PATH = os.path.join('Data_Step_SCAN', date)
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

time_now = time.strftime('%H-%M-%S', time.localtime())
SAVE_PATH = os.path.join(SAVE_PATH, time_now)
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

#%% Config Plot
SAVE_FIGURE = True
SAVE_FORMAT = 'png'
FSIZE = (11. / 2.54, 9. / 2.54)

#%% Config Scan Parameters
Area_x = 5 # in um
Area_y = 5 # in um
resolution = 0.1 # in um
z_pos = [14, 17, 20, 23, 26, 29, 32, 35, 38]
z_pos = [0]
area = (str(Area_x) + 'x' + str(Area_y))

#%% Config ASC
expTime = 1e-3
sampTime = 1e-3
average = 0
chnNo = 0
bufSize = 160

binPath = 'Installer\\ASC500CL-V2.7.13\\'
dllPath = '64bit_lib\\ASC500CL-LIB-WIN64-V2.7.13\\daisybase\\lib\\'
asc500 = ASC500(binPath, dllPath)
asc500.base.startServer()
#asc500.base.sendProfile('Installer\\ASC500CL-V2.7.13\\afm.ngp')
asc500.data.setDataEnable(1)
asc500.data.configureChannel(chnNo,
                             asc500.base.getConst('CHANCONN_PERMANENT'),
                             asc500.base.getConst('CHANADC_COUNTER'),
                             average,
                             sampTime)

asc500.data.configureDataBuffering(chnNo, bufSize)
asc500.data.setCounterExposureTime(expTime)

print(asc500.data.getChannelConfig(chnNo))
print('Exposure time ', asc500.data.getCounterExposureTime())

#%% Config Laser
laser_pow = '4.5'

# laser = iBeam.iBeam()
# laser.connect('COM3')
# laser.setLaserPowerIn_mW('1', '0')
# laser.setLaserPowerIn_mW('2', laser_pow)


#Turn Laser ON
# laser.setLaserON()
time.sleep(1)
#time.sleep(75)

#%% Config Posi
#TODO: move x to zero
posi = AMC.Device('192.168.1.1')
posi.connect()
posi_axis = [0, 1, 2]
for axis in posi_axis:
    posi.control.setControlOutput(posi_axis, True)
    posi.move.setControlEotOutputDeactive(posi_axis, True)
    #posi.setReset(axis)

axis_x = 0
axis_y = 1
axis_z = 2

#%% Define Measuring Routine
def do_meas(chnNo, bufSize):
    means_init = []
    time_init = []
    #print('Starting init measurement')
    time_start = round(time.perf_counter(), 2)
    while True:
        # Wait until buffer is full
        if asc500.data.waitForFullBuffer(chnNo) != 0:
            break
    time_init.append(round(time.perf_counter(), 2) - time_start)
    out = asc500.data.getDataBuffer(chnNo, 0, bufSize)
    counts = np.asarray(out[3][:])
    means_init.append(np.mean(counts))
    sum_counts = sum(counts)
    time_end = round(time.perf_counter(), 2) - time_start
    #print('Duration: ' + str(time_end) + ' s')
    return sum_counts, time_init, counts

def percentageCalculator(value, maxVal):
    return round((value * 100 / maxVal), 2)

#%% Calculate x and y arrays for scanning loop
x_pos = np.arange(0, Area_x, resolution)
y_pos = np.arange(0, Area_y, resolution)

#%% Initialize the size of the heatmap (and other stuff)
heatmap = np.ones((len(y_pos), len(x_pos), len(z_pos)))
all_counts = []

#%% Start scanning loop
timer_all = round(time.perf_counter(), 2)
lineTimes = []
pixelTimes = []
totalPixels = 0

for i, z in enumerate(z_pos):
    posi.move.setControlTargetPosition(axis_z, z * 1e3)
    posi.control.setControlMove(axis_z, True)
    while posi.status.getStatusMoving(axis_z)[1] == 1: pass
    posi.control.setControlMove(axis_z, False)
    for k, y in enumerate(y_pos):
        lineTimer = time.perf_counter()
        posi.move.setControlTargetPosition(axis_y, y * 1e3)
        posi.control.setControlMove(axis_y, True)
        while posi.status.getStatusMoving(axis_y)[1] == 1: pass
        posi.control.setControlMove(axis_y, False)
        if k%2 == 0:
            x_pos_shuf = x_pos
        else:
            x_pos_shuf = x_pos[::-1]

        for l, x in enumerate(x_pos_shuf):
            pixelTimer = time.perf_counter()

            posi.move.setControlTargetPosition(axis_x, x * 1e3)
            posi.control.setControlMove(axis_x, True)
            while posi.status.getStatusMoving(axis_x)[1] == 1:
                pass
            posi.control.setControlMove(axis_x, False)
            time.sleep(0.07)
            # Take a measure twice and dump it...
            do_meas(chnNo, bufSize)
            do_meas(chnNo, bufSize)
            # Then take a final measurement
            sum_counts, times, counts = do_meas(chnNo, bufSize)
            all_counts.append(counts)
            if k%2 != 0:
                l = len(x_pos_shuf) - 1 - l
            sum_counts = sum_counts / bufSize * 1000 # kilo counts per seconds
            heatmap[k,l,i] = sum_counts

            totalPixels += 1
            pixelTimes.append(time.perf_counter() - pixelTimer)
            if len(lineTimes) > 0:
                timeRemaining = np.mean([(len(y_pos) * len(x_pos) * len(z_pos) - totalPixels) * np.mean(pixelTimes),
                                         (len(y_pos) - k) * np.mean(lineTimes)])
            else:
                timeRemaining = (len(y_pos) * len(x_pos) * len(z_pos) - totalPixels) * np.mean(pixelTimes)
            m, s = divmod(timeRemaining, 60)
            h, m = divmod(m, 60)
            print('\rScan progress: {}%\tEstimated time remaining: {}:{}:{}    '.format(
                percentageCalculator(totalPixels,
                                     len(y_pos) * len(x_pos) * len(z_pos)),
                                     int(h),
                                     int(m),
                                     int(s)),
                                     end='', flush=True)

        print(str(k + 1) + ' of ' + str(len(y_pos)) + ' rows scanned in '+
              str(i + 1) + ' of ' + str(len(z_pos)) + ' planes')
        lineTimes.append(time.perf_counter() - lineTimer)
        #print('Counts: ' + str(means))
    # for axis in posi_axis:
    #     posi.move.setControlTargetPosition(axis, 0 * 1e3)
    #     posi.control.setControlMove(axis, True)
    #     while posi.status.getStatusMoving(axis)[1] == 1: pass
    #     posi.control.setControlMove(axis, False)#
duration = round((time.perf_counter() - timer_all), 2)
print('Duration of scan: ' + str(duration))

np.save(os.path.join(SAVE_PATH,
                     ('SCAN_' + str(Area_x) + ' x ' + str(Area_y) + '_heatmap')),
        heatmap)

#%% Print heatmap for every z-layer
for i, z in enumerate(z_pos):
    param_dict = ('AoS: ' + area + r' $\mu$m / '+
                   'Res: ' + str(resolution*1e3) + ' nm / ' +
                  'Depth:. ' + str(z) + '\u03BCm / ' +
                  'Exp-Time: ' + str(expTime*1e3) + ' ms')
    fig = plt.figure(1)
    pos = plt.imshow(heatmap[:,:,i], cmap = 'hot', interpolation='none')
    plt.title(str(Area_x) + ' x ' + str(Area_y) + ' \u03BC' +'m Scan')
    fig.colorbar(pos)
    yticks, xlabels = plt.yticks()
    xticks, ylabels = plt.xticks()
    ylabels = yticks*resolution
    xlabels = xticks*resolution
    plt.yticks(yticks[1:-1], ylabels[1:-1])
    plt.xticks(xticks[1:-1], xlabels[1:-1])
    plt.text(0,yticks[-1]+((yticks[-1]-yticks[-2])), param_dict, fontsize=7,
             bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 1})

    plt.show()
    fig.savefig(os.path.join(SAVE_PATH,
                             ('SCAN_' + str(Area_x) + ' x ' + str(Area_y) +
                              '_depth ' + str(z) + '.' + SAVE_FORMAT)),
                format = SAVE_FORMAT, dpi=1200, bbox_inches='tight')


meta_file = open(os.path.join(SAVE_PATH, ('meta_data' + str(z) + '.txt')), "w")
meta_file.write('ASC-Settings:' + '\n' +
                '\t Exposure Time: ' + str(expTime) + '\n' +
                '\t Sampling Time: ' + str(sampTime) + '\n' +
                '\t Buffer size: ' + str(bufSize) + '\n' +
                '\n' +
                'Scanning Settings' + '\n' +
                '\t Area: ' + str(Area_x) + ' x ' + str(Area_y) + '\n' +
                '\t Depth(s): ' + str(z_pos) + '\n'+
                'General:' + '\n' +
                '\t Measurement Duration: ' + str(duration) + ' s\n'
                )
meta_file.close()

#%% Close devices

posi.close()

asc500.data.setCounterExposureTime(163e-3)

asc500.base.stopServer()
# laser.setLaserOFF()
# laser.disconnect()
