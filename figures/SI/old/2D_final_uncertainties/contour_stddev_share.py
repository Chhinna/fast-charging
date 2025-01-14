#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 07:29:14 2018

@author: peter

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib
import glob
import pickle

plt.close('all')

CROPPED_BOUNDS = False

##############################################################################
# PARAMETERS TO CREATE POLICY SPACE
min_policy_bound, max_policy_bound = 3.6, 8
C3list = [3.6, 4.0, 4.4, 4.8, 5.2, 5.6]

C4_LIMITS = [0.1, 4.81] # Lower and upper limits specifying valid C4s
##############################################################################

one_step = 4.8
margin = 0.2 # plotting margin

FS = 14
LW = 3

rcParams['pdf.fonttype'] = 42
rcParams['ps.fonttype'] = 42
rcParams['font.size'] = FS
rcParams['axes.labelsize'] = FS
rcParams['xtick.labelsize'] = FS
rcParams['ytick.labelsize'] = FS
rcParams['font.sans-serif'] = ['Arial']

colormap = 'plasma_r'

# IMPORT RESULTS
# Get folder path containing text files
file = '4_bounds.pkl'
data = []
min_bounds = 10000
max_bounds = -1
with open(file, 'rb') as infile:
    param_space, ub, lb, mean = pickle.load(infile)
    bounds = (mean - lb)/(5*0.5**5) # divide by beta
    data.append(mean)
    min_bounds = min(np.min(bounds),min_bounds)
    max_bounds = max(np.max(bounds),max_bounds)

# Find number of batches
batchnum = len(data)

## INITIALIZE CONTOUR PLOT
# SETTINGS
fig, ax = plt.subplots(2,3,figsize=(16,8),sharex=True,sharey=True)
#plt.style.use('classic')
plt.set_cmap(colormap)
minn, maxx = min_bounds, max_bounds

# Calculate C4(CC1, CC2) values for contour lines
C1_grid = np.arange(min_policy_bound-margin,max_policy_bound + margin,0.01)
C2_grid = np.arange(min_policy_bound-margin,max_policy_bound + margin,0.01)
[X,Y] = np.meshgrid(C1_grid,C2_grid)

fig.subplots_adjust(right=0.8)
fig.subplots_adjust(top=0.93)

k2 = 0

# FUNCTION FOR LOOPING THROUGH BATCHES
for k, c3 in enumerate(C3list):
    temp_ax = ax[int(k/3)][k%3]
    plt.axis('square')

    ## PLOT CONTOURS
    C4 = 0.2/(1/6 - (0.2/X + 0.2/Y + 0.2/c3))
    C4[np.where(C4<C4_LIMITS[0])]  = float('NaN')
    C4[np.where(C4>C4_LIMITS[1])] = float('NaN')

    levels = np.arange(2.5,4.8,0.25)
    C = temp_ax.contour(X,Y,C4,levels,zorder=1,colors='k')
    plt.clabel(C,fmt='%1.1f')

    ## PLOT POLICIES
    idx_subset = np.where(param_space[:,2]==c3)
    policy_subset = param_space[idx_subset]
    bounds_subset = bounds[idx_subset]
    temp_ax.scatter(policy_subset[:,0],policy_subset[:,1],vmin=minn,vmax=maxx,
                c=bounds_subset.ravel(),zorder=2,s=100)

    ## BASELINE
    #if c3 == one_step:
    #    plt.scatter(one_step,one_step,c='k',marker='s',zorder=3,s=100)
    temp_ax.set_title(chr(k+97),loc='left', weight='bold',fontsize=FS)
    temp_ax.annotate(f'CC3={str(c3)}\n{str(len(policy_subset))} policies',\
              (3.52, 3.52), fontsize=FS)
    if int(k/3)==1:
        temp_ax.set_xlabel('CC1',fontsize=FS)
    if k%3 == 0:
        temp_ax.set_ylabel('CC2',fontsize=FS)
    temp_ax.set_xlim((min_policy_bound-margin, max_policy_bound+margin))
    temp_ax.set_ylim((min_policy_bound-margin, max_policy_bound+margin))

# ADD COLORBAR
cbar_ax = fig.add_axes([0.85, 0.15, 0.04, 0.72]) # [left, bottom, width, height]
norm = matplotlib.colors.Normalize(minn, maxx)
m = plt.cm.ScalarMappable(norm=norm, cmap=colormap)
m.set_array([])
cbar = fig.colorbar(m, cax=cbar_ax)
cbar.ax.tick_params(labelsize=FS,length=0)
cbar.ax.set_title('Std. dev. of\ncycle life\nafter round 4,\n$\mathit{σ_{4,i}}$',fontsize=FS)

## SAVE
plt.savefig('final_stdev_sharexy.png', bbox_inches = 'tight')
plt.savefig('final_stdev_sharexy.pdf', bbox_inches = 'tight',format='pdf')