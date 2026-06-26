#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
趋势启动扫描器 V2 - 优化版
- 多线程并行请求
- 过滤退市股/ST股
- 减少运行时间
"""
import pandas as pd
import numpy as np
import requests
import time
import random
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 导入行业数据
import sys
sys.path.insert(0, str(Path(__file__).parent))
from industry_data import get_industry, get_industry_emoji
from tracking import add_recommendation, calc_stop_levels
from score_v2 import calc_score_v2
from tracking import add_recommendation, get_active_recommendations, get_triggered_alerts, update_tracking
from stock_pool_merged import get_merged_stock_list as get_expanded_stock_list

# 统一评分模块
_unified_path = Path(__file__).parent.parent.parent / "scripts"
if str(_unified_path) not in sys.path:
    sys.path.insert(0, str(_unified_path))
try:
    from unified_score import calc_unified_score as _calc_unified
    HAS_UNIFIED = True
except Exception:
    HAS_UNIFIED = False
    _calc_unified = None

DATA_DIR = Path("C:/Users/Administrator/.qclaw/workspace-ag01/data/trend_scan")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 线程安全的计数器
progress_lock = threading.Lock()
results_lock = threading.Lock()


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
        r = requests.get(url, params=params, timeout=8)
        text = r.text
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
    except:
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


def calc_trend_score(df):
    """计算趋势启动评分（基于对照组验证的规律）"""
    if len(df) < 25:
        return None

    last = df.iloc[-1]
    prev5 = df.iloc[-6:-1]  # 前5天

    score = 0
    signals = {}

    # 1. MACD柱线为正（25分）
    if last["hist"] > 0:
        score += 25
        signals["macd_hist_pos"] = 1
    else:
        signals["macd_hist_pos"] = 0

    # 2. 价格在MA20上方（20分）
    if last["close"] > last["ma20"]:
        score += 20
        signals["above_ma20"] = 1
    else:
        signals["above_ma20"] = 0

    # 3. RSI在上升（15分）
    if len(prev5) > 1 and last["rsi"] > prev5["rsi"].iloc[0]:
        score += 15
        signals["rsi_rising"] = 1
    else:
        signals["rsi_rising"] = 0

    # 4. RSI>50（15分）
    if last["rsi"] > 50:
        score += 15
        signals["rsi_above50"] = 1
    else:
        signals["rsi_above50"] = 0

    # 5. 窗口内价格上升（10分）
    if len(prev5) > 1:
        slope = np.polyfit(np.arange(len(prev5)), prev5["close"].values, 1)[0]
        if slope > 0:
            score += 10
            signals["price_rising"] = 1
        else:
            signals["price_rising"] = 0
    else:
        signals["price_rising"] = 0

    # 6. 均线多头排列（10分）
    if last["ma5"] > last["ma10"] > last["ma20"]:
        score += 10
        signals["ma_bullish"] = 1
    else:
        signals["ma_bullish"] = 0

    # 7. MACD柱线在增大（5分）
    if len(prev5) > 1 and last["hist"] > prev5["hist"].iloc[0]:
        score += 5
        signals["macd_hist_rising"] = 1
    else:
        signals["macd_hist_rising"] = 0

    # 额外信息
    signals["score"] = score
    signals["rsi"] = round(last["rsi"], 1)
    signals["boll_pos"] = round(last["boll_pos"], 2)
    signals["vol_ratio"] = round(last["vol_ratio"], 2)
    signals["close"] = last["close"]
    signals["ma5"] = round(last["ma5"], 2)
    signals["ma10"] = round(last["ma10"], 2)
    signals["ma20"] = round(last["ma20"], 2)

    # 近5日涨幅
    if len(df) >= 6:
        gain_5d = (last["close"] / df.iloc[-6]["close"] - 1) * 100
        signals["gain_5d"] = round(gain_5d, 2)
    else:
        signals["gain_5d"] = 0

    return signals


def get_stock_name(code):
    """获取股票名称"""
    code = str(code).zfill(6)
    symbol = "sh" + code if code.startswith("6") else "sz" + code
    try:
        url = "https://qt.gtimg.cn/q=" + symbol
        r = requests.get(url, timeout=5)
        text = r.text
        if "~" in text:
            parts = text.split("~")
            if len(parts) > 1:
                return parts[1]
    except:
        pass
    return ""


def is_bad_stock(name):
    """检查是否为退市股或ST股"""
    if not name:
        return False
    bad_keywords = ['退', 'ST', '*ST', '退市', '终止上市']
    for keyword in bad_keywords:
        if keyword in name:
            return True
    return False


def process_single_stock(stock, min_score=55):
    """处理单只股票的评分"""
    try:
        df = fetch_kline_tencent(stock["code"], days=100)
        if df.empty or len(df) < 30:
            return None

        df = add_indicators(df)
        
        if HAS_UNIFIED:
            signals = _calc_unified(df)
            if signals:
                signals["score"] = signals["final_score"]
        else:
            signals = calc_score_v2(df)
            if signals:
                signals["score"] = signals["total"]

        if signals and signals["score"] >= min_score:
            signals["code"] = stock["code"]
            signals["name"] = get_stock_name(stock["code"]) or stock["code"]
            
            # 过滤ST股和退市股
            if is_bad_stock(signals["name"]):
                return None
                
            return signals
    except Exception as e:
        pass
    return None


def scan_stocks_parallel(stocks, min_score=55, max_workers=20):
    """并行扫描股票"""
    results = []
    processed = [0]
    total = len(stocks)
    
    def process_with_progress(stock):
        result = process_single_stock(stock, min_score)
        with progress_lock:
            processed[0] += 1
            if processed[0] % 50 == 0:
                print(f"  进度: {processed[0]}/{total}  已筛选: {len(results)} 只")
        return result
    
    print(f"\n[扫描] 使用 {max_workers} 线程并行处理 {total} 只股票...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_with_progress, stock): stock for stock in stocks}
        for future in as_completed(futures):
            result = future.result()
            if result:
                with results_lock:
                    results.append(result)
    
    return results


def generate_push_message(df_result, date_str, max_per_industry=1, active_recs=None, alerts=None):
    """生成手机友好的推送消息（按行业分散）"""
    
    # 添加行业信息
    df_result = df_result.copy()
    df_result["industry"] = df_result["code"].apply(get_industry)
    df_result["industry_emoji"] = df_result["industry"].apply(get_industry_emoji)

    # 信号映射（已停用 - 2026-05-06）
    # signal_map = {
    #     "强烈看多": "强烈看多",
    #     "看多": "看多", 
    #     "偏热": "偏热",
    #     "超跌关注": "超跌关注",
    #     "观望": "观望"
    # }

    lines = []
    lines.append(f"📈 趋势扫描 TOP10")
    lines.append(f"{date_str}")
    lines.append("─" * 30)
    lines.append("")
    lines.append("【今日 TOP10】")
    lines.append("")

    # 排名 emoji
    rank_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for idx, (_, row) in enumerate(df_result.head(10).iterrows()):
        rank = idx + 1
        emoji = rank_emojis[idx] if idx < len(rank_emojis) else f"{rank}."
        # 信号含义已停用 - 只显示评分
        
        lines.append(f"{emoji} {row['name']} {row['code']}")
        lines.append(f" {row['industry_emoji']}{row['industry']}  {row['score']:.0f}分")
        lines.append(f" 现价:{row['close']:.2f}  5日:{row['gain_5d']:+.1f}%")
        lines.append("")

    lines.append("─" * 30)
    
    # 行业分布
    industry_counts = df_result.head(10)["industry"].value_counts()
    lines.append(f"📊 行业分布：{', '.join([f'{k}x{v}' for k, v in industry_counts.items()])}")
    lines.append("")
    lines.append("⚠️ 仅供参考，不构成投资建议")

    return "\n".join(lines)


def main(use_expanded=True, min_score=55):
    print("=" * 60)
    print("趋势启动扫描器 V2")
    print("基于对照组验证的规律筛选潜力股")
    print("=" * 60)

    print("\n[Step 1] 获取股票列表...")
    if use_expanded:
        stocks = get_expanded_stock_list()
    else:
        # 使用基础股票池
        from trend_scanner import fetch_all_stocks
        stocks = fetch_all_stocks()
    print(f"  共 {len(stocks)} 只")

    print("\n[Step 2] 扫描评分...")
    start_time = time.time()
    results = scan_stocks_parallel(stocks, min_score=min_score, max_workers=20)
    elapsed = time.time() - start_time
    print(f"  扫描完成，耗时: {elapsed:.1f}秒")

    if not results:
        print("\n未找到符合条件的股票")
        return

    df_result = pd.DataFrame(results)
    df_result = df_result.sort_values("score", ascending=False)

    # 保存结果
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = DATA_DIR / f"trend_scan_{today}.csv"
    df_result.to_csv(output_path, index=False, encoding="utf-8-sig")

    # ---- 追踪：更新已推荐股票的现价 ----
    print("\n[Step 3] 更新追踪数据...")
    active_recs = get_active_recommendations()
    alerts = []
    for rec in active_recs:
        code = rec["code"]
        match = df_result[df_result["code"] == code]
        if not match.empty:
            current_price = float(match.iloc[0]["close"])
            updated = update_tracking(code, current_price)
            if updated:
                gain = updated["current_gain_pct"]
                if gain >= updated["stop_profit_pct"]:
                    alerts.append(("profit", updated))
                elif gain <= -updated["stop_loss_pct"]:
                    alerts.append(("loss", updated))

    # ---- 追踪：将本次TOP 10加入追踪 ----
    print("[Step 4] 记录本次推荐...")
    df_result["industry"] = df_result["code"].apply(get_industry)
    top10 = df_result.head(5)
    new_count = 0
    for _, row in top10.iterrows():
        stop_profit, stop_loss = calc_stop_levels(int(row["score"]))
        added = add_recommendation(
            code=row["code"],
            name=row["name"],
            score=int(row["score"]),
            price=float(row["close"]),
            industry=row["industry"],
            stop_profit=stop_profit,
            stop_loss=stop_loss
        )
        if added:
            new_count += 1
    print(f"  新增追踪: {new_count} 只  活跃追踪: {len(active_recs)} 只")

    print("\n" + "=" * 60)
    print("扫描结果")
    print("=" * 60)

    print("\n【统计】")
    print(f"  扫描: {len(stocks)} 只")
    print(f"  符合条件: {len(df_result)} 只")
    print(f"  平均分: {df_result['score'].mean():.1f}")

    print("\n【TOP 10 潜力股】")
    print("-" * 70)
    print(f"{'排名':<4} {'代码':<8} {'名称':<10} {'评分':>4} {'RSI':>6} {'布林':>6} {'5日%':>5} {'MA多':>5} {'MACD':>5} {'量比':>5}")
    print("-" * 70)

    for idx, row in df_result.head(10).iterrows():
        rank = df_result.index.get_loc(idx) + 1
        ma_flag = "Y" if row["ma_bullish"] else "N"
        macd_flag = "Y" if row["macd_hist_pos"] else "N"
        print(f"{rank:<4} {row['code']:<8} {row['name'][:8]:<10} {row['score']:>4.0f} {row['rsi']:>6.1f} {row['boll_pos']:>+6.2f} {row['gain_5d']:>+5.1f}% {ma_flag:>5} {macd_flag:>5} {row['vol_ratio']:>5.2f}")

    print("\n【文件保存】")
    print(f"  {output_path}")

    # 生成手机友好的推送消息
    push_msg = generate_push_message(df_result, today, active_recs=active_recs, alerts=alerts)
    push_path = DATA_DIR / f"push_{today}.txt"
    with open(push_path, "w", encoding="utf-8") as f:
        f.write(push_msg)
    print(f"  推送消息: {push_path}")

    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)

    return df_result


if __name__ == "__main__":
    main()
