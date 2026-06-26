#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOP5等权策略历史回测 - 使用baostock
支持2023年、2024年、2025年历史数据
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
BACKTEST_FILE = DATA_DIR / "top5_backtest_2023_2024.json"


def init_baostock():
    """初始化baostock"""
    bs.login()


def logout_baostock():
    """登出baostock"""
    bs.logout()


def fetch_klines(code, start_date, end_date):
    """获取K线数据（前复权）"""
    # 转换代码格式
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
        adjustflag='2'  # 前复权
    )
    
    if rs.error_msg != 'success':
        return []
    
    data_list = []
    while rs.next():
        row = rs.get_row_data()
        # baostock 返回 6 个字段: date, open, high, low, close, volume (索引 0-5)
        if len(row) >= 6 and row[0] and row[4]:  # 有日期和收盘价
            try:
                data_list.append({
                    'date': row[0],
                    'open': float(row[1]) if row[1] else 0,
                    'high': float(row[2]) if row[2] else 0,
                    'low': float(row[3]) if row[3] else 0,
                    'close': float(row[4]) if row[4] else 0,
                    'volume': float(row[5]) if row[5] else 0,
                })
            except (ValueError, IndexError):
                continue
    
    return data_list


def calculate_indicators(klines, date):
    """根据历史数据计算技术指标"""
    # 找到date之前的所有数据
    prices = []
    volumes = []
    
    for candle in klines:
        if candle['date'] <= date:
            prices.append(candle['close'])
            volumes.append(candle['volume'])
    
    if len(prices) < 30:
        return None
    
    close = prices[-1]
    
    # 均线
    ma5 = np.mean(prices[-5:]) if len(prices) >= 5 else close
    ma10 = np.mean(prices[-10:]) if len(prices) >= 10 else close
    ma20 = np.mean(prices[-20:]) if len(prices) >= 20 else close
    
    # RSI (14日)
    if len(prices) >= 15:
        deltas = [prices[i] - prices[i-1] for i in range(len(prices)-14, len(prices))]
    else:
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    
    gains = [d for d in deltas if d > 0]
    losses = [-d for d in deltas if d < 0]
    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 0.0001
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    # RSI变化
    if len(prices) >= 20:
        old_deltas = [prices[i] - prices[i-1] for i in range(len(prices)-14, len(prices)-7)]
        old_gains = [d for d in old_deltas if d > 0]
        old_losses = [-d for d in old_deltas if d < 0]
        old_avg_gain = sum(old_gains) / len(old_gains) if old_gains else 0
        old_avg_loss = sum(old_losses) / len(old_losses) if old_losses else 0.0001
        old_rs = old_avg_gain / old_avg_loss
        rsi_old = 100 - (100 / (1 + old_rs))
    else:
        rsi_old = 50
    
    rsi_rising = rsi > rsi_old
    
    # MACD (12,26,9)
    ema12 = close
    ema26 = close
    alpha12 = 2 / 13
    alpha26 = 2 / 27
    for p in prices[-30:]:
        ema12 = p * alpha12 + ema12 * (1 - alpha12)
        ema26 = p * alpha26 + ema26 * (1 - alpha26)
    
    macd = ema12 - ema26
    signal = macd * 0.8
    hist = macd - signal
    
    # 布林带
    bbands = prices[-20:]
    std = np.std(bbands)
    middle = np.mean(bbands)
    upper = middle + 2 * std
    lower = middle - 2 * std
    boll_pos = (close - lower) / (upper - lower) if (upper - lower) > 0 else 0.5
    
    # 5日涨幅
    gain_5d = (close / prices[-6] - 1) * 100 if len(prices) >= 6 else 0
    
    # 量比
    vol5_avg = np.mean(volumes[-5:]) if len(volumes) >= 5 else volumes[-1]
    vol_ratio = volumes[-1] / vol5_avg if vol5_avg > 0 else 1
    
    # 窗口内上涨天数
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
        'boll_pos': boll_pos,
        'gain_5d': gain_5d,
        'vol_ratio': vol_ratio,
        'rising_days': rising_days,
        'ma_bullish': ma_bullish,
    }


def calc_score(ind):
    """计算趋势评分"""
    if not ind:
        return 0
    
    score = 0
    
    # MACD柱线正 (25分)
    if ind['macd_hist'] > 0:
        score += 25
    
    # 价格>MA20 (20分)
    if ind['close'] > ind['ma20']:
        score += 20
    
    # RSI上升 (15分)
    if ind['rsi_rising']:
        score += 15
    
    # RSI>50 (15分)
    if ind['rsi'] > 50:
        score += 15
    
    # 窗口内上涨 (10分)
    if ind['rising_days'] >= 3:
        score += 10
    
    # 均线多头 (10分)
    if ind['ma_bullish']:
        score += 10
    
    # MACD柱增量 (5分)
    if ind['macd_hist'] > 0:
        score += 5
    
    return score


def get_nday_later_price(klines, start_date, n=5):
    """获取N个交易日后的收盘价"""
    count = 0
    for candle in klines:
        if candle['date'] > start_date:
            count += 1
            if count >= n:
                return candle['close'], candle['date']
    return None, None


def run_backtest(period):
    """
    执行回测
    period: '2023', '2024', '2025', '2023_2024', 'full'
    """
    init_baostock()
    
    # 加载股票池
    sys.path.insert(0, str(Path(__file__).parent))
    from stock_pool_filtered import get_filtered_stock_list
    stocks = get_filtered_stock_list()
    
    # 确定回测区间
    if period == '2023':
        start_date = '2023-01-01'
        end_date = '2023-12-31'
    elif period == '2024':
        start_date = '2024-01-01'
        end_date = '2024-12-31'
    elif period == '2025':
        start_date = '2025-01-01'
        end_date = '2025-12-31'
    elif period == '2023_2024':
        start_date = '2023-01-01'
        end_date = '2024-12-31'
    else:
        start_date = '2023-01-01'
        end_date = '2026-03-31'
    
    # 提前下载足够的数据（需要历史数据计算指标）
    data_start = (datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=120)).strftime('%Y-%m-%d')
    
    print(f"正在加载 {len(stocks)} 只股票的历史数据...")
    print(f"回测区间: {start_date} ~ {end_date}")
    
    # 批量下载K线数据
    kline_cache = {}
    for i, stock in enumerate(stocks):
        klines = fetch_klines(stock['code'], data_start, end_date)
        if klines:
            kline_cache[stock['code']] = klines
        if (i + 1) % 50 == 0:
            print(f"  已加载 {i+1}/{len(stocks)}...")
        time.sleep(0.05)  # 避免请求过快
    
    print(f"成功加载 {len(kline_cache)} 只股票的数据")
    
    # 生成回测日期列表（每周一）
    dates = []
    current = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current <= end:
        if current.weekday() == 0:  # 周一
            dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    
    print(f"共 {len(dates)} 个回测周")
    print()
    
    logout_baostock()
    
    # 逐周回测
    all_weeks = []
    
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
            
            # 获取买入价格
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
                'indicators': ind,
            })
        
        if len(scored_stocks) < 5:
            continue
        
        # 取TOP5
        top5 = sorted(scored_stocks, key=lambda x: x['score'], reverse=True)[:5]
        
        # 计算5日后收益
        week_result = {
            'date': date,
            'stocks': [],
            'avg_gain': 0,
        }
        
        total_gain = 0
        completed = 0
        
        for stock in top5:
            code = stock['code']
            if code in kline_cache:
                sell_price, sell_date = get_nday_later_price(kline_cache[code], date, 5)
                
                if sell_price and stock['buy_price']:
                    gain = (sell_price / stock['buy_price'] - 1) * 100
                    stock['sell_price'] = sell_price
                    stock['sell_date'] = sell_date
                    stock['gain_pct'] = round(gain, 2)
                    total_gain += gain
                    completed += 1
                else:
                    stock['gain_pct'] = None
            else:
                stock['gain_pct'] = None
        
        if completed > 0:
            week_result['avg_gain'] = round(total_gain / completed, 2)
        
        # 简化stock数据
        week_result['stocks'] = [{
            'code': s['code'],
            'name': s['name'],
            'score': s['score'],
            'gain_pct': s.get('gain_pct'),
        } for s in top5]
        
        all_weeks.append(week_result)
        
        gain_str = f"{week_result['avg_gain']:+.2f}%" if week_result['avg_gain'] else "N/A"
        status = "WIN" if week_result['avg_gain'] > 0 else "LOSS"
        print(f"{date}: TOP5平均 {gain_str} [{status}]")
    
    return all_weeks


def print_report(weeks, period):
    """打印回测报告"""
    if not weeks:
        print("暂无回测数据")
        return
    
    gains = [w['avg_gain'] for w in weeks if w['avg_gain'] != 0]
    
    # 统计
    total_weeks = len(weeks)
    avg_gain = sum(gains) / len(gains) if gains else 0
    total_return = sum(gains)
    win_rate = len([g for g in gains if g > 0]) / len(gains) * 100 if gains else 0
    max_gain = max(gains) if gains else 0
    min_gain = min(gains) if gains else 0
    annual = avg_gain * 52
    
    # 找到最大/最小收益的周
    max_week = None
    min_week = None
    if gains:
        for w in weeks:
            if w['avg_gain'] == max_gain:
                max_week = w
            if w['avg_gain'] == min_gain:
                min_week = w
    
    print()
    print("=" * 70)
    period_name = {
        '2023': '2023年',
        '2024': '2024年',
        '2025': '2025年',
        '2023_2024': '2023-2024年',
        'full': '2023-2026年',
    }.get(period, period)
    print(f"📊 TOP5等权策略回测报告 - {period_name}")
    print("=" * 70)
    print()
    print(f"【策略】每周一等权买入趋势TOP5，持有5个交易日卖出")
    print(f"【区间】{weeks[0]['date']} ~ {weeks[-1]['date']}，共 {total_weeks} 周")
    print()
    
    if gains:
        print("【核心指标】")
        print(f"  平均周收益: {avg_gain:+.2f}%")
        print(f"  累计收益:   {total_return:+.2f}%")
        print(f"  胜率:       {win_rate:.1f}% ({len([g for g in gains if g > 0])}/{len(gains)} 周)")
        print(f"  最大周盈利: {max_gain:+.2f}% ({max_week['date'] if max_week else ''})")
        print(f"  最大周亏损: {min_gain:+.2f}% ({min_week['date'] if min_week else ''})")
        print(f"  年化收益:   {annual:+.1f}%")
        print()
        
        # vs 指数对比
        print("【vs 大盘指数】(假设同期持有等权指数)")
        print(f"  假设同期大盘平均周涨幅: ~{avg_gain*0.5:+.2f}% (参考)")
        if annual > 10:
            print(f"  ✅ 跑赢大盘，年化超额收益约 {annual-10:+.1f}%")
        elif annual > 0:
            print(f"  🟡 略跑赢大盘")
        else:
            print(f"  🔴 跑输大盘")
        print()
    
    print("【逐周明细】")
    print("-" * 70)
    print(f"{'日期':<12} {'收益':>10} {'胜股':>6} {'TOP1':<10} {'TOP2':<10}")
    print("-" * 70)
    
    win_count = 0
    loss_count = 0
    
    for week in sorted(weeks, key=lambda x: x['date']):
        gain = week['avg_gain']
        gain_str = f"{gain:+.2f}%" if gain else "N/A"
        status = "WIN" if gain > 0 else "LOSS"
        if gain > 0:
            win_count += 1
        else:
            loss_count += 1
        
        # 获取TOP3
        top1 = week['stocks'][0] if len(week['stocks']) > 0 else {}
        top2 = week['stocks'][1] if len(week['stocks']) > 1 else {}
        
        top1_str = f"{top1.get('name','')}({top1.get('gain_pct', 0):+.0f}%)" if top1.get('gain_pct') else top1.get('name', '')
        top2_str = f"{top2.get('name','')}({top2.get('gain_pct', 0):+.0f}%)" if top2.get('gain_pct') else top2.get('name', '')
        
        print(f"{week['date']:<12} {gain_str:>10} {status:>6} {top1_str:<12} {top2_str:<12}")
    
    print()
    print("【结论】")
    if avg_gain > 2:
        print(f"  🟢 策略优秀！平均每周盈利 {avg_gain:.2f}%，年化 {annual:.1f}%")
    elif avg_gain > 0:
        print(f"  🟡 策略有效。平均每周盈利 {avg_gain:.2f}%，年化 {annual:.1f}%")
    else:
        print(f"  🔴 策略无效。平均每周亏损 {abs(avg_gain):.2f}%")
    
    print()
    print("⚠️ 回测结果仅供参考，不代表未来表现")
    print()


if __name__ == "__main__":
    period = sys.argv[1] if len(sys.argv) > 1 else '2023_2024'
    
    print(f"\n开始回测: {period}\n")
    
    weeks = run_backtest(period)
    
    # 保存结果
    with open(BACKTEST_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "period": period,
            "weeks": weeks,
            "generated": datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)
    
    print_report(weeks, period)
