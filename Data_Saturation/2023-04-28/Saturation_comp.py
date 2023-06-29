# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 09:17:14 2020

@author: grundch
"""


import numpy as np
from matplotlib import pyplot as plt
import os

#%% Config

SAVE_FIGURE = True
SAVE_FORMAT = 'png'
FSIZE = (11./ 2.54, 9. / 2.54)

DIR = os.getcwd()

data_nonNV = np.load('Saturation_0 to 70 mW_counts_nonNV.npy')/(5*160)
data_NV =np.load('Saturation_0 to 70 mW_counts_NV.npy')/(5*160)

la_pow = np.arange(0, 70, .5)

fig = plt.figure(1)
plt.plot(la_pow, data_nonNV, label='BG')
plt.plot(la_pow, data_NV, label='NV')
plt.plot(la_pow, data_NV - data_nonNV, label = 'NV - BG')

plt.title('Saturation Measurement')
plt.xlabel('Laser Power [mW]')
plt.ylabel('Counts [1/ms]')
plt.legend()
plt.grid()

plt.savefig(('Saturation_compare.' + SAVE_FORMAT), format = SAVE_FORMAT, dpi=1200, bbox_inches='tight')

SNR = (data_NV-data_nonNV)/data_nonNV
SNR_dB = 10*np.log10((data_NV-data_nonNV)/data_nonNV)

fig = plt.figure(2)
plt.plot(la_pow, SNR)
plt.title('SNR')
plt.xlabel('Laser Power [mW]')
plt.ylabel('SNR')
plt.grid()

plt.savefig(('SNR.' + SAVE_FORMAT), format = SAVE_FORMAT, dpi=1200, bbox_inches='tight')

fig = plt.figure(3)
plt.plot(la_pow, SNR_dB)
plt.title('SNR')
plt.xlabel('Laser Power [mW]')
plt.ylabel('SNR')
plt.grid()
