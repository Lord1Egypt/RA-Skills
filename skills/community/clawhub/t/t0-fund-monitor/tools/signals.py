#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信号生成引擎 - 支持快速模式（更早捕捉信号）
"""

from datetime import datetime
from typing import List, Dict
import sys
import json
import os

TRADES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'trades.json')

def check_golden_cross(current: float, prev: float, dea_current: float, dea_prev: float) -> bool:
    """检查 MACD 金叉"""
    return prev <= dea_prev and current > dea_current

def check_death_cross(current: float, prev: float, dea_current: float, dea_prev: float) -> bool:
    """检查 MACD 死叉"""
    return prev >= dea_prev and current < dea_current

def load_trades() -> list:
    """加载交易记录"""
    if os.path.exists(TRADES_FILE):
        try:
            with open(TRADES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_trades(trades: list):
    """保存交易记录"""
    trades = trades[-200:]
    with open(TRADES_FILE, 'w', encoding='utf-8') as f:
        json.dump(trades, f, ensure_ascii=False, indent=2)

def find_open_position(code: str, trades: list) -> dict:
    """查找未平仓的头寸"""
    for trade in reversed(trades):
        if trade['code'] == code and trade['type'] == 'BUY' and trade['status'] == 'OPEN':
            return trade
    return None

def calculate_profit(buy_price: float, sell_price: float) -> dict:
    """计算盈亏"""
    profit = sell_price - buy_price
    profit_pct = (profit / buy_price) * 100 if buy_price > 0 else 0
    return {'profit': round(profit, 4), 'profit_pct': round(profit_pct, 2)}

def generate_signals(code: str, name: str, indicators: dict, config: dict = None, fast_mode: bool = False) -> List[dict]:
    """生成交易信号"""
    signals = []
    
    if indicators is None:
        return signals
    
    default_config = {
        'buy': {'kdj_max': 20, 'volume_ratio': 1.5, 'kdj_early': 30},
        'sell': {'kdj_min': 80},
        'stop_loss': 2,
        'take_profit': 3
    }
    cfg = {**default_config, **(config or {})}
    
    # 快速模式：更宽松条件
    if fast_mode:
        cfg['buy']['kdj_max'] = cfg['buy'].get('kdj_early', 30)
        cfg['buy']['volume_ratio'] = 1.0
    
    macd_dif = indicators.get('macd_dif', 0)
    macd_dea = indicators.get('macd_dea', 0)
    prev_macd_dif = indicators.get('prev_macd_dif', 0)
    prev_macd_dea = indicators.get('prev_macd_dea', 0)
    kdj_k = indicators.get('kdj_k', 50)
    close = indicators.get('close', 0)
    volume = indicators.get('volume', 0)
    vma5 = indicators.get('vma5', 1)
    ma5 = indicators.get('ma5', 0)
    
    volume_ratio = volume / vma5 if vma5 > 0 else 1
    is_golden_cross = check_golden_cross(macd_dif, prev_macd_dif, macd_dea, prev_macd_dea)
    is_death_cross = check_death_cross(macd_dif, prev_macd_dif, macd_dea, prev_macd_dea)
    
    # 买入信号
    buy_conditions = [
        is_golden_cross,
        kdj_k < cfg['buy']['kdj_max'],
        volume_ratio >= cfg['buy']['volume_ratio']
    ]
    
    if all(buy_conditions):
        signals.append({
            'type': 'BUY',
            'code': code,
            'name': name,
            'price': close,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reason': f"MACD 金叉 + KDJ{'早期' if fast_mode else '超卖'} ({kdj_k:.1f}) + 成交量{'正常' if fast_mode else f'放大 ({volume_ratio:.1f}x)'}",
            'indicators': {'macd_dif': macd_dif, 'macd_dea': macd_dea, 'kdj_k': kdj_k, 'volume_ratio': volume_ratio},
            'confidence': 'HIGH' if not fast_mode else 'MEDIUM',
            'status': 'OPEN',
            'fast_mode': fast_mode
        })
    
    # 卖出信号
    if is_death_cross:
        signals.append({
            'type': 'SELL',
            'code': code,
            'name': name,
            'price': close,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reason': f"MACD 死叉",
            'indicators': {'macd_dif': macd_dif, 'macd_dea': macd_dea, 'kdj_k': kdj_k},
            'confidence': 'HIGH',
            'status': 'CLOSE'
        })
    elif kdj_k > cfg['sell']['kdj_min']:
        signals.append({
            'type': 'SELL',
            'code': code,
            'name': name,
            'price': close,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reason': f"KDJ 超买 ({kdj_k:.1f})",
            'indicators': {'kdj_k': kdj_k},
            'confidence': 'MEDIUM',
            'status': 'CLOSE'
        })
    
    if ma5 > 0 and close < ma5 * 0.98:
        signals.append({
            'type': 'SELL',
            'code': code,
            'name': name,
            'price': close,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'reason': f"跌破 5 日线 ({(1-close/ma5)*100:.1f}%)",
            'indicators': {'close': close, 'ma5': ma5},
            'confidence': 'MEDIUM',
            'status': 'CLOSE'
        })
    
    return signals

def process_signal(signal: dict) -> dict:
    """处理信号，更新交易记录"""
    trades = load_trades()
    result = {'signal': signal, 'trade_record': None, 'profit': None}
    
    if signal['type'] == 'BUY':
        result['trade_record'] = {
            'id': f"{signal['code']}_{len(trades)}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'code': signal['code'],
            'name': signal['name'],
            'type': 'BUY',
            'price': signal['price'],
            'time': signal['time'],
            'status': 'OPEN',
            'reason': signal['reason']
        }
        trades.append(result['trade_record'])
    
    elif signal['type'] == 'SELL':
        open_position = find_open_position(signal['code'], trades)
        
        if open_position:
            profit_info = calculate_profit(open_position['price'], signal['price'])
            
            for trade in trades:
                if trade['id'] == open_position['id']:
                    trade['status'] = 'CLOSED'
                    trade['sell_price'] = signal['price']
                    trade['sell_time'] = signal['time']
                    trade['profit'] = profit_info['profit']
                    trade['profit_pct'] = profit_info['profit_pct']
            
            sell_record = {
                'id': f"{signal['code']}_SELL_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'code': signal['code'],
                'name': signal['name'],
                'type': 'SELL',
                'price': signal['price'],
                'time': signal['time'],
                'status': 'CLOSED',
                'reason': signal['reason'],
                'linked_buy_id': open_position['id'],
                'buy_price': open_position['price'],
                'buy_time': open_position['time'],
                'profit': profit_info['profit'],
                'profit_pct': profit_info['profit_pct']
            }
            trades.append(sell_record)
            result['trade_record'] = sell_record
            result['profit'] = profit_info
    
    save_trades(trades)
    return result

def get_trade_history(limit: int = 20) -> list:
    """获取交易历史"""
    trades = load_trades()
    closed_trades = [t for t in trades if t.get('status') == 'CLOSED' and t['type'] == 'SELL']
    closed_trades.sort(key=lambda x: x['time'], reverse=True)
    return closed_trades[:limit]

def format_trade(trade: dict) -> str:
    """格式化交易记录"""
    profit_emoji = "🟢" if trade['profit_pct'] > 0 else "🔴" if trade['profit_pct'] < 0 else "⚪"
    return f"""
{profit_emoji} {trade['code']} ({trade['name']})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
买入：{trade['buy_price']:.3f} @ {trade['buy_time']}
卖出：{trade['price']:.3f} @ {trade['time']}
盈亏：{profit_emoji} {trade['profit_pct']:+.2f}% ({trade['profit']:+.4f})
卖出原因：{trade['reason']}
"""

def format_signal(signal: dict) -> str:
    """格式化信号输出"""
    emoji = "🟢" if signal['type'] == 'BUY' else "🔴"
    action = "买入" if signal['type'] == 'BUY' else "卖出"
    mode_tag = "⚡快速" if signal.get('fast_mode') else ""
    return f"""
{emoji} {action}信号 {mode_tag}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
代码：{signal['code']} ({signal['name']})
价格：{signal['price']:.3f}
原因：{signal['reason']}
时间：{signal['time']}
置信度：{signal['confidence']}
"""
