#!/usr/bin/env python3
"""
To import everything:
sys.path.append(str(__projectdir__ / Path('submodules/time-index-func/')))
from time_index_func import *

"""

import os
from pathlib import Path
import sys


import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import pytz


# Definitions:{{{1
listoffreqs = ['y', 'q', 'm', 'w', 'd', 'H', 'M', 'S']

# General Functions for Time:{{{1
def convertmytimetodatetime(mytime):
    try:
        freq = mytime[-1]
        if freq == 'y':
            asdatetime = datetime.datetime.strptime(mytime[: -1], '%Y')
        elif freq == 'q':
            asdatetime = datetime.datetime(int(mytime[: 4]), int(mytime[4]) * 3, 1)
        elif freq == 'm':
            asdatetime = datetime.datetime.strptime(mytime[: 6], '%Y%m')
        elif freq == 'w' or freq == 'd':
            asdatetime = datetime.datetime.strptime(mytime[: 8], '%Y%m%d')
        elif freq == 'H':
            asdatetime = datetime.datetime.strptime(mytime[: 11], '%Y%m%d_%H')
        elif freq == 'M':
            asdatetime = datetime.datetime.strptime(mytime[: 13], '%Y%m%d_%H%M')
        elif freq == 'S':
            asdatetime = datetime.datetime.strptime(mytime[: 15], '%Y%m%d_%H%M%S')
        else:
            raise ValueError('Frequency not exist')
    except Exception:
        raise ValueError('Failed convertmytimetodatetime for: ' + mytime + '.')

    return(asdatetime)


def convertmytimetodatetime_test():
    """
    Takes a date in the format I use and convert it to datetime.
    """
    print(convertmytimetodatetime('2020y'))
    print(convertmytimetodatetime('20201q'))
    print(convertmytimetodatetime('202001m'))
    print(convertmytimetodatetime('20200102w'))
    print(convertmytimetodatetime('20200102d'))
    print(convertmytimetodatetime('20200102_03H'))
    print(convertmytimetodatetime('20200102_0306M'))
    print(convertmytimetodatetime('20200102_030609S'))


def convertdatetimetomytime(dt, freq):
    """
    Takes a datetime and converts it to the format I use for my indexes.
    """
    if freq == 'y':
        asmytime = dt.strftime('%Yy')
    elif freq == 'q':
        asmytime = str(dt.year) + str((dt.month + 2) // 3) + 'q'
    elif freq == 'm':
        asmytime = dt.strftime('%Y%mm')
    elif freq == 'w':
        asmytime = dt.strftime('%Y%m%dw')
    elif freq == 'd':
        asmytime = dt.strftime('%Y%m%dd')
    elif freq == 'H':
        asmytime = dt.strftime('%Y%m%d_%HH')
    elif freq == 'M':
        asmytime = dt.strftime('%Y%m%d_%H%MM')
    elif freq == 'S':
        asmytime = dt.strftime('%Y%m%d_%H%M%SS')
    else:
        raise ValueError('freq not defined. freq: ' + str(freq) + '.')

    return(asmytime)


def convertdatetimetomytime_test():
    dt = datetime.datetime(2020, 1, 2, 3, 6, 9)
    print(convertdatetimetomytime(dt, 'y'))
    print(convertdatetimetomytime(dt, 'q'))
    print(convertdatetimetomytime(dt, 'm'))
    print(convertdatetimetomytime(dt, 'w'))
    print(convertdatetimetomytime(dt, 'd'))
    print(convertdatetimetomytime(dt, 'H'))
    print(convertdatetimetomytime(dt, 'M'))
    print(convertdatetimetomytime(dt, 'S'))


def addperiodsbyfreq(dt, freq, num):
    """
    Adds num periods to dt where the periods are of the length freq.
    """
    if freq == 'y':
        dt = dt + relativedelta(years = num)
    elif freq == 'q':
        dt = dt + relativedelta(months = 3 * num)
    elif freq == 'm':
        dt = dt + relativedelta(months = num)
    elif freq == 'w':
        dt = dt + relativedelta(days = 7 * num)
    elif freq == 'd':
        dt = dt + relativedelta(days = num)
    elif freq == 'H':
        dt = dt + relativedelta(hours = num)
    elif freq == 'M':
        dt = dt + relativedelta(minutes = num)
    elif freq == 'S':
        dt = dt + relativedelta(seconds = num)
    else:
        raise ValueError('freq not defined. freq: ' + str(freq) + '.')

    return(dt)

    
def addperiodsbyfreq_test():
    dt = datetime.datetime(2020, 1, 2, 3, 6, 9)
    print(addperiodsbyfreq(dt, 'y', 2))
    print(addperiodsbyfreq(dt, 'q', 2))
    print(addperiodsbyfreq(dt, 'm', 2))
    print(addperiodsbyfreq(dt, 'w', 2))
    print(addperiodsbyfreq(dt, 'd', 2))
    print(addperiodsbyfreq(dt, 'H', 2))
    print(addperiodsbyfreq(dt, 'M', 2))
    print(addperiodsbyfreq(dt, 'S', 2))


def getallpointsbetween(datetime1, datetime2, freq, asmytime = False):
    """
    Get all periods between two datetimes where a period is measured using freq
    """
    if freq == 'y':
        dates = pd.date_range(start = datetime1, end = datetime2, freq = 'Y')
    elif freq == 'q':
        dates = pd.date_range(start = datetime1, end = datetime2, freq = '3M')
    elif freq == 'm':
        dates = pd.date_range(start = datetime1, end = datetime2, freq = 'M')
    elif freq == 'w':
        dates = pd.date_range(start = datetime1, end = datetime2, freq = 'W')
    elif freq == 'd':
        dates = pd.date_range(start = datetime1, end = datetime2, freq = 'D')
    elif freq == 'H':
        dates = pd.date_range(start = datetime1, end = datetime2, freq = 'H')
    elif freq == 'M':
        dates = pd.date_range(start = datetime1, end = datetime2, freq = 'min')
    elif freq == 'S':
        dates = pd.date_range(start = datetime1, end = datetime2, freq = 'S')
    else:
        raise ValueError('freq not defined. freq: ' + str(freq) + '.')

    if asmytime is True:
        dates = [convertdatetimetomytime(dt, freq) for dt in list(dates)]
    else:
        dates = dates.to_pydatetime()

    return(dates)


def getallpointsbetween_test():
    dt1 = datetime.datetime(2020, 1, 2, 3, 6, 9)
    print(getallpointsbetween(dt1, addperiodsbyfreq(dt1, 'y', 2), 'y') )
    print(getallpointsbetween(dt1, addperiodsbyfreq(dt1, 'q', 2), 'q') )
    print(getallpointsbetween(dt1, addperiodsbyfreq(dt1, 'm', 2), 'm') )
    print(getallpointsbetween(dt1, addperiodsbyfreq(dt1, 'w', 2), 'w') )
    print(getallpointsbetween(dt1, addperiodsbyfreq(dt1, 'd', 2), 'd') )
    print(getallpointsbetween(dt1, addperiodsbyfreq(dt1, 'H', 2), 'H') )
    print(getallpointsbetween(dt1, addperiodsbyfreq(dt1, 'M', 2), 'M') )
    print(getallpointsbetween(dt1, addperiodsbyfreq(dt1, 'S', 2), 'S') )

    print(getallpointsbetween(dt1, addperiodsbyfreq(dt1, 'y', 2), 'y', asmytime = True) )


def getallpointsbetween_mytime(mytime1, mytime2, asmytime = True):
    """
    Get all periods between two of my datetimes
    Returns as mytime unless asmytime is False
    """
    if asmytime not in [False, True]:
        raise ValueError('asmytime is misspecified. Should be True/False. Value: ' + str(asmytime) + '.')
    freq = mytime1[-1]

    dt1 = convertmytimetodatetime(mytime1)
    dt2 = convertmytimetodatetime(mytime2)

    dates = getallpointsbetween(dt1, dt2, freq, asmytime = asmytime)

    return(dates)


def getallpointsbetween_mytime_test():
    print(getallpointsbetween_mytime('200101m', '200105m'))


# Weekdays:{{{1
def getdayofweek(index_mytime):
    """
    0 = Monday
    6 = Sunday
    """
    dayofweek = [convertmytimetodatetime(mytime).weekday() for mytime in index_mytime]

    return(dayofweek)


def getdayofweek_test():
    df = pd.DataFrame({'interestrate': [1.01, 1.02, 1.03, 1.04, 1.05]}, index = ['20100701d', '20100702d', '20100703d', '20100704d', '20100705d'])
    df['dayofweek'] = getdayofweek(df.index)
    print(df)


def get_weekend_fri_sat():
    # based on https://www.diversityresources.com/holidays-and-work-schedule/
    weekend_fri_sat = []
    weekend_fri_sat.append('AFG') # Afghanistan
    weekend_fri_sat.append('ARE') # United Arab Emirates
    weekend_fri_sat.append('BHR') # Bahrain
    weekend_fri_sat.append('DZA') # Algeria
    weekend_fri_sat.append('DJI') # Djibouti
    weekend_fri_sat.append('EGY') # Egypt
    weekend_fri_sat.append('IRN') # Iran
    weekend_fri_sat.append('IRQ') # Iraq
    weekend_fri_sat.append('ISR') # Israel
    weekend_fri_sat.append('JOR') # Jordan
    weekend_fri_sat.append('KWT') # Kuwait
    weekend_fri_sat.append('LBY') # Libya
    weekend_fri_sat.append('MRT') # Mauritania
    weekend_fri_sat.append('OMN') # Oman
    weekend_fri_sat.append('QAT') # Qatar
    weekend_fri_sat.append('SAU') # Saudi Arabia
    weekend_fri_sat.append('SDN') # Sudan
    weekend_fri_sat.append('SYR') # Syria
    weekend_fri_sat.append('PSE') # Palestine
    return(weekend_fri_sat)


def weekdaysonly(df):
    df = df[[convertmytimetodatetime(mytime).weekday() in [0, 1, 2, 3, 4] for mytime in df.index]]

    return(df)


def weekdaysonly_test():
    df = pd.DataFrame({'interestrate': [1.01, 1.02, 1.03, 1.04, 1.05]}, index = ['20100701d', '20100702d', '20100703d', '20100704d', '20100705d'])
    df = weekdaysonly(df)
    print(df)


# Fill DataFrame:{{{1
def filltime(df):
    startdate = df.index[0]
    enddate = df.index[-1]

    dates = getallpointsbetween_mytime(startdate, enddate)

    df = df.reindex(dates)

    return(df)


def filltime_test():
    df = pd.DataFrame([[100], [101], [103]], columns = ['gdp'], index = ['20001q', '20002q', '20004q'])
    print(filltime(df))


# Adjusting Frequencies of Data:{{{1
def raisefreq(df, newfreq, how = 'sameallperiod'):
    """
    Currently only works for 'y', 'q', 'm' data

    how == 'sameallperiod' means that if I have 2010Q1 = 100 then 2010M1 = 2010M2 = 2010M3 = 100 regardless of what was happening with the trend
    Need to add an interpolation method
    """
    firstdate = df.index[0]
    lastdate = df.index[-1]

    oldfreq = firstdate[-1]

    if oldfreq not in listoffreqs:
        raise ValueError('oldfreq not a frequency I use. oldfreq: ' + oldfreq + '.')
    if newfreq not in listoffreqs:
        raise ValueError('newfreq not a frequency I use. newfreq: ' + newfreq + '.')

    # verify newfreq is a higher frequency than oldfreq
    if listoffreqs.index(newfreq) <= listoffreqs.index(oldfreq):
        raise ValueError('newfreq does not have a higher frequency than oldfreq. newfreq: ' + newfreq + '. oldfreq: ' + oldfreq + '.')

    datetime1 = convertmytimetodatetime(firstdate)
    datetime2 = convertmytimetodatetime(lastdate)

    # ensure covering all periods by subtracting one (oldfreq) period from datetime1 and adding one (oldfreq) period to datetime2
    datetime1 = addperiodsbyfreq(datetime1, oldfreq, -1)
    datetime2 = addperiodsbyfreq(datetime2, oldfreq, 1)

    # get datetime range with newfreq
    newindex_dt = getallpointsbetween(datetime1, datetime2, newfreq)
    newindex = [convertdatetimetomytime(dt, newfreq) for dt in newindex_dt]
    newindex_asold = [convertdatetimetomytime(dt, oldfreq) for dt in newindex_dt]

    if how == 'sameallperiod':
        # create dict from oldindex to relevant values
        oldvalueslist = df.values.tolist()
        oldindexlist = list(df.index)
        olddict = {}
        for i in range(len(oldindexlist)):
            olddict[oldindexlist[i]] = oldvalueslist[i]

        numcol = len(df.columns)
        newvalueslist = []
        for oldind in newindex_asold:
            if oldind in olddict:
                newvalueslist.append(olddict[oldind])
            else:
                newvalueslist.append([np.nan] * numcol)

        df2 = pd.DataFrame(newvalueslist, columns = df.columns, index = newindex)

    return(df2)


def raisefreq_test():
    df = pd.DataFrame([[1], [2], [3]], columns = ['var1'], index = ['20101q', '20102q', '20103q'])

    print(raisefreq(df, 'm'))

# Strip NA Start/End:{{{1
def stripnarows_startend(df, start = True, end = True):
    """
    This function removes every na row at the start/end of a dataset until a row is reached where there is a non-na value.
    Note this is useful with time series data.

    To turn of start: start = False
    To turn of end: end = False
    """
    if start is not True and end is not True:
        raise ValueError('At least one of start and end must be specified to be True')
    numrows = len(df)

    # turn into list to make iteration faster
    valueslist = df.values.tolist()

    if start is True:
        starti = None
        for i in range(numrows):
            for element in valueslist[i]:
                if pd.isnull(element) is False:
                    starti = i
                    break
            if starti is not None:
                break
    else:
        starti = 0

    if end is True:
        endi = None
        for i in reversed(range(numrows)):
            for element in valueslist[i]:
                if pd.isnull(element) is False:
                    endi = i
                    break
            if endi is not None:
                break
    else:
        endi = numrows - 1

    if starti is None or endi is None:
        raise ValueError('All rows appear to only contain na values.')

    df = df.iloc[starti: endi + 1, :].copy()

    return(df)

                    
def stripnarows_startend_test():
    df = pd.DataFrame([[np.nan], [100], [102], [np.nan], [np.nan]], index = ['2000y', '2001y', '2002y', '2003y', '2004y'], columns = ['gdp'])
    
    print(stripnarows_startend(df))
    print(stripnarows_startend(df, start = False, end = True))
    print(stripnarows_startend(df, start = True, end = False))

# Difference Between Periods:{{{1
def getdifferenceinperiods(list_mytime, includefirst = True):
    """
    Get difference between periods.
    No easy way to do this for months/quarters/years and it's unclear that I would want an easy way since I may want to capture the fact that the difference between Feb 1st and March 1st is different to March 1st and April 1st
    So just use days for years, quarters and months
    Every other measurement use same measure of difference as index
    """
    freq = list_mytime[0][-1]
    
    list_dt = [convertmytimetodatetime(mytime) for mytime in list_mytime]
    diff_dt = [list_dt[i] - list_dt[i - 1] for i in range(1, len(list_dt))]
    
    if freq == 'y' or freq == 'q' or freq == 'm' or freq == 'd':
        diff_per = [dt.days for dt in diff_dt]
    elif freq == 'w':
        diff_per = [dt.days / 7 for dt in diff_dt]
    elif freq == 'H':
        diff_per = [dt.seconds / 3600 for dt in diff_dt]
    elif freq == 'M':
        diff_per = [dt.seconds / 60 for dt in diff_dt]
    elif freq == 'S':
        diff_per = [dt.seconds for dt in diff_dt]
    else:
        raise ValueError('freq not defined. freq: ' + str(freq) + '.')

    if includefirst is True:
        # add in first element which is na since I can't subtract the time period before
        diff_per = [np.nan] + diff_per

    return(diff_per)


def getdifferenceinperiods_test():
    print( getdifferenceinperiods(['2000y', '2001y', '2002y', '2004y']) )
    print( getdifferenceinperiods(['20001q', '20002q', '20003q','20011q']) )
    print( getdifferenceinperiods(['200001m', '200002m', '200003m','200005m']) )
    print( getdifferenceinperiods(['20000101d', '20000102d', '20000103d','20000105d']) )
    print( getdifferenceinperiods(['20000101_00H', '20000101_01H', '20000101_02H','20000101_04H']) )
    print( getdifferenceinperiods(['20000101_0000M', '20000101_0001M', '20000101_0002M','20000101_0004M']) )
    print( getdifferenceinperiods(['20000101_000000S', '20000101_000001S', '20000101_000002S','20000101_000004S']) )
# Timezone Convert:{{{1
def tzconvert_single(dt, oldtimezone, newtimezone):
    """
    Convert dt from oldtimezone to newtimezone
    Get list of timezones using pytz.common_timezones
    Basic ones:
    GMT
    America/New_York
    America/Los_Angeles
    """
    dt2 = pytz.timezone(oldtimezone).localize(dt).astimezone(pytz.timezone(newtimezone))
    return(dt2)


def tzconvert_list(dtlist, oldtimezone, newtimezone):
    dtlist2 = [tzconvert_single(dt, oldtimezone, newtimezone) for dt in dtlist]
    return(dtlist2)
