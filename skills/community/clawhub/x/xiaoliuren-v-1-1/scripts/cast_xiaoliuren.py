#!/usr/bin/env python3
"""Deterministic Xiao Liu Ren chart calculator."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date, datetime, timezone, timedelta


PALACE_BY_VALUE = {
    0: "空亡",
    1: "大安",
    2: "留连",
    3: "速喜",
    4: "赤口",
    5: "小吉",
}

PALACE_ORDER = ["大安", "留连", "速喜", "赤口", "小吉", "空亡"]
ACTIVE_GODS = ["青龙", "朱雀", "勾陈", "白虎", "玄武", "腾蛇"]

PALACES = {
    "大安": {"value": 1, "element": "木", "luck": "大吉", "dead_god": "青龙木"},
    "留连": {"value": 2, "element": "土", "luck": "中吉", "dead_god": "四方土"},
    "速喜": {"value": 3, "element": "火", "luck": "吉", "dead_god": "朱雀火"},
    "赤口": {"value": 4, "element": "金", "luck": "凶", "dead_god": "白虎金"},
    "小吉": {"value": 5, "element": "水", "luck": "小吉", "dead_god": "玄武水"},
    "空亡": {"value": 0, "element": "土", "luck": "大凶", "dead_god": "勾陈土"},
}

HOURS = {
    "子时": {"range": "23:00-01:00", "element": "水", "number": 1, "active_start": "大安"},
    "丑时": {"range": "01:00-03:00", "element": "土", "number": 2, "active_start": "留连"},
    "寅时": {"range": "03:00-05:00", "element": "木", "number": 3, "active_start": "速喜"},
    "卯时": {"range": "05:00-07:00", "element": "木", "number": 4, "active_start": "赤口"},
    "辰时": {"range": "07:00-09:00", "element": "土", "number": 5, "active_start": "小吉"},
    "巳时": {"range": "09:00-11:00", "element": "火", "number": 6, "active_start": "空亡"},
    "午时": {"range": "11:00-13:00", "element": "火", "number": 7, "active_start": "大安"},
    "未时": {"range": "13:00-15:00", "element": "土", "number": 8, "active_start": "留连"},
    "申时": {"range": "15:00-17:00", "element": "金", "number": 9, "active_start": "速喜"},
    "酉时": {"range": "17:00-19:00", "element": "金", "number": 10, "active_start": "赤口"},
    "戌时": {"range": "19:00-21:00", "element": "土", "number": 11, "active_start": "小吉"},
    "亥时": {"range": "21:00-23:00", "element": "水", "number": 12, "active_start": "空亡"},
}

GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

LUNAR_INFO = [
    0x04BD8, 0x04AE0, 0x0A570, 0x054D5, 0x0D260, 0x0D950, 0x16554, 0x056A0, 0x09AD0, 0x055D2,
    0x04AE0, 0x0A5B6, 0x0A4D0, 0x0D250, 0x1D255, 0x0B540, 0x0D6A0, 0x0ADA2, 0x095B0, 0x14977,
    0x04970, 0x0A4B0, 0x0B4B5, 0x06A50, 0x06D40, 0x1AB54, 0x02B60, 0x09570, 0x052F2, 0x04970,
    0x06566, 0x0D4A0, 0x0EA50, 0x06E95, 0x05AD0, 0x02B60, 0x186E3, 0x092E0, 0x1C8D7, 0x0C950,
    0x0D4A0, 0x1D8A6, 0x0B550, 0x056A0, 0x1A5B4, 0x025D0, 0x092D0, 0x0D2B2, 0x0A950, 0x0B557,
    0x06CA0, 0x0B550, 0x15355, 0x04DA0, 0x0A5B0, 0x14573, 0x052B0, 0x0A9A8, 0x0E950, 0x06AA0,
    0x0AEA6, 0x0AB50, 0x04B60, 0x0AAE4, 0x0A570, 0x05260, 0x0F263, 0x0D950, 0x05B57, 0x056A0,
    0x096D0, 0x04DD5, 0x04AD0, 0x0A4D0, 0x0D4D4, 0x0D250, 0x0D558, 0x0B540, 0x0B6A0, 0x195A6,
    0x095B0, 0x049B0, 0x0A974, 0x0A4B0, 0x0B27A, 0x06A50, 0x06D40, 0x0AF46, 0x0AB60, 0x09570,
    0x04AF5, 0x04970, 0x064B0, 0x074A3, 0x0EA50, 0x06B58, 0x055C0, 0x0AB60, 0x096D5, 0x092E0,
    0x0C960, 0x0D954, 0x0D4A0, 0x0DA50, 0x07552, 0x056A0, 0x0ABB7, 0x025D0, 0x092D0, 0x0CAB5,
    0x0A950, 0x0B4A0, 0x0BAA4, 0x0AD50, 0x055D9, 0x04BA0, 0x0A5B0, 0x15176, 0x052B0, 0x0A930,
    0x07954, 0x06AA0, 0x0AD50, 0x05B52, 0x04B60, 0x0A6E6, 0x0A4E0, 0x0D260, 0x0EA65, 0x0D530,
    0x05AA0, 0x076A3, 0x096D0, 0x04BD7, 0x04AD0, 0x0A4D0, 0x1D0B6, 0x0D250, 0x0D520, 0x0DD45,
    0x0B5A0, 0x056D0, 0x055B2, 0x049B0, 0x0A577, 0x0A4B0, 0x0AA50, 0x1B255, 0x06D20, 0x0ADA0,
]


@dataclass
class Cast:
    method: str
    input: str
    heaven: str
    earth: str
    human: str
    hour: str
    process: str
    question: str = ""


def normalize_num(num: int) -> int:
    if num < 0:
        raise ValueError("numbers must be non-negative")
    return 10 if num == 0 else num


def palace_from_value(value: int) -> str:
    return PALACE_BY_VALUE[value % 6]


def cast_numbers(a: int, b: int, c: int, hour: str, question: str = "", method: str = "数字起卦") -> Cast:
    p1, p2, p3 = normalize_num(a), normalize_num(b), normalize_num(c)
    heaven_value = p1 % 6
    earth_value = (heaven_value + p2 - 1) % 6
    human_value = (earth_value + p3 - 1) % 6
    process = (
        f"{a}->{p1}, {b}->{p2}, {c}->{p3}; "
        f"天宫={p1}%6={heaven_value}->{palace_from_value(heaven_value)}; "
        f"地宫=({heaven_value}+{p2}-1)%6={earth_value}->{palace_from_value(earth_value)}; "
        f"人宫=({earth_value}+{p3}-1)%6={human_value}->{palace_from_value(human_value)}"
    )
    return Cast(
        method=method,
        input=f"{a}, {b}, {c}",
        heaven=palace_from_value(heaven_value),
        earth=palace_from_value(earth_value),
        human=palace_from_value(human_value),
        hour=hour,
        process=process,
        question=question,
    )


def relation(my_element: str, other_element: str) -> str:
    if my_element == other_element:
        return "兄弟"
    if GENERATES[other_element] == my_element:
        return "父母"
    if GENERATES[my_element] == other_element:
        return "子孙"
    if CONTROLS[my_element] == other_element:
        return "妻财"
    if CONTROLS[other_element] == my_element:
        return "官鬼"
    raise ValueError(f"unknown relation: {my_element}, {other_element}")


def active_gods(hour: str) -> dict[str, str]:
    start = HOURS[hour]["active_start"]
    start_index = PALACE_ORDER.index(start)
    return {
        palace: ACTIVE_GODS[(index - start_index + 6) % 6]
        for index, palace in enumerate(PALACE_ORDER)
    }


def current_beijing_hour() -> str:
    now = current_beijing_datetime()
    hour = now.hour
    names = list(HOURS.keys())
    index = 0 if hour == 23 else ((hour + 1) // 2) % 12
    return names[index]


def current_beijing_datetime() -> datetime:
    return datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))


def leap_month(year: int) -> int:
    return LUNAR_INFO[year - 1900] & 0xF


def leap_days(year: int) -> int:
    if leap_month(year):
        return 30 if (LUNAR_INFO[year - 1900] & 0x10000) else 29
    return 0


def month_days(year: int, month: int) -> int:
    return 30 if (LUNAR_INFO[year - 1900] & (0x10000 >> month)) else 29


def lunar_year_days(year: int) -> int:
    total = 348
    mask = 0x8000
    while mask > 0x8:
        if LUNAR_INFO[year - 1900] & mask:
            total += 1
        mask >>= 1
    return total + leap_days(year)


def solar_to_lunar(solar: date) -> tuple[int, int, int, bool]:
    if solar < date(1900, 1, 31) or solar.year > 2049:
        raise ValueError("lunar conversion supports dates from 1900-01-31 through 2049-12-31")

    offset = (solar - date(1900, 1, 31)).days
    year = 1900
    while year < 2050:
        days = lunar_year_days(year)
        if offset < days:
            break
        offset -= days
        year += 1

    leap = leap_month(year)
    is_leap = False
    month = 1
    while month <= 12:
        days = leap_days(year) if is_leap else month_days(year, month)
        if offset < days:
            return year, month, offset + 1, is_leap
        offset -= days
        if leap == month and not is_leap:
            is_leap = True
        else:
            if is_leap:
                is_leap = False
            month += 1

    raise ValueError("failed to convert solar date to lunar date")


def chart(cast: Cast) -> dict:
    hour_data = HOURS[cast.hour]
    active = active_gods(cast.hour)
    human_element = PALACES[cast.human]["element"]
    return {
        "question": cast.question,
        "method": cast.method,
        "input": cast.input,
        "hour": {"name": cast.hour, **hour_data},
        "palaces": {
            "heaven": cast.heaven,
            "earth": cast.earth,
            "human": cast.human,
        },
        "table": {
            "宫位": {
                "天宫": cast.heaven,
                "地宫": cast.earth,
                "人宫": cast.human,
                "时辰": cast.hour,
            },
            "五行": {
                "天宫": PALACES[cast.heaven]["element"],
                "地宫": PALACES[cast.earth]["element"],
                "人宫": human_element,
                "时辰": hour_data["element"],
            },
            "六亲": {
                "天宫": relation(human_element, PALACES[cast.heaven]["element"]),
                "地宫": relation(human_element, PALACES[cast.earth]["element"]),
                "人宫": "我",
                "时辰": relation(human_element, hour_data["element"]),
            },
            "死六神": {
                "天宫": PALACES[cast.heaven]["dead_god"],
                "地宫": PALACES[cast.earth]["dead_god"],
                "人宫": PALACES[cast.human]["dead_god"],
                "时辰": "—",
            },
            "活六神": {
                "天宫": active[cast.heaven],
                "地宫": active[cast.earth],
                "人宫": active[cast.human],
                "时辰": "—",
            },
        },
        "human_luck": PALACES[cast.human]["luck"],
        "process": cast.process,
    }


def valid_hour(value: str | None) -> str:
    hour = value or current_beijing_hour()
    if hour not in HOURS:
        raise argparse.ArgumentTypeError(f"unknown hour: {hour}")
    return hour


def valid_palace(value: str) -> str:
    if value not in PALACES:
        raise argparse.ArgumentTypeError(f"unknown palace: {value}")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate a Xiao Liu Ren chart.")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--hour", default=None, help="Hour branch, e.g. 子时. Defaults to current Beijing hour.")
    common.add_argument("--question", default="", help="Divination question.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("now", parents=[common], help="Cast automatically from current Beijing time.")

    numbers = subparsers.add_parser("numbers", parents=[common], help="Cast with three non-negative integers.")
    numbers.add_argument("num1", type=int)
    numbers.add_argument("num2", type=int)
    numbers.add_argument("num3", type=int)

    time = subparsers.add_parser("time", parents=[common], help="Cast with lunar month, lunar day, hour number.")
    time.add_argument("lunar_month", type=int)
    time.add_argument("lunar_day", type=int)
    time.add_argument("hour_number", type=int)

    direct = subparsers.add_parser("direct", parents=[common], help="Cast with direct palace selection.")
    direct.add_argument("heaven", type=valid_palace)
    direct.add_argument("earth", type=valid_palace)
    direct.add_argument("human", type=valid_palace)

    args = parser.parse_args()

    if args.command == "now":
        now = current_beijing_datetime()
        lunar_year, lunar_month, lunar_day, is_leap = solar_to_lunar(now.date())
        hour = current_beijing_hour()
        hour_number = HOURS[hour]["number"]
        cast = cast_numbers(
            lunar_month,
            lunar_day,
            hour_number,
            hour,
            args.question or "当前整体运势",
            method="时间起卦",
        )
        leap_prefix = "闰" if is_leap else ""
        cast.input = (
            f"北京时间{now.strftime('%Y-%m-%d %H:%M')}; "
            f"农历{lunar_year}年{leap_prefix}{lunar_month}月{lunar_day}日，{hour}，时辰序号{hour_number}"
        )
    elif args.command == "time":
        matched_hour = next((name for name, data in HOURS.items() if data["number"] == args.hour_number), None)
        hour = valid_hour(args.hour or matched_hour)
        cast = cast_numbers(
            args.lunar_month,
            args.lunar_day,
            args.hour_number,
            hour,
            args.question,
            method="时间起卦",
        )
        cast.input = f"农历{args.lunar_month}月{args.lunar_day}日，时辰序号{args.hour_number}"
    elif args.command == "direct":
        hour = valid_hour(args.hour)
        cast = Cast(
            method="宫位直选",
            input=f"{args.heaven}, {args.earth}, {args.human}",
            heaven=args.heaven,
            earth=args.earth,
            human=args.human,
            hour=hour,
            process=f"宫位直选: 天宫={args.heaven}, 地宫={args.earth}, 人宫={args.human}",
            question=args.question,
        )
    else:
        hour = valid_hour(args.hour)
        cast = cast_numbers(args.num1, args.num2, args.num3, hour, args.question)

    print(json.dumps(chart(cast), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
