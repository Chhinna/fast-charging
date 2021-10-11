#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
surface_points.py creates contour plot based on policies.csv file 
    (generated by policies.py)
    
Peter Attia
Last modified June 21, 2018
"""

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def plot_surface(C1, C2, C3, C4_LIMITS, DIR, filename):
    
    # Import policies
    policies = np.genfromtxt(os.path.join(DIR, 'policies_' + filename + '.csv'), delimiter=',')
    
    COLOR_LIM = [2.5,4.8]
    
    one_step = 4.8
    margin = 0.2 # plotting margin
    
    # editable text for exported vector graphics
    # http://jonathansoma.com/lede/data-studio/matplotlib/exporting-from-matplotlib-to-open-in-adobe-illustrator/
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    
    # Calculate C4(CC1, CC2) values for contour lines
    C1_grid = np.arange(min(C1)-margin,max(C1) + margin,0.01)
    C2_grid = np.arange(min(C1)-margin,max(C1) + margin,0.01)
    [X,Y] = np.meshgrid(C1_grid,C2_grid)
    
    ## CREATE CONTOUR PLOT
    fig = plt.figure() # x = C1, y = C2, cuts = C3, contours = C4
    plt.style.use('classic')
    plt.rcParams.update({'font.size': 16})
    plt.set_cmap('viridis')
    # manager = plt.get_current_fig_manager() # Make full screen
    # manager.window.showMaximized()
    
    
    ## MAKE PLOT
    for k, c3 in enumerate(C3):
        plt.subplot(2,3,k+1)
        plt.axis('square')
        
        C4 = 0.2/(1/6 - (0.2/X + 0.2/Y + 0.2/c3))
        C4[np.where(C4<C4_LIMITS[0])]  = float('NaN')
        C4[np.where(C4>C4_LIMITS[1])] = float('NaN')
        
        ## PLOT CONTOURS
        #levels = np.arange(COLOR_LIM[0],COLOR_LIM[1],0.25)
        C = plt.pcolor(X,Y,C4,zorder=1,vmin=COLOR_LIM[0],vmax=COLOR_LIM[1])
        #plt.clabel(C,fmt='%1.1f')
        
        ## PLOT POLICIES
        if c3 == 4.8:
            plt.scatter(one_step,one_step,c='k',marker='s',zorder=3,s=50) ## BASELINE
        
        idx_subset = np.where(policies[:,2]==c3)
        policy_subset = policies[idx_subset,:][0]
        plt.scatter(policy_subset[:,0],policy_subset[:,1],c='k',zorder=2,s=50)
        
        plt.title('CC3=' + str(c3) + ': ' + str(len(policy_subset)) + ' policies',fontsize=16)
        plt.xlabel('CC1')
        plt.ylabel('CC2')
        plt.xlim((min(C1)-margin, max(C1)+margin))
        plt.ylim((min(C1)-margin, max(C1)+margin))
    
    plt.tight_layout()
    
    # Add colorbar
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    minn, maxx = COLOR_LIM[0], COLOR_LIM[1]
    norm = matplotlib.colors.Normalize(minn, maxx)
    m = plt.cm.ScalarMappable(norm=norm, cmap='viridis')
    m.set_array([])
    cbar = plt.colorbar(m, cax=cbar_ax)
    #fig.colorbar(m, cax=cbar_ax)
    plt.clim(min(C4_LIMITS),max(C4_LIMITS))
    cbar.ax.set_title('CC4')
    
    ## SAVE FIGURE
    plt.savefig(os.path.join(DIR, 'surface_' + filename + '.png'), bbox_inches='tight')
    