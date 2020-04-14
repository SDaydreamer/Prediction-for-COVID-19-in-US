'''
Accumulated diagnosis of COVID-19 in the United States
Update 2020-04-13
'''

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from functions import Days, After, sigmoid
from data import new_diagnosis

date = Days()

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
ax[0].set_title('COVID-19')

plot2 = ax[1].plot(diagnosis, color='b', label='Cumulative diagnosis')
ax[1].legend(loc='upper left')
ax[1].set_xlabel('day')
ax[1].set_ylabel('All diagnosed people')
ax[1].set_title('in')

x = np.array([ _ for _ in range(len(diagnosis))])
popt, pcov = curve_fit(sigmoid, x, diagnosis)
y = sigmoid(x, popt[0], popt[1], popt[2])

plot3 = ax[2].plot(diagnosis, color='r', label='Raw data')
plot4 = ax[2].plot(y, color='b', label='Fitted data')
ax[2].legend(loc='upper left')
ax[2].set_xlabel('day')
ax[2].set_ylabel('All diagnosed people')
ax[2].set_title('the United States')

x = np.array([ _ for _ in range(2*len(diagnosis))])
y = sigmoid(x, popt[0], popt[1], popt[2])
plot5 = ax[3].plot(x, y, color='b', label='Prediction')
plot6 = ax[3].plot(diagnosis, color='r', label='Raw data')
ax[3].legend(loc='upper left')
ax[3].set_xlabel('day')
ax[3].set_ylabel('Will be diagnosed people')
k = int(popt[0])
t = int(popt[1])
m = int(popt[2])
ax[3].set_title('parameters: k='+str(k)+', t='+str(t)+', m='+str(m))

plt.text(t, 0, r"$y=\frac{k}{1+e^{-\frac{x-t}{m}}}$", fontsize=18)

plt.subplots_adjust(left=0.08, right=0.95, wspace=0.45)

y, m, d = After(2*t-len(date))
print(f'Now: {diagnosis[-1:][0]} people\nAll: {k} people')
print(f'Epidemic may end after {2*t-len(date)} days on {y} {m} {d}.')
plt.show()
