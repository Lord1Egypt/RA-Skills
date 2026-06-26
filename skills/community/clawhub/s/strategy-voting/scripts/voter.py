#!/usr/bin/env python3
"""
多策略投票系统 - 综合多个策略信号做出交易决策
基于 quant-trading-system 的理念，结合李哥现有的突破策略
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
import numpy as np

CST = timezone(timedelta(hours=8))

class StrategyVoting:
    def __init__(self):
        self.strategies = {
            'breakout': self.strategy_breakout,
            'rsi_reversion': self.strategy_rsi_reversion,
            'macd_cross': self.strategy_macd_cross,
            'bollinger': self.strategy_bollinger
        }
        self.weights = {
            'breakout': 1.5,      # 突破策略权重最高（回测验证最好）
            'rsi_reversion': 1.0,
            'macd_cross': 1.0,
            'bollinger': 1.0
        }
    
    def strategy_breakout(self, df):
        """突破策略（现有最佳策略）"""
        if df is None or len(df) < 60:
            return 0, 'breakout', '数据不足'
        
        close = df['close'].values
        volume = df['volume'].values
        
        cur_price = close[-1]
        high_20d = np.max(close[-21:-1])
        
        # EMA
        ema20 = np.mean(close[-20:])
        ema50 = np.mean(close[-50:]) if len(close) >= 50 else ema20
        
        # 成交量
        vol_now = volume[-1]
        vol_avg = np.mean(volume[-20:])
        vol_ratio = vol_now / vol_avg if vol_avg > 0 else 0
        
        if cur_price > high_20d and vol_ratio > 1.5 and ema20 > ema50:
            return 1, 'breakout', f'突破20日高点，成交量{vol_ratio:.1f}x'
        elif cur_price < ema20:
            return -1, 'breakout', '跌破EMA20'
        return 0, 'breakout', '观望'
    
    def strategy_rsi_reversion(self, df):
        """RSI均值回归策略"""
        if df is None or len(df) < 30:
            return 0, 'rsi_reversion', '数据不足'
        
        close = df['close'].values
        
        # 计算RSI
        delta = np.diff(close)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        
        avg_gain = np.mean(gain[-14:])
        avg_loss = np.mean(loss[-14:])
        
        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        
        if rsi < 30:
            return 1, 'rsi_reversion', f'RSI={rsi:.0f} 超卖'
        elif rsi > 70:
            return -1, 'rsi_reversion', f'RSI={rsi:.0f} 超买'
        return 0, 'rsi_reversion', f'RSI={rsi:.0f} 中性'
    
    def strategy_macd_cross(self, df):
        """MACD金叉策略"""
        if df is None or len(df) < 35:
            return 0, 'macd_cross', '数据不足'
        
        close = df['close'].values
        
        # 计算EMA
        def ema(data, period):
            multiplier = 2 / (period + 1)
            ema_values = [data[0]]
            for i in range(1, len(data)):
                ema_values.append((data[i] - ema_values[-1]) * multiplier + ema_values[-1])
            return np.array(ema_values)
        
        ema12 = ema(close, 12)
        ema26 = ema(close, 26)
        
        macd_line = ema12 - ema26
        signal_line = ema(macd_line, 9)
        
        # 金叉/死叉
        if macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1]:
            return 1, 'macd_cross', 'MACD金叉'
        elif macd_line[-2] > signal_line[-2] and macd_line[-1] < signal_line[-1]:
            return -1, 'macd_cross', 'MACD死叉'
        return 0, 'macd_cross', '无交叉'
    
    def strategy_bollinger(self, df):
        """布林带策略"""
        if df is None or len(df) < 25:
            return 0, 'bollinger', '数据不足'
        
        close = df['close'].values
        
        # 布林带
        sma = np.mean(close[-20:])
        std = np.std(close[-20:])
        
        upper = sma + 2 * std
        lower = sma - 2 * std
        
        cur_price = close[-1]
        
        if cur_price < lower:
            return 1, 'bollinger', f'触及下轨({lower:.2f})'
        elif cur_price > upper:
            return -1, 'bollinger', f'触及上轨({upper:.2f})'
        return 0, 'bollinger', f'带内运行'
    
    def vote(self, df):
        """多策略投票"""
        votes = {}
        total_score = 0
        
        for name, strategy in self.strategies.items():
            try:
                signal, strategy_name, reason = strategy(df)
                weight = self.weights.get(name, 1.0)
                weighted_signal = signal * weight
                votes[name] = {
                    'signal': signal,
                    'weight': weight,
                    'weighted_signal': weighted_signal,
                    'reason': reason
                }
                total_score += weighted_signal
            except Exception as e:
                votes[name] = {
                    'signal': 0,
                    'weight': 0,
                    'weighted_signal': 0,
                    'reason': f'错误: {str(e)}'
                }
        
        # 决策阈值
        if total_score >= 1.5:
            decision = 1  # 做多
        elif total_score <= -1.5:
            decision = -1  # 平仓/做空
        else:
            decision = 0  # 观望
        
        return {
            'decision': decision,
            'total_score': total_score,
            'votes': votes,
            'timestamp': datetime.now(CST).isoformat()
        }

def generate_report(vote_result):
    """生成投票报告"""
    lines = []
    lines.append("=" * 40)
    lines.append("🗳️ 多策略投票结果")
    lines.append("=" * 40)
    
    decision_map = {1: '🟢 做多', -1: '🔴 平仓/做空', 0: '⚪ 观望'}
    lines.append(f"\n📊 最终决策: {decision_map.get(vote_result['decision'], '?')}")
    lines.append(f"📈 综合得分: {vote_result['total_score']:.2f}")
    
    lines.append("\n📋 各策略投票:")
    lines.append("-" * 30)
    
    for name, vote in vote_result['votes'].items():
        signal_map = {1: '🟢', -1: '🔴', 0: '⚪'}
        emoji = signal_map.get(vote['signal'], '?')
        lines.append(f"  {emoji} {name:15s} | 权重{vote['weight']:.1f}x | {vote['reason']}")
    
    lines.append("\n" + "=" * 40)
    
    return "\n".join(lines)

if __name__ == "__main__":
    # 简单测试
    import pandas as pd
    
    # 创建测试数据
    np.random.seed(42)
    dates = pd.date_range('2026-01-01', periods=100, freq='D')
    close = 70000 + np.cumsum(np.random.randn(100) * 500)
    volume = np.random.rand(100) * 1000000
    
    df = pd.DataFrame({
        'close': close,
        'high': close * 1.01,
        'low': close * 0.99,
        'volume': volume
    })
    
    voter = StrategyVoting()
    result = voter.vote(df)
    report = generate_report(result)
    print(report)
