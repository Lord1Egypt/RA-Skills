#!/usr/bin/env python3
"""
技术指标计算引擎
基于 TA-Lib + pandas 实现全量技术指标计算
"""

import argparse
import json
import sys
import pandas as pd
import numpy as np

try:
    import talib
    HAS_TALIB = True
except ImportError:
    HAS_TALIB = False


class IndicatorEngine:
    """技术指标计算引擎"""

    def __init__(self, df: pd.DataFrame):
        """
        df 必须包含: date, open, high, low, close, volume
        """
        self.df = df.copy()
        self.results = {}

    # ==================== 均线系统 ====================

    def calc_ma(self, periods: list[int] = [5, 10, 20, 60, 120, 250]):
        """简单移动均线"""
        ma_data = {}
        for p in periods:
            key = f"MA{p}"
            if HAS_TALIB:
                self.df[key] = talib.SMA(self.df["close"], timeperiod=p)
            else:
                self.df[key] = self.df["close"].rolling(window=p).mean()
            ma_data[key] = round(self.df[key].iloc[-1], 2) if not pd.isna(self.df[key].iloc[-1]) else None

        # 判断均线排列
        latest = {k: v for k, v in ma_data.items() if v is not None}
        sorted_vals = sorted(latest.values(), reverse=True)
        if list(latest.values()) == sorted_vals:
            arrangement = "多头排列 (看涨)"
        elif list(latest.values()) == sorted(latest.values()):
            arrangement = "空头排列 (看跌)"
        else:
            arrangement = "交叉排列 (震荡)"

        # 金叉/死叉检测
        crosses = self._detect_ma_crosses(periods)

        self.results["MA"] = {
            "values": ma_data,
            "arrangement": arrangement,
            "crosses": crosses,
        }
        return self

    def _detect_ma_crosses(self, periods: list[int]) -> list[dict]:
        """检测均线金叉/死叉"""
        crosses = []
        for i in range(len(periods) - 1):
            short_ma = f"MA{periods[i]}"
            long_ma = f"MA{periods[i+1]}"
            if short_ma in self.df.columns and long_ma in self.df.columns:
                diff = self.df[short_ma] - self.df[long_ma]
                diff_prev = diff.shift(1)
                # 最近5日内的交叉
                for j in range(-5, 0):
                    if len(diff) >= abs(j) and len(diff_prev) >= abs(j):
                        if diff.iloc[j] > 0 and diff_prev.iloc[j] <= 0:
                            crosses.append({
                                "type": "金叉",
                                "short": short_ma, "long": long_ma,
                                "date": str(self.df["date"].iloc[j]),
                                "signal": "看涨"
                            })
                        elif diff.iloc[j] < 0 and diff_prev.iloc[j] >= 0:
                            crosses.append({
                                "type": "死叉",
                                "short": short_ma, "long": long_ma,
                                "date": str(self.df["date"].iloc[j]),
                                "signal": "看跌"
                            })
        return crosses

    # ==================== MACD ====================

    def calc_macd(self, fast=12, slow=26, signal=9):
        """MACD指标"""
        if HAS_TALIB:
            dif, dea, macd_hist = talib.MACD(
                self.df["close"], fastperiod=fast, slowperiod=slow, signalperiod=signal
            )
        else:
            ema_fast = self.df["close"].ewm(span=fast, adjust=False).mean()
            ema_slow = self.df["close"].ewm(span=slow, adjust=False).mean()
            dif = ema_fast - ema_slow
            dea = dif.ewm(span=signal, adjust=False).mean()
            macd_hist = (dif - dea) * 2

        self.df["DIF"] = dif
        self.df["DEA"] = dea
        self.df["MACD"] = macd_hist

        # 背离检测
        divergence = self._detect_macd_divergence()

        # 金叉/死叉
        cross = "无"
        if len(dif) >= 2:
            if dif.iloc[-1] > dea.iloc[-1] and dif.iloc[-2] <= dea.iloc[-2]:
                cross = "金叉 (买入信号)"
            elif dif.iloc[-1] < dea.iloc[-1] and dif.iloc[-2] >= dea.iloc[-2]:
                cross = "死叉 (卖出信号)"

        # 零轴位置
        axis_position = "零轴上方 (多头)" if dif.iloc[-1] > 0 else "零轴下方 (空头)"

        self.results["MACD"] = {
            "DIF": round(dif.iloc[-1], 4),
            "DEA": round(dea.iloc[-1], 4),
            "MACD_hist": round(macd_hist.iloc[-1], 4),
            "cross": cross,
            "axis_position": axis_position,
            "divergence": divergence,
            "trend": "柱状图放大" if abs(macd_hist.iloc[-1]) > abs(macd_hist.iloc[-2]) else "柱状图缩小",
        }
        return self

    def _detect_macd_divergence(self) -> dict:
        """MACD顶底背离检测"""
        close = self.df["close"]
        dif = self.df["DIF"]
        result = {"top_divergence": False, "bottom_divergence": False, "description": "无背离"}

        # 简化版：比较最近两个高/低点
        window = min(60, len(close))
        recent_close = close.iloc[-window:]
        recent_dif = dif.iloc[-window:]

        # 寻找价格高点与DIF高点 (顶背离)
        price_peaks = self._find_peaks(recent_close, order=5)
        dif_peaks = self._find_peaks(recent_dif, order=5)

        if len(price_peaks) >= 2 and len(dif_peaks) >= 2:
            if recent_close.iloc[price_peaks[-1]] > recent_close.iloc[price_peaks[-2]]:
                if recent_dif.iloc[dif_peaks[-1]] < recent_dif.iloc[dif_peaks[-2]]:
                    result["top_divergence"] = True
                    result["description"] = "⚠️ 顶背离（价格创新高但MACD未创新高，可能见顶回落）"

        # 寻找价格低点与DIF低点 (底背离)
        price_troughs = self._find_troughs(recent_close, order=5)
        dif_troughs = self._find_troughs(recent_dif, order=5)

        if len(price_troughs) >= 2 and len(dif_troughs) >= 2:
            if recent_close.iloc[price_troughs[-1]] < recent_close.iloc[price_troughs[-2]]:
                if recent_dif.iloc[dif_troughs[-1]] > recent_dif.iloc[dif_troughs[-2]]:
                    result["bottom_divergence"] = True
                    result["description"] = "🔔 底背离（价格创新低但MACD未创新低，可能触底反弹）"

        return result

    @staticmethod
    def _find_peaks(series, order=5):
        peaks = []
        for i in range(order, len(series) - order):
            if all(series.iloc[i] >= series.iloc[i-j] for j in range(1, order+1)) and \
               all(series.iloc[i] >= series.iloc[i+j] for j in range(1, order+1)):
                peaks.append(i)
        return peaks

    @staticmethod
    def _find_troughs(series, order=5):
        troughs = []
        for i in range(order, len(series) - order):
            if all(series.iloc[i] <= series.iloc[i-j] for j in range(1, order+1)) and \
               all(series.iloc[i] <= series.iloc[i+j] for j in range(1, order+1)):
                troughs.append(i)
        return troughs

    # ==================== KDJ ====================

    def calc_kdj(self, n=9, m1=3, m2=3):
        """KDJ随机指标"""
        if HAS_TALIB:
            k, d = talib.STOCH(
                self.df["high"], self.df["low"], self.df["close"],
                fastk_period=n, slowk_period=m1, slowk_matype=0,
                slowd_period=m2, slowd_matype=0,
            )
            j = 3 * k - 2 * d
        else:
            low_n = self.df["low"].rolling(window=n).min()
            high_n = self.df["high"].rolling(window=n).max()
            rsv = (self.df["close"] - low_n) / (high_n - low_n) * 100
            k = rsv.ewm(com=m1 - 1, adjust=False).mean()
            d = k.ewm(com=m2 - 1, adjust=False).mean()
            j = 3 * k - 2 * d

        self.df["K"], self.df["D"], self.df["J"] = k, d, j

        # 超买超卖判断
        status = "中性区间"
        if k.iloc[-1] > 80 and d.iloc[-1] > 80:
            status = "⚠️ 超买区间（K={:.1f}, D={:.1f}，注意回调风险）".format(k.iloc[-1], d.iloc[-1])
        elif k.iloc[-1] < 20 and d.iloc[-1] < 20:
            status = "🔔 超卖区间（K={:.1f}, D={:.1f}，关注反弹机会）".format(k.iloc[-1], d.iloc[-1])

        # 金叉/死叉
        cross = "无"
        if len(k) >= 2:
            if k.iloc[-1] > d.iloc[-1] and k.iloc[-2] <= d.iloc[-2]:
                cross = "金叉"
            elif k.iloc[-1] < d.iloc[-1] and k.iloc[-2] >= d.iloc[-2]:
                cross = "死叉"

        self.results["KDJ"] = {
            "K": round(k.iloc[-1], 2),
            "D": round(d.iloc[-1], 2),
            "J": round(j.iloc[-1], 2),
            "status": status,
            "cross": cross,
        }
        return self

    # ==================== RSI ====================

    def calc_rsi(self, periods: list[int] = [6, 12, 24]):
        """RSI相对强弱指标"""
        rsi_data = {}
        for p in periods:
            if HAS_TALIB:
                rsi = talib.RSI(self.df["close"], timeperiod=p)
            else:
                delta = self.df["close"].diff()
                gain = delta.where(delta > 0, 0).rolling(window=p).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=p).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
            rsi_data[f"RSI{p}"] = round(rsi.iloc[-1], 2) if not pd.isna(rsi.iloc[-1]) else None

        # 综合判断
        rsi6 = rsi_data.get("RSI6")
        strength = "中性"
        if rsi6 and rsi6 > 80:
            strength = "⚠️ 极强（超买，RSI6={:.1f}）".format(rsi6)
        elif rsi6 and rsi6 > 60:
            strength = "偏强（RSI6={:.1f}）".format(rsi6)
        elif rsi6 and rsi6 < 20:
            strength = "🔔 极弱（超卖，RSI6={:.1f}）".format(rsi6)
        elif rsi6 and rsi6 < 40:
            strength = "偏弱（RSI6={:.1f}）".format(rsi6)

        self.results["RSI"] = {"values": rsi_data, "strength": strength}
        return self

    # ==================== 布林带 ====================

    def calc_boll(self, period=20, nbdev=2):
        """布林带"""
        if HAS_TALIB:
            upper, mid, lower = talib.BBANDS(self.df["close"], timeperiod=period, nbdevup=nbdev, nbdevdn=nbdev)
        else:
            mid = self.df["close"].rolling(window=period).mean()
            std = self.df["close"].rolling(window=period).std()
            upper = mid + nbdev * std
            lower = mid - nbdev * std

        close = self.df["close"].iloc[-1]
        bandwidth = (upper.iloc[-1] - lower.iloc[-1]) / mid.iloc[-1] * 100

        # 位置判断
        if close > upper.iloc[-1]:
            position = "突破上轨（强势/超买）"
        elif close > mid.iloc[-1]:
            position = "中轨上方（偏强）"
        elif close > lower.iloc[-1]:
            position = "中轨下方（偏弱）"
        else:
            position = "跌破下轨（弱势/超卖）"

        # 收口/扩张
        bw_list = ((upper - lower) / mid * 100).dropna()
        bw_trend = "收口（变盘信号）" if bw_list.iloc[-1] < bw_list.iloc[-5] else "扩张（趋势延续）"

        self.results["BOLL"] = {
            "upper": round(upper.iloc[-1], 2),
            "mid": round(mid.iloc[-1], 2),
            "lower": round(lower.iloc[-1], 2),
            "bandwidth": round(bandwidth, 2),
            "position": position,
            "trend": bw_trend,
        }
        return self

    # ==================== 综合评分 ====================

    def calc_composite_score(self) -> dict:
        """综合技术评分 (0-100)"""
        score = 50  # 中性起点
        signals = []

        # MA 评分 (+/-15)
        if "MA" in self.results:
            arr = self.results["MA"]["arrangement"]
            if "多头" in arr:
                score += 15; signals.append("均线多头排列 +15")
            elif "空头" in arr:
                score -= 15; signals.append("均线空头排列 -15")

        # MACD 评分 (+/-15)
        if "MACD" in self.results:
            macd = self.results["MACD"]
            if "金叉" in macd["cross"]:
                score += 10; signals.append("MACD金叉 +10")
            elif "死叉" in macd["cross"]:
                score -= 10; signals.append("MACD死叉 -10")
            if "上方" in macd["axis_position"]:
                score += 5; signals.append("MACD零轴上方 +5")
            else:
                score -= 5; signals.append("MACD零轴下方 -5")
            if macd["divergence"].get("bottom_divergence"):
                score += 10; signals.append("MACD底背离 +10")
            if macd["divergence"].get("top_divergence"):
                score -= 10; signals.append("MACD顶背离 -10")

        # KDJ 评分 (+/-10)
        if "KDJ" in self.results:
            kdj = self.results["KDJ"]
            if "超买" in kdj["status"]:
                score -= 10; signals.append("KDJ超买 -10")
            elif "超卖" in kdj["status"]:
                score += 10; signals.append("KDJ超卖 +10")

        # RSI 评分 (+/-10)
        if "RSI" in self.results:
            strength = self.results["RSI"]["strength"]
            if "极强" in strength:
                score -= 5; signals.append("RSI超买 -5")
            elif "极弱" in strength:
                score += 5; signals.append("RSI超卖 +5")

        # BOLL 评分 (+/-10)
        if "BOLL" in self.results:
            pos = self.results["BOLL"]["position"]
            if "上轨" in pos:
                score += 5; signals.append("突破布林上轨 +5")
            elif "下轨" in pos:
                score -= 5; signals.append("跌破布林下轨 -5")

        score = max(0, min(100, score))

        if score >= 70:
            conclusion = "🟢 技术面偏多，短期看涨"
        elif score >= 55:
            conclusion = "🟡 技术面中性偏多，可适度关注"
        elif score >= 45:
            conclusion = "⚪ 技术面中性，观望为主"
        elif score >= 30:
            conclusion = "🟡 技术面中性偏空，谨慎操作"
        else:
            conclusion = "🔴 技术面偏空，短期看跌"

        return {
            "score": score,
            "conclusion": conclusion,
            "signals": signals,
        }

    # ==================== 运行全部 ====================

    def run_all(self) -> dict:
        self.calc_ma().calc_macd().calc_kdj().calc_rsi().calc_boll()
        self.results["composite"] = self.calc_composite_score()
        return self.results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="技术指标计算引擎")
    parser.add_argument("--input", required=True, help="K线数据JSON文件路径")
    parser.add_argument("--indicators", default="all", help="指标列表，逗号分隔")
    args = parser.parse_args()

    df = pd.read_json(args.input)
    engine = IndicatorEngine(df)

    if args.indicators == "all":
        results = engine.run_all()
    else:
        indicators = args.indicators.split(",")
        for ind in indicators:
            method = f"calc_{ind.lower().strip()}"
            if hasattr(engine, method):
                getattr(engine, method)()
        results = engine.results

    print(json.dumps(results, ensure_ascii=False, indent=2))