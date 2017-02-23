import os, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib  
from matplotlib.font_manager import  FontProperties 
#%matplotlib inline
myfont = FontProperties(fname='/home/pyy/tool/msyh.ttf') 
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus']=False

usedColumns =['_ALTITUDE', '_GLIDE', '_LOC', 
              '_SSTICK_CAPT', '_SSTICK_CAPT-1', '_SSTICK_CAPT-2', '_SSTICK_CAPT-3',
              '_PITCH_CAPT_SSTICK', '_PITCH_CAPT_SSTICK-1', '_PITCH_CAPT_SSTICK-2', '_PITCH_CAPT_SSTICK-3', 
              '_ROLL_CAPT_SSTICK', '_ROLL_CAPT_SSTICK-1', '_ROLL_CAPT_SSTICK-2', '_ROLL_CAPT_SSTICK-3',
              '_SSTICK_FO', '_SSTICK_FO-1', '_SSTICK_FO-2', '_SSTICK_FO-3',
              '_PITCH_FO_SSTICK', '_PITCH_FO_SSTICK-1', '_PITCH_FO_SSTICK-2', '_PITCH_FO_SSTICK-3', 
              '_ROLL_FO_SSTICK', '_ROLL_FO_SSTICK-1', '_ROLL_FO_SSTICK-2', '_ROLL_FO_SSTICK-3']

sstickCaptColumns = usedColumns[3:7]
pitchCaptColumns = usedColumns[7:11]
rollCaptColumns = usedColumns[11:15]
sstickFoColumns = usedColumns[15:19]
pitchFoColumns = usedColumns[19:23]
rollFoColumns = usedColumns[23:]

wd = '/home/pyy/data/cast/A320_300_20/'
table_dir = '/home/pyy/data/cast/StableApproach.csv'
files = os.listdir(wd)