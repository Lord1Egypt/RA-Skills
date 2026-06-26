#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新旧评分对比 - 基于已有回测数据
策略：
  旧评分：直接用 top5_backtest_2023_2024.json（已有结果）
  新评分：重新用 score_v2 对同一批股票打分，看选出的TOP5是否不同，收益是否更好
"""
import baostock as bs
import pandas as pd
import numpy as np
import sys, json, time
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

sys.path.insert(0, 'C:/Users/Administrator/.qclaw/workspace-ag01/skills/trend-launch-scanner')
from stock_pool_filtered import get_filtered_stock_list
from score_v2 import calc_score_v2

DATA_DIR = Path("C:/Users/Administrator/.qclaw/workspace-ag01/data/trend_scan")

# ── 加载旧回测结果 ──────────────────────────────────────
with open(DATA_DIR / 'top5_backtest_2023_2024.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

old_weeks = old_data['weeks']
print(f"旧回测数据: {len(old_weeks)} 周", flush=True)

# ── 只取2024年的周 ──────────────────────────────────────
old_2024 = [w for w in old_weeks if w['date'].startswith('2024')]
print(f"2024年: {len(old_2024)} 周", flush=True)

# ── 旧评分汇总 ──────────────────────────────────────────
old_gains = [w['avg_gain'] for w in old_2024 if w['avg_gain'] != 0]
print(f"\n旧评分 2024年:")
print(f"  平均周收益: {sum(old_gains)/len(old_gains):+.2f}%")
print(f"  累计收益:   {sum(old_gains):+.2f}%")
print(f"  胜率:       {sum(1 for g in old_gains if g>0)}/{len(old_gains)} = {sum(1 for g in old_gains if g>0)/len(old_gains)*100:.0f}%")
print(f"  年化:       {sum(old_gains)/len(old_gains)*52:+.1f}%", flush=True)

# ── 用新评分重跑2024年 ──────────────────────────────────
# 分批加载K线，每批50只
stocks = get_filtered_stock_list()
print(f"\n开始新评分回测 (2024年)...", flush=True)
print(f"分批加载K线，每批50只", flush=True)

def fetch_batch(codes, start_date, end_date):
    cache = {}
    bs.login()
    for code in codes:
        bs_code = f'sh.{code}' if code.startswith('6') else f'sz.{code}'
        rs = bs.query_history_k_data_plus(
            bs_code, 'date,open,high,low,close,volume',
            start_date=start_date, end_date=end_date,
            frequency='d', adjustflag='2'
        )
        if rs is None or rs.error_msg != 'success':
            continue
        rows = []
        while rs.next():
            r = rs.get_row_data()
            if len(r) >= 6 and r[0] and r[4]:
                try:
                    rows.append({'date': r[0], 'open': float(r[1]),
                                 'high': float(r[2]), 'low': float(r[3]),
                                 'close': float(r[4]), 'volume': float(r[5]) if r[5] else 0})
                except: continue
        if rows:
            df = pd.DataFrame(rows)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
            cache[code] = df
    bs.logout()
    return cache

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

SECTOR_KEYWORDS = {
    '医药': ['制药','药业','医药','生物','医疗','健康','康','药'],
    '证券': ['证券','基金','投资'],
    '银行': ['银行'], '保险': ['保险'],
    '白酒': ['酒','茅台','五粮'],
    '化工': ['化工','化学','材料'],
}
def guess_sector(code, name):
    for sector, kws in SECTOR_KEYWORDS.items():
        for kw in kws:
            if kw in name: return sector
    return f'other_{code[:3]}'

def get_price_n_later(df, date_str, n):
    idx_list = df.index[df['date'].dt.strftime('%Y-%m-%d') == date_str].tolist()
    if not idx_list:
        for i in range(5):
            d = (datetime.strptime(date_str,'%Y-%m-%d')+timedelta(days=i)).strftime('%Y-%m-%d')
            idx_list = df.index[df['date'].dt.strftime('%Y-%m-%d') == d].tolist()
            if idx_list: break
    if not idx_list: return None
    target = idx_list[0] + n
    return df.iloc[target]['close'] if target < len(df) else None

# 生成2024年每周一
dates = []
cur = datetime(2024,1,1)
while cur <= datetime(2024,12,31):
    if cur.weekday() == 0:
        dates.append(cur.strftime('%Y-%m-%d'))
    cur += timedelta(days=1)

data_start = '2023-09-01'
end_date   = '2024-12-31'
codes = [s['code'] for s in stocks]

# 分批加载
kline_cache = {}
batch_size = 60
for i in range(0, len(codes), batch_size):
    batch = codes[i:i+batch_size]
    print(f"  加载 {i+1}~{min(i+batch_size, len(codes))}/{len(codes)}...", flush=True)
    batch_data = fetch_batch(batch, data_start, end_date)
    for code, df in batch_data.items():
        kline_cache[code] = add_indicators(df)
    time.sleep(1)

print(f"成功加载 {len(kline_cache)} 只", flush=True)

# 回测
new_weeks = []
for date_str in dates:
    scored = []
    for stock in stocks:
        code = stock['code']
        name = stock.get('name', code)
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
        if score >= 55:
            scored.append({'code': code, 'name': name, 'score': score,
                           'buy_price': buy_price, 'sector': guess_sector(code, name)})

    if len(scored) < 5: continue
    scored.sort(key=lambda x: x['score'], reverse=True)
    sector_used = defaultdict(int)
    top5 = []
    for s in scored:
        if sector_used[s['sector']] < 1:
            top5.append(s)
            sector_used[s['sector']] += 1
        if len(top5) >= 5: break

    if len(top5) < 3: continue
    gains = []
    for s in top5:
        sell = get_price_n_later(kline_cache[s['code']], date_str, 5)
        if sell and s['buy_price']:
            gains.append((sell/s['buy_price']-1)*100)
    if not gains: continue
    avg = sum(gains)/len(gains)
    new_weeks.append({'date': date_str, 'avg_gain': round(avg,2),
                      'stocks': [s['name'] for s in top5]})

# ── 汇总对比 ──────────────────────────────────────────
new_gains = [w['avg_gain'] for w in new_weeks]

print(f"\n{'='*55}")
print(f"  2024年 新旧评分对比")
print(f"{'='*55}")
print(f"{'指标':<14} {'旧评分':>10} {'新评分v2':>10}")
print(f"{'-'*36}")
print(f"{'样本周数':<14} {len(old_gains):>10} {len(new_gains):>10}")
print(f"{'平均周收益':<14} {sum(old_gains)/len(old_gains):>+10.2f}% {sum(new_gains)/len(new_gains):>+10.2f}%")
print(f"{'累计收益':<14} {sum(old_gains):>+10.2f}% {sum(new_gains):>+10.2f}%")
print(f"{'年化收益':<14} {sum(old_gains)/len(old_gains)*52:>+10.1f}% {sum(new_gains)/len(new_gains)*52:>+10.1f}%")
print(f"{'胜率':<14} {sum(1 for g in old_gains if g>0)/len(old_gains)*100:>10.0f}% {sum(1 for g in new_gains if g>0)/len(new_gains)*100:>10.0f}%")
print(f"{'最大盈利':<14} {max(old_gains):>+10.2f}% {max(new_gains):>+10.2f}%")
print(f"{'最大亏损':<14} {min(old_gains):>+10.2f}% {min(new_gains):>+10.2f}%")

# 月度对比
print(f"\n月度对比:")
print(f"{'月份':<8} {'旧评分':>8} {'新评分':>8}")
old_monthly = defaultdict(list)
new_monthly = defaultdict(list)
for w in old_2024: old_monthly[w['date'][:7]].append(w['avg_gain'])
for w in new_weeks: new_monthly[w['date'][:7]].append(w['avg_gain'])
for m in sorted(set(list(old_monthly.keys())+list(new_monthly.keys()))):
    og = sum(old_monthly[m])/len(old_monthly[m]) if old_monthly[m] else 0
    ng = sum(new_monthly[m])/len(new_monthly[m]) if new_monthly[m] else 0
    better = '✅新' if ng > og else ('✅旧' if og > ng else '=')
    print(f"  {m}  {og:>+7.2f}%  {ng:>+7.2f}%  {better}")

# 保存
with open(DATA_DIR / 'backtest_v2_2024.json', 'w', encoding='utf-8') as f:
    json.dump({'old': old_2024, 'new': new_weeks}, f, ensure_ascii=False, indent=2)
print(f"\n结果已保存", flush=True)
