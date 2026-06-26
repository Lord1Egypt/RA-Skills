# -*- coding:utf-8 -*-
"""技术指标计算（RSI/MACD/MA）"""
import pandas as pd
import numpy as np


def calculate_rsi(closes: pd.Series, period: int = 14) -> pd.Series:
    """计算RSI"""
    delta = closes.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(closes: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """计算MACD返回DIF/MACD/SIGNAL"""
    ema_fast = closes.ewm(span=fast, adjust=False).mean()
    ema_slow = closes.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd = (dif - dea) * 2  # 柱状图
    return pd.DataFrame({"DIF": dif, "MACD": macd, "SIGNAL": dea})


def calculate_ma(closes: pd.Series, windows: list = None) -> pd.DataFrame:
    """计算MA均线"""
    if windows is None:
        windows = [5, 10, 20, 60]
    result = {}
    for w in windows:
        result[f"MA_{w}d"] = closes.rolling(window=w, min_periods=w).mean()
    return pd.DataFrame(result)


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    给price_df添加技术指标列
    df须包含: stock_code, trade_date, open, high, low, close, volume
    """
    df = df.sort_values(["stock_code", "trade_date"]).copy()
    result_rows = []
    for code, grp in df.groupby("stock_code"):
        grp = grp.sort_values("trade_date").copy()
        closes = grp["close"]
        grp["RSI_14"] = calculate_rsi(closes, 14)
        macd_df = calculate_macd(closes)
        grp["MACD_DIF"] = macd_df["DIF"]
        grp["MACD"] = macd_df["MACD"]
        grp["MACD_SIGNAL"] = macd_df["SIGNAL"]
        ma_df = calculate_ma(closes)
        for col in ma_df.columns:
            grp[col] = ma_df[col]
        # MA偏离度
        grp["MA_20d_DIFF"] = (grp["close"] - grp["MA_20d"]) / grp["MA_20d"]
        # 成交量均线（用于情绪）
        grp["VOL_MA20"] = grp["volume"].rolling(20, min_periods=5).mean()
        grp["VOL_RATIO"] = grp["volume"] / grp["VOL_MA20"].replace(0, np.nan)
        result_rows.append(grp)
    return pd.concat(result_rows, ignore_index=True)


def calculate_sentiment(price_df: pd.DataFrame, stock_code: str) -> dict:
    """
    基于成交量和价格动量计算情绪评分
    返回: {score, detail, signal}
    """
    stock = price_df[price_df["stock_code"] == stock_code].sort_values("trade_date").tail(20)
    if len(stock) < 5:
        return {"score": 0.5, "detail": "数据不足", "signal": "中性"}

    vol_ratio = float(stock.iloc[-1]["VOL_RATIO"]) if "VOL_RATIO" in stock.columns else 1.0
    vol_ratio = min(3.0, max(0.1, vol_ratio))  # 限制范围

    # 5日价格动量
    if len(stock) >= 5:
        ret_5d = (stock.iloc[-1]["close"] / stock.iloc[-5]["close"] - 1) if len(stock) >= 5 else 0
    else:
        ret_5d = 0

    score = 0.5

    # 成交量放大（资金关注）
    if vol_ratio > 1.5:
        score += 0.15
        vol_comment = f"量能放大({vol_ratio:.1f}x)"
    elif vol_ratio < 0.6:
        score -= 0.1
        vol_comment = f"量能萎缩({vol_ratio:.1f}x)"
    else:
        vol_comment = f"量能正常({vol_ratio:.1f}x)"

    # 短期动量（资金流入）
    if ret_5d > 0.03:
        score += 0.15
        mom_comment = "短期强势"
    elif ret_5d < -0.03:
        score -= 0.1
        mom_comment = "短期走弱"
    else:
        mom_comment = "震荡整理"

    score = max(0, min(1, score))

    detail = f"{vol_comment}，{mom_comment}"
    signal = "看多" if score > 0.6 else ("看空" if score < 0.4 else "中性")

    return {"score": round(score, 3), "detail": detail, "signal": signal}


if __name__ == "__main__":
    from src.collectors.ashare_collector import AshareCollector
    ac = AshareCollector()
    df = ac.get_daily_hist("600036", count=60)
    df["stock_code"] = "600036"
    df = add_technical_indicators(df)
    row = df.iloc[-1]
    print("RSI_14:", row.get("RSI_14"))
    print("MACD:", row.get("MACD"))
    print("MACD_DIF:", row.get("MACD_DIF"))
    print("MA_20d_DIFF:", row.get("MA_20d_DIFF"))
