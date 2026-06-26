#!/usr/bin/env python3
"""
量价分析器
分析成交量与价格的关系，识别放量/缩量、量价背离
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


def analyze_volume(df: pd.DataFrame) -> dict:
    """分析量价关系"""
    if df is None or len(df) < 20:
        return {'error': '数据不足'}
    
    close = df['close']
    volume = df['volume']
    
    latest_close = close.iloc[-1]
    latest_volume = volume.iloc[-1]
    
    # === 成交量均线 ===
    vol_ma5 = volume.rolling(5).mean()
    vol_ma10 = volume.rolling(10).mean()
    vol_ma20 = volume.rolling(20).mean()
    
    # === 量比 ===
    vol_ratio = latest_volume / vol_ma5.iloc[-1] if vol_ma5.iloc[-1] > 0 else 0
    
    # === 量价配合分析 ===
    # 近5日涨跌
    pct_changes = close.pct_change().iloc[-5:]
    vol_changes = volume.pct_change().iloc[-5:]
    
    # 判断量价是否背离
    price_trend = pct_changes.mean()  # 正=上涨趋势
    volume_trend = vol_changes.mean()  # 正=放量趋势
    
    # 量价配合判断
    if price_trend > 0 and volume_trend > 0:
        price_volume = '量价齐升（健康上涨）'
        signal = '偏多'
    elif price_trend > 0 and volume_trend < 0:
        price_volume = '价升量缩（背离，上涨动力不足）'
        signal = '偏空'
    elif price_trend < 0 and volume_trend > 0:
        price_volume = '价跌量增（恐慌抛售）'
        signal = '偏空'
    elif price_trend < 0 and volume_trend < 0:
        price_volume = '量价齐跌（健康回调）'
        signal = '偏多'
    else:
        price_trend = '横盘整理'
        signal = '中性'
    
    # === 放量/缩量分析 ===
    vol_level = '正常'
    if vol_ratio > 3:
        vol_level = '巨量（异常放大，可能变盘）'
    elif vol_ratio > 2:
        vol_level = '显著放量'
    elif vol_ratio > 1.5:
        vol_level = '温和放量'
    elif vol_ratio < 0.5:
        vol_level = '极度缩量（地量，可能见底）'
    elif vol_ratio < 0.8:
        vol_level = '缩量'
    else:
        vol_level = '量能平稳'
    
    # === 换手率 ===
    turnover = df['turnover'].iloc[-1] if 'turnover' in df.columns else None
    
    # === 近5日量价变化 ===
    daily_vol_profile = []
    for i in range(-5, 0):
        if len(close) >= abs(i):
            idx = i
            daily_vol_profile.append({
                'date': str(df['date'].iloc[idx]) if 'date' in df.columns else '',
                'close': round(close.iloc[idx], 2),
                'volume': round(volume.iloc[idx], 0),
                'vol_ratio': round(volume.iloc[idx] / vol_ma5.iloc[idx] if vol_ma5.iloc[idx] > 0 else 0, 2),
                'pct_change': round(pct_changes.iloc[idx] * 100, 2) if idx >= -5 else 0
            })
    
    # === 资金流向估算（简化版） ===
    # 通过涨跌和成交量估算
    price_change = (close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] if len(close) >= 2 else 0
    
    if price_change > 0:
        capital_flow = '净流入（上涨中）'
    else:
        capital_flow = '净流出（下跌中）'
    
    return {
        'latest': {
            'price': round(latest_close, 2),
            'volume': round(latest_volume, 0),
            'vol_ratio': round(vol_ratio, 2),
            'turnover': round(turnover, 2) if turnover else None,
        },
        'volume_ma': {
            'MA5': round(vol_ma5.iloc[-1], 0) if not pd.isna(vol_ma5.iloc[-1]) else None,
            'MA10': round(vol_ma10.iloc[-1], 0) if not pd.isna(vol_ma10.iloc[-1]) else None,
            'MA20': round(vol_ma20.iloc[-1], 0) if not pd.isna(vol_ma20.iloc[-1]) else None,
        },
        'analysis': {
            'price_volume': price_volume,
            'signal': signal,
            'vol_level': vol_level,
            'capital_flow': capital_flow,
        },
        'daily_profile': daily_vol_profile,
        'summary': f"今日量比{vol_ratio:.2f}，{vol_level}，{price_volume}"
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='量价分析器')
    parser.add_argument('--input', required=True, help='K线数据JSON文件')
    parser.add_argument('--output', default='/tmp/volume.json', help='输出文件')
    
    args = parser.parse_args()
    
    with open(args.input) as f:
        kline_data = json.load(f)
    
    if not kline_data.get('data'):
        print('❌ 无K线数据')
        sys.exit(1)
    
    df = pd.DataFrame(kline_data['data'])
    result = analyze_volume(df)
    
    with open(args.output, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 量价分析完成")
    print(f"   {result['summary']}")
