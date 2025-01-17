"""	Plot offline data.
"""

__author__ = 'Achin Jain'
__email__ = 'achinj@seas.upenn.edu'


import numpy as np
import matplotlib.pyplot as plt

from bayes_race.params import ORCA
from bayes_race.tracks import ETHZ, ETHZMobil
from bayes_race.models import Dynamic
import matplotlib

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 22}

matplotlib.rc('font', **font)

#####################################################################
# settings

SAVE_RESULTS = False

CTYPE = 'PP'
SAMPLING_TIME = 0.02
TRACK_NAME = 'ETHZ'

filepath = 'track_training'
N_SAMPLES = 500

#####################################################################
# load vehicle parameters

params = ORCA(control='pwm')
model = Dynamic(**params)

#####################################################################
# load track

track = ETHZ(reference='optimal')

#####################################################################
# load inputs used to simulate Dynamic model

data = np.load('../data/DYN-{}-{}.npz'.format(CTYPE, TRACK_NAME))
time = data['time'][:N_SAMPLES+1]

states = np.zeros([7,N_SAMPLES+1])
states[:6,:] = data['states'][:6,:N_SAMPLES+1]
states[6,1:] = data['inputs'][1,:N_SAMPLES]

inputs = data['inputs'][:,:N_SAMPLES]
inputs[1,0] = inputs[1,0]
inputs[1,1:] = np.diff(inputs[1])
inputs[1] /= SAMPLING_TIME

#####################################################################
# plots

plt.figure(figsize=(12,8))
plt.axis('equal')

plt.plot(-track.y_outer, track.x_outer, 'k', lw=2.0, alpha=0.5)
plt.plot(-track.y_inner, track.x_inner, 'k', lw=2.0, alpha=0.5)
# plt.plot(track.x_raceline, track.y_raceline, '--r', alpha=0.8, lw=1, label='raceline')
# plt.plot(states[0], states[1], 'k', lw=1, label='pure pursuit')

plt.xlabel('$x$ [m]')
plt.ylabel('$y$ [m]')
plt.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5,1.15), frameon=False)

if SAVE_RESULTS:
	plt.savefig(filepath+'.png', dpi=600, bbox_inches='tight')

plt.show()
