# just_time
A module that implements useful methods that should have been in the python `datetime.time` library. Supports addition, subtraction and logical operations with python `datetime.time`, `datetime.timedelta` and other instances of itself.
The `JustTime` class allows representing time greater than 24hrs without going into days, months or years. If time is greater than 24hrs then only the hour will increase past its normal limit of <= 23. Minute, second, and microsecond remain under their limit.
### Installation
##### Using Https:

    pip install git+https://git@github.com/zznixt07/just-time.git

##### Using SSH

    pip install git+ssh://git@github.com:zznixt07/just-time.git

#### Usage

```
from just_time import JustTime
age_of_earth = JustTime(hour=39_823_120_260_000)
````

#### Features
This module tries to follow API of python's `datetime.time`.

 - properties like hour, minute, second, and microsecond
    ```
    >>> one_hour = JustTime(hour=1, minute=0, second=0, microsecond=0)
    >>> one_day = JustTime(23, 59, 59)
    >>> one_hour.minute
    0   
    >>> one_hour.second # Note: not the total seconds
    1
    ```
- total_seconds() and total_microseconds()
    ```
    >>> one_hour.total_seconds()
    3600.0  
    >>> one_hour.total_microseconds()
    3600000000
    ```
 - Arithmetic and logical operation
    ```
    >>> one_day = JustTime(24, 0, 0)
    >>> one_hour + one_day
    JustTime(25, 0, 0, 0) # repr outputs a valid JustTime instance

    >>> print(JustTime(25, 0, 0, 0))
    25:00:00:000000 # HH:MM:SS:μs format

    >>> one_day - one_hour
    datetime.timedelta(seconds=82800)

    >>> one_hour < one_day and one_hour != one_day
    True

    >>> import datetime
    >>> one_hour - datetime.timedelta(hours=1)
    > JustTime(0, 0, 0, 0)
    ```
- supports method `strftime` like python `datetime`
- convert from seconds to HH:MM:SS:μs
    ```
    >>> print(JustTime(second=60))
    00:01:00:000000
    ```
- no limit on integers passed to the args.
    ```
    >>> precise_time = JustTime(minute=69, second=42, microsecond=69_000_000_000)
    JustTime(20, 19, 42, 0)
    ```

