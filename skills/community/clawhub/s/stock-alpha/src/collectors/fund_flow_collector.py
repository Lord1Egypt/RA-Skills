"""
资金流数据采集器 — 双层策略

Layer 1 (主): 价量关系估算（基于Ashare行情，不依赖外部API）
Layer 2 (优): akshare 个股资金流（当网络可用时）

slsv_factor 需要 net_inflow_main 列来计算行为面评分。
"""

import time
import random
import logging
import concurrent.futures

import pandas as pd
import numpy as np
from typing import Optional

logger = logging.getLogger(__name__)


class FundFlowCollector:
    """资金流数据采集"""

    def __init__(self, prefer_akshare: bool = False):
        self.name = "FundFlowCollector"
        self._prefer_akshare = prefer_akshare
        self._akshare_available = None  # 延迟检测

    def get_fund_flow(self, symbol: str, price_df: pd.DataFrame = None, **kwargs) -> pd.DataFrame:
        """
        获取个股资金流

        策略：
        1. 如果 prefer_akshare 且 akshare 可用 → 用 akshare
        2. 如果有 price_df → 价量估算
        3. 返回空

        Args:
            symbol: 股票代码
            price_df: 行情DataFrame（必需，否则只能返回空）

        Returns:
            DataFrame: [stock_code, trade_date, net_inflow_main, amount, net_inflow_rate]
        """
        # Layer 1: akshare (当明确要求且可用时)
        if self._prefer_akshare:
            df = self._try_akshare(symbol)
            if df is not None and len(df) > 0:
                return df

        # Layer 2: 价量估算
        if price_df is not None and len(price_df) > 0:
            df = self._estimate_from_price(symbol, price_df)
            if df is not None and len(df) > 0:
                return df

        return pd.DataFrame()

    def _try_akshare(self, symbol: str) -> pd.DataFrame:
        """尝试 akshare（带重试）"""
        for attempt in range(2):
            try:
                import akshare as ak
                market = "sh" if symbol.startswith("6") else "sz"
                df = ak.stock_individual_fund_flow(stock=symbol, market=market)
                if df is None or df.empty:
                    return pd.DataFrame()

                col_map = {
                    "日期": "trade_date", "收盘价": "close",
                    "主力净流入-净额": "net_inflow_main",
                    "主力净流入-净占比": "net_inflow_rate",
                }
                rename = {k: v for k, v in col_map.items() if k in df.columns}
                df = df.rename(columns=rename)
                df["stock_code"] = symbol

                for c in ["net_inflow_main", "net_inflow_rate"]:
                    if c in df.columns:
                        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
                if "net_inflow_rate" in df.columns:
                    df["net_inflow_rate"] = df["net_inflow_rate"] / 100.0
                if "trade_date" in df.columns and df["trade_date"].dtype == "object":
                    df["trade_date"] = pd.to_datetime(df["trade_date"])

                df["amount"] = 0.0
                self._akshare_available = True
                logger.info(f"[FundFlow] {symbol}: akshare OK ({len(df)} rows)")
                return df

            except Exception as e:
                delay = (attempt + 1) * 2 + random.random()
                time.sleep(delay)

        self._akshare_available = False
        return pd.DataFrame()

    def _estimate_from_price(self, symbol: str, price_df: pd.DataFrame) -> pd.DataFrame:
        """
        价量关系估算资金流

        核心逻辑：
        - pct_change = (close - open) / open（日内价格变动方向）
        - vol_ratio = volume / vol_5d_ma（放量/缩量）
        - 主力净流入估算 = volume * pct_change * avg_price * 0.3
          （假设30%为主动资金，放量时置信度更高）

        Args:
            symbol: 股票代码
            price_df: 行情DataFrame

        Returns:
            DataFrame: [stock_code, trade_date, net_inflow_main, amount, net_inflow_rate]
        """
        if price_df is None or len(price_df) < 10:
            return pd.DataFrame()

        df = price_df.copy()
        stock_code = symbol

        # 确定列名
        vol_col = "volume" if "volume" in df.columns else ("vol" if "vol" in df.columns else None)
        if vol_col is None or "open" not in df.columns or "close" not in df.columns:
            return pd.DataFrame()

        df["_vol"] = pd.to_numeric(df[vol_col], errors="coerce").fillna(0)
        df["_open"] = pd.to_numeric(df["open"], errors="coerce").fillna(0)
        df["_close"] = pd.to_numeric(df["close"], errors="coerce").fillna(0)
        df["_high"] = pd.to_numeric(df.get("high", df["close"]), errors="coerce").fillna(0)
        df["_low"] = pd.to_numeric(df.get("low", df["close"]), errors="coerce").fillna(0)

        # 价格变动百分比
        df["pct_change"] = np.where(
            df["_open"] > 0,
            (df["_close"] - df["_open"]) / df["_open"],
            0.0,
        )

        # 5日均量
        df["_vol_5d_ma"] = df["_vol"].rolling(window=5, min_periods=3).mean().replace(0, np.nan)

        # 成交量比率（放量/缩量）
        df["vol_ratio"] = df["_vol"] / df["_vol_5d_ma"]

        # 均价
        avg_price = (df["_high"] + df["_low"]) / 2

        # 主力净流入估算
        # 公式: volume * pct_change * avg_price * factor
        # factor 由放量程度决定：放量大则估算置信度高
        df["net_inflow_main"] = df["_vol"] * df["pct_change"] * avg_price * 0.3

        # 无放量时缩小估算幅度
        no_vol = df["vol_ratio"].fillna(0) <= 1.0
        df.loc[no_vol, "net_inflow_main"] *= 0.3

        # 极端值截断
        df["net_inflow_main"] = df["net_inflow_main"].clip(-1e10, 1e10)

        # net_inflow_rate: 净流入占比（标准化）
        total_val = df["_vol"] * avg_price
        total_val = total_val.replace(0, np.nan)
        df["net_inflow_rate"] = np.where(
            total_val.notna() & (total_val > 0),
            df["net_inflow_main"] / total_val,
            0.0,
        )
        df["net_inflow_rate"] = df["net_inflow_rate"].clip(-0.3, 0.3)

        # amount
        df["amount"] = total_val.fillna(0)

        # 交易日期
        if "trade_date" in df.columns:
            trade_dates = df["trade_date"]
        elif "date" in df.columns:
            trade_dates = df["date"]
        else:
            trade_dates = df.index

        result = pd.DataFrame({
            "stock_code": stock_code,
            "trade_date": trade_dates,
            "net_inflow_main": df["net_inflow_main"].fillna(0),
            "amount": df["amount"].fillna(0),
            "net_inflow_rate": df["net_inflow_rate"].fillna(0),
        })

        logger.info(f"[FundFlow] {symbol}: estimated {len(result)} rows (no akshare)")
        return result

    def batch_fund_flow(self, symbols: list, price_df: pd.DataFrame = None, max_workers: int = 1) -> pd.DataFrame:
        """
        批量获取资金流

        关键变化：对于价量估算模式，price_df 是必需的。
        如果提供了全量 price_df，直接按 stock_code 分组估算，无需并发。

        Args:
            symbols: 股票代码列表
            price_df: 全量行情 DataFrame（包含 stock_code 列）
            max_workers: 对 akshare 模式的并发数

        Returns:
            合并的 DataFrame
        """
        # 价量估算模式：直接从 price_df 按股分组计算
        if price_df is not None and "stock_code" in price_df.columns:
            frames = []
            for sym in symbols:
                sub = price_df[price_df["stock_code"] == sym]
                if len(sub) > 0:
                    df = self._estimate_from_price(sym, sub)
                    if len(df) > 0:
                        frames.append(df)
            if frames:
                return pd.concat(frames, ignore_index=True)
            return pd.DataFrame()

        # akshare 模式（需要 price_df 的场景实际上走了上面分支）
        # 这里仅作为兜底
        self._prefer_akshare = True
        frames = []
        batch_size = max_workers * 3
        for batch_start in range(0, len(symbols), batch_size):
            batch = symbols[batch_start:batch_start + batch_size]
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(max_workers, 2)) as pool:
                fut_to_sym = {pool.submit(self._try_akshare, sym): sym for sym in batch}
                for fut in concurrent.futures.as_completed(fut_to_sym):
                    try:
                        df = fut.result()
                        if df is not None and len(df) > 0:
                            frames.append(df)
                    except Exception:
                        pass
            if batch_start + batch_size < len(symbols):
                time.sleep(3)

        if frames:
            return pd.concat(frames, ignore_index=True)
        return pd.DataFrame()
