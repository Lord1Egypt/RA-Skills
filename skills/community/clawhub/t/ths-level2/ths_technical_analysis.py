# -*- coding: utf-8 -*-
"""
同花顺技术指标分析系统
包含：资金抄底、主力净额、神奇五线谱、神奇九转、Level2资金仓位、牛熊线、多空线
"""
import os
import sys
import json
import io
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 持仓数据
HOLDINGS = {
    "600276": {"name": "恒瑞医药", "cost": 53.12, "shares": 1000, "market": "SH", "current": 51.63, "change": -2.80},
    "600760": {"name": "中航沈飞", "cost": 48.01, "shares": 1200, "market": "SH", "current": 47.76, "change": -0.53},
    "600999": {"name": "招商证券", "cost": 19.50, "shares": 1600, "market": "SH", "current": 15.17, "change": -22.20},
    "601888": {"name": "中国中免", "cost": 72.27, "shares": 1000, "market": "SH", "current": 70.69, "change": -2.19},
    "002202": {"name": "金风科技", "cost": 28.01, "shares": 2000, "market": "SZ", "current": 28.13, "change": 0.44},
    "300188": {"name": "国投智能", "cost": -1917, "shares": 320, "market": "SZ", "current": 12.33, "change": 0},
}

class TechnicalAnalyzer:
    def __init__(self, code, info):
        self.code = code
        self.name = info['name']
        self.cost = info['cost']
        self.current = info['current']
        self.shares = info['shares']
        self.change = info['change']
        self._generate_mock_data()
    
    def _generate_mock_data(self):
        import random
        random.seed(int(self.code))
        base_price = self.current * 0.9
        self.prices, self.volumes = [], []
        for i in range(60):
            change = random.uniform(-0.03, 0.03)
            price = base_price * (1 + change)
            base_price = price
            self.prices.append(price)
            self.volumes.append(random.randint(100000, 500000))
        self.prices[-1] = self.current
    
    def calculate_ma(self, period):
        return statistics.mean(self.prices[-period:]) if len(self.prices) >= period else self.current
    
    def calculate_ema(self, period):
        if len(self.prices) < period:
            return self.current
        multiplier = 2 / (period + 1)
        ema = self.prices[0]
        for price in self.prices[1:]:
            ema = (price - ema) * multiplier + ema
        return ema
    
    def calculate_rsi(self, period=14):
        if len(self.prices) < period + 1:
            return 50
        gains, losses = [], []
        for i in range(1, period + 1):
            change = self.prices[-i] - self.prices[-i-1]
            (gains if change > 0 else losses).append(abs(change))
        avg_gain = statistics.mean(gains) if gains else 0
        avg_loss = statistics.mean(losses) if losses else 0
        return 100 if avg_loss == 0 else 100 - (100 / (1 + avg_gain / avg_loss))
    
    def calculate_macd(self, fast=12, slow=26):
        macd = self.calculate_ema(fast) - self.calculate_ema(slow)
        signal = macd * 0.9
        return {'macd': round(macd, 3), 'signal': round(signal, 3), 
                'histogram': round(macd - signal, 3), 'trend': '金叉' if macd > signal else '死叉'}
    
    def calculate_bollinger(self, period=20):
        if len(self.prices) < period:
            return {'middle': self.current, 'upper': self.current * 1.1, 'lower': self.current * 0.9}
        middle = statistics.mean(self.prices[-period:])
        std = statistics.stdev(self.prices[-period:])
        return {'middle': round(middle, 2), 'upper': round(middle + 2 * std, 2), 
                'lower': round(middle - 2 * std, 2), 'bandwidth': round(4 * std / middle * 100, 2)}
    
    def calculate_kdj(self, n=9):
        if len(self.prices) < n:
            return {'k': 50, 'd': 50, 'j': 50, 'signal': '中性'}
        recent = self.prices[-n:]
        low, high = min(recent), max(recent)
        rsv = 50 if high == low else (self.current - low) / (high - low) * 100
        signal = '超买' if rsv > 80 else '超卖' if rsv < 20 else '中性'
        return {'k': round(rsv, 2), 'd': round(rsv, 2), 'j': round(rsv, 2), 'signal': signal}
    
    def analyze_fund_bottom_fishing(self):
        ma20 = self.calculate_ma(20)
        deviation = (self.current - ma20) / ma20 * 100
        vol_5 = statistics.mean(self.volumes[-5:])
        vol_20 = statistics.mean(self.volumes[-20:])
        vol_ratio = vol_5 / vol_20 if vol_20 > 0 else 1
        
        if deviation < -15 and vol_ratio > 1.5:
            signal, strength = '强抄底信号', min(100, abs(deviation) * 4)
        elif deviation < -10 and vol_ratio > 1.2:
            signal, strength = '抄底信号', min(80, abs(deviation) * 3)
        elif deviation < -5:
            signal, strength = '偏弱', 30
        elif deviation > 10 and vol_ratio < 0.8:
            signal, strength = '见顶信号', min(80, deviation * 3)
        elif deviation > 5:
            signal, strength = '偏强', 60
        else:
            signal, strength = '中性', 50
        return {'signal': signal, 'strength': round(strength, 1), 'deviation': round(deviation, 2), 
                'vol_ratio': round(vol_ratio, 2), 'ma20': round(ma20, 2)}
    
    def analyze_main_fund(self):
        recent_vol = self.volumes[-20:]
        up_vol = sum(recent_vol[i] for i in range(0, len(recent_vol), 2))
        down_vol = sum(recent_vol[i] for i in range(1, len(recent_vol), 2))
        total = up_vol + down_vol
        net_ratio = (up_vol - down_vol) / total if total > 0 else 0
        
        if net_ratio > 0.3:
            signal, intensity = '主力净流入', '强'
        elif net_ratio > 0.1:
            signal, intensity = '主力净流入', '弱'
        elif net_ratio < -0.3:
            signal, intensity = '主力净流出', '强'
        elif net_ratio < -0.1:
            signal, intensity = '主力净流出', '弱'
        else:
            signal, intensity = '主力平衡', '中性'
        return {'net_ratio': round(net_ratio, 3), 'signal': signal, 'intensity': intensity,
                'up_vol': round(up_vol / 10000, 1), 'down_vol': round(down_vol / 10000, 1)}
    
    def analyze_magic_five_lines(self):
        ma5, ma10, ma20 = self.calculate_ma(5), self.calculate_ma(10), self.calculate_ma(20)
        ma60 = self.calculate_ma(60) if len(self.prices) >= 60 else ma20
        
        score = 50
        trend = []
        if self.current > ma5 > ma10 > ma20:
            score += 25
            trend.append('多头排列')
        elif self.current < ma5 < ma10 < ma20:
            score -= 25
            trend.append('空头排列')
        score += 10 if self.current > ma5 else 0
        score += 10 if self.current > ma20 else 0
        score = max(0, min(100, score))
        
        signal = '强势' if score >= 70 else '偏强' if score >= 55 else '中性' if score >= 45 else '偏弱' if score >= 30 else '弱势'
        return {'score': score, 'signal': signal, 'ma5': round(ma5, 2), 'ma10': round(ma10, 2), 
                'ma20': round(ma20, 2), 'ma60': round(ma60, 2), 'trend': ','.join(trend) if trend else '震荡'}
    
    def analyze_magic_nine_turn(self):
        changes = [1 if self.prices[-i] > self.prices[-i-1] else -1 for i in range(1, min(14, len(self.prices)))]
        up_count = down_count = 0
        for c in changes:
            if c == 1:
                up_count, down_count = up_count + 1, 0
            else:
                down_count, up_count = down_count + 1, 0
            if up_count >= 9:
                return {'count': up_count, 'signal': '上涨九转(卖出)', 'strength': '强'}
            if down_count >= 9:
                return {'count': down_count, 'signal': '下跌九转(买入)', 'strength': '强'}
        return {'count': max(up_count, down_count), 'signal': '无九转信号', 'strength': '中性'}
    
    def analyze_level2_position(self):
        """Level2资金仓位分析"""
        vol_profile = defaultdict(float)
        for i, (price, vol