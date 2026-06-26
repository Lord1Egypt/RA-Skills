"""
股智Alpha - 六维评分引擎

维度：
1. 行为面（SLSV羊群效应）— 30%
2. 技术面（RSI/MACD/MA偏离）— 25%
3. 资金面（主力净流入率）— 15%
4. 动量面（多周期价格动量）— 15%（NEW）
5. 风险面（波动率/回撤）— 10%（NEW）
6. 成交异常面（量比/放量信号）— 5%（NEW）

全部基于真实数据计算，无占位维度。
"""

import logging
import pandas as pd
import numpy as np
from typing import Optional, Dict
from ..factors.factor_registry import FactorRegistry

logger = logging.getLogger(__name__)


class ScoringEngine:
    """六维评分引擎"""

    WEIGHTS = {
        "behavior": 0.30,
        "technical": 0.25,
        "fund_flow": 0.15,
        "momentum": 0.15,
        "risk": 0.10,
        "volume": 0.05,
    }

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or self.WEIGHTS.copy()
        self._missing_dims = []

    def score(
        self,
        candidates: pd.DataFrame,
        price_df: pd.DataFrame,
        flow_df: Optional[pd.DataFrame] = None,
    ) -> pd.DataFrame:
        self._missing_dims = []
        if len(candidates) == 0:
            return candidates

        df = candidates.copy()

        # === 1. 行为面：SLSV因子 ===
        if flow_df is not None and len(flow_df) > 0:
            slsv = FactorRegistry.create("SLSV")
            slsv_scores = slsv.calculate(price_df, flow_df)
            raw = df["stock_code"].map(slsv_scores).fillna(0)
            df["score_behavior"] = (raw + 1) / 2.0
        else:
            df["score_behavior"] = np.nan
            self._missing_dims.append("行为面(SLSV)")

        # === 2. 技术面 ===
        df["score_technical"] = self._calc_technical_score(price_df, df["stock_code"]).values

        # === 3. 资金面 ===
        if flow_df is not None and len(flow_df) > 0:
            latest_flow = (
                flow_df.sort_values("trade_date")
                .groupby("stock_code")
                .tail(1)
                .set_index("stock_code")
            )
            if "net_inflow_rate" in latest_flow.columns:
                rate = latest_flow["net_inflow_rate"]
                df["score_fund_flow"] = df["stock_code"].map(
                    1.0 / (1.0 + np.exp(-rate * 20))
                ).fillna(0.5)
            else:
                inflow = latest_flow.get("net_inflow_main", pd.Series(0))
                if len(inflow) > 0 and inflow.std() > 0:
                    df["score_fund_flow"] = df["stock_code"].map(
                        (inflow - inflow.min()) / (inflow.max() - inflow.min() + 1e-9)
                    ).fillna(0.5).values
                else:
                    df["score_fund_flow"] = 0.5
        else:
            df["score_fund_flow"] = np.nan
            self._missing_dims.append("资金面")

        # === 4. 动量面（NEW）===
        df["score_momentum"] = self._calc_momentum_score(price_df, df["stock_code"]).values

        # === 5. 风险面（NEW）===
        df["score_risk"] = self._calc_risk_score(price_df, df["stock_code"]).values

        # === 6. 成交异常面（NEW）===
        df["score_volume"] = self._calc_volume_score(price_df, df["stock_code"]).values

        # === 综合评分 ===
        df = self._combine_scores(df)
        df = df.sort_values("score_total", ascending=False)
        return df

    def get_missing_dims(self) -> list:
        return self._missing_dims

    # ───────────── 各维度评分方法 ─────────────

    def _calc_technical_score(self, price_df, stock_codes):
        """技术面：RSI+MACD+MA"""
        scores = pd.Series(0.5, index=stock_codes)
        latest = price_df.sort_values("trade_date").groupby("stock_code").tail(1).set_index("stock_code")

        for code in stock_codes:
            if code not in latest.index:
                continue
            row = latest.loc[code]
            s = 0.5
            if "RSI_14" in row.index:
                rsi = row["RSI_14"]
                if rsi < 30: s += 0.3
                elif rsi > 70: s -= 0.2
            if "MACD" in row.index and "MACD_SIGNAL" in row.index:
                if row["MACD"] > row["MACD_SIGNAL"]: s += 0.2
            if "MA_20d_DIFF" in row.index:
                s += min(max(row["MA_20d_DIFF"] * 2, -0.3), 0.3)
            scores[code] = max(0, min(1, s))
        return scores

    def _calc_momentum_score(self, price_df, stock_codes):
        """
        动量面：多周期动量 + 价格位置

        因子：
        - RET_5d, RET_10d, RET_20d: 多周期动量
        - Price position in 20-day range: 趋势强度
        """
        scores = pd.Series(0.5, index=stock_codes)
        for code in stock_codes:
            d = price_df[price_df["stock_code"] == code].sort_values("trade_date")
            if len(d) < 20:
                continue
            close = d["close"].values
            high_20 = d["high"].rolling(20).max().iloc[-1]
            low_20 = d["low"].rolling(20).min().iloc[-1]

            ret_5 = (close[-1] / close[-6] - 1) if len(close) > 5 else 0
            ret_10 = (close[-1] / close[-11] - 1) if len(close) > 10 else 0
            ret_20 = (close[-1] / close[-21] - 1) if len(close) > 20 else 0

            # 加权动量（近端权重更高）
            mom = ret_5 * 0.5 + ret_10 * 0.3 + ret_20 * 0.2

            # 价格在20日区间位置（高位=趋势强）
            pos = (close[-1] - low_20) / (high_20 - low_20) if high_20 > low_20 else 0.5

            # 综合：动量正+趋势强=高分
            s = 0.5 + mom * 3 + (pos - 0.5) * 0.3
            scores[code] = max(0, min(1, s))
        return scores

    def _calc_risk_score(self, price_df, stock_codes):
        """
        风险面：波动率越低=得分越高 + 回撤控制

        因子：
        - 年化波动率（越低越好）
        - 最大回撤（越小越好）
        """
        scores = pd.Series(0.5, index=stock_codes)
        for code in stock_codes:
            d = price_df[price_df["stock_code"] == code].sort_values("trade_date")
            if len(d) < 20:
                continue
            close = d["close"].values

            # 波动率
            ret = pd.Series(close).pct_change().dropna()
            vol = ret.tail(20).std() * (252 ** 0.5) if len(ret) >= 20 else 0.3
            # 年化波动率10%~60% → 得分1~0
            vol_score = max(0, min(1, 1 - (vol - 0.10) / 0.50))

            # 最大回撤
            peak = pd.Series(close).cummax()
            dd = ((pd.Series(close) - peak) / peak).min()
            dd_score = max(0, min(1, 1 + dd * 2))  # -50%→0, 0%→1

            # 综合
            scores[code] = vol_score * 0.6 + dd_score * 0.4
        return scores

    def _calc_volume_score(self, price_df, stock_codes):
        """
        成交异常面：放量信号 + 量比趋势

        因子：
        - 量比（当日/MA5）：放量=正分
        - 成交量趋势（MA5/MA20）：放量趋势
        - 放量上涨=强信号
        """
        scores = pd.Series(0.5, index=stock_codes)
        for code in stock_codes:
            d = price_df[price_df["stock_code"] == code].sort_values("trade_date")
            if len(d) < 20:
                continue

            vol = d["volume"].values if "volume" in d.columns else (
                d["vol"].values if "vol" in d.columns else None
            )
            if vol is None or len(vol) < 20:
                continue

            close = d["close"].values
            vol_series = pd.Series(vol)

            # 量比
            vol_ma5 = vol_series.rolling(5).mean().iloc[-1]
            vol_ratio = vol[-1] / vol_ma5 if vol_ma5 > 0 else 1

            # 成交量趋势
            vol_ma20 = vol_series.rolling(20).mean().iloc[-1]
            vol_trend = vol_ma5 / vol_ma20 if vol_ma20 > 0 else 1

            # 价格变化
            pct_chg = (close[-1] / close[-2] - 1) if len(close) >= 2 else 0

            # 放量上涨=强信号
            s = 0.5
            if vol_ratio > 1.5 and pct_chg > 0:
                s += 0.3  # 放量上涨
            elif vol_ratio > 1.5 and pct_chg < 0:
                s -= 0.1  # 放量下跌（分歧大）
            if vol_trend > 1.2:
                s += 0.15  # 持续放量趋势
            elif vol_trend < 0.8:
                s -= 0.1  # 持续缩量

            scores[code] = max(0, min(1, s))
        return scores

    # ───────────── 综合评分 ─────────────

    def _combine_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """六维几何加权"""
        w = self.weights
        score_cols = [
            "score_behavior", "score_fund_flow", "score_technical",
            "score_momentum", "score_risk", "score_volume"
        ]

        for col in score_cols:
            valid = df[col].dropna()
            if len(valid) == 0:
                df[col + "_norm"] = 0.5
            elif valid.nunique() <= 1:
                df[col + "_norm"] = 0.5
            else:
                lo, hi = valid.min(), valid.max()
                df[col + "_norm"] = (df[col] - lo) / (hi - lo)

        for col in score_cols:
            df[col + "_norm"] = df[col + "_norm"].fillna(0.5)

        # 几何加权
        df["score_total"] = 1.0
        for col, weight in w.items():
            key = f"score_{col}_norm"
            if key in df.columns:
                df["score_total"] *= df[key] ** weight

        df["score_total"] = df["score_total"] ** (1 / sum(w.values()))
        return df
