"""通用解析工具（无重依赖，供 validate / field_extractor 共用）。"""
import re


def parse_amount(s):
    """从字符串中提取金额数字，去掉 ¥ , 等符号。返回 float 或 None。"""
    if not s:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).replace(",", "").replace("，", "").replace("¥", "").replace("￥").strip()
    m = re.search(r"(\d+(?:\.\d+)?)", s)
    return float(m.group(1)) if m else None


def parse_date(s):
    """支持 2026-07-08 / 2026年07月08日 / 20260708，返回 YYYY-MM-DD 或 None。"""
    if not s:
        return None
    m = re.search(r"(\d{4})\D*(\d{1,2})\D*(\d{1,2})", str(s))
    if not m:
        return None
    y, mo, d = m.groups()
    return f"{int(y):04d}-{int(mo):02d}-{int(d):02d}"


def month_of(date_str):
    d = parse_date(date_str)
    return d[:7] if d else "未知月份"
