'''
Accumulated diagnosis of COVID-19 in the United States
Update 2020-05-18
'''

import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from datetime import timedelta as delta
from datetime import datetime as dt

from utils import sigmoid
from data import new_diagnosis as new_diagnosis_origin
from make_gif import create_gif


# default start time 2020 01 23

day0 = dt(2020,1,23)
start = dt(2020,3,23)
today = dt.now()
duration = (today-day0).days

print('Plotting data...')

img_path = './plots'
if len(os.listdir(img_path)) > 0:
    for file in os.listdir(img_path):
        os.remove(os.path.join(img_path,file))
os.makedirs(img_path, exist_ok=True)

count = 0
#fig, ax = plt.subplots(1, 4, figsize=(15,5))
for dur in range((start-day0).days,duration):
    new_diagnosis = new_diagnosis_origin[:dur]

    diagnosis = []
    for i in range(len(new_diagnosis)):
        if i == 0:
            diagnosis.append(new_diagnosis[0])
        else:
            diagnosis.append(sum(new_diagnosis[:i]))

    new_diagnosis = np.array(new_diagnosis)
    diagnosis = np.array(diagnosis)

    fig, ax = plt.subplots(1, 4, figsize=(15,5))

    plot1 = ax[0].plot(new_diagnosis, color='r', label='New diagnosis')
    ax[0].legend(loc='upper left')
    ax[0].set_xlabel('day')
    ax[0].set_ylabel('Newly diagnosed people')

    plot2 = ax[1].plot(diagnosis, color='b', label='Cumulative diagnosis')
    ax[1].legend(loc='upper left')
    ax[1].set_xlabel('day')
    ax[1].set_ylabel('All diagnosed people')

    try:
        x = np.array([ _ for _ in range(len(diagnosis))])
        popt, pcov = curve_fit(sigmoid, x, diagnosis)
        y = sigmoid(x, popt[0], popt[1], popt[2])

        plot3 = ax[2].plot(diagnosis, color='r', label='Raw data')
        plot4 = ax[2].plot(y, color='b', label='Fitted data')
        ax[2].legend(loc='upper left')
        ax[2].set_xlabel('day')
        ax[2].set_ylabel('All diagnosed people')

        x = np.array([ _ for _ in range(2*len(diagnosis))])
        y = sigmoid(x, popt[0], popt[1], popt[2])
        plot5 = ax[3].plot(x, y, color='b', label='Prediction')
        plot6 = ax[3].plot(diagnosis, color='r', label='Raw data')
        ax[3].legend(loc='upper left')
        ax[3].set_xlabel('day')
        ax[3].set_ylabel('Will be diagnosed people')
        k = int(popt[0])
        t = int(popt[1])
        r = int(popt[2])

        plt.text(t, 0, r"$y=\frac{k}{1+e^{-\frac{x-t}{r}}}$", fontsize=18)

        plt.subplots_adjust(left=0.08, right=0.95, wspace=0.45)
        
        y = (day0+delta(days=dur) + (delta(days=2*t)-delta(days=dur))).year
        m = (day0+delta(days=dur) + (delta(days=2*t)-delta(days=dur))).month
        d = (day0+delta(days=dur) + (delta(days=2*t)-delta(days=dur))).day

        now_data = diagnosis[-1:][0]
        all_data = k
        after_days = (dt(y,m,d)-(day0+delta(days=dur))).days
        
        ax[0].set_title('COVID-19 in the U.S.A.')
        ax[1].set_title('Now: %9d people\nAll: %9d people' % (now_data, all_data))
        ax[2].set_title('Epidemic may end after %3d days on %4d %2d %2d.\n' % (after_days, y, m, d))
        ax[3].set_title('parameters: k=%9d, t=%3d, r=%3d' % (k, t, r))
        
        figname = str((day0+delta(days=dur)).year) + '-' + str((day0+delta(days=dur)).month) + '-' + str((day0+delta(days=dur)).day)
        cnt = '%003d' % count
        plt.savefig(os.path.join(img_path, cnt+'-'+figname+'.png'), dpi=fig.dpi)
        plt.close()
        count += 1
        if count % 10 == 0 or count == duration-(start-day0).days:
            print('|PROCESSING|{:6.2f}%'.format(100*count/(duration-(start-day0).days)))
    except: # (ValueError, TypeError, RuntimeError):
        print('Error occured, please check.')
        break


image_list = []
print('Building...')

dirs = os.listdir(img_path)
for img in dirs:
    if img[-4:] == '.png':
        image_list.append(os.path.join(img_path,img))

image_list.sort()

gif_name = 'plots' + '.gif'

gif_duration = 0.1

create_gif(image_list, gif_name, gif_duration)
print('GIF completed.')
