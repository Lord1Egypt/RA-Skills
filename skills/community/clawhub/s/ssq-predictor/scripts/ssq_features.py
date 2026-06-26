#!/usr/bin/env python3
"""
双色球特征工程模块
提供冷热号分析、遗漏值、区间分布、奇偶比、大小比等特征
"""

import numpy as np
import pandas as pd
from collections import Counter
from datetime import datetime

class SSQFeatureEngineer:
    """双色球特征工程类"""
    
    def __init__(self, csv_path='ssq_history_100.csv'):
        self.data = self._load_data(csv_path)
        self.red_history = self.data[:, :6]
        self.blue_history = self.data[:, 6]
        
    def _load_data(self, csv_path):
        df = pd.read_csv(csv_path, skiprows=4)
        data = []
        for _, row in df.iterrows():
            red_balls = [int(row[f'红球{i}']) for i in range(1, 7)]
            blue_ball = int(row['蓝球'])
            data.append(red_balls + [blue_ball])
        return np.array(data)
    
    def get_hot_cold_numbers(self, periods=30):
        recent_data = self.data[-periods:]
        red_counter = Counter()
        blue_counter = Counter()
        
        for period in recent_data:
            for i in range(6):
                red_counter[period[i]] += 1
            blue_counter[period[6]] += 1
        
        hot_red = red_counter.most_common()
        cold_red = list(reversed(hot_red))
        hot_blue = blue_counter.most_common()
        cold_blue = list(reversed(hot_blue))
        
        return {
            'hot_red': hot_red,
            'cold_red': cold_red,
            'hot_blue': hot_blue,
            'cold_blue': cold_blue,
            'periods': periods
        }
    
    def get_missing_values(self):
        red_missing = {}
        blue_missing = {}
        
        for ball in range(1, 34):
            found = False
            for i in range(len(self.data) - 1, -1, -1):
                if ball in self.data[i, :6]:
                    red_missing[ball] = len(self.data) - 1 - i
                    found = True
                    break
            if not found:
                red_missing[ball] = len(self.data)
        
        for ball in range(1, 17):
            found = False
            for i in range(len(self.data) - 1, -1, -1):
                if ball == self.data[i, 6]:
                    blue_missing[ball] = len(self.data) - 1 - i
                    found = True
                    break
            if not found:
                blue_missing[ball] = len(self.data)
        
        return {'red_missing': red_missing, 'blue_missing': blue_missing}
    
    def get_zone_distribution(self, periods=10):
        recent_data = self.data[-periods:]
        zone_stats = {'zone1': 0, 'zone2': 0, 'zone3': 0}
        
        for period in recent_data:
            for i in range(6):
                ball = period[i]
                if 1 <= ball <= 11:
                    zone_stats['zone1'] += 1
                elif 12 <= ball <= 22:
                    zone_stats['zone2'] += 1
                else:
                    zone_stats['zone3'] += 1
        
        return zone_stats
    
    def generate_feature_vector(self):
        features = {}
        
        hot_cold = self.get_hot_cold_numbers(30)
        features['hot_red_top5'] = [x[0] for x in hot_cold['hot_red'][:5]]
        features['cold_red_top5'] = [x[0] for x in hot_cold['cold_red'][:5]]
        features['hot_blue_top3'] = [x[0] for x in hot_cold['hot_blue'][:3]]
        
        missing = self.get_missing_values()
        features['high_missing_red'] = [
            k for k, v in sorted(missing['red_missing'].items(), 
                                key=lambda x: x[1], reverse=True)[:5]
        ]
        features['high_missing_blue'] = [
            k for k, v in sorted(missing['blue_missing'].items(), 
                                key=lambda x: x[1], reverse=True)[:3]
        ]
        
        zone_dist = self.get_zone_distribution(10)
        features['zone_distribution'] = zone_dist
        features['dominant_zone'] = max(zone_dist, key=zone_dist.get)
        
        return features
    
    def print_feature_report(self):
        print("=" * 60)
        print("📊 双色球特征分析报告")
        print("=" * 60)
        
        print("\n🔥 冷热号分析 (最近30期)")
        print("-" * 40)
        hot_cold = self.get_hot_cold_numbers(30)
        print(f"热红球 TOP5: {[f'{x[0]:02d}({x[1]}次)' for x in hot_cold['hot_red'][:5]]}")
        print(f"冷红球 TOP5: {[f'{x[0]:02d}({x[1]}次)' for x in hot_cold['cold_red'][:5]]}")
        print(f"热蓝球 TOP3: {[f'{x[0]:02d}({x[1]}次)' for x in hot_cold['hot_blue'][:3]]}")
        
        print("\n⏱️ 遗漏值分析")
        print("-" * 40)
        missing = self.get_missing_values()
        high_missing_red = sorted(missing['red_missing'].items(), 
                                  key=lambda x: x[1], reverse=True)[:5]
        high_missing_blue = sorted(missing['blue_missing'].items(), 
                                   key=lambda x: x[1], reverse=True)[:3]
        print(f"红球遗漏 TOP5: {[f'{x[0]:02d}({x[1]}期)' for x in high_missing_red]}")
        print(f"蓝球遗漏 TOP3: {[f'{x[0]:02d}({x[1]}期)' for x in high_missing_blue]}")
        
        print("\n📍 区间分布 (最近10期)")
        print("-" * 40)
        zone_dist = self.get_zone_distribution(10)
        print(f"一区(01-11): {zone_dist['zone1']}次")
        print(f"二区(12-22): {zone_dist['zone2']}次")
        print(f"三区(23-33): {zone_dist['zone3']}次")
        
        print("\n" + "=" * 60)


if __name__ == '__main__':
    import os
    workspace = os.path.expanduser('~/.openclaw/workspace')
    csv_path = os.path.join(workspace, 'ssq_history_100.csv')
    engineer = SSQFeatureEngineer(csv_path)
    engineer.print_feature_report()
