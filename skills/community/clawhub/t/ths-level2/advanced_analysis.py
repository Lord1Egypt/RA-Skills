# -*- coding: utf-8 -*-
"""
同花顺高级数据分析 - 资金抄底、神奇五线谱、主力资金
"""
import os
import sys
import json
import statistics
from datetime import datetime, timedelta

os.environ['PYTHONIOENCODING'] = 'utf-8'

import tushare as ts
import pandas as pd

token = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(token)
pro = ts.pro_api()

print("=" * 80)
print(" 同花顺Level2高级数据分析")
print(" 功能: 资金抄底、神奇五线谱、主力资金")
print(f" 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 80)

# ============ 资金抄底分析 ============
def analyze_capital_bottom(prices, volumes):
    """资金抄底指标"""
    if len(prices) < 20:
        return None
    
    avg_price = statistics.mean(prices[-20:])
    current_price = prices[-1]
    deviation = (current_price - avg_price) / avg_price * 100
    
    vol_ratio = statistics.mean(volumes[-5:]) / statistics.mean(volumes[-20:]) if statistics.mean(volumes[-20:]) > 0 else 1
    
    if deviation < -10 and vol_ratio > 1.2:
        signal, strength = '抄底信号', min(100, abs(deviation) * 5)
        desc = f'严重超跌({deviation:.1f}%)，放量({vol_ratio:.2f}倍)'
    elif deviation < -5:
        signal, strength = '偏弱', 30
        desc = f'低于均价{deviation:.1f}%'
    elif deviation > 10 and vol_ratio < 0.8:
        signal, strength = '见顶信号', min(100, deviation * 3)
        desc = f'严重超涨({deviation:.1f}%)，缩量'
    elif deviation > 5:
        signal, strength = '偏强', 60
        desc = f'高于均价{deviation:.1f}%'
    else:
        signal, strength = '中性', 50
        desc = '正常波动'
    
    return {'signal': signal, 'strength': strength, 'deviation': deviation, 'vol_ratio': vol_ratio, 'desc': desc}

# ============ 神奇五线谱分析 ============
def analyze_magic_five_lines(prices, volumes):
    """神奇五线谱 - 综合均线、成交量、资金流向"""
    if len(prices) < 60:
        return None
    
    current = prices[-1]
    ma5 = statistics.mean(prices[-5:])
    ma10 = statistics.mean(prices[-10:])
    ma20 = statistics.mean(prices[-20:])
    ma60 = statistics.mean(prices[-60:])
    
    vol_ratio = statistics.mean(volumes[-5:]) / statistics.mean(volumes[-20:]) if statistics.mean(volumes[-20:]) > 0 else 1
    
    # 计算资金流向
    up_vol = sum(volumes[i] for i in range(-20, 0) if prices[i] > prices[i-1])
    down_vol = sum(volumes[i] for i in range(-20, 0) if prices[i] <= prices[i-1])
    money_ratio = up_vol / down_vol if down_vol > 0 else 1
    
    score = 50
    if ma5 > ma10 > ma20: score += 20
    elif ma5 < ma10 < ma20: score -= 20
    if current > ma5: score += 5
    if vol_ratio > 1.2: score += 10
    elif vol_ratio < 0.8: score -= 5
    if money_ratio > 1.2: score += 15
    elif money_ratio < 0.8: score -= 15
    
    score = max(0, min(100, score))
    
    lines = {
        'MA5': {'value': ma5, 'pos': '上方' if current > ma5 else '下方'},
        'MA10': {'value': ma10, 'pos': '上方' if current > ma10 else '下方'},
        'MA20': {'value': ma20, 'pos': '上方' if current > ma20 else '下方'},
        'Volume': {'ratio': vol_ratio, 'trend': '放量' if vol_ratio > 1.2 else '缩量' if vol_ratio < 0.8 else '正常'},
        'MoneyFlow': {'ratio': money_ratio, 'trend': '流入' if money_ratio > 1.2 else '流出' if money_ratio < 0.8 else '平衡'}
    }
    
    if score >= 70: signal = '强势'
    elif score >= 55: signal = '偏强'
    elif score >= 45: signal = '中性'
    elif score >= 30: signal = '偏弱'
    else: signal = '弱势'
    
    return {'score': score, 'signal': signal, 'lines': lines}

# ============ 主力资金分析 ============
def analyze_main_capital(prices, volumes):
    """主力资金动向分析"""
    if len(prices) < 20:
        return None
    
    up_vol = sum(volumes[i] for i in range(-20, 0) if prices[i] > prices[i-1])
    down_vol = sum(volumes[i] for i in range(-20, 0) if prices[i] <= prices[i-1])
    ratio = up_vol / down_vol if down_vol > 0 else 1
    
    vol_trend = statistics.mean(volumes[-5:]) / statistics.mean(volumes[-20:]) if statistics.mean(volumes[-20:]) > 0 else 1
    
    if ratio > 1.5:
        trend, strength, analysis = '主力做多', min(100, (ratio-1)*50), '上涨放量，资金积极买入'
    elif ratio < 0.67:
        trend, strength, analysis = '主力出逃', min(100, (1-ratio)*50), '下跌放量，资金撤离'
    else:
        trend, strength, analysis = '多空平衡', 50, '量价关系正常'
    
    return {'trend': trend, 'strength': strength, 'ratio': ratio, 'vol_trend': vol_trend, 'analysis': analysis}

# ============ 分析单只股票 ============
def analyze_stock(code, name):
    print(f"\n{'='*80}")
    print(f" {name} ({code})")
    print("="*80)
    
    try:
        end = datetime.now().strftime('%Y%m%d')
        start = (datetime.now() - timedelta(days=120)).strftime('%Y%m%d')
        df = pro.daily(ts_code=code, start_date=start, end_date=end)
        if df is None or len(df) == 0:
            print("  无数据")
            return None
        df = df.sort_values('trade_date')
        prices = df['close'].tolist()
        volumes = df['vol'].tolist()
    except Exception as e:
        print(f"  获取失败: {e}")
        return None
    
    print(f"  最新价: {prices[-1]:.2f}元")
    
    # 资金抄底
    print(f"\n  [资金抄底]")
    bottom = analyze_capital_bottom(prices, volumes)
    if bottom:
        print(f"    信号: {bottom['signal']} ({bottom['strength']:.0f}%)")
        print(f"    偏离: {bottom['deviation']:.1f}%, 量比: {bottom['vol_ratio']:.2f}")
    
    # 神奇五线谱
    print(f"\n  [神奇五线谱]")
    magic = analyze_magic_five_lines(prices, volumes)
    if magic:
        print(f"    评分: {magic['score']:.0f}分 - {magic['signal']}")
        for ln, ld in magic['lines'].items():
            if ln.startswith('MA'):
                print(f"    {ln}: {ld['value']:.2f} ({ld['pos']})")
            else:
                print(f"    {ln}: {ld.get('trend', ld.get('ratio', 'N/A'))}")
    
    # 主力资金
    print(f"\n  [主力资金]")
    capital = analyze_main_capital(prices, volumes)
    if capital:
        print(f"    趋势: {capital['trend']} ({capital['strength']:.0f}%)")
        print(f"    分析: {capital['analysis']}")
    
    total = (bottom['strength'] + magic['score'] + capital['strength']) / 3 if bottom and magic and capital else 0
    
    return {'code': code, 'name': name, 'price': prices[-1], 'bottom': bottom, 'magic': magic, 'capital': capital, 'total': total}

# ============ 主函数 ============
def main():
    stocks = [
        ('600760.SH', '中航沈飞'), ('601888.SH', '中国中免'),
        ('600276.SH', '恒瑞医药'), ('002202.SZ', '金风科技'),
        ('688235.SH', '百济神州'), ('300188.SZ', '美亚柏科'),
    ]
    
    results = [analyze_stock(c, n) for c, n in stocks]
    results = [r for r in results if r]
    
    print("\n" + "="*80)
    print(" 综合排名")
    print("="*80)
    print(f"\n| 股票 | 价格 | 抄底信号 | 五线评分 | 主力趋势 | 综合 |")
    print("|------|------|----------|----------|----------|------|")
    for r in sorted(results, key=lambda x: x['total'], reverse=True):
        b = r['bottom']['signal'] if r['bottom'] else '-'
        m = f"{r['magic']['score']:.0f}" if r['magic'] else '-'
        c = r['capital']['trend'] if r['capital'] else '-'
        print(f"| {r['name']} | {r['price']:.2f} | {b} | {m}分 | {c} | {r['total']:.0f} |")

if __name__ == '__main__':
    main()