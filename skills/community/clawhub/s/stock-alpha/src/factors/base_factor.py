"""
因子基类
所有因子继承此基类，统一接口
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Optional


class BaseFactor(ABC):
    """因子基类"""

    name: str = "BaseFactor"
    description: str = ""

    def __init__(self):
        self._cache = {}

    @abstractmethod
    def calculate(self, price_df: pd.DataFrame, flow_df: Optional[pd.DataFrame] = None) -> pd.Series:
        """
        计算因子值

        Args:
            price_df: 日线行情 DataFrame，需包含 col: open/high/low/close/volume/amount
            flow_df: 资金流 DataFrame，需包含 col: net_inflow_main/net_inflow_large

        Returns:
            Series: index=stock_code, value=因子值
        """
        raise NotImplementedError

    @staticmethod
    def rank(series: pd.Series) -> pd.Series:
        """横截面排名归一化（0~1）"""
        return series.rank(pct=True)

    @staticmethod
    def winsorize(series: pd.Series, lower=0.01, upper=0.99) -> pd.Series:
        """去极值（截尾法）"""
        lo = series.quantile(lower)
        hi = series.quantile(upper)
        return series.clip(lo, hi)

    def calc_ic(
        self,
        factor: pd.Series,
        forward_return: pd.Series,
    ) -> dict:
        """
        计算因子 IC（信息系数）

        Args:
            factor: 因子值
            forward_return: 次日收益

        Returns:
            dict: {ic, icir, rank_ic}
        """
        # 对齐索引
        common_idx = factor.index.intersection(forward_return.index)
        f = factor.loc[common_idx].dropna()
        r = forward_return.loc[common_idx].dropna()
        common = f.index.intersection(r.index)
        f = f.loc[common]
        r = r.loc[common]

        if len(f) < 3:
            return {"ic": np.nan, "rank_ic": np.nan, "icir": np.nan}

        ic = f.corr(r)

        # 手动计算 Spearman 相关系数（避免 scipy 依赖）
        f_rank = f.rank()
        r_rank = r.rank()
        rank_ic = f_rank.corr(r_rank)

        return {
            "ic": ic,
            "rank_ic": rank_ic,
            "icir": ic / len(f) ** 0.5 if len(f) > 0 else np.nan,
        }
