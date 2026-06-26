#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策略回测 v3: 70分以上等权持有5天
用 baostock 批量加载，预先计算所有指标
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


def fetch_all():
    bs.login()
    stocks = get_filtered_stock_list()
    cache = {}
    for i, s in enumerate(stocks):
        bs_code = f'sh.{s["code"]}' if s['code'].startswith('6') else f'sz.{s["code"]}'
        rs = bs.query_history_k_data_plus(
            bs_code,
            'date,open,high,low,close,volume',
            start_date='2023-09-01',
            end_date='2024-12-31',
            frequency='d',
            adjustflag='2'
        )
        if rs is None or rs.error_msg != 'success':
            time.sleep(0.05)
            continue
        rows = []
        while rs.next():
            r = rs.get_row_data()
            if len(r) >= 6 and r[0] and r[4]:
                try:
                    rows.append({
                        'date': pd.to_datetime(r[0]),
                        'close': float(r[4]),
                        'volume': float(r[5]) if r[5] else 0
                    })
                except:
                    pass
        if rows:
            df = pd.DataFrame(rows).sort_values('date').reset_index(drop=True)
            cache[s['code']] = {'name': s.get('name', s['code']), 'df': df}
        if (i+1) % 50 == 0:
            print(f'  {i+1}/{len(stocks)}', flush=True)
        time.sleep(0.05)
    bs.logout()
    return cache


def compute_indicators(df):
    """预先计算所有指标，避免切片后缺失列"""
    df = df.copy()
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


def backtest_year(cache, year):
    # 生成当年每周一
    dates = []
    cur = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    while cur <= end:
        if cur.weekday() == 0:
            dates.append(cur)
        cur += timedelta(days=1)

    weeks = []
    for d in dates:
        d_str = d.strftime('%Y-%m-%d')
        scored = []

        for code, info in cache.items():
            df_full = info['df']
            # 截取到当天
            df_sub = df_full[df_full['date'] <= d].copy()
            if len(df_sub) < 30:
                continue
            # 当天是否交易
            day_rows = df_sub[df_sub['date'] == d]
            if day_rows.empty:
                continue

            # 预先计算指标
            df_ind = compute_indicators(df_sub)
            day_row = df_ind[df_ind['date'] == d].iloc[-1]
            buy_price = day_row['close']

            sig = calc_score_v2(df_ind)
            if sig and sig['total'] >= 70:
                scored.append({
                    'code': code,
                    'name': info['name'],
                    'score': sig['total'],
                    'buy': buy_price,
                    'date': d
                })

        if not scored:
            continue

        top5 = sorted(scored, key=lambda x: x['score'], reverse=True)[:5]
        gains = []
        for s in top5:
            df2 = cache[s['code']]['df']
            idx_list = df2.index[df2['date'] == s['date']].tolist()
            if not idx_list:
                continue
            sell_idx = idx_list[0] + 5
            if sell_idx < len(df2):
                sell_price = df2.iloc[sell_idx]['close']
                gains.append((sell_price / s['buy'] - 1) * 100)

        if gains:
            weeks.append({
                'date': d_str,
                'avg_gain': round(sum(gains) / len(gains), 2),
                'n': len(gains),
                'max_score': max(s['score'] for s in top5[:len(gains)])
            })

    return weeks


def summarize(weeks, year):
    if not weeks:
        print(f'{year}: 无数据')
        return None
    gains = [w['avg_gain'] for w in weeks]
    wins = sum(1 for g in gains if g > 0)
    total = sum(gains)
    avg = total / len(gains)
    return {
        'year': year,
        'weeks': len(weeks),
        'total': round(total, 2),
        'avg': round(avg, 2),
        'annual': round(avg * 52, 1),
        'winrate': round(wins / len(gains) * 100, 0),
        'max_win': round(max(gains), 2),
        'max_loss': round(min(gains), 2),
        'weeks_70plus': sum(1 for w in weeks if w['max_score'] >= 70)
    }


if __name__ == '__main__':
    print('加载K线数据...', flush=True)
    cache = fetch_all()
    print(f'加载完成: {len(cache)}只', flush=True)

    results = {}
    for year in [2023, 2024]:
        print(f'\n回测 {year}（70分以上）...', flush=True)
        weeks = backtest_year(cache, year)
        r = summarize(weeks, year)
        if r:
            results[year] = r
            print(f'  周数: {r["weeks"]}')
            print(f'  平均周收益: {r["avg"]:+.2f}%')
            print(f'  累计: {r["total"]:+.2f}%')
            print(f'  年化: {r["annual"]:+.1f}%')
            print(f'  胜率: {r["winrate"]:.0f}%')
            print(f'  最大盈利: {r["max_win"]:+.2f}%')
            print(f'  最大亏损: {r["max_loss"]:+.2f}%')

    # 对比
    print(f'\n{"="*50}')
    print(f'  策略对比: 80分以上等权持有5天')
    print(f'{"="*50}')
    print(f'{"年份":<6} {"周数":>4} {"平均周益":>10} {"累计":>8} {"年化":>8} {"胜率":>6}')
    print(f'{"-"*45}')
    for year, r in results.items():
        print(f'{year}   {r["weeks"]:>4} {r["avg"]:>+10.2f}% {r["total"]:>+7.2f}% {r["annual"]:>+7.1f}% {r["winrate"]:>5.0f}%')

    with open(DATA_DIR / 'backtest_70plus_v2.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f'\n结果已保存到 backtest_70plus_v2.json', flush=True)
