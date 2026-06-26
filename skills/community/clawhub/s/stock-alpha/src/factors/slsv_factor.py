"""
SLSV 羊群效应因子

原理 (Barber-Odean 行为金融学):
- 散户喜欢"追涨杀跌"，买最近涨得多的，卖跌得多的
- 反向操作：买近期跌得多 + 有资金流入的，卖近期涨得多 + 资金流出的
- 这创造了一个可预测的收益反转效应

SLSV = rank(RET_low20) * rank(INFLOW_20) - rank(RET_high20) * rank(OUTFLOW_20)

IC 基准: 年化 > 0.05, 夏普 > 1.0
"""

import pandas as pd
import numpy as np
from typing import Optional
from .base_factor import BaseFactor


class SLSVFactor(BaseFactor):
    """SLSV 羊群效应因子"""

    name = "SLSV"
    description = "羊群效应因子：买跌卖涨的资金流异象"

    def calculate(
        self,
        price_df: pd.DataFrame,
        flow_df: Optional[pd.DataFrame] = None,
        lookback: int = 20,
    ) -> pd.Series:
        """
        计算 SLSV 因子

        Args:
            price_df: 日线行情
                必须列: stock_code, trade_date, close
            flow_df: 资金流数据
                必须列: stock_code, trade_date, net_inflow_main
            lookback: 回看天数，默认20

        Returns:
            Series: index=stock_code, value=SLSV因子值（越高越看多）
        """
        # 计算收益率
        price_df = price_df.copy()
        price_df = price_df.sort_values(["stock_code", "trade_date"])
        price_df["RET"] = price_df.groupby("stock_code")["close"].pct_change(5)  # 用5日收益，更宽容

        # 过去N日最低/最高收益率
        price_df["RET_LOW"] = price_df.groupby("stock_code")["RET"].transform(
            lambda x: x.rolling(10, min_periods=5).min()
        )
        price_df["RET_HIGH"] = price_df.groupby("stock_code")["RET"].transform(
            lambda x: x.rolling(10, min_periods=5).max()
        )

        result = pd.Series(dtype=float)

        if flow_df is not None and len(flow_df) > 0:
            flow_df = flow_df.copy()
            flow_df = flow_df.sort_values(["stock_code", "trade_date"])

            # 资金流入率（20日累计）
            flow_df["INFLOW_20"] = flow_df.groupby("stock_code")["net_inflow_main"].transform(
                lambda x: x.rolling(lookback, min_periods=10).sum()
            )
            flow_df["OUTFLOW_20"] = flow_df.groupby("stock_code")["net_inflow_main"].transform(
                lambda x: x.rolling(lookback, min_periods=10).apply(lambda y: y[y < 0].sum(), raw=True)
            )

            # 合并
            merged = price_df.merge(
                flow_df[["stock_code", "trade_date", "INFLOW_20", "OUTFLOW_20"]],
                on=["stock_code", "trade_date"],
                how="inner",
            )

            if len(merged) > 0:
                merged["RANK_RET_LOW"] = self.rank(merged["RET_LOW"])
                merged["RANK_RET_HIGH"] = self.rank(merged["RET_HIGH"])
                merged["RANK_INFLOW"] = self.rank(merged["INFLOW_20"])
                merged["RANK_OUTFLOW"] = self.rank(merged["OUTFLOW_20"])

                # SLSV = 低估值因子 * 正资金流 - 高估值因子 * 负资金流
                merged["SLSV"] = (
                    merged["RANK_RET_LOW"] * merged["RANK_INFLOW"]
                    - merged["RANK_RET_HIGH"] * merged["RANK_OUTFLOW"]
                )

                # 取最新截面（去重，避免非唯一索引）
                latest_date = merged["trade_date"].max()
                latest = merged[merged["trade_date"] == latest_date].drop_duplicates(subset="stock_code")
                result = latest.set_index("stock_code")["SLSV"]

        # 无资金流时：用价格反转因子（跌越多=反弹机会）
        if len(result) == 0:
            price_only = price_df.dropna(subset=["RET"])
            if len(price_only) > 0:
                price_only["SLSV_PRICE"] = -price_only["RET_LOW"]
                latest_date = price_only["trade_date"].max()
                latest = price_only[price_only["trade_date"] == latest_date].drop_duplicates(subset="stock_code")
                result = latest.set_index("stock_code")["SLSV_PRICE"]

        # 去极值 + 保证唯一索引
        result = self.winsorize(result)
        if result.index.duplicated().any():
            result = result.groupby(result.index).mean()
        return result


if __name__ == "__main__":
    # 演示：用模拟数据计算 SLSV
    import numpy as np

    np.random.seed(42)
    stocks = [f"{str(i).zfill(6)}" for i in range(1, 51)]
    dates = pd.bdate_range("2026-01-01", "2026-04-15")

    records = []
    for s in stocks:
        for d in dates:
            records.append({
                "stock_code": s,
                "trade_date": d,
                "close": 10 + np.random.randn() * 2,
                "net_inflow_main": np.random.randn() * 1e6,
            })

    price_df = pd.DataFrame(records)
    flow_df = price_df[["stock_code", "trade_date", "net_inflow_main"]].copy()

    factor = SLSVFactor()
    result = factor.calculate(price_df, flow_df)

    print(f"SLSV 因子计算完成: {len(result)} 只股票")
    print(f"因子分布: mean={result.mean():.4f}, std={result.std():.4f}")
    print(f"Top 5:\n{result.nlargest(5)}")
