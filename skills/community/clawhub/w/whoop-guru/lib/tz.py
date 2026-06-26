"""
Timezone Utilities - 统一使用北京时间 (UTC+8)

所有时间操作统一通过本模块，避免时区混乱。
"""

from datetime import datetime, timedelta, date


# ============================================================
# 北京时区常量
# ============================================================

BEIJING_OFFSET_HOURS = 8


# ============================================================
# 核心时间函数
# ============================================================

def now() -> datetime:
    """当前北京时间"""
    return datetime.utcnow() + timedelta(hours=BEIJING_OFFSET_HOURS)


def today() -> date:
    """当前北京日期"""
    return now().date()


def today_str() -> str:
    """当前北京日期字符串 YYYY-MM-DD"""
    return today().strftime('%Y-%m-%d')


def yesterday_str() -> str:
    """昨天北京日期字符串 YYYY-MM-DD"""
    return (today() - timedelta(days=1)).strftime('%Y-%m-%d')


def cutoff_datetime(days_ago: int) -> datetime:
    """N天前此刻的北京时间"""
    return now() - timedelta(days=days_ago)


def cutoff_str(days_ago: int) -> str:
    """N天前此刻的北京时间字符串 YYYY-MM-DD"""
    return cutoff_datetime(days_ago).strftime('%Y-%m-%d')


def datetime_to_bj(dt: datetime) -> datetime:
    """UTC datetime 转北京时间"""
    return dt + timedelta(hours=BEIJING_OFFSET_HOURS)


def is_bj_today(utc_timestamp: str) -> bool:
    """
    判断一个 UTC ISO 时间戳是否属于今日北京时间。

    北京时间今日 = UTC [今天08:00 ~ 明天07:59]
    （因为 WHOOP 跑步数据通常在北京 00:00-08:00 同步，对应 UTC 前一天16:00-00:00）
    """
    try:
        dt = datetime.fromisoformat(utc_timestamp.replace('Z', '+00:00'))
        dt_bj = datetime_to_bj(dt)
        today_bj = today()
        window_start = datetime(today_bj.year, today_bj.month, today_bj.day, 0, 0, 0)
        window_end = datetime(today_bj.year, today_bj.month, today_bj.day, 23, 59, 59)
        return window_start <= dt_bj <= window_end
    except Exception:
        return False


def format_bj(iso_str: str, fmt: str = '%H:%M') -> str:
    """将 UTC ISO 时间字符串格式化为北京时间的指定格式"""
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        return datetime_to_bj(dt).strftime(fmt)
    except Exception:
        return ''
