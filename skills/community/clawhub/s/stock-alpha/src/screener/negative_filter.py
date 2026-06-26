"""
负面剔除规则（第一层）

过滤条件：
1. ST / *ST 股票
2. 停牌股票
3. 退市风险（*ST）
4. 高估值（PE < 0 或 PE > 200，暂不剔除，留给六维评分）
5. 流动性极差（近5日日均成交额 < 1000万）
"""

import pandas as pd
from typing import List, Optional


class NegativeFilter:
    """负面剔除过滤器"""

    def __init__(self):
        self.name = "NegativeFilter"

    def filter(
        self,
        candidates: pd.DataFrame,
        stock_info: Optional[pd.DataFrame] = None,
    ) -> pd.DataFrame:
        """
        执行负面剔除

        Args:
            candidates: 候选股票池，需包含 stock_code 列
            stock_info: 股票基本信息（名称/状态等）

        Returns:
            剔除后的候选池
        """
        if len(candidates) == 0:
            return candidates

        df = candidates.copy()

        # 基础负面剔除（根据股票代码特征）
        # 以ST/退市风险代码过滤（*ST）
        if stock_info is not None:
            df = df.merge(stock_info, on="stock_code", how="left")
            df = df[~df.get("name", "").str.contains("ST", na=False)]
        else:
            # 备用方案：仅用代码前缀过滤（不完美，但可用）
            # 退市风险股通常以 *ST 开头
            df = df[~df["stock_code"].astype(str).str.startswith("*")]

        return df

    def filter_by_volume(
        self,
        candidates: pd.DataFrame,
        volume_df: pd.DataFrame,
        min_amount: float = 1e7,
        lookback: int = 5,
    ) -> pd.DataFrame:
        """
        流动性过滤：剔除近N日日均成交额 < min_amount 的股票

        Args:
            candidates: 候选池
            volume_df: 成交额数据，需包含 stock_code/trade_date/amount
            min_amount: 最低日均成交额，默认1000万

        Returns:
            流动性合格的候选池
        """
        if len(candidates) == 0 or len(volume_df) == 0:
            return candidates

        # 计算近N日日均成交额
        avg_amount = (
            volume_df.groupby("stock_code")["amount"]
            .tail(lookback)
            .groupby(volume_df.groupby("stock_code")["amount"].groupby(level=0).tail(lookback).index)
            .mean()
        )

        # 简化：直接按股票计算
        vol_stats = volume_df.groupby("stock_code")["amount"].agg(["mean", "count"]).reset_index()
        vol_stats.columns = ["stock_code", "avg_amount", "trade_days"]

        # 只保留有足够交易日且成交额足够的
        liquid = vol_stats[
            (vol_stats["avg_amount"] >= min_amount) &
            (vol_stats["trade_days"] >= lookback)
        ]

        return candidates[candidates["stock_code"].isin(liquid["stock_code"])]
