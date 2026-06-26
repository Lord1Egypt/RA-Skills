#!/usr/bin/env python3
"""
趋势分析器
基于K线数据，分析价格趋势、支撑阻力位、趋势强度
"""

import argparse
import json
import sys
import os
import pandas as pd
import numpy as np

_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
_trading_src = os.path.join(_base, 'toc-trading', 'src')
if _trading_src not in sys.path:
    sys.path.insert(0, _trading_src)


def analyze_trend(df: pd.DataFrame) -> dict:
    """分析价格趋势"""
    if df is None or len(df) < 20:
        return {'error': '数据不足'}
    
    close = df['close']
    high = df['high']
    low = df['low']
    volume = df['volume']
    
    latest_close = close.iloc[-1]
    
    # === 计算移动均线 ===
    ma5 = close.rolling(5).mean()
    ma10 = close.rolling(10).mean()
    ma20 = close.rolling(20).mean()
    ma60 = close.rolling(60).mean()
    
    # === 趋势判断 ===
    # 基于均线多头排列
    ma_arrangement = '震荡'
    if len(close) >= 20:
        if ma5.iloc[-1] > ma20.iloc[-1] > ma60.iloc[-1]:
            ma_arrangement = '多头排列（上升趋势）'
        elif ma5.iloc[-1] < ma20.iloc[-1] < ma60.iloc[-1]:
            ma_arrangement = '空头排列（下降趋势）'
        else:
            ma_arrangement = '震荡整理'
    
    # === 趋势强度 ===
    # 计算近20日斜率
    x = np.arange(min(20, len(close)))
    y = close.iloc[-min(20, len(close)):].values
    slope = np.polyfit(x, y, 1)[0] if len(x) > 1 else 0
    slope_pct = (slope / latest_close) * 100 if latest_close > 0 else 0
    
    if slope_pct > 0.5:
        strength = '强势上涨'
    elif slope_pct > 0.1:
        strength = '温和上涨'
    elif slope_pct < -0.5:
        strength = '强势下跌'
    elif slope_pct < -0.1:
        strength = '温和下跌'
    else:
        strength = '横盘整理'
    
    # === 支撑位和阻力位 ===
    # 近20日高低点
    recent_high = high.iloc[-20:].max()
    recent_low = low.iloc[-20:].min()
    
    # 布林带
    mid = close.rolling(20).mean()
    std = close.rolling(20).std()
    upper_band = mid + 2 * std
    lower_band = mid - 2 * std
    
    # === 关键价位 ===
    supports = []
    resistances = []
    
    # 均线支撑/阻力
    for ma, name in [(ma5, 'MA5'), (ma10, 'MA10'), (ma20, 'MA20'), (ma60, 'MA60')]:
        val = ma.iloc[-1] if not pd.isna(ma.iloc[-1]) else None
        if val and val < latest_close:
            supports.append({'price': round(val, 2), 'name': name})
        elif val and val > latest_close:
            resistances.append({'price': round(val, 2), 'name': name})
    
    # 前期高低点
    if recent_low < latest_close:
        supports.append({'price': round(recent_low, 2), 'name': '前低'})
    if recent_high > latest_close:
        resistances.append({'price': round(recent_high, 2), 'name': '前高'})
    
    # 布林带
    lower = lower_band.iloc[-1] if not pd.isna(lower_band.iloc[-1]) else None
    upper = upper_band.iloc[-1] if not pd.isna(upper_band.iloc[-1]) else None
    if lower and lower < latest_close:
        supports.append({'price': round(lower, 2), 'name': 'BOLL下轨'})
    if upper and upper > latest_close:
        resistances.append({'price': round(upper, 2), 'name': 'BOLL上轨'})
    
    # 按价格排序
    supports = sorted(supports, key=lambda x: x['price'], reverse=True)[:4]
    resistances = sorted(resistances, key=lambda x: x['price'])[:4]
    
    # === 趋势稳定性 ===
    # 计算R-squared
    if len(x) > 2:
        y_pred = np.poly1d(np.polyfit(x, y, 1))(x)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    else:
        r_squared = 0
    
    stability = '稳定' if r_squared > 0.7 else '一般' if r_squared > 0.4 else '不稳'
    
    return {
        'current_price': round(latest_close, 2),
        'trend': {
            'arrangement': ma_arrangement,
            'strength': strength,
            'slope_pct': round(slope_pct, 3),
            'stability': stability,
            'r_squared': round(r_squared, 3),
        },
        'supports': supports,
        'resistances': resistances,
        'key_levels': {
            'recent_high_20d': round(recent_high, 2),
            'recent_low_20d': round(recent_low, 2),
            'boll_upper': round(upper, 2) if upper else None,
            'boll_mid': round(mid.iloc[-1], 2) if not pd.isna(mid.iloc[-1]) else None,
            'boll_lower': round(lower, 2) if lower else None,
        },
        'moving_averages': {
            'MA5': round(ma5.iloc[-1], 2) if not pd.isna(ma5.iloc[-1]) else None,
            'MA10': round(ma10.iloc[-1], 2) if not pd.isna(ma10.iloc[-1]) else None,
            'MA20': round(ma20.iloc[-1], 2) if not pd.isna(ma20.iloc[-1]) else None,
            'MA60': round(ma60.iloc[-1], 2) if not pd.isna(ma60.iloc[-1]) else None,
        }
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='趋势分析器')
    parser.add_argument('--input', required=True, help='K线数据JSON文件')
    parser.add_argument('--output', default='/tmp/trend.json', help='输出文件')
    
    args = parser.parse_args()
    
    with open(args.input) as f:
        kline_data = json.load(f)
    
    if not kline_data.get('data'):
        print('❌ 无K线数据')
        sys.exit(1)
    
    df = pd.DataFrame(kline_data['data'])
    result = analyze_trend(df)
    
    with open(args.output, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 趋势分析完成")
    print(f"   当前价: {result.get('current_price')}")
    print(f"   趋势: {result['trend']['arrangement']} / {result['trend']['strength']}")
    print(f"   支撑: {[s['price'] for s in result.get('supports', [])[:3]]}")
    print(f"   阻力: {[r['price'] for r in result.get('resistances', [])[:3]]}")
