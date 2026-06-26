#!/usr/bin/env python3
"""分析师目标价策略 - 基于盈利预测计算隐含目标价空间"""

import pandas as pd
from typing import Dict, Optional, Any
from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class AnalystTargetStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "analyst_target"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "min_target_upside": 20.0,      # 最低目标价上行空间（%）
            "min_consecutive_forecasts": 2, # 最少连续盈利预测期数
            "forecast_years": 2,             # 预测年数（1=当年 2=当年+次年）
            "min_roe": 8.0,                # 最低ROE
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "score"

    def analyze_stock(self, ts_code: str, name: str,
                      params: Dict[str, Any]) -> Optional[Dict[str, Any]]:

        # 获取盈利预测
        forecast_df = self._get_forecast_data(ts_code, params["forecast_years"])
        if forecast_df is None or len(forecast_df) < params["min_consecutive_forecasts"]:
            return None

        # 财务验证
        fina_df = _u.get_fina_indicator(ts_code, limit=2)
        if fina_df is None or fina_df.empty:
            roe = None
        else:
            roe = fina_df["roe"].iloc[0] if "roe" in fina_df.columns else None

        if roe is not None and roe < params["min_roe"]:
            return None

        # 获取最新收盘价
        daily_df = _u.get_daily_data(ts_code, end_date="", limit=1)
        if daily_df is None or daily_df.empty:
            current_price = None
        else:
            close_col = "close"
            if close_col not in daily_df.columns:
                close_col = "open"  # 兜底
            current_price = float(daily_df[close_col].iloc[-1])

        if current_price is None or current_price <= 0:
            return None

        # ── 计算隐含目标价 ────────────────────────────────────────────────────
        # 方法：取最新预测期的 EPS，乘以行业平均 PE（或取预测 PE）估算目标价
        # 盈利预测数据字段：end_date（报告期）, ptype（预测类型）, values（预测值）
        # values[0]=营业收入, values[1]=净利润, values[2]=净利润率, values[3]=EPS...
        target_price, upside = self._calc_target(forecast_df, current_price)
        if target_price is None or upside < params["min_target_upside"]:
            return None

        # ── 评分 ──────────────────────────────────────────────────────────────
        score = self._score(upside, len(forecast_df), roe)

        return {
            "ts_code":           ts_code,
            "name":              name,
            "current_price":     round(current_price, 2),
            "target_price":      round(target_price, 2),
            "upside_pct":        round(upside, 2),
            "forecast_periods":  len(forecast_df),
            "forecasts":         forecast_df[["end_date", "values"]].to_dict("records"),
            "roe":               round(roe, 2) if roe else None,
            "score":             round(score, 2),
        }

    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def _get_forecast_data(ts_code: str, years: int) -> Optional[pd.DataFrame]:
        """
        获取个股盈利预测数据。
        接口：earning_forecast（盈利预测）
        字段：ts_code, ann_date, end_date(报告期), ptype(预测类型), values...
        """
        import time
        params = {"ts_code": ts_code, "type": "1"}  # type=1 综合预测
        time.sleep(0.05)
        data = _u.call_api("earning_forecast", params)
        if not data or "items" not in data or len(data["items"]) < 1:
            return None

        df = pd.DataFrame(data["items"], columns=data["fields"])

        # 标准化字段
        needed = ["end_date", "ptype", "values"]
        for col in needed:
            if col not in df.columns:
                return None

        df = df.sort_values("end_date", ascending=True)  # 从早到晚
        return df.head(years * 4)  # 每年最多4个季度预测

    @staticmethod
    def _calc_target(forecast_df: pd.DataFrame,
                     current_price: float) -> tuple:
        """
        计算隐含目标价。
        策略：取最新一期净利润预测，计算：目标价 = 当年预测EPS × 历史行业PE中位数
        values 字段顺序（earning_forecast）：营业收入,净利润,每股收益(EPS),市盈率(PE)
        """
        try:
            latest = forecast_df.iloc[-1]
            # values 是字符串格式 "val1,val2,val3,val4"
            vals = str(latest.get("values", "")).split(",")
            if len(vals) < 4:
                return None, 0.0

            # 取 EPS（第3个字段，索引2）和 PE（第4个字段，索引3）
            eps = float(vals[2].strip()) if vals[2].strip() not in ("", "None") else None
            pred_pe = float(vals[3].strip()) if vals[3].strip() not in ("", "None") else None

            if eps is None or eps <= 0:
                return None, 0.0

            # 优先用预测PE，否则用隐含PE = 当前价/EPS
            if pred_pe is not None and pred_pe > 0:
                target_price = eps * pred_pe
            else:
                # 用隐含PE法：目标价 = EPS × (当前PE × 1.2)，即给予20%溢价
                implied_pe = current_price / eps if eps > 0 else None
                if implied_pe is None or implied_pe <= 0:
                    return None, 0.0
                target_price = eps * implied_pe * 1.2  # 20% 上行空间作为目标

            upside = (target_price - current_price) / current_price * 100
            return target_price, upside

        except (ValueError, TypeError, IndexError):
            return None, 0.0

    @staticmethod
    def _score(upside: float, periods: int,
               roe: Optional[float]) -> float:
        """
        评分（0-100）：
          上行空间   0-50分  越高越好
          预测期数   0-25分  越多说明分析师覆盖越持续
          ROE       0-25分  越高说明基本面越好
        """
        s  = max(0, min(50, upside / 50 * 50))              # 上行空间（50%满分）
        s += max(0, min(25, periods * 6))                   # 预测期数
        if roe is not None and roe > 0:
            s += max(0, min(25, roe / 25 * 25))             # ROE
        return min(max(s, 0), 100)
