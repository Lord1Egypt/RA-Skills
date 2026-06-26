# -*- coding: utf-8 -*-
"""
通达信高级指标分析
模拟实现: 金股猎手、火焰山、至尊老鸭头
"""
import struct
import statistics
from pathlib import Path

TDX_PATH = Path(r"D:\new_tdx")

def read_day_file(filepath):
    """读取日线文件"""
    records = []
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(32)
            if len(data) < 32: break
            date_int = struct.unpack('<I', data[0:4])[0]
            o = struct.unpack('<I', data[4:8])[0] / 100.0
            h = struct.unpack('<I', data[8:12])[0] / 100.0
            l = struct.unpack('<I', data[12:16])[0] / 100.0
            c = struct.unpack('<I', data[16:20])[0] / 100.0
            amt = struct.unpack('<f', data[20:24])[0]
            vol = struct.unpack('<I', data[24:28])[0]
            year = date_int // 10000
            month = (date_int % 10000) // 100
            day = date_int % 100
            records.append({'date': f"{year}-{month:02d}-{day:02d}", 'o': o, 'h': h, 'l': l, 'c': c, 'v': vol, 'a': amt})
    return records

def calc_ma(prices, period):
    """计算均线"""
    if len(prices) < period: return None
    return sum(prices[-period:]) / period

def jingu_lieshou(records):
    """
    金股猎手信号
    综合评分: 主力资金 + 筹码集中 + 放量突破
    """
    if len(records) < 20: return {'score': 0, 'signal': '数据不足'}
    
    closes = [r['c'] for r in records]
    volumes = [r['v'] for r in records]
    
    # 1. 主力资金 (量价关系)
    up_vol = sum(r['v'] for r in records[-20:] if r['c'] > records[records.index(r)-1]['c']) if len(records) > 1 else 0
    down_vol = sum(r['v'] for r in records[-20:] if r['c'] < records[records.index(r)-1]['c']) if len(records) > 1 else 1
    money_flow = up_vol / down_vol if down_vol > 0 else 1
    
    # 2. 筹码集中度 (价格波动)
    std = statistics.stdev(closes[-20:])
    mean = statistics.mean(closes[-20:])
    concentration = 1 - (std / mean) if mean > 0 else 0
    
    # 3. 放量突破
    vol_ma5 = calc_ma(volumes, 5)
    vol_ma20 = calc_ma(volumes, 20)
    volume_ratio = vol_ma5 / vol_ma20 if vol_ma20 and vol_ma20 > 0 else 1
    
    # 评分
    score = 50
    if money_flow > 1.3: score += 20
    elif money_flow < 0.7: score -= 20
    if concentration > 0.9: score += 10
    if volume_ratio > 1.5: score += 15
    elif volume_ratio < 0.7: score -= 10
    
    signal = '买入' if score >= 70 else '关注' if score >= 55 else '观望' if score >= 40 else '回避'
    
    return {
        'score': score,
        'signal': signal,
        'money_flow': money_flow,
        'concentration': concentration,
        'volume_ratio': volume_ratio
    }

def huoyanshan(records):
    """
    火焰山信号
    资金热度指标
    """
    if len(records) < 10: return {'heat': 0, 'color': '蓝色'}
    
    volumes = [r['v'] for r in records]
    closes = [r['c'] for r in records]
    
    # 成交量变化
    vol_change = volumes[-1] / calc_ma(volumes, 5) if calc_ma(volumes, 5) else 1
    
    # 价格变化
    price_change = (closes[-1] - closes[-5]) / closes[-5] * 100 if closes[-5] else 0
    
    # 热度计算
    heat = 50 + (vol_change - 1) * 30 + price_change
    heat = max(0, min(100, heat))
    
    if heat > 70: color = '红色'
    elif heat > 40: color = '白色'
    else: color = '蓝色'
    
    return {'heat': heat, 'color': color, 'vol_change': vol_change}

def laoyatou(records):
    """
    至尊老鸭头
    趋势反转信号
    """
    if len(records) < 60: return {'signal': '数据不足', 'stage': '无'}
    
    closes = [r['c'] for r in records]
    
    ma5 = calc_ma(closes, 5)
    ma10 = calc_ma(closes, 10)
    ma20 = calc_ma(closes, 20)
    
    current = closes[-1]
    
    # 判断均线排列
    if ma5 > ma10 > ma20:
        arrangement = '多头'
    elif ma5 < ma10 < ma20:
        arrangement = '空头'
    else:
        arrangement = '交叉'
    
    # 老鸭头形态
    signal = '观望'
    stage = '无'
    
    if arrangement == '多头':
        # 检查是否回测MA20
        if current > ma20 and closes[-5] < ma20 * 1.02:
            signal = '鸭嘴形成'
            stage = '回调买入'
        elif current > ma5:
            signal = '多头持有'
            stage = '持有'
    elif arrangement == '空头':
        signal = '空头观望'
        stage = '等待'
    else:
        signal = '变盘信号'
        stage = '关注'
    
    return {'signal': signal, 'stage': stage, 'arrangement': arrangement, 'ma5': ma5, 'ma10': ma10, 'ma20': ma20}

# 主分析
print("=" * 70)
print(" 通达信高级指标分析 - 恒瑞医药(600276)")
print("=" * 70)

day_file = TDX_PATH / "vipdoc" / "sh" / "lday" / "sh600276.day"
if day_file.exists():
    records = read_day_file(day_file)
    
    print(f"\n数据: {records[0]['date']} ~ {records[-1]['date']} ({len(records)}条)")
    print(f"最新: {records[-1]['date']} 收盘 {records[-1]['c']:.2f}")
    
    print("\n" + "-" * 70)
    print(" [1] 金股猎手")
    print("-" * 70)
    result = jingu_lieshou(records)
    print(f"  评分: {result['score']}/100")
    print(f"  信号: {result['signal']}")
    print(f"  资金流向比: {result['money_flow']:.2f}")
    print(f"  筹码集中度: {result['concentration']:.2%}")
    print(f"  量比: {result['volume_ratio']:.2f}")
    
    print("\n" + "-" * 70)
    print(" [2] 火焰山")
    print("-" * 70)
    result = huoyanshan(records)
    print(f"  热度: {result['heat']:.0f}")
    print(f"  颜色: {result['color']}火焰")
    print(f"  量比: {result['vol_change']:.2f}")
    
    print("\n" + "-" * 70)
    print(" [3] 至尊老鸭头")
    print("-" * 70)
    result = laoyatou(records)
    print(f"  均线排列: {result['arrangement']}")
    print(f"  MA5: {result['ma5']:.2f}")
    print(f"  MA10: {result['ma10']:.2f}")
    print(f"  MA20: {result['ma20']:.2f}")
    print(f"  信号: {result['signal']}")
    print(f"  阶段: {result['stage']}")

print("\n" + "=" * 70)
print(" 分析完成")
print("=" * 70)