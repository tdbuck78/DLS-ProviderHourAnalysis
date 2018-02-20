'''

	----------PROVIDER HOUR ANALYSIS---------------------

Project for Developmental Learning Solutions Inc. usage

This project produces a data visualization of DLS provider hours over a two year period

  This script
  
  (1) Grabs data from csv datafile produced from a sql query ran on the dls server   (github: table data was censored for privacy)
  
  (2) Produces analysis of total monthly hours per provider, as well as a DLS collective total
  
  (3) Outputs visualization to image file using matplotlib
  
'''


''' -------------importing libraries and reading in data-----------'''
import matplotlib.pyplot as plt
import matplotlib
%matplotlib inline
import numpy as np
import pandas as pd
import datetime
import time 
import matplotlib.dates as mdates
from datetime import datetime

df = pd.read_excel('x2_actions.xlsx')
df['Start'] = pd.to_datetime(df['Start'])

'''-----------Getting an array of months in unix time------------'''
unix_months = []
for year in range (2015,2018):
    for month in range(1,13):
        dt = datetime(year, month, 1)
        unix_months.append(time.mktime(dt.timetuple()))
dt = datetime(2018, 1, 1)
unix_months.append(time.mktime(dt.timetuple()))

# Making x-axis labels
x_months_arr = []
for year in range (2015,2018):
    for month in range(1,13):
        dt = datetime(year,month,1)
        x_months_arr.append(dt)
x_months = np.array(x_months_arr)

fig,axes = plt.subplots(nrows=2,ncols=1,figsize=(40,25))

matplotlib.rcParams.update({'font.size': 20})

'''-----------------------calculating hours --------------------------------'''

for provider in ['Kamau','wgarrick','Claire','Susan','Ssujatha','Leti','Aram','Rachel','tnick','John']:
    temp = []
    for i in range (0,len(unix_months)-1):
        temp.append( df[
        (df['Provider']== provider) & (df['Start Unix']>unix_months[i])  & (df['Start Unix']<unix_months[i+1])
                            ] ['Hours'].sum()
                         )
    y1 = np.array(temp)
    axes[0].plot(x_months,y1,label=provider)


    
#DLS total hours
temp = []
for i in range (0,len(unix_months)-1):
        temp.append( df[
        (df['Start Unix']>unix_months[i])  & (df['Start Unix']<unix_months[i+1])
                            ] ['Hours'].sum()
                         )
y2 = np.array(temp)
axes[1].plot(x_months,y2,label='Combined Providers (All)')


'''---------------------------formatting visual---------------------------'''

axes[0].set_xticks(x_months)
axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%m-%y'))
axes[0].xaxis.set_tick_params(which='major', pad=50)
axes[0].grid(True,which='minor')
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Hours')
axes[0].set_title('Top 10 Providers - Monthly Hours')
axes[0].legend()

axes[1].set_xticks(x_months)
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Hours')
axes[1].set_title('DLS Total - Monthly Hours')
axes[1].legend()