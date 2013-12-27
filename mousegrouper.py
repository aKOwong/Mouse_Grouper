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

datafile = 'datafilename.csv'
bodyweightfile = './mousedatabw.csv'
glcfile = './mousedataglc.csv'
group_size = 4
n_of_mice = 20
n_groups = n_of_mice/group_size #TODO add function to check if no remainder

# read in files
bw_df = pandas.read_csv(bodyweightfile, index_col = 0)
glc_df = pandas.read_csv(glcfile)
mouse_IDs = bw_df.columns.values

n_of_ttest = (n_groups**2 - n_groups)/2 # number of ttest given n_groups (arithmetic series)
# function to perform t test with dataframes
def groupttest(dataframe, n_mice, n_group): # will probably need to iterate across...
    x = 0 # counter for group 1 to be tested
    while x < n_group:
# t.test function
stats.ttest_ind()
# need numpy 0.11 or higher for Welch's test

# randomizer function
# I could shuffle the whole array. But the smarter way is to shuffle indices!!(for unison shuffle anyways)
# don't know which way is faster though 

random.shuffle(mouse_IDs) # will shuffle mouse_IDs in place


# primary loops, while iteration < n and threshold not reached
# insert results into an object of some sort, probably can keep all of it if n is not too large



