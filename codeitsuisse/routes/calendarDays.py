from ast import Str
from datetime import datetime
from datetime import date
from typing import List 
import pandas as pd

import logging

from flask import request

from codeitsuisse import app

#part 1
def calendar_dates(list: List):
    res = ""
    arr = []
    arr = ["       ," for i in range(12)]
    filter = [ele for ele in list if ele > 0]
    dts = filter[1:]
    dts.sort()
    for i in range(len(dts)): 
        date = datetime.strptime(str(list[0]) + "-" + str(dts[i]), "%Y-%j")
        d = pd.Timestamp(date)
        day = d.day_name().lower()
        day_num = d.weekday() # index harinya 
        arr[d.month-1] = arr[d.month-1][:day_num] + day[0] + arr[d.month-1][day_num+1:]
    for i in range(12):
        if(arr[i] == 'mtwtfss,'):
            arr[i] = 'alldays,'
        elif(arr[i] == '     ss,'):
            arr[i] = 'weekends,'
        elif(arr[i] == 'mtwtf  ,'):
            arr[i] = 'weekdays,'
    res = ''.join(arr)
    return res

def first_dow(year, month, dow):
    day = ((8 + dow) - date(year, month, 1).weekday()) % 7
    if(day==0):
        day=7
    number = date(year, month, day).timetuple().tm_yday
    return number

# part 2
def part2(string: Str):
    res = []
    for i in range(len(string)):
        if(string[i] == ' '):
            year = i + 2001
            break
    res.append(year)
    print(string)
    x = string.split(",")
    x.pop()
    for i in range(len(x)): #12
        if(x[i] == 'weekday'):
            for y in range(5):
                res.append(first_dow(year, i+1,0) + y)
        elif(x[i] == 'weekend'):
            for y in range(2):
                res.append(first_dow(year, i+1,5) + y)
        elif(x[i] == 'alldays'):
            for y in range(7):
                res.append(first_dow(year, i+1,0) + y)
        elif(x[i] != '       '):
            if(x[i][0] == 'm'):
                res.append(first_dow(year, i+1,0))
            if(x[i][1] == 't'):
                res.append(first_dow(year, i+1,1))
            if(x[i][2] == 'w'):
                res.append(first_dow(year, i+1,2))
            if(x[i][3] == 't'):
                res.append(first_dow(year, i+1,3))
            if(x[i][4] == 'f'):
                res.append(first_dow(year, i+1,4))
            if(x[i][5] == 's'):
                res.append(first_dow(year, i+1,5))
            if(x[i][6] == 's'):
                res.append(first_dow(year, i+1,6))
    print(res)
    return res

@app.route('/calendarDays', methods=['POST'])          
def calendar():
    data = request.get_json()
    numbers = data.get("numbers")
    part1_var = calendar_dates(numbers)
    logging.info(part1_var)
    part2_var = part2(part1_var)
    logging.info(part2_var)
    return {"part1": part1_var, "part2": part2_var}
            
