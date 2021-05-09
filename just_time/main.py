from __future__ import annotations
from typing import Dict, Union
from datetime import time, timedelta, timezone, tzinfo


class JustTime:

    def __init__(self,
        hour: int = 0, minute: int = 0, second: int = 0, microsecond: int = 0,
        tzinfo: tzinfo = timezone.utc):
        '''JustTime allows representing time greater than 24hrs.
        If time is greater than 24hrs then only the hour will increase past its
        normal limit of <= 23. Minute, second, and microsecond remain under their
        limit.
        Supports addition and substraction with other JustTime, time and timedelta object.

        You can also convert seconds to HH:MM:SS format by specifying just the
        :param:seconds
        '''

        self._total_microseconds: int = (hour * 3600 + minute * 60 + second) * (10 ** 6) + microsecond
        self._total_seconds: int = self._total_microseconds * (10 ** -6)
        rem = self._total_microseconds % (3600 * 10 ** 6)
        hh = self._total_microseconds // (3600 * 10 ** 6)
        mm = rem // (60 * 10 ** 6)
        ss = rem % (60 * 10 ** 6) // (10 ** 6)
        self._hour: int = hh
        self._minute: int = mm
        self._second: int = ss
        self._microsecond: int = self._total_microseconds % (10 ** 6)

    @property
    def hour(self) -> int:
        "[-inf, +inf]"
        return self._hour

    @property
    def minute(self) -> int:
        "[-inf, +59]"
        return self._minute
    
    @property
    def second(self) -> int:
        "[-inf, +59]"
        return self._second
    
    @property
    def microsecond(self):
        "[-inf, +1_000_000]"
        return self._microsecond
    
    def __str__(self) -> str:
        return f'{self.hour:02}:{self.minute:02}:{self.second:02}:{self.microsecond:06}'

    def __repr__(self) -> str:
        return f'JustTime({self.hour}, {self.minute}, {self.second}, {self.microsecond})'

    def __lt__(self, other) -> bool:
        if isinstance(other, (JustTime, time)):
            other = JustTime(other.hour, other.minute, other.second, other.microsecond)
        return self.total_seconds() < other.total_seconds()

    def __gt__(self, other) -> bool:
        if isinstance(other, (JustTime, time)):
            other = JustTime(other.hour, other.minute, other.second, other.microsecond)
        return self.total_seconds() > other.total_seconds()

    def __eq__(self, other) -> bool:
        if isinstance(other, (JustTime, time)):
            other = JustTime(other.hour, other.minute, other.second, other.microsecond)
        return self.total_seconds() == other.total_seconds()

    def __le__(self, other) -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other) -> bool:
        return self.__gt__(other) or self.__eq__(other)      
               
    def __add__(self, other) -> JustTime:
        "TODO support tzinfo"

        other_obj: Union[time, JustTime]
        if isinstance(other, (time, JustTime)):
            other_obj = other
        elif isinstance(other, timedelta):
            other_obj = JustTime(second=int(other.total_seconds()))
        else:
            return NotImplemented

        return JustTime(
            hour=self.hour+other_obj.hour,
            minute=self.minute+other_obj.minute,
            second=self.second+other_obj.second,
            microsecond=self.microsecond+other_obj.microsecond,
        )

    def __sub__(self, other) -> Union[timedelta, JustTime]:
        "TODO support tzinfo"

        other_obj: Union[time, JustTime]
        if isinstance(other, (time, JustTime)):
            # return timedelta(seconds=self.total_seconds()-int(other.total_seconds()))
            return timedelta(
                hours=self.hour-other.hour,
                minutes=self.minute-other.minute,
                seconds=self.second-other.second,
                microseconds=self.microsecond-other.microsecond,
            )
        elif isinstance(other, timedelta):
            # return JustTime(second=self.total_seconds()-int(other.total_seconds()))
            other_obj = JustTime(second=int(other.total_seconds()))
            return JustTime(
                hour=self.hour-other_obj.hour,
                minute=self.minute-other_obj.minute,
                second=self.second-other_obj.second,
                microsecond=self.microsecond-other_obj.microsecond,
            )
        else:
            return NotImplemented

    def strftime(self, str_f: str) -> str:
        frmt_info: Dict[str, str] = {
            'H': f'{self.hour:02}',
            'I': f'{self.hour % 12:02}' if self.hour > 12 else f'{self.hour:02}',
            'p': 'AM' if self.hour < 12 else 'PM',
            'M': f'{self.minute:02}',
            'S': f'{self.second:02}',
            'f': f'{self.microsecond:06}'
        }
        # translation: Dict[int, int] = str.maketrans(frmt_info)
        for character in frmt_info:
            # str_f = str_f.replace('%' + character, translation[ord(character)])
            str_f = str_f.replace('%' + character, frmt_info[character])
        
        return str_f

    def total_seconds(self) -> float:
        return self._total_seconds

    def total_microseconds(self) -> int:
        return self._total_microseconds

    def lies_between(self, starting, ending) -> bool:
        return bool(
            self.total_microseconds() in range(
                starting.total_microseconds(), ending.total_microseconds()
        ))


if __name__ == '__main__':

    one_hour = JustTime(hour=1, minute=0, second=0, microsecond=66_000_000)
    one_day = JustTime(23, 59, 59)
    # print(one_hour.strftime('%I:%M %p'))
    # print(one_day.strftime('%I:%M %p'))
    print(one_hour.hour)
    print(one_hour.minute)
    print(one_hour.second)
    print(one_hour.microsecond)
    print(one_hour.total_seconds())

    # print(one_hour + one_day)
    # print(one_hour - one_day)
    # print(one_day - one_hour)
    # d1 = timedelta(hours=3, minutes=5)
    # print(one_hour + d1)
    # print(one_hour - d1)
    t3 = JustTime(0,0,2,4_000_100)
    t4 = JustTime(0,0,2,1_001_300)
    # print(t3._total_microseconds)
    print(t3 + t4)
    print(t3 - t4)
    print(t4 - t3)
    print(t4 <= t3)
    # print(t3.total_seconds())
    # print(t3.hour)
