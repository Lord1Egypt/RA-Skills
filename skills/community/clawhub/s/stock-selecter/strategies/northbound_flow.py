#!/usr/bin/env python3
"""北向资金策略 - 沪深港通北向资金连续净买入"""

import pandas as pd
from typing import Dict, Optional, Any
from .base import BaseStrategy
from utils.loader import import_shared_libs

_u, _i = import_shared_libs()


class NorthboundFlowStrategy(BaseStrategy):

    @property
    def strategy_name(self) -> str:
        return "northbound_flow"

    @property
    def default_params(self) -> Dict[str, Any]:
        return {
            "min_consecutive_days": 5,      # 最少连续净买入天数
            "min_daily_net": 1.0,           # 单日最低净买入额（亿元）
            "min_total_net": 5.0,           # 累计最低净买入额（亿元）
            "lookback_days": 20,            # 回看天数
            "north_type": "all",            # 北向类型: all沪股通+深股通 / sh沪股通 / sz深股通
            "exclude_st": True,
            "top_n": 0,
        }

    @property
    def sort_key(self) -> str:
        return "score"

    def analyze_stock(self, ts_code: str, name: str,
                      params: Dict[str, Any]) -> Optional[Dict[str, Any]]:

        # 北向资金只覆盖沪深港通标的，先判断是否在港股通列表内
        hsgt_df = self._get_hsgt_top(ts_code, params["lookback_days"])
        if hsgt_df is None or len(hsgt_df) < params["min_consecutive_days"]:
            return None

        # 筛选北向类型
        north_type = params["north_type"]
        if north_type == "sh":
            hsgt_df = hsgt_df[hsgt_df["exchange_id"] == "沪股通"]
        elif north_type == "sz":
            hsgt_df = hsgt_df[hsgt_df["exchange_id"] == "深股通"]

        if hsgt_df.empty:
            return None

        # 按日期降序（最新在前）
        hsgt_df = hsgt_df.sort_values("trade_date", ascending=False)

        # ── 连续净买入天数 ──────────────────────────────────────────────────────
        consecutive_days = 0
        net_amounts = []
        for _, row in hsgt_df.iterrows():
            net = row.get("net_amount", 0)
            if net is None:
                continue
            net = float(net)
            net_amounts.append(net)
            if net >= params["min_daily_net"]:
                consecutive_days += 1
            else:
                break  # 中断则停止计数

        if consecutive_days < params["min_consecutive_days"]:
            return None

        # ── 累计净买入总额 ─────────────────────────────────────────────────────
        total_net = sum(net_amounts)
        if total_net < params["min_total_net"]:
            return None

        # ── 财务验证（ROE）─────────────────────────────────────────────────────
        fina_df = _u.get_fina_indicator(ts_code, limit=2)
        if fina_df is None or fina_df.empty:
            roe = None
        else:
            roe = fina_df["roe"].iloc[0] if "roe" in fina_df.columns else None

        # ── 评分 ──────────────────────────────────────────────────────────────
        score = self._score(consecutive_days, total_net, roe, len(net_amounts))

        return {
            "ts_code":           ts_code,
            "name":              name,
            "consecutive_days":  consecutive_days,
            "total_net_amount":  round(total_net, 2),   # 亿元
            "avg_daily_net":     round(total_net / len(net_amounts), 2) if net_amounts else 0,
            "net_amounts":       [round(x, 2) for x in net_amounts[:10]],  # 最多显示10天
            "roe":               round(roe, 2) if roe else None,
            "score":             round(score, 2),
        }

    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def _get_hsgt_top(ts_code: str, limit: int) -> Optional[pd.DataFrame]:
        """
        获取个股的北向资金成交数据（沪股通/深股通）。
        接口：moneyflow_hsgt（沪深港通资金流向）
        返回：合并后的北向资金数据
        """
        # 判断交易所：沪股通 600/601/688/000 开头；深股通 000/001/002/003 开头
        code = ts_code.split(".")[0]
        if code.startswith("6") or code.startswith("688"):
            hsgt_list = "sh"
        else:
            hsgt_list = "sz"

        params = {
            "trade_date": "",         # 留空则返回最近交易日
            "ts_code":    ts_code,
            "start_date": "",
            "end_date":   "",
        }
        data = _u.call_api("moneyflow_hsgt", params)
        if not data or "items" not in data or len(data["items"]) < 2:
            return None

        df = pd.DataFrame(data["items"], columns=data["fields"])
        # 过滤字段
        needed = ["trade_date", "exchange_id", "hsgt_type", "net_amount"]
        for col in needed:
            if col not in df.columns:
                return None

        # 只保留北向（沪股通+深股通，排除南向）
        df = df[df["hsgt_type"].isin([1, 3])]  # 1=沪股通 3=深股通
        df["net_amount"] = pd.to_numeric(df["net_amount"], errors="coerce")
        df = df.dropna(subset=["net_amount"])
        df["trade_date"] = pd.to_datetime(df["trade_date"])
        df = df.sort_values("trade_date", ascending=False).head(limit)
        return df

    @staticmethod
    def _score(consecutive_days: int, total_net: float,
               roe: Optional[float], days: int) -> float:
        """
        评分（0-100）：
          连续天数   0-35分  越连续越好
          累计净买入  0-35分  越多越好
          ROE        0-20分  有ROE数据时加分
          天数覆盖   0-10分  回看天数内有效天数越多越好
        """
        s  = max(0, min(35, consecutive_days * 5))           # 连续天数
        s += max(0, min(35, total_net / 20 * 35))            # 累计净买入
        if roe is not None and roe > 0:
            s += max(0, min(20, roe / 20 * 20))             # ROE加分
        s += max(0, min(10, days / 20 * 10))                  # 有效天数
        return min(max(s, 0), 100)
