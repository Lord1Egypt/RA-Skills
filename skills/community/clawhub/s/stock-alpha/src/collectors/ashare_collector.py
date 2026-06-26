# -*- coding:utf-8 -*-
"""
AshareCollector - 新浪+腾讯双源实时行情
基于 Ashare: https://github.com/mpquant/Ashare

增强功能：
- 批量实时行情（新浪源直接调用）
- 股票名称自动解析
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from Ashare import get_price
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Optional, Dict
import logging

logger = logging.getLogger(__name__)


class AshareCollector:
    """Ashare 实时行情采集器"""

    MARKET_PREFIX = {
        "000": "sz",  # 深圳主板
        "001": "sz",  # 深圳主板
        "002": "sz",  # 中小板
        "003": "sz",  # 深圳
        "300": "sz",  # 创业板
        "301": "sz",  # 创业板
        "600": "sh",  # 上海主板
        "601": "sh",  # 上海主板
        "603": "sh",  # 上海主板
        "605": "sh",  # 上海主板
        "688": "sh",  # 科创板
        "689": "sh",  # 科创板
    }

    # ──────────────────────────────────────────
    # 代码转换
    # ──────────────────────────────────────────

    def _code_to_ashare(self, code: str) -> str:
        """将 600036 转换为 sh600036，000001 转换为 sz000001"""
        prefix = code[:3]
        market = self.MARKET_PREFIX.get(prefix, "sz")
        return f"{market}{code}"

    def _code_to_sina(self, code: str) -> str:
        """将 600036 转换为 sh600036（新浪格式，不含交易所后缀）"""
        return self._code_to_ashare(code)

    @staticmethod
    def _sina_to_code(sina_code: str) -> str:
        """将 sh600036 转换回 600036"""
        return sina_code.replace("sh", "").replace("sz", "").replace("SH", "").replace("SZ", "")

    @staticmethod
    def _get_market(code: str) -> str:
        """返回 sh 或 sz"""
        prefix = code[:3]
        return "sh" if prefix in ("600", "601", "603", "605", "688", "689") else "sz"

    # ──────────────────────────────────────────
    # 日线历史数据
    # ──────────────────────────────────────────

    def get_daily_hist(self, code: str, start_date: str = None, end_date: str = None, count: int = 30) -> pd.DataFrame:
        """
        获取日线历史数据
        code: 股票代码如 600036
        start_date: YYYYMMDD
        end_date: YYYYMMDD
        count: 获取最近N天
        """
        ashare_code = self._code_to_ashare(code)

        # 转换日期格式 YYYYMMDD -> YYYY-MM-DD
        if end_date and len(end_date) == 8:
            end_date = f"{end_date[:4]}-{end_date[4:6]}-{end_date[6:8]}"

        df = get_price(ashare_code, frequency='1d', count=count)
        if df is None or df.empty:
            return pd.DataFrame()

        # Ashare 返回: index=date, columns=[open,high,low,close,volume]
        df = df.reset_index()
        df.columns = ["trade_date", "open", "high", "low", "close", "volume"]
        df["trade_date"] = pd.to_datetime(df["trade_date"])

        # 过滤日期范围
        if start_date:
            start_dt = pd.to_datetime(f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:8]}")
            df = df[df["trade_date"] >= start_dt]
        if end_date:
            end_dt = pd.to_datetime(end_date)
            df = df[df["trade_date"] <= end_dt]

        return df

    # ──────────────────────────────────────────
    # 单只股票实时行情
    # ──────────────────────────────────────────

    def get_realtime(self, code: str) -> dict:
        """获取单只股票实时行情（最新价）"""
        ashare_code = self._code_to_ashare(code)
        df = get_price(ashare_code, frequency='1d', count=1)
        if df is None or df.empty:
            return {}
        row = df.iloc[-1]
        return {
            "code": code,
            "date": str(df.index[-1].date()),
            "close": float(row["close"]),
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "volume": float(row["volume"]),
        }

    # ──────────────────────────────────────────
    # 批量实时行情（新浪源直接调用）
    # ──────────────────────────────────────────

    def get_realtime_quotes(self, symbols: List[str]) -> pd.DataFrame:
        """
        批量获取实时行情（新浪源）

        直接调用新浪实时行情接口，比 Ashare 逐只查询更高效。

        Args:
            symbols: 股票代码列表，如 ["600036", "000001", "000333"]

        Returns:
            pd.DataFrame with columns:
            [symbol, name, open, close, high, low, volume, amount, change, change_pct]
        """
        if not symbols:
            return pd.DataFrame()

        sina_codes = [self._code_to_sina(c) for c in symbols]
        codes_str = ",".join(sina_codes)

        url = f"http://hq.sinajs.cn/list={codes_str}"

        try:
            import requests
            resp = requests.get(url, timeout=10)
            resp.encoding = "gbk"
            lines = resp.text.strip().split("\n")
        except Exception as e:
            logger.warning(f"[Ashare] get_realtime_quotes request failed: {e}")
            return pd.DataFrame()

        records = []
        for line in lines:
            line = line.strip()
            if not line or "hq_str_" not in line:
                continue
            try:
                # Format: var hq_str_sh600036="招商银行,50.23,..."
                parts = line.split('="')
                if len(parts) < 2:
                    continue
                var_name = parts[0].replace("var hq_str_", "").strip()
                data_str = parts[1].rstrip('";').strip()
                fields = data_str.split(",")

                if len(fields) < 32:
                    continue

                code = self._sina_to_code(var_name)
                name = fields[0]

                # Parse numeric fields
                open_p = self._safe_float(fields[1])
                pre_close = self._safe_float(fields[2])
                close = self._safe_float(fields[3])
                high = self._safe_float(fields[4])
                low = self._safe_float(fields[5])
                buy = self._safe_float(fields[6])
                sell = self._safe_float(fields[7])
                volume = self._safe_float(fields[8])  # 手
                amount = self._safe_float(fields[9])  # 元

                # change and change%
                change = round(close - pre_close, 2) if close and pre_close else 0
                change_pct = round(change / pre_close * 100, 2) if pre_close and pre_close > 0 else 0.0

                records.append({
                    "symbol": code,
                    "name": name,
                    "open": open_p,
                    "pre_close": pre_close,
                    "close": close,
                    "high": high,
                    "low": low,
                    "volume": volume,
                    "amount": amount,
                    "change": change,
                    "change_pct": change_pct,
                })
            except Exception as e:
                logger.warning(f"[Ashare] parse realtime line failed: {e}")
                continue

        if not records:
            return pd.DataFrame()

        df = pd.DataFrame(records)
        return df

    # ──────────────────────────────────────────
    # 批量获取股票名称
    # ──────────────────────────────────────────

    def get_stock_names(self, symbols: Optional[List[str]] = None) -> Dict[str, str]:
        """
        批量获取股票名称

        Args:
            symbols: 股票代码列表，为 None 则返回已实现的包含名称的字典

        Returns:
            dict: {code: name}
        """
        if symbols is None or len(symbols) == 0:
            return {}

        # 分批查询（新浪批量限制）
        names = {}
        batch_size = 50
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i:i + batch_size]
            df = self.get_realtime_quotes(batch)
            if df is not None and len(df) > 0:
                for _, row in df.iterrows():
                    names[row["symbol"]] = row.get("name", "")
            # 小延时避免限流
            if i + batch_size < len(symbols):
                import time
                time.sleep(0.3)

        return names

    def resolve_name(self, code: str) -> str:
        """
        解析单只股票名称（通过实时行情接口）
        失败返回空字符串
        """
        df = self.get_realtime_quotes([code])
        if df is not None and len(df) > 0:
            return df.iloc[0].get("name", "")
        return ""

    # ──────────────────────────────────────────
    # 工具方法
    # ──────────────────────────────────────────

    @staticmethod
    def _safe_float(val) -> float:
        try:
            return float(val) if val else 0.0
        except (ValueError, TypeError):
            return 0.0


if __name__ == "__main__":
    c = AshareCollector()
    print("=== 测试上证指数 ===")
    df = c.get_daily_hist("000001", count=3)
    print(df)

    print("\n=== 测试招商银行 ===")
    df = c.get_daily_hist("600036", count=3)
    print(df)

    print("\n=== 测试批量实时行情 ===")
    df = c.get_realtime_quotes(["600036", "000001", "000333", "600519"])
    if not df.empty:
        print(df.to_string())

    print("\n=== 测试股票名称解析 ===")
    names = c.get_stock_names(["600036", "000001", "000333"])
    print(names)
