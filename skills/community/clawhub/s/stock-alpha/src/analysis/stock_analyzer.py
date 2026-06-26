"""
个股六维分析器

维度：
1. 行为面：SLSV因子
2. 技术面：RSI/MACD/趋势
3. 资金面：主力净流入
4. 动量面：多周期动量
5. 风险面：波动率/回撤
6. 成交异常面：放量信号
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List
from dataclasses import dataclass
from ..factors.factor_registry import FactorRegistry


@dataclass
class DimensionScore:
    name: str
    score: float
    label: str
    detail: str
    signal: str


class StockAnalyzer:
    def __init__(self):
        self.name = "StockAnalyzer"

    def analyze(
        self,
        stock_code: str,
        stock_name: str,
        price_df: pd.DataFrame,
        flow_df: Optional[pd.DataFrame] = None,
        sentiment_detail: Optional[Dict] = None,
    ) -> Dict:
        latest_price = self._get_latest_price(price_df, stock_code)

        dims = {
            "behavior": self._analyze_behavior(stock_code, price_df, flow_df),
            "technical": self._analyze_technical(stock_code, price_df),
            "fund_flow": self._analyze_fund_flow(stock_code, flow_df),
            "momentum": self._analyze_momentum(stock_code, price_df),
            "risk": self._analyze_risk_stock(stock_code, price_df),
            "volume": self._analyze_volume(stock_code, price_df),
        }

        if sentiment_detail:
            dims["sentiment"] = self._analyze_sentiment(sentiment_detail)

        radar = [d.score for d in dims.values()]
        signals = [d.signal for d in dims.values()]
        bullish = signals.count("看多")
        bearish = signals.count("看空")

        if bullish >= 4:
            verdict = "**强烈看多**"
        elif bullish >= 3:
            verdict = "**偏多**"
        elif bearish >= 3:
            verdict = "**偏空**"
        else:
            verdict = "**中性观望**"

        # 超卖机会
        tech = dims.get("technical")
        if tech and tech.score < 0.3:
            verdict = "**超卖反弹机会**"

        avg_score = np.mean(radar)
        warnings = self._check_warnings(dims, price_df, stock_code)

        return {
            "stock_code": stock_code,
            "stock_name": stock_name,
            "latest_price": latest_price,
            "dimensions": dims,
            "radar_data": radar,
            "avg_score": avg_score,
            "verdict": verdict,
            "risk_warnings": warnings,
        }

    def _get_latest_price(self, df, code):
        d = df[df["stock_code"] == code].sort_values("trade_date").tail(1)
        return float(d["close"].iloc[0]) if len(d) > 0 else 0.0

    # ─── 各维度分析 ───

    def _analyze_behavior(self, code, price_df, flow_df):
        s, detail, signal = 0.5, "", "中性"
        if flow_df is not None and len(flow_df) > 0:
            try:
                slsv = FactorRegistry.create("SLSV")
                ss = slsv.calculate(price_df, flow_df)
                if code in ss.index:
                    r = float((ss[code] + 1) / 2)
                    s = max(0, min(1, r))
                    if s > 0.65:
                        signal = "看多"
                        detail = f"SLSV={s:.2f}，机构资金主导"
                    elif s < 0.35:
                        signal = "看空"
                        detail = f"SLSV={s:.2f}，散户资金主导"
                    else:
                        detail = f"SLSV={s:.2f}，无明显方向"
            except Exception as e:
                detail = f"SLSV异常: {e}"
        else:
            detail = "资金流数据缺失"
        return DimensionScore("行为面", s, signal, detail, signal)

    def _analyze_technical(self, code, price_df):
        d = price_df[price_df["stock_code"] == code].sort_values("trade_date").tail(60)
        s, parts, sigs = 0.5, [], []
        if len(d) >= 20:
            r = d.iloc[-1]
            rsi = r.get("RSI_14", 50)
            if rsi < 30: s += 0.15; parts.append(f"RSI={rsi:.0f}(超卖↑)"); sigs.append("看多")
            elif rsi > 70: s -= 0.1; parts.append(f"RSI={rsi:.0f}(超买↓)"); sigs.append("看空")
            else: parts.append(f"RSI={rsi:.0f}")
            md = r.get("MA_20d_DIFF", 0)
            if md > 0.05: s += 0.1; parts.append(f"均线上方+{md*100:.1f}%"); sigs.append("看多")
            elif md < -0.05: s -= 0.1; parts.append(f"均线下方{md*100:.1f}%"); sigs.append("看空")
            macd = r.get("MACD", 0)
            if macd > 0: s += 0.1; parts.append("MACD金叉"); sigs.append("看多")
            else: parts.append("MACD死叉")
            s = max(0, min(1, s))
        sig = "看多" if sigs.count("看多") > sigs.count("看空") else ("看空" if sigs.count("看空") > sigs.count("看多") else "中性")
        det = "；".join(parts) if parts else "数据不足"
        return DimensionScore("技术面", s, sig, det, sig)

    def _analyze_fund_flow(self, code, flow_df):
        s, detail, signal = 0.5, "", "中性"
        if flow_df is not None and len(flow_df) > 0:
            sf = flow_df[flow_df["stock_code"] == code].sort_values("trade_date").tail(20)
            if len(sf) > 0:
                inflow = sf["net_inflow_main"].sum()
                rate = sf["net_inflow_rate"].mean() if "net_inflow_rate" in sf.columns else 0
                s = max(0, min(1, 0.5 + rate * 50))
                signal = "看多" if inflow > 0 else "看空"
                detail = f"近20日主力{'净流入' if inflow>0 else '净流出'}{abs(inflow)/1e8:.1f}亿"
        else:
            detail = "资金流数据缺失"
        return DimensionScore("资金面", s, signal, detail, signal)

    def _analyze_momentum(self, code, price_df):
        d = price_df[price_df["stock_code"] == code].sort_values("trade_date")
        if len(d) < 20:
            return DimensionScore("动量面", 0.5, "中性", "数据不足", "中性")
        c = d["close"].values
        r5 = (c[-1]/c[-6]-1) if len(c)>5 else 0
        r10 = (c[-1]/c[-11]-1) if len(c)>10 else 0
        r20 = (c[-1]/c[-21]-1) if len(c)>20 else 0
        mom = r5 * 0.5 + r10 * 0.3 + r20 * 0.2
        s = max(0, min(1, 0.5 + mom * 3))
        signal = "看多" if mom > 0.03 else ("看空" if mom < -0.03 else "中性")
        detail = f"5日{r5*100:+.1f}% 10日{r10*100:+.1f}% 20日{r20*100:+.1f}%"
        return DimensionScore("动量面", s, signal, detail, signal)

    def _analyze_risk_stock(self, code, price_df):
        d = price_df[price_df["stock_code"] == code].sort_values("trade_date")
        if len(d) < 20:
            return DimensionScore("风险面", 0.5, "中性", "数据不足", "中性")
        c = d["close"].values
        ret = pd.Series(c).pct_change().dropna()
        vol = ret.tail(20).std() * (252**0.5)
        vol_score = max(0, min(1, 1 - (vol - 0.10) / 0.50))
        peak = pd.Series(c).cummax()
        dd = ((pd.Series(c) - peak) / peak).min()
        dd_score = max(0, min(1, 1 + dd * 2))
        s = vol_score * 0.6 + dd_score * 0.4
        signal = "低风险" if vol < 0.20 else ("中等" if vol < 0.40 else "高波动")
        detail = f"年化波动率{vol*100:.1f}%，最大回撤{dd*100:.1f}%"
        return DimensionScore("风险面", s, signal, detail, signal)

    def _analyze_volume(self, code, price_df):
        d = price_df[price_df["stock_code"] == code].sort_values("trade_date")
        if len(d) < 20:
            return DimensionScore("成交面", 0.5, "中性", "数据不足", "中性")
        vol_col = "volume" if "volume" in d.columns else ("vol" if "vol" in d.columns else None)
        if vol_col is None:
            return DimensionScore("成交面", 0.5, "中性", "无成交量数据", "中性")
        vol_s = pd.Series(d[vol_col].values)
        c = d["close"].values
        vr = vol_s.iloc[-1] / vol_s.rolling(5).mean().iloc[-1] if vol_s.rolling(5).mean().iloc[-1] > 0 else 1
        vt = vol_s.rolling(5).mean().iloc[-1] / vol_s.rolling(20).mean().iloc[-1] if vol_s.rolling(20).mean().iloc[-1] > 0 else 1
        pct = (c[-1] / c[-2] - 1) if len(c) >= 2 else 0
        s = 0.5
        if vr > 1.5 and pct > 0: s += 0.3; signal = "放量上涨"
        elif vr > 1.5 and pct < 0: s -= 0.1; signal = "放量下跌"
        else: signal = "正常"
        if vt > 1.2: s += 0.15
        s = max(0, min(1, s))
        detail = f"量比{vr:.2f}，趋势{vt:.2f}"
        return DimensionScore("成交面", s, signal, detail, "看多" if s > 0.6 else "中性" if s > 0.4 else "看空")

    def _analyze_sentiment(self, sd):
        score = sd.get("score", 0.5)
        bullish = sd.get("bullish_pct", 50)
        bearish = sd.get("bearish_pct", 50)
        signal = "看多" if bullish > 60 else ("看空" if bearish > 60 else "中性")
        return DimensionScore("情绪面", score, signal, sd.get("summary", ""), signal)

    def _check_warnings(self, dims, price_df, code):
        warnings = []
        d = price_df[price_df["stock_code"] == code].sort_values("trade_date").tail(60)
        if len(d) >= 20:
            peak = d["close"].cummax()
            dd = ((d["close"] - peak) / peak).min()
            if dd < -0.15:
                warnings.append(f"近60日最大回撤{dd*100:.1f}%")
        t = dims.get("technical")
        if t and t.score < 0.25:
            warnings.append("技术面严重超卖")
        r = dims.get("risk")
        if r and r.score < 0.25:
            warnings.append("风险面高波动警示")
        return warnings
