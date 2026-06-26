#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
truetime-cn  —  中文优先、跨平台的时间精确处理引擎

设计原则（Linus 式好品味）：
- 单元表统一固定单位与日历单位，无 if-else 分支堆叠
- DST 检测：一条 UTC 往返规则覆盖"模糊"和"不存在"两种情况
- 中国节假日：调休表 > 放假表 > 周末规则，三段查表，零分支

灵感来自 cccat6/truetime（OpenClaw），独立实现，未复制其 .mjs 代码。
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, available_timezones

# 优先用 vendor 内的 cnlunar（消除供应链风险，零特殊分支）
_VENDOR_DIR = str(Path(__file__).resolve().parent.parent / "vendor")
if _VENDOR_DIR not in sys.path:
    sys.path.insert(0, _VENDOR_DIR)
import cnlunar  # vendored 副本，参见 vendor/README.md


# ───────────────────────── 单元表 ─────────────────────────
# 表驱动：每个单位要么是固定毫秒（fixed_ms），要么是日历月（cal_months）
# 所有日历单位（month/year/decade/century）都规约为"月"，不写四套逻辑
UNIT_TABLE = [
    # (匹配关键字按长度倒序，正则会贪婪匹配; aliases, fixed_ms, cal_months)
    (("milliseconds", "millisecond", "msecs", "msec", "ms"), 1, 0),
    (("seconds", "second", "sec", "s"),                     1_000, 0),
    (("minutes", "minute", "min", "m"),                     60_000, 0),
    (("hours", "hour", "hr", "h"),                          3_600_000, 0),
    (("days", "day", "d"),                                  86_400_000, 0),
    (("weeks", "week", "w"),                                604_800_000, 0),
    (("months", "month", "mon", "mo"),                      0, 1),
    (("years", "year", "yr", "y"),                          0, 12),
    (("decades", "decade"),                                 0, 120),
    (("centuries", "century"),                              0, 1200),
]

# 展开成 alias→(fixed_ms, cal_months)，aliases 按长度倒序保证最长匹配
_ALIAS_MAP = {}
for aliases, ms, mo in UNIT_TABLE:
    for a in aliases:
        _ALIAS_MAP[a] = (ms, mo)
_ALIAS_PATTERN = "|".join(sorted(_ALIAS_MAP.keys(), key=len, reverse=True))

# 一个 token：数字（含小数）+ 单位
_TOKEN_RE = re.compile(rf"(\d+(?:\.\d+)?)\s*({_ALIAS_PATTERN})", re.IGNORECASE)


def parse_duration(expr: str) -> list[tuple[float, int, int]]:
    """
    "1h30m" → [(1.0, 3_600_000, 0), (30.0, 60_000, 0)]
    "1.5month" → [(1.5, 0, 1)]
    返回 (value, fixed_ms_per_unit, cal_months_per_unit) 列表。
    """
    expr = expr.strip().replace(",", ".").replace(" ", "")
    if not expr:
        raise ValueError(f"空 duration 表达式")
    tokens = _TOKEN_RE.findall(expr)
    if not tokens:
        raise ValueError(f"无法解析 duration: {expr!r}（合法单位见 --help）")
    consumed = "".join(num + unit for num, unit in tokens)
    if consumed.lower() != expr.lower():
        raise ValueError(f"duration 含未识别字符: {expr!r}（已解析: {consumed}）")
    out = []
    for num, unit in tokens:
        ms, mo = _ALIAS_MAP[unit.lower()]
        out.append((float(num), ms, mo))
    return out


# ───────────────────────── 日历运算 ─────────────────────────
def _last_day_of_month(year: int, month: int) -> int:
    """返回 year-month 月的最后一天（处理闰年）"""
    if month == 12:
        next_first = datetime(year + 1, 1, 1)
    else:
        next_first = datetime(year, month + 1, 1)
    return (next_first - timedelta(days=1)).day


def add_calendar_months(dt: datetime, months: float) -> datetime:
    """
    日历加月（含小数）。
    整数部分按月历移位（1/31 + 1mo = 2/28/29，月末钳位）。
    小数部分按"目标月实际天数"换算成毫秒，避免 30/31 天月份的偏差。
    """
    int_part = int(months // 1) if months >= 0 else -int(-months // 1)
    frac_part = months - int_part

    total_months = (dt.month - 1) + int_part
    new_year = dt.year + total_months // 12
    new_month = total_months % 12 + 1
    last_day = _last_day_of_month(new_year, new_month)
    new_day = min(dt.day, last_day)

    shifted = dt.replace(year=new_year, month=new_month, day=new_day)

    if frac_part:
        days_in_target_month = _last_day_of_month(shifted.year, shifted.month)
        frac_ms = int(frac_part * days_in_target_month * 86_400_000)
        shifted += timedelta(milliseconds=frac_ms)
    return shifted


def apply_duration(dt: datetime, parsed: list[tuple[float, int, int]],
                   calendar_tz: ZoneInfo) -> datetime:
    """
    在 dt 上应用一组 duration token。日历单位用 calendar_tz 做月历移位（避免 UTC 跨月偏差）。
    """
    fixed_ms = 0.0
    cal_months = 0.0
    for value, ms_per, mo_per in parsed:
        fixed_ms += value * ms_per
        cal_months += value * mo_per

    if cal_months:
        local = dt.astimezone(calendar_tz)
        local = add_calendar_months(local, cal_months)
        dt = local.astimezone(dt.tzinfo)
    if fixed_ms:
        dt += timedelta(milliseconds=fixed_ms)
    return dt


# ───────────────────────── DST ─────────────────────────
def check_dst_validity(naive: datetime, tz: ZoneInfo) -> str | None:
    """
    返回 None 表示 OK。否则返回错误描述。
    判断顺序很重要：
      1) UTC 往返后不等 → 不存在 (spring-forward gap)
      2) 否则 off0 != off1 → 模糊 (fall-back overlap)
      3) 否则正常
    """
    aware0 = naive.replace(tzinfo=tz, fold=0)
    aware1 = naive.replace(tzinfo=tz, fold=1)
    back0 = aware0.astimezone(timezone.utc).astimezone(tz).replace(tzinfo=None)
    if back0 != naive:
        return f"DST 不存在时间: {naive.isoformat()} 在 {tz} 因春令时跳过；请改用有效本地时间"
    off0, off1 = aware0.utcoffset(), aware1.utcoffset()
    if off0 != off1:
        return f"DST 模糊时间: {naive.isoformat()} 在 {tz} 存在两次 (offsets {off0} / {off1})；请用 --target 'YYYY-MM-DDTHH:MM:SS±HH:MM' 显式指定"
    return None


# ───────────────────────── 农历 ─────────────────────────


def lunar_info(local_dt: datetime) -> dict:
    """生成 '丙午年三月廿二' 等中文字段。cnlunar 已 vendor，必然可用。"""
    naive = local_dt.replace(tzinfo=None)
    a = cnlunar.Lunar(naive, godType="8char")
    month_clean = re.sub(r"[大小]$", "", a.lunarMonthCn)  # 去掉"大/小"后缀
    leap = "闰" if a.isLunarLeapMonth else ""
    display = f"{a.year8Char}年{leap}{month_clean}{a.lunarDayCn}"
    return {
        "display": display,
        "year_ganzhi": a.year8Char,
        "month": f"{leap}{month_clean}",
        "day": a.lunarDayCn,
        "zodiac": a.chineseYearZodiac,
        "is_leap_month": bool(a.isLunarLeapMonth),
        "next_solar_term": a.nextSolarTerm,
        "next_solar_term_date": f"{a.nextSolarTermYear}-{a.nextSolarTermDate[0]:02d}-{a.nextSolarTermDate[1]:02d}",
    }


# ───────────────────────── 中国节假日 ─────────────────────────
_HOLIDAY_DATA: dict | None = None


def load_holidays() -> dict:
    """懒加载节假日 JSON。"""
    global _HOLIDAY_DATA
    if _HOLIDAY_DATA is not None:
        return _HOLIDAY_DATA
    base = Path(__file__).resolve().parent.parent
    paths = [base / "data" / "cn_holidays.json", Path("/mnt/skills/user/truetime-cn/data/cn_holidays.json")]
    for p in paths:
        if p.exists():
            _HOLIDAY_DATA = json.loads(p.read_text(encoding="utf-8"))
            return _HOLIDAY_DATA
    _HOLIDAY_DATA = {}
    return _HOLIDAY_DATA


def cn_holiday_info(local_dt: datetime) -> dict:
    """
    查表三段式：
    1) 调休补班日（周末上班）→ 必为工作日，holiday_name=None
    2) 放假日 → holiday_name=节日名，is_workday=False
    3) 否则按周一到周五判定
    返回 {holiday_name, is_workday, source, year_data_available}
    """
    data = load_holidays()
    year_str = str(local_dt.year)
    iso = local_dt.strftime("%Y-%m-%d")
    if year_str not in data:
        # 没数据时降级：仅按周末判断
        return {"holiday_name": None, "is_workday": local_dt.weekday() < 5,
                "source": "fallback_weekend_only", "year_data_available": False}
    year = data[year_str]
    if iso in year.get("workdays", []):
        return {"holiday_name": None, "is_workday": True,
                "source": "compensatory_workday", "year_data_available": True}
    for name, dates in year.get("holidays", {}).items():
        if iso in dates:
            return {"holiday_name": name, "is_workday": False,
                    "source": "statutory_holiday", "year_data_available": True}
    return {"holiday_name": None, "is_workday": local_dt.weekday() < 5,
            "source": "weekend_rule", "year_data_available": True}


# ───────────────────────── 人类可读 delta ─────────────────────────
def humanize_delta_zh(total_seconds: float) -> str:
    """大小自适应的中文 delta。如 '约 4 个月零 22 天'、'1 小时 30 分钟'。"""
    sign = "" if total_seconds >= 0 else "-"
    s = abs(total_seconds)
    if s < 60:
        return f"{sign}{s:.1f} 秒"
    if s < 3600:
        m, sec = divmod(s, 60)
        return f"{sign}{int(m)} 分 {int(sec)} 秒"
    if s < 86400:
        h, rem = divmod(s, 3600)
        m, _ = divmod(rem, 60)
        return f"{sign}{int(h)} 小时 {int(m)} 分钟"
    if s < 86400 * 30:
        d, rem = divmod(s, 86400)
        h, _ = divmod(rem, 3600)
        return f"{sign}{int(d)} 天 {int(h)} 小时"
    if s < 86400 * 365:
        # 用 30.44 天近似月
        months = s / (86400 * 30.44)
        d_remainder = (s - int(months) * 86400 * 30.44) / 86400
        return f"约 {sign}{int(months)} 个月零 {int(d_remainder)} 天"
    years = s / (86400 * 365.25)
    return f"约 {sign}{years:.1f} 年"


# ───────────────────────── 主流程 ─────────────────────────
def build_output(now_utc: datetime, target_utc: datetime,
                 user_tz: ZoneInfo, server_tz: ZoneInfo, calendar_tz: ZoneInfo,
                 lunar_tz: ZoneInfo, time_source: str, assumptions: list[str]) -> dict:
    target_user = target_utc.astimezone(user_tz)
    target_server = target_utc.astimezone(server_tz)
    now_user = now_utc.astimezone(user_tz)
    delta_ms = int((target_utc - now_utc).total_seconds() * 1000)

    now_lunar_local = now_utc.astimezone(lunar_tz)
    target_lunar_local = target_utc.astimezone(lunar_tz)
    now_holiday = cn_holiday_info(now_user)
    target_holiday = cn_holiday_info(target_user)

    return {
        "now_utc": now_utc.isoformat().replace("+00:00", "Z"),
        "now_user_tz": now_user.isoformat(),
        "now_lunar": lunar_info(now_lunar_local),
        "now_zh_holiday": now_holiday["holiday_name"],
        "now_is_workday": now_holiday["is_workday"],
        "target_utc": target_utc.isoformat().replace("+00:00", "Z"),
        "target_user_tz": target_user.isoformat(),
        "target_server_tz": target_server.isoformat(),
        "target_lunar": lunar_info(target_lunar_local),
        "target_zh_holiday": target_holiday["holiday_name"],
        "target_is_workday": target_holiday["is_workday"],
        "target_holiday_source": target_holiday["source"],
        "delta_milliseconds": delta_ms,
        "delta_seconds": delta_ms / 1000,
        "delta_human_zh": humanize_delta_zh(delta_ms / 1000),
        "user_tz": str(user_tz),
        "server_tz": str(server_tz),
        "calendar_tz": str(calendar_tz),
        "lunar_tz": str(lunar_tz),
        "time_source": time_source,
        "holiday_data_year_available": target_holiday["year_data_available"],
        "assumptions": assumptions,
    }


def parse_target(target_str: str, target_tz_str: str | None) -> tuple[datetime, list[str]]:
    """
    解析 ISO 8601 target 字符串。
    带 Z 或 ±offset 直接用；否则需要 target_tz；否则 fallback UTC 并给 assumption。
    """
    assumptions = []
    s = target_str.strip()
    # 带 Z
    if s.endswith("Z"):
        return datetime.fromisoformat(s.replace("Z", "+00:00")), assumptions
    # 带 ±offset
    if re.search(r"[+-]\d\d:\d\d$", s):
        return datetime.fromisoformat(s), assumptions
    # naive
    naive = datetime.fromisoformat(s)
    if target_tz_str:
        tz = ZoneInfo(target_tz_str)
        err = check_dst_validity(naive, tz)
        if err:
            raise ValueError(err)
        return naive.replace(tzinfo=tz).astimezone(timezone.utc), assumptions
    assumptions.append("target 无时区信息且未提供 --target-tz；按 UTC 解释")
    return naive.replace(tzinfo=timezone.utc), assumptions


def get_now(time_source: str) -> datetime:
    """目前只支持 server。NTP 留作 v2。"""
    if time_source != "server":
        raise NotImplementedError(f"暂不支持 time-source={time_source}（v1 仅 server）")
    return datetime.now(timezone.utc)


def main():
    p = argparse.ArgumentParser(
        description="truetime-cn — 中文时区与时间精确处理（Claude.ai 沙箱原生）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python truetime_cn.py                           # 当前时间（默认 Asia/Shanghai）\n"
               "  python truetime_cn.py --plus 1.5month\n"
               "  python truetime_cn.py --plus 1h30m --user-tz America/New_York\n"
               "  python truetime_cn.py --target 2026-09-25T09:00:00 --target-tz Asia/Shanghai --user-tz America/Los_Angeles\n"
               "  python truetime_cn.py --list-timezones | head -20")
    p.add_argument("--plus", help="相对偏移，如 '1.5month'、'1h30m'、'250ms'")
    p.add_argument("--target", help="ISO8601 绝对时间，如 '2026-09-25T09:00:00'（可带 Z 或 ±offset）")
    p.add_argument("--target-tz", help="--target 的时区（IANA），如 'Asia/Shanghai'")
    p.add_argument("--user-tz", default="Asia/Shanghai", help="用户时区，默认 Asia/Shanghai")
    p.add_argument("--calendar-tz", help="日历运算时区（默认与 user-tz 相同）")
    p.add_argument("--lunar-tz", default="Asia/Shanghai", help="农历计算时区，默认 Asia/Shanghai")
    p.add_argument("--time-source", default="server", choices=["server"], help="时间源（v1 仅 server）")
    p.add_argument("--list-timezones", action="store_true", help="列出所有 IANA 时区后退出")
    p.add_argument("--human", action="store_true", help="附加中文人类可读摘要")
    args = p.parse_args()

    if args.list_timezones:
        for tz in sorted(available_timezones()):
            print(tz)
        return

    if args.plus and args.target:
        sys.exit("错误: --plus 与 --target 互斥")

    user_tz = ZoneInfo(args.user_tz)
    # server_tz：尝试从系统读，失败回退 UTC
    try:
        local_tz = datetime.now().astimezone().tzinfo
        server_tz = local_tz if isinstance(local_tz, ZoneInfo) else ZoneInfo("UTC")
    except Exception:
        server_tz = ZoneInfo("UTC")
    calendar_tz = ZoneInfo(args.calendar_tz) if args.calendar_tz else user_tz
    lunar_tz = ZoneInfo(args.lunar_tz)

    assumptions = []
    now_utc = get_now(args.time_source)

    if args.plus:
        parsed = parse_duration(args.plus)
        target_utc = apply_duration(now_utc, parsed, calendar_tz)
    elif args.target:
        target_utc, assump2 = parse_target(args.target, args.target_tz)
        assumptions.extend(assump2)
    else:
        target_utc = now_utc

    out = build_output(now_utc, target_utc, user_tz, server_tz, calendar_tz, lunar_tz,
                       args.time_source, assumptions)
    print(json.dumps(out, ensure_ascii=False, indent=2))

    if args.human:
        print("\n--- 中文摘要 ---")
        print(f"现在: {out['now_user_tz']} ({out['now_lunar']['display']})")
        if out["now_zh_holiday"]:
            print(f"今天是: {out['now_zh_holiday']} (节假日)")
        elif not out["now_is_workday"]:
            print(f"今天: 周末/休息日")
        else:
            print(f"今天: 工作日")
        if target_utc != now_utc:
            print(f"目标: {out['target_user_tz']} ({out['target_lunar']['display']})")
            print(f"距离: {out['delta_human_zh']}")
            if out["target_zh_holiday"]:
                print(f"目标日: {out['target_zh_holiday']} (节假日)")
            elif not out["target_is_workday"]:
                print(f"目标日: 非工作日")
            else:
                print(f"目标日: 工作日")
        if assumptions:
            print(f"假设: {'; '.join(assumptions)}")


if __name__ == "__main__":
    main()
