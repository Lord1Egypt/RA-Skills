#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass
from korean_lunar_calendar import KoreanLunarCalendar

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
KOR_TO_HAN = {
    "갑":"甲","을":"乙","병":"丙","정":"丁","무":"戊",
    "기":"己","경":"庚","신":"辛","임":"壬","계":"癸",
    "자":"子","축":"丑","인":"寅","묘":"卯","진":"辰","사":"巳",
    "오":"午","미":"未","신":"申","유":"酉","술":"戌","해":"亥",
}
DAY_STEM_TO_ZI_START = {
    "甲": "甲", "己": "甲",
    "乙": "丙", "庚": "丙",
    "丙": "戊", "辛": "戊",
    "丁": "庚", "壬": "庚",
    "戊": "壬", "癸": "壬",
}

@dataclass
class Pillar:
    stem: str
    branch: str


def hour_to_branch(hour: int, minute: int) -> str:
    hm = hour * 60 + minute
    if hm >= 23 * 60 or hm < 1 * 60:
        return "子"
    idx = ((hm - 60) // 120) + 1
    return BRANCHES[idx]


def hour_pillar(day_stem: str, hour: int, minute: int) -> Pillar:
    branch = hour_to_branch(hour, minute)
    zi_stem = DAY_STEM_TO_ZI_START[day_stem]
    stem_idx = STEMS.index(zi_stem)
    branch_idx = BRANCHES.index(branch)
    stem = STEMS[(stem_idx + branch_idx) % 10]
    return Pillar(stem, branch)


def parse_gapja_chinese(s: str):
    # Example: 丙午年 辛卯月 壬寅日
    parts = s.strip().split()
    if len(parts) != 3:
        raise ValueError(f"Unexpected gapja format: {s}")
    year = parts[0][:2]
    month = parts[1][:2]
    day = parts[2][:2]
    return Pillar(year[0], year[1]), Pillar(month[0], month[1]), Pillar(day[0], day[1])


def build_calendar(args):
    cal = KoreanLunarCalendar()
    if args.calendar == "solar":
        ok = cal.setSolarDate(args.year, args.month, args.day)
    else:
        ok = cal.setLunarDate(args.year, args.month, args.day, args.leap_month)
    if not ok:
        raise ValueError("Invalid date for KoreanLunarCalendar")
    return cal


def main():
    p = argparse.ArgumentParser(description="Calculate Four Pillars from solar/lunar date and time")
    p.add_argument("--calendar", choices=["solar", "lunar"], default="solar")
    p.add_argument("--year", type=int, required=True)
    p.add_argument("--month", type=int, required=True)
    p.add_argument("--day", type=int, required=True)
    p.add_argument("--time", required=True, help="HH:MM 24-hour")
    p.add_argument("--leap-month", action="store_true", help="Use for lunar leap month input")
    p.add_argument("--zi-hour-mode", choices=["civil", "split"], default="civil", help="split mode marks 23:00-23:59 as next-day zi hour candidate")
    args = p.parse_args()

    hour, minute = map(int, args.time.split(":"))
    cal = build_calendar(args)
    year_p, month_p, day_p = parse_gapja_chinese(cal.getChineseGapJaString())
    hour_p = hour_pillar(day_p.stem, hour, minute)

    result = {
        "input": {
            "calendar": args.calendar,
            "year": args.year,
            "month": args.month,
            "day": args.day,
            "time": args.time,
            "leap_month": args.leap_month,
            "zi_hour_mode": args.zi_hour_mode,
        },
        "solar_date": cal.SolarIsoFormat(),
        "lunar_date": cal.LunarIsoFormat(),
        "pillars": {
            "year": {"stem": year_p.stem, "branch": year_p.branch},
            "month": {"stem": month_p.stem, "branch": month_p.branch},
            "day": {"stem": day_p.stem, "branch": day_p.branch},
            "hour": {"stem": hour_p.stem, "branch": hour_p.branch},
        },
        "korean_gapja": f"{year_p.stem}{year_p.branch}년 {month_p.stem}{month_p.branch}월 {day_p.stem}{day_p.branch}일 {hour_p.stem}{hour_p.branch}시",
        "notes": [
            "Year/month/day pillars come from korean_lunar_calendar.",
            "Hour pillar is derived from day stem + time branch rule.",
            "23:00-00:59 zi-hour handling varies by school; review manually for strict use.",
        ],
    }

    if args.zi_hour_mode == "split" and hour == 23:
        result["notes"].append("split zi-hour mode: 23:00-23:59 may be treated as next-day start in some schools.")

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
