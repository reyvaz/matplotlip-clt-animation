#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Animation of the Central Limit Theorem and the Law of Large Numbers

Creates an animated plot depicting the CLT and the LNN using matplotlib
Note: Saving requires a movie writter. i.e. FFmpeg

Author: Reynaldo Vazquez 
Created: Oct 18, 2017
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

sub_size = 100 # size of the subsamples for CLT demo
def get_subsamples_means(big_sample, sub_size = sub_size):
    """
    Calculates the subsample means of a larger random variable sample 
    """
    n = len(big_sample)
    subsamples_means = []   
    for i in range(int(n/sub_size)):
        start_ind = i*sub_size
        end_ind   = start_ind + sub_size - 1
        subsamples_means.append(np.mean(big_sample[start_ind:end_ind]))
    return np.array(subsamples_means)

np.random.seed(400)
n = 1000000 # size of main (the larger) sample
x1 = np.random.normal(0, 1, n)
x2 = np.random.exponential(1, n)
x3 = np.random.uniform(0,1, n)
rand_samples = [x1,x2,x3]
subsample_means = [get_subsamples_means(d) for d in rand_samples]
distr = rand_samples + subsample_means

colors = ['red', 'blue', 'green']*2
distr_type = ['Normal', 'Exponential', 'Uniform', 'Means of Normal Subsamples', 
              'Means of Exponential Subsamples', 'Means of Uniform Subsamples']

# x axes edges required for plot consistency
x_mins = [min(distr[i]) for i in range(len(distr))]
x_maxs = [max(distr[i]) for i in range(len(distr))]
num_bins = 65

def fill_fig(i, sample_size = None):
    """
    Plots the histograms and customizes the subplots
    """
    ax = axs[i]
    d = distr[i]
    if sample_size is None:
        sample_size = len(d)
    bins = all_bins[i]
    num_subsamples = int(sample_size/sub_size)
    if i > 2:
        sample_size = num_subsamples
    ax.cla()
    if sample_size != 0: # avoids div by zero warning
        ax.hist(d[:sample_size], normed=True, bins=bins, 
                alpha=0.65, color=colors[i])
    ax.tick_params(direction='out', length=2, width=0.5, colors='0.35', 
                   labelsize = 9)
    ax.set_xlim(x_mins[i], bins[-1])
    ax.set_ylim(0, ylims[i])
    ax.locator_params(tight=True, nbins=5)
    subplot_title(i)
    for spine in ax.spines.values():
        spine.set_edgecolor('#969494')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

def subplot_title(i):
    """
    Adds a title to each figure 
    """
    xval = x_mins[i] + (x_maxs[i] - x_mins[i])*0.05
    yval = ylims[i]*0.92
    t = axs[i].text(xval, yval, distr_type[i], fontsize=11, color = '0.45',
       fontweight = 'normal')
    t.set_bbox(dict(facecolor='white', alpha=0.5, edgecolor='white'))

number_frames = 100 # i.e. number of iterations
expn = np.log(n)/np.log(number_frames) # gets the log_number_frames(n) so that 
                                       # update_fig iterates number_frames times
                                       # w/ sample size increasing exponentially
def update_fig(curr):
    """
    Updates animation iterating over fillfig()
    """
    sample_size = int(curr**expn)
    num_subsamples = int(sample_size/sub_size)
    if sample_size > 1000:
        sample_size = num_subsamples*sub_size
    if curr >= number_frames-1: 
        a.event_source.stop()
        sample_size = n
        num_subsamples = int(n/sub_size)
    for i in range(0,len(axs)):
        fill_fig(i, sample_size)
    fig.suptitle('\nsample number: {} \nsample size: {} \nnumber of subsamples: {}'.format(curr+1,
                 sample_size, num_subsamples), size=8, color = '0.35', 
                 fontweight = 'bold', x = 0.74, ha = 'left')

ylims = []
all_bins = []
plt.ioff() # supress plot printing in order to calculate ylims below
for i in range(0,len(distr)): 
    """
    Finds: The y-axes upper limits for consistent y-axes fitting the last plot 
    iteration. Allows some extra space on top. And,
    The x-cordinates for the bins (all_bins)
    """
    x_min = x_mins[i]
    x_max = x_maxs[i]
    bins = np.arange(x_min, x_max, (x_max-x_min)/num_bins)
    ylims.append(max(plt.hist(distr[i], normed=True, bins=bins)[0]*1.3))
    all_bins.append(bins)
plt.ion() # restart plot printing

# Initialize the figure
fig, ((ax1,ax2,ax3), (ax4,ax5,ax6)) = plt.subplots(2, 3)
axs = [ax1,ax2,ax3,ax4,ax5,ax6]
fig.set_size_inches(12, 5)

for i in range(0,len(axs)):
    """
    Starts blank plots
    """
    fill_fig(i, sample_size = 0)

a = animation.FuncAnimation(fig, update_fig, frames = number_frames, interval=2)
#a.save('media/clt_lln_animation720.mp4', fps=10, dpi=720)
