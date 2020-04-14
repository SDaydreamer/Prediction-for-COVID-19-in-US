from datetime import datetime
import numpy as np

# by default, from 2020.01.23 to today
def Days(year=2020, month=1, day=23):
    dt = datetime.now()
    date = []

    while True:
        date.append(str(year)+'-'+str(month)+'-'+str(day))
        
        if (year==dt.year)and(month==dt.month)and(day==dt.day):
            break
        
        day += 1
        
        if (month==1)|(month==3)|(month==5)|(month==7)|(month==8)|(month==10)|(month==12):
            if day == 32:
                day = 1
                month += 1
        elif (month==4)|(month==6)|(month==9)|(month==11):
            if day == 31:
                day = 1
                month += 1
        else:
            if year//4 == year/4:
                if day == 30:
                    day = 1
                    month += 1
            else:
                if day == 29:
                    day = 1
                    month += 1

        if month == 13:
            month == 1
            year += 1

    return date

def After(days, year=None, month=None, day=None):
    if not year:
        dt = datetime.now()
        year = dt.year
        month = dt.month
        day = dt.day

    while True:
        if days == 0:
            break
        
        day += 1

        if (month==1)|(month==3)|(month==5)|(month==7)|(month==8)|(month==10)|(month==12):
            if day == 32:
                day = 1
                month += 1
        elif (month==4)|(month==6)|(month==9)|(month==11):
            if day == 31:
                day = 1
                month += 1
        else:
            if year//4 == year/4:
                if day == 30:
                    day = 1
                    month += 1
            else:
                if day == 29:
                    day = 1
                    month += 1

        if month == 13:
            month == 1
            year += 1

        days -= 1

    return year, month, day

def sigmoid(x, k=1, t=0, m=1):
    return k/(1+np.exp(-(x-t)/m))

if __name__ == '__main__':
    date = Days()
    print(date[-1:][0])

    after_n_days = 0
    y, m, d = After(after_n_days,2020,1,23)
    date = Days(y,m,d)
    print(date)
    print(f'y={y},m={m},d={d}')
