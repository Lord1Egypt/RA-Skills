"""
选股系统统一数据获取
三源优先级: tushare → baostock → efinance
"""

import time
import efinance as ef
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ts_data import get_quote_history_ts


def fetch_stock_data(code: str) -> pd.DataFrame | None:
    """
    获取单只股票日线数据，优先 tushare，成功则直接返回
    失败则回退 baostock → efinance
    返回: DataFrame（efinance 兼容格式的列名）
    """
    # 方法1: tushare
    try:
        df = get_quote_history_ts(code, start_date='20200101', end_date='20500101')
        if df is not None and len(df) >= 60:
            return df
    except Exception:
        pass

    # 方法2: baostock
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from bs_data import get_quote_history_bs
        df, _ = get_quote_history_bs(code, start_date='2020-01-01', end_date='2050-01-01')
        if df is not None and len(df) >= 60:
            return df
    except Exception:
        pass

    # 方法3: efinance
    try:
        df = ef.stock.get_quote_history(code, beg='20220101', end='20500101', klt=101, fqt=1)
        if df is not None and len(df) >= 60:
            return df
    except Exception:
        pass

    return None
