#Import all the stuff I'll need
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from pandas import *
from numpy import *
from datetime import datetime
matplotlib.style.use('ggplot')
%matplotlib inline
print "Done."

jumptracker = pd.read_csv('jumptracker.csv') #Read in csv
jumptracker[:2]

'''CLEAN THE DATE CATEGORY'''

#Create a month
month_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

for index, row in jumptracker.iterrows():
    for i in range(12):
        if month_list[i] in jumptracker.loc[index,'Date']:
             jumptracker.loc[index, 'Month'] = i+1
        else:
            pass
jumptracker['Month'] = jumptracker['Month'].astype(int)

#Create a day
jumptracker['Day'] = jumptracker['Date'].apply(lambda x: x.split('-')[0])
jumptracker['Day'] = jumptracker['Day'].astype(int)

#Create a year
jumptracker['Year'] = 2017
jumptracker['Year'] = jumptracker['Year'].astype(int)

#Put it all together in DateTime
jumptracker['DateTime'] = pd.to_datetime((jumptracker.Year*10000
                                          +jumptracker.Month*100
                                          +jumptracker.Day).apply(str),format='%Y%m%d')
                                          
'''CLEAN UP VARIABLE NAMES'''
old_names = [u'Day', u'Date', u'Lift', u'Other Exercise', u'Political Activity',
       u'Exercise', u'Politics', u'Veg Cups', u'Avoid >10pm Eating', u'Month',
       u'Year', u'DateTime']
new_names = [u'Day', u'Date', u'lift_description', u'exercise_description', u'politics_description',
       u'exercise_yn', u'politics_yn', u'veg_count', u'eating_yn', u'Month',
       u'Year', u'DateTime']
jumptracker.rename(columns=dict(zip(old_names, new_names)), inplace=True)

'''LIMIT TO PREFERRED DATE RANGE'''
today_date = '2017-09-28' #####SET THIS UP#####
jumptracker_current = jumptracker[jumptracker['DateTime']<today_date]
jumptracker_current.head()

'''REPLACE Y/N WITH BINARIES 0/1'''
jumptracker_current['exercise_yn'].replace(['NO','YES'], [0,1],inplace=True)
jumptracker_current['politics_yn'].replace(['NO','YES'], [0,1],inplace=True)
jumptracker_current['exercise_yn'] = jumptracker_current.exercise_yn.astype(float)
jumptracker_current['politics_yn'] = jumptracker_current.politics_yn.astype(float)

#TOTAL EXERCISE BY DAY
ax2 = jumptracker_current.plot(y='exercise_yn',kind='bar',figsize=(16,2), color='b', legend=False)

#TOTAL POLITICS BY DAY
ax1 = jumptracker_current.plot(y='politics_yn',kind='bar',figsize=(16,2), color='r', legend=False)

#VEG COUNT OVER TIME
ax = jumptracker_current.plot(y='veg_count',kind='line',figsize=(16,2), color='g', legend=False)

# skip ticks for X axis
ax.set_xticklabels([dt.strftime('%Y-%m') for dt in jumptracker_current.DateTime])
for i, tick in enumerate(ax.xaxis.get_major_ticks()):
    if (i % (31) != 0):
        tick.set_visible(False)
        
# skip ticks for X axis
ax1.set_xticklabels([dt.strftime('%Y-%m') for dt in jumptracker_current.DateTime])
for i, tick in enumerate(ax1.xaxis.get_major_ticks()):
    if (i % (31) != 0):
        tick.set_visible(False)
        
# skip ticks for X axis
ax2.set_xticklabels([dt.strftime('%Y-%m') for dt in jumptracker_current.DateTime])
for i, tick in enumerate(ax2.xaxis.get_major_ticks()):
    if (i % (31) != 0):
        tick.set_visible(False)
        
#Deep dive into exercise activity

#Create a new exercise dataframe
exercise_frame = jumptracker_current[['DateTime','lift_description','exercise_description','exercise_yn']]
exercise_frame['lift_description'] = exercise_frame['lift_description'].astype('str')
exercise_frame['exercise_description'] = exercise_frame['exercise_description'].astype('str')
exercise_frame[:5]

#Create 'Lifting' column
exercise_frame['lifting'] = np.where(exercise_frame['lift_description'].str.contains('nan'), 0, 1)

#Create a list of exercises
exercise_list = ['Basketball', 'Hiking', 'Volleyball', 'Biking', 'Urban hiking',
            'Jump', 'Swimming', 'Beach', 'Tennis', 'Kayak']

for i in range(len(exercise_list)):
    exercise_frame[exercise_list[i]] = np.where(exercise_frame['exercise_description'].str.contains(exercise_list[i]), 1, 0)
exercise_frame[:10]

graph_exercise = ['exercise_yn'] + ['lifting'] + exercise_list

#Visualize exercises over time

matplotlib.style.use('classic')

#Set the number of graphs
graphs = len(graph_exercise)

#create a list of positions for the chart
position = []
for i in range(4):
    for j in range(3):
        b = i,j
        position.append(b)

#Create base of subplot chart.. rows x columbs = graphs
fig, axes = plt.subplots(nrows=4, ncols=3, sharey=True, sharex=False, figsize=(16,4))
fig.subplots_adjust(hspace=.5)

#Fill in base with graphs based off of position
for i in range(graphs):
    exercise_frame[graph_exercise[i]].plot(ax=axes[position[i]], kind='bar', color='g')

#Set the formatting elements of the axes for each graph
for i in range(graphs):
    axes[position[i]].set_title(graph_exercise[i], size = 6)
    axes[position[i]].tick_params(
                    axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom='off',      # ticks along the bottom edge are off
                    top='off',         # ticks along the top edge are off
                    labelbottom='off') # labels along the bottom edge are off
    axes[position[i]].tick_params(
                    axis='y',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    left='off',      # ticks along the bottom edge are off
                    right='off',         # ticks along the top edge are off
                    labelleft='off') # labels along the bottom edge are off
    axes[position[i]].set_xlabel("date", size = 5)
    
#WEIGHT LIFTING ACTIVITY BY DAY

#Create a new lifting dataframe
lift_frame = jumptracker_current[['DateTime','lift_description']]
lift_frame['lift_description'] = lift_frame['lift_description'].astype('str')

#Create a list of lifting exercises
lift_list = ['bench', 'chinups', 'incline', 'shoulder press', 'squats',
            'vertical rows', 'curls', 'pushups', 'lat pulldown']

for i in range(len(lift_list)):
    lift_frame[lift_list[i]] = np.where(lift_frame['lift_description'].str.contains(lift_list[i]), 1, 0)
lift_frame[:5]

#Visualize lifting exercises over time

matplotlib.style.use('classic')

#Set the number of graphs
graphs = len(lift_list)

#create a list of positions for the chart
position = []
for i in range(3):
    for j in range(3):
        b = i,j
        position.append(b)

#Create base of subplot chart.. rows x columbs = graphs
fig, axes = plt.subplots(nrows=3, ncols=3, sharey=True, sharex=False, figsize=(12,4))
fig.subplots_adjust(hspace=.5)

#Fill in base with graphs based off of position
for i in range(graphs):
    lift_frame[lift_list[i]].plot(ax=axes[position[i]], kind='bar', color='r')

#Set the formatting elements of the axes for each graph
for i in range(graphs):
    axes[position[i]].set_title(lift_list[i], size = 6)
    axes[position[i]].tick_params(
                    axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom='off',      # ticks along the bottom edge are off
                    top='off',         # ticks along the top edge are off
                    labelbottom='off') # labels along the bottom edge are off
    axes[position[i]].tick_params(
                    axis='y',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    left='off',      # ticks along the bottom edge are off
                    right='off',         # ticks along the top edge are off
                    labelleft='off') # labels along the bottom edge are off
    axes[position[i]].set_xlabel("date", size = 5)
