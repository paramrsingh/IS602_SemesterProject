import pandas as pd
from pandas import Series
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

casedf = pd.read_csv('~/Downloads/SPCS10RSA.csv')
zillowdf = pd.read_csv('~/Downloads/Zip_Zhvi_AllHomes.csv')

print casedf.info()
print zillowdf.info()

print casedf.dtypes
# print zillowdf.dtypes

print casedf.head()
print zillowdf.head()

casedf['DATE'] = pd.to_datetime(casedf['DATE'])
print casedf.head()
print casedf.info()

# Don't care about the Case Shiller data from before 2010
casedf = casedf.ix[92:]
print casedf

# Don't care about the Zillow data for zip 11101 before 2010 (doesn't exist)
colcounter = range(0, 172)
# Grab just the columns interested in
licdata = zillowdf.drop(zillowdf.columns[[colcounter]], axis=1)
print "Watch this:"
licdata = licdata[2998:2999].T

# Since the case-schiller data is by quarter, remove the datapoints to keep n observations the same for both
excludelist = []
years = ['2010', '2011', '2012', '2013', '2014', '2015']
months = ['02', '03', '05', '06', '08', '09', '11', '12']
for i in years:
    for j in months:
        excludelist.append(str(i) + "-" + str(j))
# manually dropping the last two months in 2015 as they are not present in the data
del excludelist[-2:]
licdata = licdata.drop(excludelist, axis=0)
licdata = licdata.ix[:-1]
print licdata

# Align both datasets so that they can be plotted to determine if there is a positive correlation
Y = np.array(licdata[[2998]])
Y = Y/1000
Y = Y.squeeze()
print Y.shape
X = np.array(casedf[['VALUE']])
X = X.squeeze()
print X.shape
# lin reg

slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
print r_value
#plt.scatter(X, Y)
#plt.plot(X, slope*X + intercept)
#plt.show()

casedf = pd.read_csv('~/Downloads/SPCS10RSA.csv')
casedf = casedf.ix[52:]
casedf['DATE'] = pd.to_datetime(casedf['DATE'])
X = np.array(casedf[['DATE']])
Y = np.array(casedf[['VALUE']])
X = X.squeeze()
Y = Y.squeeze()
maxYvalue = max(Y)
maxresult = casedf.loc[casedf['VALUE'] == maxYvalue]
current = Y[-1]
dx = maxresult[['DATE']].squeeze()
print maxresult[['VALUE']]
#plt.scatter(X, Y)
#plt.scatter(dx, maxYvalue, color='red', marker='>', s=100)
#plt.annotate('max value: %s' % maxYvalue, xy=(dx, maxYvalue))
#plt.scatter('2015-07-01 00:00:00', current, color='green', marker='*', s=100)
#plt.annotate('current value: %s' % current, xy=('2013-07-01 00:00:00', current))
#plt.show()

nycopendata = pd.read_csv('~/Downloads/DOB_Permit_Issuance-3a.csv')
print nycopendata.info()

#drop columns not needed
colcounter = range(0, 19)
nycopendata = nycopendata.drop(nycopendata.columns[[colcounter]], axis=1)
colcounter = range(6, 35)
nycopendata = nycopendata.drop(nycopendata.columns[[colcounter]], axis=1)
colcounter = range(1, 5)
nycopendata = nycopendata.drop(nycopendata.columns[[colcounter]], axis=1)
print nycopendata.info()

#change Filing Date to datetime
nycopendata['Filing Date'] = pd.to_datetime(nycopendata['Filing Date'])

#sort by permit type
nycopendata = nycopendata[(nycopendata['Permit Type'] != 'PL') | (nycopendata['Permit Type'] == 'SG')]
print nycopendata.info()
print nycopendata.head()

#count per quarter per year
nycopendata['Filing Date'] = nycopendata['Filing Date'].apply(lambda t: t.to_period(freq='q'))

#group filing date by quarter and count the number of filed permits
count_per_quarter = nycopendata[['Permit Type', 'Filing Date']].groupby(['Filing Date']).agg(['count'])
count_per_quarter.reset_index(inplace=True)
count_per_quarter.columns = count_per_quarter.columns.get_level_values(0)

X = np.array(count_per_quarter[['Filing Date']]).squeeze()
print X
Y = np.array(count_per_quarter[['Permit Type']]).squeeze()
print Y

ao = Series(Y, index=X)
print ao
ao.plot(kind='bar')
plt.show()