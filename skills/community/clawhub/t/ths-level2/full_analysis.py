# -*- coding: utf-8 -*-
"""
5只股票深度分析 - 筹码、资金抄底、五线谱、大单净量、成交量
"""
import os
import sys
import json
import statistics
from datetime import datetime, timedelta
from pathlib import Path

os.environ['PYTHONIOENCODING'] = 'utf-8'

import tushare as ts

token = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(token)
pro = ts.pro_api()

# 股票列表
STOCKS = [
    {'code': '600276.SH', 'name': '恒瑞医药'},
    {'code': '688235.SH', 'name': '百济神州'},
    {'code': '600760.SH', 'name': '中航沈飞'},
    {'code': '601888.SH', 'name': '中国中免'},
    {'code': '002202.SZ', 'name': '金风科技'},
]

def get_stock_data(code, days=60):
    """获取股票数据"""
    end = datetime.now().strftime('%Y%m%d')
    start = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    
    try:
        df = pro.daily(ts_code=code, start_date=start, end_date=end)
        if df is not None and len(df) > 0:
            return df.sort_values('trade_date').reset_index(drop=True)
    except Exception as e:
        print(f"获取{code}数据失败：{e}")
    return None

def analyze_chips(df):
    """筹码分析"""
    if df is None or len(df) < 20:
        return {'status': '数据不足'}
    
    closes = df['close'].tolist()
    volumes = df['vol'].tolist()
    
    # 筹码集中度（价格波动率）
    std = statistics.stdev(closes[-20:])
    mean = statistics.mean(closes[-20:])
    concentration = 1 - (std / mean) if mean > 0 else 0
    
    # 获利盘比例
    current = closes[-1]
    profitable = len([c for c in closes[-60:] if c < current]) / len(closes[-60:]) * 100
    
    # 平均成本（VWAP）
    total_amount = sum(df['amount'].tolist()[-20:])
    total_volume = sum(volumes[-20:]) * 100  # 手转股
    avg_cost = total_amount / total_volume if total_volume > 0 else mean
    
    # 筹码状态
    if current < avg_cost * 0.9:
        chip_state = '深度套牢'
    elif current < avg_cost:
        chip_state = '多数套牢'
    elif current > avg_cost * 1.1:
        chip_state = '多数获利'
    else:
        chip_state = '成本区震荡'
    
    return {
        'concentration': round(concentration, 4),
        'profitable_ratio': round(profitable, 1),
        'avg_cost': round(avg_cost, 2),
        'current_price': current,
        'chip_state': chip_state
    }

def analyze_capital_bottom(df):
    """资金抄底分析"""
    if df is None or len(df) < 20:
        return {'signal': '数据不足'}
    
    closes = df['close'].tolist()
    volumes = df['vol'].tolist()
    
    avg_price = statistics.mean(closes[-20:])
    current = closes[-1]
    deviation = (current - avg_price) / avg_price * 100
    
    vol_ma5 = statistics.mean(volumes[-5:])
    vol_ma20 = statistics.mean(volumes[-20:])
    vol_ratio = vol_ma5 / vol_ma20 if vol_ma20 > 0 else 1
    
    # 判断信号
    if deviation < -10 and vol_ratio > 1.2:
        signal = '抄底信号'
        strength = min(100, abs(deviation) * 5)
    elif deviation < -5:
        signal = '偏弱'
        strength = 30
    elif deviation > 10 and vol_ratio < 0.8:
        signal = '见顶信号'
        strength = min(100, deviation * 3)
    elif deviation > 5:
        signal = '偏强'
        strength = 60
    else:
        signal = '中性'
        strength = 50
    
    return {
        'signal': signal,
        'strength': round(strength, 1),
        'deviation': round(deviation, 2),
        'vol_ratio': round(vol_ratio, 2)
    }

def analyze_five_lines(df):
    """神奇五线谱分析"""
    if df is None or len(df) < 60:
        return {'score': 0, 'signal': '数据不足'}
    
    closes = df['close'].tolist()
    volumes = df['vol'].tolist()
    current = closes[-1]
    
    # 计算均线
    ma5 = statistics.mean(closes[-5:])
    ma10 = statistics.mean(closes[-10:])
    ma20 = statistics.mean(closes[-20:])
    
    # 成交量线
    vol_ma5 = statistics.mean(volumes[-5:])
    vol_ma20 = statistics.mean(volumes[-20:])
    vol_ratio = vol_ma5 / vol_ma20 if vol_ma20 > 0 else 1
    vol_trend = '放量' if vol_ratio > 1.2 else '缩量' if vol_ratio < 0.8 else '正常'
    
    # 资金流向线
    up_vol = sum(volumes[i] for i in range(-20, 0) if closes[i] > closes[i-1])
    down_vol = sum(volumes[i] for i in range(-20, 0) if closes[i] < closes[i-1])
    money_ratio = up_vol / down_vol if down_vol > 0 else 1
    money_trend = '流入' if money_ratio > 1.2 else '流出' if money_ratio < 0.8 else '平衡'
    
    # 计算评分
    score = 50
    if ma5 > ma10 > ma20:
        score += 20
    elif ma5 < ma10 < ma20:
        score -= 20
    if current > ma5:
        score += 5
    if vol_ratio > 1.2:
        score += 10
    elif vol_ratio < 0.8:
        score -= 5
    if money_ratio > 1.2:
        score += 15
    elif money_ratio < 0.8:
        score -= 15
    
    score = max(0, min(100, score))
    
    if score >= 70:
        signal = '强势'
    elif score >= 55:
        signal = '偏强'
    elif score >= 45:
        signal = '中性'
    elif score >= 30:
        signal = '偏弱'
    else:
        signal = '弱势'
    
    return {
        'score': round(score, 1),
        'signal': signal,
        'lines': {
            'MA5': {'value': round(ma5, 2), 'position': '上方' if current > ma5 else '下方'},
            'MA10': {'value': round(ma10, 2), 'position': '上方' if current > ma10 else '下方'},
            'MA20': {'value': round(ma20, 2), 'position': '上方' if current > ma20 else '下方'},
            'Volume': {'ratio': round(vol_ratio, 2), 'trend': vol_trend},
            'MoneyFlow': {'ratio': round(money_ratio, 2), 'trend': money_trend}
        }
    }

def analyze_big_order(df):
    """大单净量分析（模拟）"""
    if df is None or len(df) < 20:
        return {'status': '数据不足'}
    
    volumes = df['vol'].tolist()
    closes = df['close'].tolist()
    
    # 模拟大单净量（基于量价关系）
    up_days = [i for i in range(-20, 0) if closes[i] > closes[i-1]]
    down_days = [i for i in range(-20, 0) if closes[i] < closes[i-1]]
    
    up_vol = sum(volumes[i] for i in up_days if i > -len(volumes))
    down_vol = sum(volumes[i] for i in down_days if i > -len(volumes))
    
    net_ratio = (up_vol - down_vol) / (up_vol + down_vol) if (up_vol + down_vol) > 0 else 0
    
    if net_ratio > 0.3:
        signal = '大单净流入'
    elif net_ratio < -0.3:
        signal = '大单净流出'
    else:
        signal = '大单平衡'
    
    return {
        'net_ratio': round(net_ratio, 3),
        'signal': signal,
        'up_vol': round(up_vol/10000, 1),
        'down_vol': round(down_vol/10000, 1)
    }

def analyze_volume(df):
    """成交量分析"""
    if df is None or len(df) < 20:
        return {'status': '数据不足'}
    
    volumes = df['vol'].tolist()
    
    vol_ma5 = statistics.mean(volumes[-5:])
    vol_ma10 = statistics.mean(volumes[-10:])
    vol_ma20 = statistics.mean(volumes[-20:])
    
    vol_ratio_5_20 = vol_ma5 / vol_ma20 if vol_ma20 > 0 else 1
    vol_ratio_10_20 = vol_ma10 / vol_ma20 if vol_ma20 > 0 else 1
    
    if vol_ratio_5_20 > 1.5:
        trend = '明显放量'
    elif vol_ratio_5_20 > 1.2:
        trend = '温和放量'
    elif vol_ratio_5_20 < 0.7:
        trend = '明显缩量'
    elif vol_ratio_5_20 < 0.85:
        trend = '温和缩量'
    else:
        trend = '正常'
    
    return {
        'vol_ma5': round(vol_ma5/10000, 1),
        'vol_ma10': round(vol_ma10/10000, 1),
        'vol_ma20': round(vol_ma20/10000, 1),
        'vol_ratio': round(vol_ratio_5_20, 2),
        'trend': trend
    }

def analyze_stock_full(code, name):
    """完整分析单只股票"""
    print(f"\n{'='*70}")
    print(f" {name} ({code})")
    print(f"{'='*70}")
    
    df = get_stock_data(code)
    
    if df is None or len(df) == 0:
        print("  无法获取数据")
        return None
    
    latest = df.iloc[-1]
    
    print(f"\n【基础数据】")
    print(f"  最新价：{latest['close']:.2f}元")
    print(f"  涨跌：{latest['pct_chg']:.2f}%")
    print(f"  日期：{latest['trade_date']}")
    
    # 筹码分析
    print(f"\n【筹码情况】")
    chips = analyze_chips(df)
    if 'status' not in chips:
        print(f"  集中度：{chips['concentration']:.1%}")
        print(f"  获利盘：{chips['profitable_ratio']:.1f}%")
        print(f"  平均成本：{chips['avg_cost']:.2f}元")
        print(f"  状态：{chips['chip_state']}")
    
    # 资金抄底
    print(f"\n【资金抄底】")
    bottom = analyze_capital_bottom(df)
    if 'status' not in bottom:
        print(f"  信号：{bottom['signal']} (强度{bottom['strength']}%)")
        print(f"  偏离度：{bottom['deviation']:.2f}%")
        print(f"  量比：{bottom['vol_ratio']:.2f}")
    
    # 五线谱
    print(f"\n【神奇五线谱】")
    five = analyze_five_lines(df)
    if 'status' not in five:
        print(f"  评分：{five['score']}/100 - {five['signal']}")
        for line_name, line_data in five['lines'].items():
            if 'value' in line_data:
                print(f"  {line_name}: {line_data['value']} ({line_data['position']})")
            else:
                print(f"  {line_name}: {line_data['trend']} (比{line_data['ratio']})")
    
    # 大单净量
    print(f"\n【大单净量】")
    big_order = analyze_big_order(df)
    if 'status' not in big_order:
        print(f"  净量比：{big_order['net_ratio']:.3f}")
        print(f"  信号：{big_order['signal']}")
        print(f"  上涨量：{big_order['up_vol']}万手 | 下跌量：{big_order['down_vol']}万手")
    
    # 成交量
    print(f"\n【成交量】")
    vol = analyze_volume(df)
    if 'status' not in vol:
        print(f"  5日均量：{vol['vol_ma5']}万手")
        print(f"  20日均量：{vol['vol_ma20']}万手")
        print(f"  量比：{vol['vol_ratio']}")
        print(f"  趋势：{vol['trend']}")
    
    # 综合评分
    total_score = 0
    if 'status' not in chips:
        if chips['profitable_ratio'] > 50:
            total_score += 20
    if 'status' not in bottom:
        total_score += bottom['strength'] * 0.3
    if 'status' not in five:
        total_score += five['score'] * 0.3
    if 'status' not in big_order:
        if big_order['net_ratio'] > 0:
            total_score += 10
    
    if total_score >= 70:
        suggestion = '积极关注'
    elif total_score >= 55:
        suggestion = '适度关注'
    elif total_score >= 40:
        suggestion = '观望'
    else:
        suggestion = '回避'
    
    print(f"\n{'='*70}")
    print(f" 综合评分：{total_score:.1f} - {suggestion}")
    print(f"{'='*70}")
    
    return {
        'code': code,
        'name': name,
        'price': latest['close'],
        'change': latest['pct_chg'],
        'chips': chips,
        'bottom': bottom,
        'five_lines': five,
        'big_order': big_order,
        'volume': vol,
        'total_score': total_score,
        'suggestion': suggestion
    }

def main():
    print("=" * 70)
    print(" 5只股票深度分析 - 筹码/资金抄底/五线谱/大单净量/成交量")
    print(f" 分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    results = []
    for stock in STOCKS:
        try:
            result = analyze_stock_full(stock['code'], stock['name'])
            if result:
                results.append(result)
        except Exception as e:
            print(f"\n分析{stock['name']}出错：{e}")
    
    # 汇总对比
    print(f"\n{'='*70}")
    print(" 综合对比汇总")
    print(f"{'='*70}")
    
    print(f"\n| 股票 | 价格 | 涨跌 | 五线谱 | 抄底 | 大单 | 综合 | 建议 |")
    print("|------|------|------|--------|------|------|------|------|")
    
    for r in sorted(results, key=lambda x: x['total_score'], reverse=True):
        bottom_signal = r['bottom'].get('signal', '-') if 'status' not in r['bottom'] else '-'
        five_score = f"{r['five_lines']['score']}" if 'status' not in r['five_lines'] else '-'
        big_order = r['big_order'].get('signal', '-') if 'status' not in r['big_order'] else '-'
        
        print(f"| {r['name']} | {r['price']:.2f} | {r['change']:+.1f}% | {five_score} | {bottom_signal} | {big_order} | {r['total_score']:.0f} | {r['suggestion']} |")
    
    # 保存结果
    output_file = Path(__file__).parent / 'full_analysis_result.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n结果已保存至：{output_file}")

if __name__ == '__main__':
    main()
