#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方案C深挖版 v3 - 使用腾讯API
"""
import pandas as pd
import numpy as np
import requests
import time
import random
from pathlib import Path

DATA_DIR = Path("C:/Users/Administrator/.qclaw/workspace-ag01/data/trend_analysis")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def fetch_kline_tencent(code, days=100):
    """使用腾讯API获取前复权日K线"""
    code = str(code).zfill(6)
    symbol = "sh" + code if code.startswith("6") else "sz" + code
    
    url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
    params = {
        "_var": "kline_dayqfq",
        "param": f"{symbol},day,,,{days},qfq",
        "r": str(random.random())
    }
    
    try:
        r = requests.get(url, params=params, timeout=10)
        text = r.text
        
        # 解析JSONP
        import json
        json_str = text.split("=")[1]
        data = json.loads(json_str)
        
        if data.get("code") != 0:
            return pd.DataFrame()
        
        kline_data = data.get("data", {}).get(symbol, {}).get("qfqday", [])
        
        if not kline_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(kline_data, columns=["date", "open", "close", "high", "low", "volume"])
        
        for col in ["open", "close", "high", "low", "volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)
        
        return df
    except Exception as e:
        return pd.DataFrame()


def add_indicators(df):
    """添加技术指标"""
    closes = df["close"]
    
    df["ma5"] = closes.rolling(5).mean()
    df["ma10"] = closes.rolling(10).mean()
    df["ma20"] = closes.rolling(20).mean()
    
    # RSI
    delta = closes.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    df["rsi"] = 100 - 100 / (1 + gain / loss.replace(0, 1e-9))
    
    # MACD
    ema12 = closes.ewm(span=12, adjust=False).mean()
    ema26 = closes.ewm(span=26, adjust=False).mean()
    df["dif"] = ema12 - ema26
    df["dea"] = df["dif"].ewm(span=9, adjust=False).mean()
    df["hist"] = (df["dif"] - df["dea"]) * 2
    
    # 量比
    df["vol_ratio"] = df["volume"] / df["volume"].rolling(5).mean()
    
    # 布林带
    df["boll_mid"] = closes.rolling(20).mean()
    df["boll_std"] = closes.rolling(20).std()
    df["boll_pos"] = (closes - df["boll_mid"]) / (df["boll_std"] * 2 + 1e-9)
    
    return df


def extract_window_features(df, end_idx, window=5):
    """提取窗口特征"""
    if end_idx < window + 15:
        return None
    
    w = df.iloc[end_idx - window: end_idx]
    last = df.iloc[end_idx - 1]
    closes = w["close"]
    
    # 趋势
    ma_bullish = int(last["ma5"] > last["ma10"] > last["ma20"])
    above_ma20 = int(last["close"] > last["ma20"])
    x = np.arange(len(closes))
    slope = np.polyfit(x, closes.values, 1)[0]
    price_slope_pos = int(slope > 0)
    
    # 动能
    rsi_val = last["rsi"]
    rsi_40_60 = int(40 <= rsi_val <= 60)
    rsi_above50 = int(rsi_val > 50)
    rsi_rising = int(w["rsi"].iloc[-1] > w["rsi"].iloc[0]) if len(w) > 1 else 0
    
    macd_dif_pos = int(last["dif"] > 0)
    macd_hist_pos = int(last["hist"] > 0)
    macd_hist_rising = int(w["hist"].iloc[-1] > w["hist"].iloc[0]) if len(w) > 1 else 0
    
    # 量能
    avg_vol_ratio = w["vol_ratio"].mean()
    vol_shrink = int(avg_vol_ratio < 1.0)
    vol_moderate = int(0.8 <= avg_vol_ratio <= 1.5)
    
    # 位置
    boll_pos_val = last["boll_pos"]
    boll_lower_half = int(boll_pos_val < 0)
    boll_near_low = int(boll_pos_val < -0.3)
    
    # 回撤
    recent_high = df.iloc[end_idx - 20: end_idx]["close"].max()
    drawdown = (last["close"] / recent_high - 1) * 100
    drawdown_5_15 = int(-15 <= drawdown <= -5)
    drawdown_mild = int(-10 <= drawdown <= -2)
    
    # 形态
    daily_chg = closes.pct_change().dropna()
    max_drop = daily_chg.min() * 100 if len(daily_chg) > 0 else 0
    no_panic = int(max_drop > -5)
    
    volatility = closes.std() / closes.mean() * 100 if closes.mean() > 0 else 0
    low_volatility = int(volatility < 3)
    
    return {
        "ma_bullish": ma_bullish,
        "above_ma20": above_ma20,
        "price_slope_pos": price_slope_pos,
        "rsi_40_60": rsi_40_60,
        "rsi_above50": rsi_above50,
        "rsi_rising": rsi_rising,
        "macd_dif_pos": macd_dif_pos,
        "macd_hist_pos": macd_hist_pos,
        "macd_hist_rising": macd_hist_rising,
        "vol_shrink": vol_shrink,
        "vol_moderate": vol_moderate,
        "boll_lower_half": boll_lower_half,
        "boll_near_low": boll_near_low,
        "drawdown_5_15": drawdown_5_15,
        "drawdown_mild": drawdown_mild,
        "no_panic": no_panic,
        "low_volatility": low_volatility,
        "rsi_val": rsi_val,
        "boll_pos_val": boll_pos_val,
        "avg_vol_ratio": avg_vol_ratio,
        "drawdown": drawdown,
        "volatility": volatility,
    }


def find_launch_points(df, min_gain=15):
    """找上涨启动点（之后20日涨幅>15%）"""
    launches = []
    
    for i in range(20, len(df) - 5):
        price = df.iloc[i]["close"]
        future_end = min(i + 21, len(df))
        future_high = df.iloc[i+1:future_end]["close"].max()
        future_gain = (future_high / price - 1) * 100
        
        if future_gain >= min_gain:
            launches.append(i)
    
    # 去重
    filtered = []
    for idx in launches:
        if not filtered or idx - filtered[-1] > 10:
            filtered.append(idx)
    
    return filtered


def find_control_points(df, launch_set):
    """找对照组（之后20日涨幅<5%）"""
    launch_expanded = set()
    for l in launch_set:
        for offset in range(-15, 15):
            launch_expanded.add(l + offset)
    
    controls = []
    for i in range(20, len(df) - 5):
        if i in launch_expanded:
            continue
        
        price = df.iloc[i]["close"]
        future_end = min(i + 21, len(df))
        future_high = df.iloc[i+1:future_end]["close"].max()
        future_gain = (future_high / price - 1) * 100
        
        if future_gain < 5:
            controls.append(i)
    
    if len(controls) > 3:
        controls = random.sample(controls, 3)
    
    return controls


def fetch_all_stocks():
    """获取股票列表"""
    # 使用本地预定义列表，避免额外API调用
    # 这里用沪深300部分成分股 + 部分热门股
    stocks = [
        "000001", "000002", "000063", "000333", "000338",
        "000425", "000568", "000625", "000651", "000708",
        "000725", "000768", "000776", "000858", "000876",
        "000938", "000963", "001979", "002001", "002007",
        "002008", "002024", "002027", "002049", "002050",
        "002120", "002142", "202304", "002230", "002236",
        "002241", "002271", "002304", "002311", "002352",
        "002371", "002410", "002415", "002422", "002460",
        "002475", "002493", "002508", "002594", "002601",
        "002607", "002624", "002653", "002709", "002714",
        "002756", "002812", "002841", "002850", "002938",
        "003816", "600000", "600009", "600010", "600011",
        "600015", "600016", "600019", "600025", "600028",
        "600029", "600030", "600031", "600036", "600048",
        "600050", "600104", "600109", "600111", "600115",
        "600118", "600132", "600150", "600183", "600196",
        "600276", "600309", "600332", "600340", "600346",
        "600352", "600406", "600438", "600486", "600489",
        "600498", "600519", "600547", "600570", "600585",
        "600588", "600660", "600690", "600703", "600745",
        "600809", "600837", "600845", "600848", "600887",
        "600893", "600900", "600918", "600926", "600941",
        "601012", "601021", "601066", "601088", "601111",
        "601138", "601166", "601211", "601225", "601236",
        "601288", "601318", "601319", "601328", "601336",
        "601390", "601398", "601601", "601628", "601633",
        "601658", "601668", "601669", "601688", "601728",
        "601766", "601788", "601800", "601808", "601818",
        "601857", "601877", "601888", "601899", "601901",
        "601919", "601933", "601939", "601985", "601988",
        "601989", "603019", "603087", "601127", "603160",
        "601727", "603259", "603260", "603288", "603369",
        "603501", "603596", "603833", "603899", "603986",
    ]
    
    result = [{"code": code, "name": ""} for code in stocks]
    return result


def main():
    print("=" * 60)
    print("方案C深挖 v3 - 腾讯API + 对照组对比")
    print("=" * 60)
    
    print("\n[Step 1] 获取股票列表...")
    stocks = fetch_all_stocks()
    print("  共 {} 只".format(len(stocks)))
    
    random.seed(42)
    sample = random.sample(stocks, min(100, len(stocks)))
    print("  抽样 {} 只".format(len(sample)))
    
    print("\n[Step 2] 收集启动组 + 对照组...")
    launch_rows = []
    control_rows = []
    
    for i, stock in enumerate(sample, 1):
        if i % 20 == 0:
            print("  进度: {}/{}  启动:{} 对照:{}".format(
                i, len(sample), len(launch_rows), len(control_rows)))
        
        df = fetch_kline_tencent(stock["code"], days=100)
        if df.empty or len(df) < 30:
            continue
        
        df = add_indicators(df)
        
        # 启动组
        launches = find_launch_points(df, min_gain=15)
        for idx in launches:
            feat = extract_window_features(df, idx, window=5)
            if feat:
                feat["code"] = stock["code"]
                feat["name"] = stock["name"]
                feat["group"] = "launch"
                launch_rows.append(feat)
        
        # 对照组
        controls = find_control_points(df, set(launches))
        for idx in controls:
            feat = extract_window_features(df, idx, window=5)
            if feat:
                feat["code"] = stock["code"]
                feat["name"] = stock["name"]
                feat["group"] = "control"
                control_rows.append(feat)
        
        time.sleep(0.2)
    
    print("\n  启动组: {} 个样本".format(len(launch_rows)))
    print("  对照组: {} 个样本".format(len(control_rows)))
    
    if not launch_rows:
        print("未找到启动点")
        return
    
    df_launch = pd.DataFrame(launch_rows)
    df_control = pd.DataFrame(control_rows)
    
    df_all = pd.concat([df_launch, df_control], ignore_index=True)
    df_all.to_csv(DATA_DIR / "launch_vs_control_v3.csv", index=False, encoding="utf-8-sig")
    
    # 对比分析
    print("\n" + "=" * 60)
    print("启动组 vs 对照组 对比")
    print("=" * 60)
    
    binary_features = [
        ("ma_bullish", "均线多头"),
        ("above_ma20", "价格>MA20"),
        ("price_slope_pos", "窗口内上升"),
        ("rsi_40_60", "RSI中性40-60"),
        ("rsi_above50", "RSI>50"),
        ("rsi_rising", "RSI上升"),
        ("macd_dif_pos", "MACD DIF>0"),
        ("macd_hist_pos", "MACD柱线正"),
        ("macd_hist_rising", "MACD柱线增"),
        ("vol_shrink", "缩量<1x"),
        ("vol_moderate", "温和量"),
        ("boll_lower_half", "布林下半区"),
        ("boll_near_low", "近布林下轨"),
        ("drawdown_5_15", "回撤5-15%"),
        ("drawdown_mild", "温和回调"),
        ("no_panic", "无恐慌"),
        ("low_volatility", "低波动"),
    ]
    
    print("\n{:<14} {:>6} {:>6} {:>6}".format("特征", "启动", "对照", "差值"))
    print("-" * 38)
    
    diffs = []
    for key, label in binary_features:
        l_pct = df_launch[key].mean() * 100
        c_pct = df_control[key].mean() * 100 if len(df_control) > 0 else 0
        diff = l_pct - c_pct
        diffs.append((abs(diff), diff, key, label, l_pct, c_pct))
    
    diffs.sort(reverse=True)
    
    for _, diff, key, label, l_pct, c_pct in diffs:
        print("  {:<12} {:>5.0f}% {:>5.0f}% {:>+5.0f}%".format(label, l_pct, c_pct, diff))
    
    # 连续值
    print("\n{:<12} {:>8} {:>8} {:>8}".format("连续指标", "启动", "对照", "差值"))
    print("-" * 40)
    for key, label in [
        ("rsi_val", "RSI"),
        ("boll_pos_val", "布林位置"),
        ("avg_vol_ratio", "量比"),
        ("drawdown", "回撤%"),
        ("volatility", "波动率%"),
    ]:
        l_val = df_launch[key].mean()
        c_val = df_control[key].mean() if len(df_control) > 0 else 0
        diff = l_val - c_val
        print("  {:<10} {:>8.2f} {:>8.2f} {:>+8.2f}".format(label, l_val, c_val, diff))
    
    # 关键发现
    print("\n" + "=" * 60)
    print("关键发现（差值>=10%的特征）")
    print("=" * 60)
    
    top = [(d, diff, k, label, l, c) for d, diff, k, label, l, c in diffs if d >= 10]
    if top:
        for _, diff, key, label, l_pct, c_pct in top:
            direction = "启动组更高" if diff > 0 else "启动组更低"
            print("  - {}: 启动{:.0f}% vs 对照{:.0f}% (差{:+.0f}%) [{}]".format(
                label, l_pct, c_pct, diff, direction))
    else:
        print("  暂无差值>=10%的特征")
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
