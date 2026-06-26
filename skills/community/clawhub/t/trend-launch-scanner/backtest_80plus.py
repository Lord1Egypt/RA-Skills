#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策略回测：每周一买入80分以上股票，持有5天后卖出
"""
import baostock as bs
import pandas as pd
import numpy as np
import json
import time
import sys
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
        bs_code, 'date,open,high,low,close,volume',
        start_date=start_date, end_date=end_date,
        frequency='d', adjustflag='2'
    )
    if rs is None or rs.error_msg != 'success':
        return pd.DataFrame()
    rows = []
    while rs.next():
        r = rs.get_row_data()
        if len(r) >= 6 and r[0] and r[4]:
            try:
                rows.append({'date': r[0], 'close': float(r[4]), 'volume': float(r[5]) if r[5] else 0})
            except: continue
    if not rows: return pd.DataFrame()
    df = pd.DataFrame(rows)
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date').reset_index(drop=True)


def add_indicators(df):
    c = df['close']
    df['ma5'] = c.rolling(5).mean()
    df['ma10'] = c.rolling(10).mean()
    df['ma20'] = c.rolling(20).mean()
    d = c.diff()
    g = d.clip(lower=0).rolling(14).mean()
    l = (-d.clip(upper=0)).rolling(14).mean()
    df['rsi'] = 100 - 100 / (1 + g / l.replace(0, 1e-9))
    e12 = c.ewm(span=12, adjust=False).mean()
    e26 = c.ewm(span=26, adjust=False).mean()
    df['dif'] = e12 - e26
    df['dea'] = df['dif'].ewm(span=9, adjust=False).mean()
    df['hist'] = (df['dif'] - df['dea']) * 2
    df['vol_ratio'] = df['volume'] / df['volume'].rolling(5).mean()
    df['boll_mid'] = c.rolling(20).mean()
    df['boll_std'] = c.rolling(20).std()
    df['boll_pos'] = (c - df['boll_mid']) / (df['boll_std'] * 2 + 1e-9)
    return df


def get_price_n_days_later(df, date_str, n):
    idx_list = df.index[df['date'].dt.strftime('%Y-%m-%d') == date_str].tolist()
    if not idx_list:
        for i in range(5):
            d = (datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')
            idx_list = df.index[df['date'].dt.strftime('%Y-%m-%d') == d].tolist()
            if idx_list: break
    if not idx_list: return None
    target = idx_list[0] + n
    return df.iloc[target]['close'] if target < len(df) else None


def run_backtest(year):
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'
    data_start = (datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=120)).strftime('%Y-%m-%d')
    
    stocks = get_filtered_stock_list()
    print(f"\n加载 {len(stocks)} 只股票K线...", flush=True)
    
    bs.login()
    kline_cache = {}
    for i, stock in enumerate(stocks):
        df = fetch_klines_bs(stock['code'], data_start, end_date)
        if not df.empty:
            kline_cache[stock['code']] = add_indicators(df)
        if (i+1) % 50 == 0:
            print(f"  {i+1}/{len(stocks)}", flush=True)
        time.sleep(0.05)
    bs.logout()
    print(f"成功加载 {len(kline_cache)} 只", flush=True)
    
    # 每周一日期
    dates = []
    cur = datetime.strptime(start_date, '%Y-%m-%d')
    while cur <= datetime.strptime(end_date, '%Y-%m-%d'):
        if cur.weekday() == 0:
            dates.append(cur.strftime('%Y-%m-%d'))
        cur += timedelta(days=1)
    
    weeks = []
    for date_str in dates:
        scored = []
        for stock in stocks:
            code = stock['code']
            if code not in kline_cache: continue
            df = kline_cache[code]
            sub = df[df['date'].dt.strftime('%Y-%m-%d') <= date_str].copy()
            if len(sub) < 30: continue
            
            day_rows = sub[sub['date'].dt.strftime('%Y-%m-%d') == date_str]
            if day_rows.empty: continue
            buy_price = day_rows.iloc[-1]['close']
            
            sig = calc_score_v2(sub)
            if not sig: continue
            score = sig['total']
            
            # 策略：只买80分以上的
            if score >= 80:
                scored.append({'code': code, 'name': stock.get('name', code), 
                               'score': score, 'buy_price': buy_price})
        
        if len(scored) < 1: continue
        
        # 最多买5只，等权
        top5 = sorted(scored, key=lambda x: x['score'], reverse=True)[:5]
        
        gains = []
        stock_details = []
        for s in top5:
            sell = get_price_n_days_later(kline_cache[s['code']], date_str, 5)
            if sell and s['buy_price']:
                gain = (sell / s['buy_price'] - 1) * 100
                gains.append(gain)
                stock_details.append(f"{s['name']}({gain:+.1f}%)")
        
        if not gains: continue
        
        avg_gain = sum(gains) / len(gains)
        weeks.append({
            'date': date_str,
            'avg_gain': round(avg_gain, 2),
            'n_stocks': len(gains),
            'scores': [s['score'] for s in top5[:len(gains)]],
            'details': stock_details,
            'max_score': max(s['score'] for s in top5[:len(gains)]) if top5 else 0
        })
    
    return weeks


def summarize(weeks, year):
    if not weeks:
        print(f"{year}: 无数据")
        return
    
    gains = [w['avg_gain'] for w in weeks]
    wins = sum(1 for g in gains if g > 0)
    total = sum(gains)
    avg = total / len(gains)
    annual = avg * 52
    
    print(f"\n{'='*60}")
    print(f"  {year}年 策略回测")
    print(f"{'='*60}")
    print(f"  样本周数: {len(weeks)}")
    print(f"  平均周收益: {avg:+.2f}%")
    print(f"  累计收益: {total:+.2f}%")
    print(f"  年化收益: {annual:+.1f}%")
    print(f"  胜率: {wins}/{len(weeks)} = {wins/len(weeks)*100:.0f}%")
    print(f"  最大盈利: {max(gains):+.2f}%")
    print(f"  最大亏损: {min(gains):+.2f}%")
    
    # 月度
    monthly = defaultdict(list)
    for w in weeks:
        monthly[w['date'][:7]].append(w['avg_gain'])
    
    print(f"\n  月度表现:")
    for m in sorted(monthly):
        gs = monthly[m]
        tag = '✅' if sum(gs)/len(gs) > 0 else '❌'
        print(f"    {m}: {sum(gs)/len(gs):+.2f}% {tag}")
    
    # 有80分以上的周数
    weeks_80plus = sum(1 for w in weeks if w['max_score'] >= 80)
    print(f"\n  有80分以上股票的周: {weeks_80plus}/{len(weeks)} ({weeks_80plus/len(weeks)*100:.0f}%)")
    
    return {'weeks': weeks, 'total': total, 'avg': avg, 'annual': annual, 'winrate': wins/len(weeks)*100}


if __name__ == '__main__':
    results = {}
    for year in [2023, 2024]:
        weeks = run_backtest(year)
        results[year] = summarize(weeks, year)
        time.sleep(1)
    
    # 对比
    print(f"\n{'='*60}")
    print(f"  策略对比")
    print(f"{'='*60}")
    print(f"{'年份':<8} {'平均周收益':>12} {'年化收益':>10} {'胜率':>8}")
    print(f"{'-'*40}")
    for year, r in results.items():
        if r:
            print(f"{year}年    {r['avg']:>+12.2f}% {r['annual']:>+10.1f}% {r['winrate']:>7.0f}%")
    
    # 保存
    with open(DATA_DIR / 'backtest_80plus.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到 backtest_80plus.json")