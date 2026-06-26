#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOP5等权策略历史回测
用历史K线数据反推过去哪些股票会是TOP5
然后计算持有1周的收益
"""
import pandas as pd
import json
import requests
import time
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

DATA_DIR = Path("C:/Users/Administrator/.qclaw/workspace-ag01/data/trend_scan")
CACHE_DIR = DATA_DIR / "kline_cache"
BACKTEST_FILE = DATA_DIR / "top5_backtest_full.json"


def load_cached_klines(code, force=False):
    """加载或下载K线数据缓存"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{code}.json"
    
    # 30天内的缓存可用
    if cache_file.exists() and not force:
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if (datetime.now() - mtime).days < 1:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
    
    # 下载数据（过去180天）
    code = str(code).zfill(6)
    sym = 'sh' + code if code.startswith('6') else 'sz' + code
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d")
    
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq&param={sym},day,{start_date},{end_date},500,qfq"
    
    try:
        r = requests.get(url, timeout=10)
        text = r.text
        
        if 'kline_dayhfq=' in text:
            json_str = text.split('kline_dayhfq=')[1]
            data = json.loads(json_str)
            
            if 'data' in data and sym in data['data']:
                day_data = data['data'][sym].get('qfqday') or []
                
                # 缓存
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(day_data, f)
                
                return day_data
    except Exception as e:
        print(f"下载{code}数据失败: {e}")
    
    return []


def get_price_on_date(klines, target_date):
    """从K线数据中获取指定日期的价格"""
    for candle in reversed(klines):
        if candle[0] <= target_date:
            return float(candle[2])  # 收盘价
    return None


def get_nday_later_price(klines, start_date, n=5):
    """获取N个交易日后的价格"""
    count = 0
    for candle in klines:
        if candle[0] > start_date:
            count += 1
            if count >= n:
                return float(candle[2]), candle[0]
    return None, None


def calculate_indicators(klines, date):
    """根据历史数据计算技术指标"""
    # 提取截止到date的所有数据
    prices = []
    volumes = []
    
    for candle in klines:
        if candle[0] <= date:
            prices.append(float(candle[2]))  # 收盘
            volumes.append(float(candle[4]))  # 成交量
    
    if len(prices) < 30:
        return None
    
    prices = prices[-60:]  # 保留足够多的数据
    volumes = volumes[-60:]
    
    close = prices[-1]
    
    # 均线
    ma5 = sum(prices[-5:]) / 5
    ma10 = sum(prices[-10:]) / 10
    ma20 = sum(prices[-20:]) / 20
    
    # RSI
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [d for d in deltas if d > 0]
    losses = [-d for d in deltas if d < 0]
    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 0
    rs = avg_gain / avg_loss if avg_loss > 0 else 100
    rsi = 100 - (100 / (1 + rs))
    
    # RSI变化
    rsi_old = 50
    if len(prices) > 10:
        old_deltas = [prices[i] - prices[i-1] for i in range(len(prices)-9, len(prices))]
        old_gains = [d for d in old_deltas if d > 0]
        old_losses = [-d for d in old_deltas if d < 0]
        old_avg_gain = sum(old_gains) / len(old_gains) if old_gains else 0
        old_avg_loss = sum(old_losses) / len(old_losses) if old_losses else 0
        old_rs = old_avg_gain / old_avg_loss if old_avg_loss > 0 else 100
        rsi_old = 100 - (100 / (1 + old_rs))
    
    rsi_rising = rsi > rsi_old
    
    # MACD (12,26,9)
    ema12 = prices[-1]
    ema26 = prices[-1]
    alpha12 = 2 / 13
    alpha26 = 2 / 27
    for p in prices:
        ema12 = p * alpha12 + ema12 * (1 - alpha12)
        ema26 = p * alpha26 + ema26 * (1 - alpha26)
    
    macd = ema12 - ema26
    signal = macd * 0.8  # 简化
    hist = macd - signal
    
    # 布林带
    import numpy as np
    bbands = prices[-20:]
    std = np.std(bbands)
    middle = np.mean(bbands)
    upper = middle + 2 * std
    lower = middle - 2 * std
    boll_pos = (close - lower) / (upper - lower) if (upper - lower) > 0 else 0.5
    
    # 5日涨幅
    gain_5d = (close / prices[-6] - 1) * 100 if len(prices) >= 6 else 0
    
    # 量比
    vol5_avg = sum(volumes[-5:]) / 5 if len(volumes) >= 5 else volumes[-1]
    vol_ratio = volumes[-1] / vol5_avg if vol5_avg > 0 else 1
    
    # 窗口内上涨天数
    window = prices[-5:] if len(prices) >= 5 else prices
    rising_days = sum(1 for i in range(1, len(window)) if window[i] > window[i-1])
    
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
        'ma_bullish': ma5 > ma10 > ma20 if len(prices) >= 20 else ma5 > ma10,
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


def run_backtest(start_date="2026-01-01", end_date=None):
    """执行历史回测"""
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    # 加载股票池
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from stock_pool_filtered import get_filtered_stock_list
    stocks = get_filtered_stock_list()
    
    print(f"加载 {len(stocks)} 只股票的K线数据...")
    
    # 下载所有K线数据
    kline_cache = {}
    for i, stock in enumerate(stocks):
        code = stock['code']
        klines = load_cached_klines(code)
        if klines:
            kline_cache[code] = klines
        if (i + 1) % 20 == 0:
            print(f"  已加载 {i+1}/{len(stocks)}...")
        time.sleep(0.1)  # 避免请求过快
    
    print(f"成功加载 {len(kline_cache)} 只股票的数据")
    print()
    
    # 生成回测日期列表（每周一）
    dates = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    while current <= end:
        if current.weekday() == 0:  # 周一
            dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    
    print(f"回测区间: {dates[0]} ~ {dates[-1]}，共 {len(dates)} 周")
    print()
    
    # 逐周回测
    all_weeks = []
    
    for date in dates:
        # 获取每只股票的评分
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
            buy_price = get_price_on_date(klines, date)
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
        
        week_result['stocks'] = top5
        all_weeks.append(week_result)
        
        gain_str = f"{week_result['avg_gain']:+.2f}%" if week_result['avg_gain'] else "N/A"
        status = "✅" if week_result['avg_gain'] > 0 else "❌"
        print(f"{date}: TOP5平均收益 {gain_str} {status}")
    
    return all_weeks


def print_report(weeks):
    """打印回测报告"""
    if not weeks:
        print("暂无回测数据")
        return
    
    gains = [w['avg_gain'] for w in weeks if w['avg_gain'] != 0]
    
    print()
    print("=" * 70)
    print("📊 TOP5等权策略历史回测报告")
    print("=" * 70)
    print()
    print(f"【策略】每周一等权买入当日趋势TOP5，持有5个交易日后卖出")
    print(f"【区间】{weeks[0]['date']} ~ {weeks[-1]['date']}，共 {len(weeks)} 周")
    print()
    
    if gains:
        print("【汇总统计】")
        print(f"  平均周收益: {sum(gains)/len(gains):+.2f}%")
        print(f"  累计收益:   {sum(gains):+.2f}%")
        print(f"  胜率:       {len([g for g in gains if g > 0])/len(gains)*100:.1f}%")
        print(f"  最大周盈利: {max(gains):+.2f}%")
        print(f"  最大周亏损: {min(gains):+.2f}%")
        
        #  annualized
        annual = (sum(gains)/len(gains)) * 52
        print(f"  年化收益:   {annual:+.1f}%")
        print()
    
    print("【逐周明细】")
    print("-" * 70)
    print(f"{'日期':<12} {'平均收益':>10} {'胜股数':>8} {'TOP5明细'}")
    print("-" * 70)
    
    for week in sorted(weeks, key=lambda x: x['date']):
        gain = week['avg_gain']
        gain_str = f"{gain:+.2f}%" if gain else "N/A"
        status = "✅" if gain > 0 else "❌"
        
        # 计算胜股数
        completed = [s for s in week['stocks'] if s.get('gain_pct') is not None]
        winners = len([s for s in completed if s['gain_pct'] > 0])
        completed_count = len(completed) if completed else 0
        detail = " / ".join([
            f"{s['name']}({s['gain_pct']:+.0f}%)" if s.get('gain_pct') is not None else f"{s['name']}(?)" 
            for s in week['stocks'][:3]
        ])
        
        print(f"{week['date']:<12} {gain_str:>10} {status} {winners}/{completed_count:<4}  {detail}")
    
    print()
    print("⚠️ 回测结果仅供参考，不代表未来表现")
    print()


if __name__ == "__main__":
    import sys
    
    # 默认回测最近3个月
    start = "2025-12-29"  # 从2026年初开始
    
    if len(sys.argv) > 1:
        start = sys.argv[1]
    
    weeks = run_backtest(start_date=start)
    
    # 保存结果
    with open(BACKTEST_FILE, "w", encoding="utf-8") as f:
        json.dump({"weeks": weeks, "generated": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
    
    print_report(weeks)
