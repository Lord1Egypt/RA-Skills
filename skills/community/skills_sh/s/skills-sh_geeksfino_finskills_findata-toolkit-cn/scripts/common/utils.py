"""
金融数据工具包共享工具
所有脚本通用函数。
"""
import json
import sys
import time
import functools
from datetime import datetime, date
from typing import Any


# ---------------------------------------------------------------------------
# 输出助手
# ---------------------------------------------------------------------------

class JSONEncoder(json.JSONEncoder):
    """自定义编码器，处理日期、numpy 类型等。"""

    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        try:
            import numpy as np
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, np.bool_):
                return bool(obj)
        except ImportError:
            pass
        try:
            import pandas as pd
            if isinstance(obj, pd.Timestamp):
                return obj.isoformat()
            if pd.isna(obj):
                return None
        except ImportError:
            pass
        return super().default(obj)


def output_json(data: Any, pretty: bool = True) -> str:
    """将数据序列化为 JSON 并输出到标准输出。"""
    text = json.dumps(data, cls=JSONEncoder, indent=2 if pretty else None,
                      ensure_ascii=False)
    print(text)
    return text


def output_table(headers: list[str], rows: list[list], title: str = ""):
    """输出格式化文本表格。"""
    try:
        from tabulate import tabulate
        if title:
            print(f"\n{'='*60}")
            print(f"  {title}")
            print(f"{'='*60}")
        print(tabulate(rows, headers=headers, tablefmt="pipe",
                        floatfmt=".2f"))
    except ImportError:
        if title:
            print(f"\n--- {title} ---")
        print(" | ".join(headers))
        print("-" * (len(" | ".join(headers))))
        for row in rows:
            print(" | ".join(str(c) for c in row))


def error_exit(message: str, code: int = 1):
    """输出错误信息并退出。"""
    print(json.dumps({"error": message}), file=sys.stderr)
    sys.exit(code)


# ---------------------------------------------------------------------------
# 速率限制
# ---------------------------------------------------------------------------

def rate_limit(calls_per_second: float = 2.0):
    """限速装饰器。"""
    min_interval = 1.0 / calls_per_second

    def decorator(func):
        last_call = [0.0]

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)

        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# 安全数值助手
# ---------------------------------------------------------------------------

def safe_div(a, b, default=None):
    """安全除法，b 为 0 或任一值为 None 时返回 default。"""
    if a is None or b is None:
        return default
    try:
        if float(b) == 0:
            return default
        return float(a) / float(b)
    except (ValueError, TypeError):
        return default


def safe_float(val, default=None):
    """安全转换为 float，失败时返回 default。处理 %、亿、万 等后缀。

    Note: '%' is stripped but the value is NOT divided by 100 — e.g. "15.3%"
    returns 15.3.  Callers that need a fraction should divide by 100 themselves.
    """
    if val is None or val is False:  # AKShare may return False for missing data
        return default
    import math
    if isinstance(val, (int, float)):
        if math.isnan(val) or math.isinf(val):
            return default
        return float(val)
    try:
        s = str(val).strip()
        if not s:
            return default
        multiplier = 1.0
        if s.endswith('%'):
            s = s[:-1]
        elif s.endswith('亿'):
            s = s[:-1]
            multiplier = 1e8
        elif s.endswith('万'):
            s = s[:-1]
            multiplier = 1e4
        result = float(s) * multiplier
        if math.isnan(result) or math.isinf(result):
            return default
        return result
    except (ValueError, TypeError):
        return default


def pct(val, decimals=2):
    """将小数格式化为百分比字符串。"""
    if val is None:
        return "N/A"
    return f"{val * 100:.{decimals}f}%"
