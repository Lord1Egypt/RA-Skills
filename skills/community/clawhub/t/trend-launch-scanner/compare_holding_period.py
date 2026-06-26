#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOP5等权策略 - 不同持有期对比
测试持有1天、3天、5天、7天、10天、14天
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

DATA_DIR = Path("C:/Users/Administrator/.qclaw/workspace-ag01/data/trend_scan")


def init_baostock():
    bs.login()


def logout_baostock():
    bs.logout()


def fetch_klines(code, start_date, end_date):
    if code.startswith('6'):
        bs_code = f'sh.{code}'
    else:
        bs_code = f'sz.{code}'
    
    rs = bs.query_history_k_data_plus(
        bs_code,
        'date,open,high,low,close,volume',
        start_date=start_date,
        end_date=end_date,
        frequency='d',
        adjustflag='2'
    )
    
    if rs.error_msg != 'success':
        return []
    
    data_list = []
    while rs.next():
        row = rs.get_row_data()
        if len(row) >= 6 and row[0] and row[4]:
            try:
                data_list.append({
                    'date': row[0],
                    'close': float(row[4]),
                    'volume': float(row[5]) if row[5] else 0,
                })
            except:
                continue
    return data_list


def calculate_indicators(klines, date):
    prices = []
    volumes = []
    
    for candle in klines:
        if candle['date'] <= date:
            prices.append(candle['close'])
            volumes.append(candle['volume'])
    
    if len(prices) < 30:
        return None
    
    close = prices[-1]
    ma5 = np.mean(prices[-5:]) if len(prices) >= 5 else close
    ma10 = np.mean(prices[-10:]) if len(prices) >= 10 else close
    ma20 = np.mean(prices[-20:]) if len(prices) >= 20 else close
    
    # RSI
    deltas = [prices[i] - prices[i-1] for i in range(len(prices)-14, len(prices))]
    gains = [d for d in deltas if d > 0]
    losses = [-d for d in deltas if d < 0]
    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 0.0001
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    # RSI变化
    old_deltas = [prices[i] - prices[i-1] for i in range(len(prices)-14, len(prices)-7)]
    old_gains = [d for d in old_deltas if d > 0]
    old_losses = [-d for d in old_deltas if d < 0]
    old_avg_gain = sum(old_gains) / len(old_gains) if old_gains else 0
    old_avg_loss = sum(old_losses) / len(old_losses) if old_losses else 0.0001
    old_rs = old_avg_gain / old_avg_loss
    rsi_old = 100 - (100 / (1 + old_rs))
    rsi_rising = rsi > rsi_old
    
    # MACD
    ema12 = close
    ema26 = close
    for p in prices[-30:]:
        ema12 = p * (2/13) + ema12 * (11/13)
        ema26 = p * (2/27) + ema26 * (25/27)
    macd = ema12 - ema26
    hist = macd - macd * 0.8
    
    # 5日涨幅
    gain_5d = (close / prices[-6] - 1) * 100 if len(prices) >= 6 else 0
    
    # 窗口上涨
    window = prices[-5:] if len(prices) >= 5 else prices
    rising_days = sum(1 for i in range(1, len(window)) if window[i] > window[i-1])
    
    # 均线多头
    ma_bullish = ma5 > ma10 > ma20 if len(prices) >= 20 else ma5 > ma10
    
    return {
        'close': close,
        'ma5': ma5,
        'ma10': ma10,
        'ma20': ma20,
        'rsi': rsi,
        'rsi_rising': rsi_rising,
        'macd_hist': hist,
        'gain_5d': gain_5d,
        'rising_days': rising_days,
        'ma_bullish': ma_bullish,
    }


def calc_score(ind):
    if not ind:
        return 0
    score = 0
    if ind['macd_hist'] > 0:
        score += 25
    if ind['close'] > ind['ma20']:
        score += 20
    if ind['rsi_rising']:
        score += 15
    if ind['rsi'] > 50:
        score += 15
    if ind['rising_days'] >= 3:
        score += 10
    if ind['ma_bullish']:
        score += 10
    if ind['macd_hist'] > 0:
        score += 5
    return score


def get_nday_later_price(klines, start_date, n):
    count = 0
    for candle in klines:
        if candle['date'] > start_date:
            count += 1
            if count >= n:
                return candle['close'], candle['date']
    return None, None


def run_backtest_for_days(n_days, period='2024'):
    if period == '2024':
        start_date = '2024-01-01'
        end_date = '2024-12-31'
    else:
        start_date = '2023-01-01'
        end_date = '2024-12-31'
    
    init_baostock()
    
    sys.path.insert(0, str(Path(__file__).parent))
    from stock_pool_filtered import get_filtered_stock_list
    stocks = get_filtered_stock_list()
    
    data_start = (datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=120)).strftime('%Y-%m-%d')
    
    print(f"加载K线数据... (持有{n_days}天测试)")
    
    kline_cache = {}
    for stock in stocks:
        klines = fetch_klines(stock['code'], data_start, end_date)
        if klines:
            kline_cache[stock['code']] = klines
    time.sleep(0.05)
    
    logout_baostock()
    
    # 生成回测日期
    dates = []
    current = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    while current <= end:
        if current.weekday() == 0:
            dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    
    weeks = []
    for date in dates:
        scored_stocks = []
        
        for stock in stocks:
            code = stock['code']
            if code not in kline_cache:
                continue
            
            klines = kline_cache[code]
            ind = calculate_indicators(klines, date)
            if not ind:
                continue
            
            score = calc_score(ind)
            
            buy_price = None
            for candle in klines:
                if candle['date'] == date:
                    buy_price = candle['close']
                    break
            
            if not buy_price:
                continue
            
            scored_stocks.append({
                'code': code,
                'name': stock['name'],
                'score': score,
                'buy_price': buy_price,
            })
        
        if len(scored_stocks) < 5:
            continue
        
        top5 = sorted(scored_stocks, key=lambda x: x['score'], reverse=True)[:5]
        
        week_result = {'date': date, 'stocks': [], 'avg_gain': 0}
        total_gain = 0
        completed = 0
        
        for stock in top5:
            code = stock['code']
            if code in kline_cache:
                sell_price, sell_date = get_nday_later_price(kline_cache[code], date, n_days)
                if sell_price and stock['buy_price']:
                    gain = (sell_price / stock['buy_price'] - 1) * 100
                    stock['gain_pct'] = round(gain, 2)
                    total_gain += gain
                    completed += 1
                else:
                    stock['gain_pct'] = None
            else:
                stock['gain_pct'] = None
        
        if completed > 0:
            week_result['avg_gain'] = round(total_gain / completed, 2)
        
        week_result['stocks'] = [{
            'code': s['code'],
            'name': s['name'],
            'score': s['score'],
            'gain_pct': s.get('gain_pct'),
        } for s in top5]
        
        weeks.append(week_result)
    
    return weeks


def analyze_results(all_results):
    print("\n" + "=" * 70)
    print("📊 不同持有期对比分析")
    print("=" * 70)
    print()
    print(f"{'持有期':<8} {'平均收益':>10} {'累计收益':>10} {'胜率':>8} {'最大盈利':>10} {'最大亏损':>10} {'年化':>8}")
    print("-" * 70)
    
    for n_days, weeks in all_results:
        gains = [w['avg_gain'] for w in weeks if w['avg_gain'] != 0]
        if not gains:
            continue
        
        avg = sum(gains) / len(gains)
        total = sum(gains)
        win_rate = len([g for g in gains if g > 0]) / len(gains) * 100
        max_gain = max(gains)
        max_loss = min(gains)
        annual = avg * (52 / (n_days / 5))  # 折算到周
        
        print(f"{n_days}天{'':<5} {avg:>+10.2f}% {total:>+10.2f}% {win_rate:>7.0f}% {max_gain:>+10.2f}% {max_loss:>+10.2f}% {annual:>+7.1f}%")
    
    print()
    
    # 找最优持有期
    best = None
    best_avg = -999
    for n_days, weeks in all_results:
        gains = [w['avg_gain'] for w in weeks if w['avg_gain'] != 0]
        if gains:
            avg = sum(gains) / len(gains)
            if avg > best_avg:
                best_avg = avg
                best = n_days
    
    if best:
        print(f"✅ 最优持有期: {best}天 (平均收益 {best_avg:+.2f}%)")
    
    print()
    print("⚠️ 回测结果仅供参考，不代表未来表现")


if __name__ == "__main__":
    periods_to_test = [1, 3, 5, 7, 10, 14]
    all_results = []
    
    for n_days in periods_to_test:
        print(f"\n测试持有{n_days}天...")
        weeks = run_backtest_for_days(n_days, period='2024')
        all_results.append((n_days, weeks))
    
    analyze_results(all_results)
