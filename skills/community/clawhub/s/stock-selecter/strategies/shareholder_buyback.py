#!/usr/bin/env python3
"""股东/高管增持策略 - 大股东或高管近期公告增持"""

import pandas as pd
from typing import Dict, Optional, Any
from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class ShareholderBuybackStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "shareholder_buyback"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "min_buyback_ratio": 0.5,      # 最低增持占总股本比例（%）
            "min_consecutive_periods": 1,   # 最少增持期数（1=单次也算）
            "lookback_days": 90,            # 回看天数
            "holder_type": "all",           # all=任意 / major=大股东 / manager=高管
            "min_roe": 8.0,                # 最低ROE（财务验证）
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "score"

    def analyze_stock(self, ts_code: str, name: str,
                      params: Dict[str, Any]) -> Optional[Dict[str, Any]]:

        buyback_df = self._get_buyback_data(ts_code, params["lookback_days"])
        if buyback_df is None or buyback_df.empty:
            return None

        # 财务验证
        fina_df = _u.get_fina_indicator(ts_code, limit=2)
        if fina_df is None or fina_df.empty:
            roe = None
        else:
            roe = fina_df["roe"].iloc[0] if "roe" in fina_df.columns else None

        if roe is not None and roe < params["min_roe"]:
            return None

        # ── 过滤增持类型 ──────────────────────────────────────────────────────
        holder_type = params["holder_type"]
        if holder_type == "major":
            # 大股东：holder_type in [1,2]（不同数据源定义略有差异，统一用1,2）
            buyback_df = buyback_df[buyback_df["holder_type"].isin([1, 2, 10])]
        elif holder_type == "manager":
            buyback_df = buyback_df[buyback_df["holder_type"].isin([3, 4])]

        if buyback_df.empty:
            return None

        # ── 累计增持比例 ───────────────────────────────────────────────────────
        total_ratio = 0.0
        periods = 0
        latest_date = None
        for _, row in buyback_df.iterrows():
            ratio = row.get("buyback_ratio", 0)
            if ratio is None or pd.isna(ratio):
                continue
            total_ratio += float(ratio)
            periods += 1
            if latest_date is None:
                latest_date = row.get("ann_date", None)

        if total_ratio < params["min_buyback_ratio"]:
            return None

        # ── 评分 ───────────────────────────────────────────────────────────────
        score = self._score(total_ratio, periods, roe)

        return {
            "ts_code":           ts_code,
            "name":              name,
            "total_buyback_ratio": round(total_ratio, 3),   # 累计增持比例%
            "periods":           periods,
            "latest_ann_date":   latest_date,
            "roe":               round(roe, 2) if roe else None,
            "score":             round(score, 2),
        }

    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def _get_buyback_data(ts_code: str, lookback_days: int) -> Optional[pd.DataFrame]:
        """
        获取个股增持/回购数据。
        接口：repurchase（股票回购），holder_type 字段区分增持类型
        注意：Tushare Pro 的 repurchase 接口记录的是公司主动回购，
        而非大股东/高管增持。若需增持数据，可使用 stk_holder_record 或爬虫补充。
        这里优先使用 repurchase 数据，holder_type=10 表示股权激励回购。
        """
        import time
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=lookback_days)).strftime("%Y%m%d")

        params = {
            "ann_date":  "",
            "ts_code":   ts_code,
            "start_date": start_date,
            "end_date":   end_date,
        }
        # 限流保护
        time.sleep(0.05)
        data = _u.call_api("repurchase", params)
        if not data or "items" not in data or len(data["items"]) < 1:
            return None

        df = pd.DataFrame(data["items"], columns=data["fields"])

        # 标准化字段（repurchase 接口字段：ann_date, ts_code, holder_type, buyback_ratio...）
        needed = ["ann_date", "holder_type", "buyback_ratio"]
        for col in needed:
            if col not in df.columns:
                return None

        df["buyback_ratio"] = pd.to_numeric(df["buyback_ratio"], errors="coerce")
        df = df.dropna(subset=["buyback_ratio"])
        df = df[df["buyback_ratio"] > 0]
        df = df.sort_values("ann_date", ascending=False)
        return df

    @staticmethod
    def _score(total_ratio: float, periods: int,
               roe: Optional[float]) -> float:
        """
        评分（0-100）：
          增持比例  0-45分   越高越好
          增持期数  0-25分   越多越好
          ROE      0-30分   越高越好
        """
        s  = max(0, min(45, total_ratio / 5 * 45))           # 增持比例（5%以上满分）
        s += max(0, min(25, periods * 8))                    # 增持期数
        if roe is not None and roe > 0:
            s += max(0, min(30, roe / 20 * 30))             # ROE
        return min(max(s, 0), 100)
