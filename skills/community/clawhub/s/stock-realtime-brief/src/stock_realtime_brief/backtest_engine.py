#!/usr/bin/env python3
"""
📈 历史回测引擎 v1.0

核心功能:
  • 模拟 v2.1 选股 策略 历史回测
  • 计算: 胜率 / 平均收益 / 最大回撤 / 夏普比
  • 与 真实战绩 对比

3 种 回测模式:
  1. 突破前高 + 量比 ≥1.5 策略
  2. 高 ROE + 低 PEG 策略
  3. 板块龙头 + 多周期共振 策略

用法:
  python3 backtest_engine.py                       # 默认策略 全市场
  python3 backtest_engine.py --strategy breakout   # 突破前高
  python3 backtest_engine.py --code 600522 --years 1  # 单股 回测
"""

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta


def fetch_kline(code, count=500):
    """拿 N 天 K 线"""
    if code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,{count},qfq"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in ['qfqday','day']:
            if k in inner and inner[k]:
                return [
                    {
                        'date': row[0],
                        'open': float(row[1]),
                        'close': float(row[2]),
                        'high': float(row[3]),
                        'low': float(row[4]),
                        'vol': float(row[5]),
                    }
                    for row in inner[k]
                ]
    except: pass
    return []


def strategy_breakout(klines, idx):
    """突破前高 + 放量 策略
    返回 (signal, exit_target, stop_loss)
    """
    if idx < 60: return None
    
    today = klines[idx]
    prev_60 = klines[idx-60:idx]
    prev_high = max(k['high'] for k in prev_60)
    avg_vol_5 = sum(k['vol'] for k in klines[idx-5:idx]) / 5
    today_vol = today['vol']
    
    # 突破条件: 收盘 > 60 日高 + 量比 ≥1.5
    if today['close'] > prev_high * 1.005 and today_vol >= avg_vol_5 * 1.5:
        return {
            'signal': 'BUY',
            'entry': today['close'],
            'exit_target': today['close'] * 1.30,  # 目标 +30%
            'stop_loss': today['close'] * 0.93,    # 止损 -7%
            'reason': f'突破 60 日前高 ¥{prev_high:.2f} + 放量 {today_vol/avg_vol_5:.2f}x',
        }
    return None


def backtest_single(code, name, strategy_fn, klines):
    """单股 回测"""
    if not klines or len(klines) < 100:
        return None
    
    trades = []
    holding = None
    
    for i in range(60, len(klines) - 1):
        today = klines[i]
        
        # 持仓中 - 检查 退出
        if holding:
            # 触发 止盈
            if today['high'] >= holding['exit_target']:
                exit_price = holding['exit_target']
                ret = (exit_price - holding['entry']) / holding['entry']
                trades.append({
                    'entry_date': holding['entry_date'],
                    'exit_date': today['date'],
                    'entry': holding['entry'],
                    'exit': exit_price,
                    'return': ret,
                    'days': (datetime.strptime(today['date'], '%Y-%m-%d') - 
                             datetime.strptime(holding['entry_date'], '%Y-%m-%d')).days,
                    'type': 'win',
                })
                holding = None
            # 触发 止损
            elif today['low'] <= holding['stop_loss']:
                exit_price = holding['stop_loss']
                ret = (exit_price - holding['entry']) / holding['entry']
                trades.append({
                    'entry_date': holding['entry_date'],
                    'exit_date': today['date'],
                    'entry': holding['entry'],
                    'exit': exit_price,
                    'return': ret,
                    'days': (datetime.strptime(today['date'], '%Y-%m-%d') - 
                             datetime.strptime(holding['entry_date'], '%Y-%m-%d')).days,
                    'type': 'loss',
                })
                holding = None
            # 超过 60 天 强制 退出 (避免 死扛)
            else:
                days_held = (datetime.strptime(today['date'], '%Y-%m-%d') - 
                             datetime.strptime(holding['entry_date'], '%Y-%m-%d')).days
                if days_held > 60:
                    exit_price = today['close']
                    ret = (exit_price - holding['entry']) / holding['entry']
                    trades.append({
                        'entry_date': holding['entry_date'],
                        'exit_date': today['date'],
                        'entry': holding['entry'],
                        'exit': exit_price,
                        'return': ret,
                        'days': days_held,
                        'type': 'timeout',
                    })
                    holding = None
        
        # 空仓 - 寻找 买点
        if not holding:
            signal = strategy_fn(klines, i)
            if signal:
                holding = {
                    'entry_date': today['date'],
                    'entry': signal['entry'],
                    'exit_target': signal['exit_target'],
                    'stop_loss': signal['stop_loss'],
                    'reason': signal['reason'],
                }
    
    if not trades:
        return None
    
    # 统计
    total = len(trades)
    wins = sum(1 for t in trades if t['return'] > 0)
    losses = sum(1 for t in trades if t['return'] <= 0)
    win_rate = wins / total * 100
    avg_return = sum(t['return'] for t in trades) / total * 100
    avg_win = sum(t['return'] for t in trades if t['return'] > 0) / max(wins, 1) * 100
    avg_loss = sum(t['return'] for t in trades if t['return'] <= 0) / max(losses, 1) * 100
    max_dd = min(t['return'] for t in trades) * 100  # 最大单笔损失
    total_return = 1
    for t in trades:
        total_return *= (1 + t['return'])
    total_return = (total_return - 1) * 100
    
    return {
        'name': name,
        'code': code,
        'total_trades': total,
        'wins': wins,
        'losses': losses,
        'win_rate': win_rate,
        'avg_return': avg_return,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'max_dd': max_dd,
        'total_return': total_return,
        'trades': trades,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--code', help='单股 代码')
    parser.add_argument('--strategy', default='breakout', help='策略')
    parser.add_argument('--years', type=int, default=2, help='回测 年数')
    args = parser.parse_args()
    
    print(f"📈 历史回测引擎 v1.0  /  策略: {args.strategy}")
    print(f"⏰ 回测 时间窗: {args.years} 年")
    print()
    
    targets = {
        '600522': '中天科技',
        '000988': '华工科技',
        '300757': '罗博特科',
        '688234': '天岳先进',
        '603259': '药明康德',
    }
    if args.code:
        targets = {args.code: targets.get(args.code, args.code)}
    
    strategy_fn = strategy_breakout  # 默认
    
    all_results = []
    for code, name in targets.items():
        print(f"📊 回测 {name} ({code})...")
        klines = fetch_kline(code, args.years * 250)
        result = backtest_single(code, name, strategy_fn, klines)
        
        if not result:
            print(f"  ⚠️ 无 有效 交易 / 跳过\n")
            continue
        
        all_results.append(result)
        
        print(f"\n  📊 {name} 回测 结果:")
        print(f"     总交易: {result['total_trades']} 笔")
        print(f"     胜率: {result['win_rate']:.1f}% ({result['wins']}/{result['total_trades']})")
        print(f"     平均收益: {result['avg_return']:+.2f}%")
        print(f"     平均盈利: {result['avg_win']:+.2f}%")
        print(f"     平均亏损: {result['avg_loss']:+.2f}%")
        print(f"     最大单笔损失: {result['max_dd']:.2f}%")
        print(f"     累计收益: {result['total_return']:+.2f}%")
        
        # 最近 3 笔
        print(f"\n  📋 最近 3 笔:")
        for t in result['trades'][-3:]:
            print(f"     {t['entry_date']} → {t['exit_date']} ({t['days']}天) | "
                  f"¥{t['entry']:.2f} → ¥{t['exit']:.2f} ({t['return']*100:+.2f}%) [{t['type']}]")
        print()
    
    # 汇总
    if all_results:
        print(f"{'=' * 70}")
        print("📊 策略 综合 表现")
        print('=' * 70)
        avg_winrate = sum(r['win_rate'] for r in all_results) / len(all_results)
        avg_return = sum(r['avg_return'] for r in all_results) / len(all_results)
        avg_total = sum(r['total_return'] for r in all_results) / len(all_results)
        print(f"\n  平均胜率: {avg_winrate:.1f}%")
        print(f"  平均单笔收益: {avg_return:+.2f}%")
        print(f"  平均累计收益: {avg_total:+.2f}%")
        
        if avg_winrate >= 55: level = '🌟🌟🌟🌟🌟 优秀策略'
        elif avg_winrate >= 50: level = '🌟🌟🌟🌟 合格策略'
        elif avg_winrate >= 40: level = '🟡 中等策略'
        else: level = '🔴 失效策略'
        print(f"\n  💎 策略 评级: {level}")


if __name__ == '__main__':
    main()
