#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
趋势启动扫描器 V2 - 优化版
- 多线程并行请求
- 腾讯批量API预获取市值（替代东方财富逐只请求）
- 过滤退市股/ST股/科创板/白酒/银行/房地产
"""
import pandas as pd
import numpy as np
import requests
import time
import random
import json
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

import sys
sys.path.insert(0, str(Path(__file__).parent))
from industry_data import get_industry, get_industry_emoji
from tracking import add_recommendation, calc_stop_levels
from score_v2 import calc_score_v2
from tracking import add_recommendation, get_active_recommendations, get_triggered_alerts, update_tracking
from stock_pool_merged import get_merged_stock_list as get_expanded_stock_list

# 全市场股票池（优先使用）
try:
    from stock_pool_full import get_stock_pool_full
    USE_FULL_POOL = True
except ImportError:
    USE_FULL_POOL = False

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

progress_lock = threading.Lock()
results_lock = threading.Lock()

# 市值缓存: {code: 市值(亿元)}
MARKET_CAP_CACHE = {}


def _sym(code):
    code = str(code).zfill(6)
    return ("sh" + code) if code.startswith("6") else ("sz" + code)


def batch_fetch_market_caps(codes, batch_size=50, retries=2):
    """
    腾讯批量行情API获取总市值
    f72 = 总股本(股)，f3 = 现价(元)
    总市值(亿元) = f72 × f3 / 1e8
    返回: {code: 市值(亿元)}，失败则不缓存该code
    """
    cache = {}
    symbols = [_sym(c) for c in codes]

    for i in range(0, len(symbols), batch_size):
        batch_syms = symbols[i:i+batch_size]
        query = ",".join(batch_syms)
        url = f"https://qt.gtimg.cn/q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

        for attempt in range(retries):
            try:
                r = requests.get(url, headers=headers, timeout=10)
                # 每只股票一行，用\n分隔
                for line in r.text.strip().split("\n"):
                    if not line.strip():
                        continue
                    parts = line.split("~")
                    if len(parts) < 73:
                        continue
                    sym = parts[0].replace('v_', '')
                    if '="' in sym:
                        sym = sym.split('="')[0]
                    if not sym.startswith(('sh', 'sz')):
                        continue
                    code = sym[2:]
                    try:
                        # f72=总股本(股), f3=现价(元), 总市值(亿元) = f72 × f3 / 1e8
                        mktcap = float(parts[72]) * float(parts[3]) / 1e8
                        cache[code] = mktcap
                    except (ValueError, IndexError):
                        continue
                break
            except Exception:
                if attempt < retries - 1:
                    time.sleep(0.5)
                continue

    return cache


def fetch_kline_tencent(code, days=100):
    code = str(code).zfill(6)
    sym = "sh" + code if code.startswith("6") else "sz" + code
    url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
    params = {
        "_var": "kline_dayqfq",
        "param": f"{sym},day,,,{days},qfq",
        "r": str(random.random())
    }
    try:
        r = requests.get(url, params=params, timeout=8)
        json_str = r.text.split("=")[1]
        data = json.loads(json_str)
        if data.get("code") != 0:
            return pd.DataFrame()
        kline_data = data.get("data", {}).get(sym, {}).get("qfqday", [])
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
    closes = df["close"]
    df["ma5"] = closes.rolling(5).mean()
    df["ma10"] = closes.rolling(10).mean()
    df["ma20"] = closes.rolling(20).mean()
    delta = closes.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    df["rsi"] = 100 - 100 / (1 + gain / loss.replace(0, 1e-9))
    ema12 = closes.ewm(span=12, adjust=False).mean()
    ema26 = closes.ewm(span=26, adjust=False).mean()
    df["dif"] = ema12 - ema26
    df["dea"] = df["dif"].ewm(span=9, adjust=False).mean()
    df["hist"] = (df["dif"] - df["dea"]) * 2
    df["vol_ratio"] = df["volume"] / df["volume"].rolling(5).mean()
    df["boll_mid"] = closes.rolling(20).mean()
    df["boll_std"] = closes.rolling(20).std()
    df["boll_pos"] = (closes - df["boll_mid"]) / (df["boll_std"] * 2 + 1e-9)
    return df


def get_market_cap(code):
    return MARKET_CAP_CACHE.get(str(code).zfill(6))


def get_stock_name(code):
    code = str(code).zfill(6)
    sym = "sh" + code if code.startswith("6") else "sz" + code
    try:
        r = requests.get("https://qt.gtimg.cn/q=" + sym, timeout=5)
        parts = r.text.split("~")
        if len(parts) > 1:
            return parts[1]
    except:
        pass
    return ""


def is_bad_stock(name):
    if not name:
        return False
    for kw in ['退', 'ST', '*ST', '退市', '终止上市']:
        if kw in name:
            return True
    return False


def is_kcb_stock(code):
    return str(code).zfill(6).startswith("688")


def process_single_stock(stock, min_score=55):
    try:
        code = str(stock["code"]).zfill(6)

        # 市值过滤（从预缓存）
        mktcap = get_market_cap(code)
        if mktcap is None or mktcap < 100:
            return None

        df = fetch_kline_tencent(code, days=100)
        if df.empty or len(df) < 30:
            return None

        # 过滤退市/停牌股票：K线最新日期必须在30天内
        last_date = df['date'].iloc[-1]
        if (pd.Timestamp.now() - last_date).days > 30:
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
            signals["code"] = code
            signals["name"] = get_stock_name(code) or code

            if is_bad_stock(signals["name"]):
                return None
            if is_kcb_stock(code):
                return None
            industry = get_industry(code)
            name = signals.get("name", "")
            if industry in ("白酒", "银行", "房地产", "券商", "证券") or "地产" in name or "证券" in name:
                return None

            return signals
    except Exception:
        pass
    return None


def scan_stocks_parallel(stocks, min_score=55, max_workers=20):
    results = []
    processed = [0]
    total = len(stocks)

    def worker(stock):
        result = process_single_stock(stock, min_score)
        with progress_lock:
            processed[0] += 1
            if processed[0] % 50 == 0:
                print(f"  {processed[0]}/{total}  已筛选: {len(results)}")
        return result

    print(f"\n[扫描] {max_workers}线程 | {total}只")
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(worker, s): s for s in stocks}
        for f in as_completed(futures):
            r = f.result()
            if r:
                with results_lock:
                    results.append(r)
    print(f"  扫描耗时: {time.time()-t0:.1f}秒")
    return results


def generate_push_message(df_result, date_str):
    df_result = df_result.copy()
    df_result["industry"] = df_result["code"].apply(get_industry)
    df_result["industry_emoji"] = df_result["industry"].apply(get_industry_emoji)

    lines = []
    lines.append(f"📈 趋势扫描 TOP10")
    lines.append(f"{date_str}")
    lines.append("━" * 30)
    lines.append("")
    lines.append("【今日 TOP10】")
    lines.append("")
    emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    for idx, (_, row) in enumerate(df_result.head(10).iterrows()):
        emoji = emojis[idx] if idx < len(emojis) else f"{idx+1}."
        signal = row.get("signal_type", "观望")
        conf = row.get("buy_confidence", "")
        if conf and str(conf) != "nan":
            conf_str = f"  {conf}"
        else:
            conf_str = ""

        lines.append(f"{emoji} {row['name']} {row['code']}")
        lines.append(f" {row['industry_emoji']}{row['industry']}  {row['score']:.0f}分 {signal}{conf_str}")
        lines.append(f" 现价:{row['close']:.2f}  5日:{row['gain_5d']:+.1f}%")
        lines.append("")

    lines.append("━" * 30)
    ic = df_result.head(10)["industry"].value_counts()
    lines.append(f"📊 行业分布：{', '.join([f'{k}x{v}' for k,v in ic.items()])}")
    lines.append("")
    lines.append("⚠️ 仅供参考，不构成投资建议")
    return "\n".join(lines)


def main(use_full_pool=None, use_expanded=True, min_score=55):
    global MARKET_CAP_CACHE
    print("=" * 60)
    print("趋势启动扫描器 V2")
    print("=" * 60)

    print("\n[Step 1] 股票列表...")
    
    # 优先使用全市场股票池
    if use_full_pool is None:
        use_full_pool = USE_FULL_POOL
    
    if use_full_pool:
        stocks = get_stock_pool_full()
        print(f"  使用全市场股票池: {len(stocks)} 只")
    else:
        stocks = get_expanded_stock_list() if use_expanded else []
        print(f"  使用行业均衡股票池: {len(stocks)} 只")

    print("\n[Step 2] 批量获取市值...")
    t0 = time.time()
    all_codes = [str(s["code"]).zfill(6) for s in stocks]
    MARKET_CAP_CACHE = batch_fetch_market_caps(all_codes, batch_size=50)
    ok = sum(1 for v in MARKET_CAP_CACHE.values() if v >= 150)
    print(f"  获取 {len(MARKET_CAP_CACHE)} 只  (>=150亿: {ok})  {time.time()-t0:.1f}秒")

    print("\n[Step 3] 扫描评分...")
    results = scan_stocks_parallel(stocks, min_score=min_score, max_workers=20)

    if not results:
        print("\n未找到符合条件的股票")
        return None

    df_result = pd.DataFrame(results).sort_values("score", ascending=False)

    today = datetime.now().strftime("%Y-%m-%d")
    out = DATA_DIR / f"trend_scan_{today}.csv"
    df_result.to_csv(out, index=False, encoding="utf-8-sig")

    # 追踪
    print("\n[Step 4] 追踪更新...")
    active = get_active_recommendations()
    for rec in active:
        m = df_result[df_result["code"] == rec["code"]]
        if not m.empty:
            p = float(m.iloc[0]["close"])
            upd = update_tracking(rec["code"], p)
            if upd and upd["current_gain_pct"] >= upd["stop_profit_pct"]:
                print(f"  ! {rec['name']} 触及止盈 {upd['current_gain_pct']:+.1f}%")

    df_result["industry"] = df_result["code"].apply(get_industry)
    for _, row in df_result.head(5).iterrows():
        sp, sl = calc_stop_levels(int(row["score"]))
        add_recommendation(row["code"], row["name"], int(row["score"]),
                           float(row["close"]), row["industry"], sp, sl)

    # 输出
    print("\n" + "=" * 60)
    print(f"扫描: {len(stocks)} 只  符合: {len(df_result)} 只  平均分: {df_result['score'].mean():.1f}")
    print("-" * 70)
    print(f"{'排名':<4} {'代码':<8} {'名称':<10} {'评分':>4} {'RSI':>6} {'5日%':>6} {'行业':<8} {'信号'}")
    print("-" * 70)
    for idx, (_, row) in enumerate(df_result.head(10).iterrows()):
        sig = row.get("signal_type", "观望")
        conf = row.get("buy_confidence", "")
        cs = f"({conf})" if conf and str(conf) != "nan" else ""
        print(f"{idx+1:<4} {row['code']:<8} {row['name'][:8]:<10} {row['score']:>4.0f} "
              f"{row['rsi']:>6.1f} {row['gain_5d']:>+6.1f}% {row['industry']:<8} {sig}{cs}")

    push = generate_push_message(df_result, today)
    ppath = DATA_DIR / f"push_{today}.txt"
    with open(ppath, "w", encoding="utf-8") as f:
        f.write(push)
    print(f"\n文件: {out}")
    print(f"推送: {ppath}")
    print("完成!")
    return df_result


if __name__ == "__main__":
    main()
