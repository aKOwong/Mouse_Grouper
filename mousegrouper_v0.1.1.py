#### A python program to group mice based on various bodily properties.
#### By Andrew K.O. Wong
#### v 0.1

#### Program design:
# The goal of this program is to group the mice in such a way so that
# the groups are statistically the same.
# The easiest to come at this is probably just by binning mice randomly
# and then ttesting the groups. This should be repeated n times, or until
# a threshold p value is reached, or n iterations is reached. The option
# to continue searching for even lower p should be included if time of
# this program is short.

# I will probably need:
# - A way to do ttest (does scipy do stats?)
# - A suitable container to ttests (probably dependent on stat method)
# - A way to save mouse groupings that are good.




# Preliminaries

import numpy as np
from scipy import stats
import random
import pandas # need v 0.12.0 or higher
import timeit
import time

datafile = 'datafilename.csv'
bodyweightfile = './mousedatabw.csv'
glcfile = './mousedataglc.csv'

# read in files
bw_df = pandas.read_csv(bodyweightfile, index_col = 0)
glc_df = pandas.read_csv(glcfile, index_col = 0)
mouse_IDs = bw_df.columns.values

# parameters
n_of_mice = len(mouse_IDs)
group_size = 5 
n_groups = n_of_mice/group_size #TODO add function to check if no remainder
#n_of_ttest = (n_groups**2 - n_groups)/2 # number of ttest given n_groups (arithmetic series)
# One-way ANOVA code, gives F-value, then p value
#stats.f_oneway(bw_df.iloc[0,0:2], bw_df.iloc[0,2:4])

# use bw_df.iloc[1:4,3:4] for example to call by integer positon in pandas
def iterator(df, n_iter): #TODO currently not getting right pvals
    p_val_box_top = np.array([0] * 5) # init p_val container, TODO flex number of observations
    stat_counter = 0 # counter for n_iter
    mouse_numbers = range(0,n_of_mice) # seq of ints to stand in as columns numbers
    mouse_nums_slice_ind = group_slicer(n_of_mice, n_groups, group_size, mouse_numbers)
    while stat_counter < n_iter:
        # runs up stat_counter. Randomizes mouse_numbers, and runs grouptest()
        # if p vals from group test higher then currently top p vals,
        # top p vals get replaced, and a mouse numbering is assigned a fresh list
        # if not, just runs up stat counter
        randomizer(mouse_numbers)
        mouse_nums_scrambled = []
        for x in mouse_nums_slice_ind:
            mouse_nums_scrambled.append(np.array(mouse_numbers)[x])
        current_p_val_box = grouptest(df, 5, *mouse_nums_scrambled)
        if (p_val_box_top < current_p_val_box).all():
            p_val_box_top = current_p_val_box # doing this is okay cuz current box gets reassigned above
            stat_counter += 1
            top_mouse_numbers = mouse_numbers[:]
            #print(stat_counter)
            #print(p_val_box_top)
            #print(mouse_numbers, "current")
            #print(top_mouse_numbers, "top")
        else:
            stat_counter += 1
            #print(stat_counter)
            #print(p_val_box_top)
            #print(mouse_numbers, "current")
            #print(top_mouse_numbers, "top")
    print("\n\n")
    print(top_mouse_numbers, "top")
    print(p_val_box_top)
    return((p_val_box_top,top_mouse_numbers))

# need something to do integer sequence for mouse IDs
def randomizer(mouse_ilocs):
    random.shuffle(mouse_ilocs)
    #return([mouse_ilocs[0:2],mouse_ilocs[2:4]])

# function to perform ANOVA with dataframes
def grouptest(df, n_days_observe, *groups): # will probably need to iterate across...
    #x = 0 # counter for group 1 to be tested
    inner_p_val_box = [0] * 5 # init the p_val container
    for i in xrange(0, n_days_observe):
        stat_test_groups = []
        for x in groups:
            stat_test_groups.append(df.iloc[i,x])
        inner_p_val_box[i] = stats.f_oneway(*stat_test_groups)[1]
    return(np.array(inner_p_val_box))

# defining numbers to slice groups from, giving n_groups, group_size, and n_of_mice
# returns list of lists of individual indices
def group_slicer(n_of_mice, n_groups, group_size, object_to_be_sliced):
    slicer_box = []
    for i in xrange(0,n_groups):
        slicer_box.append(object_to_be_sliced[slice(group_size*i,group_size*i+group_size)])
    return(slicer_box)

# p val confirmation
stats.f_oneway(bw_df.iloc[4,[17,9,6,7,13]], bw_df.iloc[4,[10,4,0,18,2]], bw_df.iloc[4,[8,15,12,3,11]], bw_df.iloc[4,[5,1,19,14,16]])[1]

# t.test function
#stats.ttest_ind()
# need numpy 0.11 or higher for Welch's test

# randomizer function
# I could shuffle the whole array. But the smarter way is to shuffle indices!!(for unison shuffle anyways)
# don't know which way is faster though 

#random.shuffle(mouse_IDs) # will shuffle mouse_IDs in place


# primary loops, while iteration < n and threshold not reached
# insert results into an object of some sort, probably can keep all of it if n is not too large


# check stats with timer thing
def ttest_loop(n):
    xcount = 0
        while xcount < n:
        stats.ttest_ind(bw_df.iloc[0,0:2], bw_df.iloc[0,2:4])
        xcount = xcount + 1

tstart = time.time()
ttest_loop(1000000)
tend = time.time()
print("Time Elapsed tas %g second" % (tend - tstart))

tstart = time.time()
iterator(bw_df,10000000)
tend = time.time()
print("Time Elapsed tas %g second" % (tend - tstart))

tstart = time.time()
iterator(glc_df, 10000000)
tend = time.time()
print("Time Elapsed tas %g second" % (tend - tstart))
