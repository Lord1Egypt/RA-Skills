"""
时区工具 v3.6.0
- UTC ↔ 北京时间 转换
- Polymarket endDate (UTC ISO 8601) 解析
- 北京时间当天比赛范围查询
"""

from datetime import datetime, timedelta, timezone
from typing import Tuple, Optional


BJT = timezone(timedelta(hours=8))  # 北京时间 (UTC+8)
UTC = timezone.utc


def bjt_to_utc(bjt_str: str) -> datetime:
    """
    北京时间字符串 → UTC datetime
    Args:
        bjt_str: "2026-06-18 03:00" 或 "2026-06-18T03:00:00"
    Returns:
        UTC tz-aware datetime
    """
    s = bjt_str.replace('T', ' ').replace('/', '-')
    if len(s) == 10:  # 仅有日期
        s += ' 00:00:00'
    elif len(s) == 16:  # "2026-06-18 03:00"
        s += ':00'
    dt = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    return dt.replace(tzinfo=BJT).astimezone(UTC)


def utc_to_bjt(utc_str: str) -> datetime:
    """
    UTC ISO 字符串 → 北京时间 datetime
    Args:
        utc_str: "2026-06-17T22:00:00Z" 或 "2026-06-17T22:00:00+00:00"
    Returns:
        北京时间 tz-aware datetime
    """
    s = utc_str.replace('Z', '+00:00')
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(BJT)


def utc_to_bjt_str(utc_str: str, fmt: str = '%m-%d %H:%M') -> str:
    """
    UTC ISO 字符串 → 北京时间显示字符串
    Returns:
        "06-18 06:00" (默认) 或其他格式
    """
    bjt = utc_to_bjt(utc_str)
    return bjt.strftime(fmt) + ' 北京时间'


def bjt_day_range(bjt_date_str: str) -> Tuple[datetime, datetime]:
    """
    给定"北京时间日期字符串"，返回该天的 UTC 起止 datetime
    Args:
        bjt_date_str: "2026-06-18"
    Returns:
        (utc_start, utc_end) - 北京时间当天的 00:00 → 23:59
    Example:
        bjt_day_range("2026-06-18")
        → (datetime(2026,6,17,16,0,tzinfo=UTC), datetime(2026,6,18,15,59,59,tzinfo=UTC))
    """
    bjt_start = datetime.strptime(bjt_date_str, '%Y-%m-%d').replace(tzinfo=BJT)
    bjt_end = bjt_start + timedelta(days=1)
    return bjt_start.astimezone(UTC), bjt_end.astimezone(UTC)


def is_in_bjt_day(utc_str: str, bjt_date_str: str) -> bool:
    """判断 UTC 时间是否在指定北京时间当天"""
    try:
        utc_dt = utc_to_bjt(utc_str)
        target = datetime.strptime(bjt_date_str, '%Y-%m-%d').date()
        return utc_dt.date() == target
    except Exception:
        return False


def now_bjt_str(fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """当前北京时间字符串"""
    return datetime.now(BJT).strftime(fmt)


def now_bjt_date() -> str:
    """当前北京时间日期 (YYYY-MM-DD)"""
    return datetime.now(BJT).strftime('%Y-%m-%d')


# === 转换速查表 ===
# 北京时间 6/18 00:00 = UTC 6/17 16:00
# 北京时间 6/18 03:00 = UTC 6/17 19:00
# 北京时间 6/18 12:00 = UTC 6/18 04:00
# 北京时间 6/18 23:59 = UTC 6/18 15:59
# 北京时间 6/19 00:00 = UTC 6/18 16:00


if __name__ == '__main__':
    # 测试
    print('=== 时区工具测试 ===')
    print('北京 6/18 00:00 →', bjt_to_utc('2026-06-18 00:00'))
    print('UTC 6/17 22:00 →', utc_to_bjt_str('2026-06-17T22:00:00Z'))
    print('北京时间 6/18 当天范围:')
    s, e = bjt_day_range('2026-06-18')
    print('  UTC start:', s)
    print('  UTC end:  ', e)
    print('  对应北京时间:', s.astimezone(BJT), '~', e.astimezone(BJT))
    print('当前北京时间:', now_bjt_str())
