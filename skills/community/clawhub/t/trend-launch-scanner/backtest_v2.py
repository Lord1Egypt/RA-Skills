#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新评分 v2.0 历史回测 - 对比旧评分
使用 baostock 获取历史K线
"""
import baostock as bs
import pandas as pd
import numpy as np
import sys, time, json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

sys.path.insert(0, 'C:/Users/Administrator/.qclaw/workspace-ag01/skills/trend-launch-scanner')
from stock_pool_filtered import get_filtered_stock_list
from score_v2 import calc_score_v2

DATA_DIR = Path("C:/Users/Administrator/.qclaw/workspace-ag01/data/trend_scan")


def fetch_klines_bs(code, start_date, end_date):
    bs_code = f'sh.{code}' if code.startswith('6') else f'sz.{code}'
    rs = bs.query_history_k_data_plus(
        bs_code,
        'date,open,high,low,close,volume',
        start_date=start_date,
        end_date=end_date,
        frequency='d',
        adjustflag='2'
    )
    if rs is None or rs.error_msg != 'success':
        return pd.DataFrame()
    rows = []
    while rs.next():
        r = rs.get_row_data()
        if len(r) >= 6 and r[0] and r[4]:
            try:
                rows.append({
                    'date': r[0],
                    'open': float(r[1]),
                    'high': float(r[2]),
                    'low': float(r[3]),
                    'close': float(r[4]),
                    'volume': float(r[5]) if r[5] else 0,
                })
            except:
                continue
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date').reset_index(drop=True)


def add_indicators(df):
    closes = df['close']
    df['ma5']  = closes.rolling(5).mean()
    df['ma10'] = closes.rolling(10).mean()
    df['ma20'] = closes.rolling(20).mean()
    delta = closes.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    df['rsi'] = 100 - 100 / (1 + gain / loss.replace(0, 1e-9))
    ema12 = closes.ewm(span=12, adjust=False).mean()
    ema26 = closes.ewm(span=26, adjust=False).mean()
    df['dif'] = ema12 - ema26
    df['dea'] = df['dif'].ewm(span=9, adjust=False).mean()
    df['hist'] = (df['dif'] - df['dea']) * 2
    df['vol_ratio'] = df['volume'] / df['volume'].rolling(5).mean()
    df['boll_mid'] = closes.rolling(20).mean()
    df['boll_std'] = closes.rolling(20).std()
    df['boll_pos'] = (closes - df['boll_mid']) / (df['boll_std'] * 2 + 1e-9)
    return df


def calc_old_score(df):
    """旧评分（7个二元信号）"""
    if len(df) < 25:
        return 0
    last = df.iloc[-1]
    prev5 = df.iloc[-6:-1]
    score = 0
    if last['hist'] > 0: score += 25
    if last['close'] > last['ma20']: score += 20
    if len(prev5) > 1 and last['rsi'] > prev5['rsi'].iloc[0]: score += 15
    if last['rsi'] > 50: score += 15
    if len(prev5) > 1:
        slope = np.polyfit(np.arange(len(prev5)), prev5['close'].values, 1)[0]
        if slope > 0: score += 10
    if last['ma5'] > last['ma10'] > last['ma20']: score += 10
    if len(prev5) > 1 and last['hist'] > prev5['hist'].iloc[0]: score += 5
    return score


def get_price_n_days_later(df, date_str, n):
    """获取date_str之后第n个交易日的收盘价"""
    idx_list = df.index[df['date'].dt.strftime('%Y-%m-%d') == date_str].tolist()
    if not idx_list:
        # 找最近的交易日
        for i in range(5):
            d = (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')
            idx_list = df.index[df['date'].dt.strftime('%Y-%m-%d') == d].tolist()
            if idx_list:
                break
    if not idx_list:
        return None
    idx = idx_list[0]
    target_idx = idx + n
    if target_idx < len(df):
        return df.iloc[target_idx]['close']
    return None


def run_backtest(year, score_fn, score_threshold, score_label):
    start_date = f'{year}-01-01'
    end_date   = f'{year}-12-31'
    data_start = (datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=120)).strftime('%Y-%m-%d')

    stocks = get_filtered_stock_list()
    print(f"\n加载 {len(stocks)} 只股票K线 ({year})...", flush=True)

    kline_cache = {}
    for i, stock in enumerate(stocks):
        df = fetch_klines_bs(stock['code'], data_start, end_date)
        if not df.empty:
            df = add_indicators(df)
            kline_cache[stock['code']] = df
        if (i+1) % 50 == 0:
            print(f"  {i+1}/{len(stocks)}", flush=True)

    print(f"成功加载 {len(kline_cache)} 只", flush=True)

    # 生成每周一日期
    dates = []
    cur = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    while cur <= end:
        if cur.weekday() == 0:
            dates.append(cur.strftime('%Y-%m-%d'))
        cur += timedelta(days=1)

    # 行业关键词分散
    SECTOR_KEYWORDS = {
        '医药': ['制药','药业','医药','生物','医疗','健康','康','药'],
        '证券': ['证券','基金','投资'],
        '银行': ['银行'],
        '保险': ['保险'],
        '白酒': ['酒','茅台','五粮'],
        '化工': ['化工','化学','材料'],
    }
    def guess_sector(code, name):
        for sector, kws in SECTOR_KEYWORDS.items():
            for kw in kws:
                if kw in name:
                    return sector
        return f'other_{code[:3]}'

    weeks = []
    for date_str in dates:
        scored = []
        for stock in stocks:
            code = stock['code']
            name = stock.get('name', code)
            if code not in kline_cache:
                continue
            df = kline_cache[code]
            # 截取到当天
            sub = df[df['date'].dt.strftime('%Y-%m-%d') <= date_str].copy()
            if len(sub) < 30:
                continue
            # 当天收盘价
            day_rows = sub[sub['date'].dt.strftime('%Y-%m-%d') == date_str]
            if day_rows.empty:
                continue
            buy_price = day_rows.iloc[-1]['close']

            sig = score_fn(sub)
            score = sig.get('total', sig) if isinstance(sig, dict) else sig
            if score >= score_threshold:
                scored.append({'code': code, 'name': name, 'score': score,
                               'buy_price': buy_price, 'sector': guess_sector(code, name)})

        if len(scored) < 5:
            continue

        # 行业分散选TOP5
        scored.sort(key=lambda x: x['score'], reverse=True)
        sector_used = defaultdict(int)
        top5 = []
        for s in scored:
            if sector_used[s['sector']] < 1:
                top5.append(s)
                sector_used[s['sector']] += 1
            if len(top5) >= 5:
                break

        if len(top5) < 3:
            continue

        gains = []
        for s in top5:
            sell = get_price_n_days_later(kline_cache[s['code']], date_str, 5)
            if sell and s['buy_price']:
                gains.append((sell / s['buy_price'] - 1) * 100)

        if not gains:
            continue

        avg = sum(gains) / len(gains)
        weeks.append({'date': date_str, 'avg_gain': round(avg, 2),
                      'n': len(gains), 'stocks': [s['name'] for s in top5]})

    return weeks


def summarize(weeks, label):
    if not weeks:
        print(f"{label}: 无数据")
        return
    gains = [w['avg_gain'] for w in weeks]
    total = sum(gains)
    avg   = total / len(gains)
    wins  = sum(1 for g in gains if g > 0)
    annual = avg * 52
    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"{'='*55}")
    print(f"  样本周数:   {len(weeks)}")
    print(f"  平均周收益: {avg:+.2f}%")
    print(f"  累计收益:   {total:+.2f}%")
    print(f"  年化收益:   {annual:+.1f}%")
    print(f"  胜率:       {wins}/{len(weeks)} = {wins/len(weeks)*100:.0f}%")
    print(f"  最大盈利:   {max(gains):+.2f}%")
    print(f"  最大亏损:   {min(gains):+.2f}%")

    # 月度汇总
    monthly = defaultdict(list)
    for w in weeks:
        m = w['date'][:7]
        monthly[m].append(w['avg_gain'])
    print(f"\n  月度表现:")
    for m in sorted(monthly):
        gs = monthly[m]
        tag = '✅' if sum(gs)/len(gs) > 0 else '❌'
        print(f"    {m}  {sum(gs)/len(gs):+.2f}%  {tag}")


if __name__ == '__main__':
    bs.login()

    results = {}
    for year in [2024]:
        print(f"\n{'#'*55}")
        print(f"  回测年份: {year}")
        print(f"{'#'*55}")

        # 旧评分
        def old_fn(df): return calc_old_score(df)
        old_weeks = run_backtest(year, old_fn, 60, f'旧评分 {year}')
        results[f'old_{year}'] = old_weeks

        # 新评分
        def new_fn(df): return calc_score_v2(df)
        new_weeks = run_backtest(year, new_fn, 55, f'新评分v2 {year}')
        results[f'new_{year}'] = new_weeks

    bs.logout()

    print("\n\n" + "="*55)
    print("  新旧评分对比汇总")
    print("="*55)
    for year in [2024]:
        summarize(results[f'old_{year}'], f'旧评分 {year}年')
        summarize(results[f'new_{year}'], f'新评分v2 {year}年')

    # 保存
    out = {k: v for k, v in results.items()}
    with open(DATA_DIR / 'backtest_v2_compare.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 backtest_v2_compare.json")

