#!/usr/bin/env python3
"""
区间平衡版双色球预测算法
确保区间分布和大小分布符合历史规律
"""

import numpy as np
import pandas as pd
import random
from datetime import datetime
from ssq_features import SSQFeatureEngineer

def balanced_predict(data, features, zone_dist=(2, 2, 2)):
    """
    生成区间平衡的双色球预测
    zone_dist: (一区个数, 二区个数, 三区个数)
    """
    # 基础频率统计
    freq_red = np.zeros(33)
    freq_blue = np.zeros(16)
    
    for period in data:
        for j in range(6):
            freq_red[period[j] - 1] += 1
        freq_blue[period[6] - 1] += 1
    
    # 冷热号调整
    hot_red = features['hot_red_top5']
    for ball in hot_red:
        freq_red[ball - 1] += 1.5
    
    # 遗漏值调整
    high_missing_red = features['high_missing_red']
    for ball in high_missing_red[:3]:
        freq_red[ball - 1] += 1
    
    # 添加随机扰动
    freq_red += np.random.normal(0, 0.4, 33)
    blue_scores = freq_blue + np.random.normal(0, 0.3, 16)
    
    # 按指定区间分布选择
    zones = [
        (list(range(1, 12)), zone_dist[0]),    # 一区 01-11
        (list(range(12, 23)), zone_dist[1]),   # 二区 12-22
        (list(range(23, 34)), zone_dist[2])    # 三区 23-33
    ]
    
    selected_red = []
    for zone_balls, count in zones:
        zone_scores = [(ball, freq_red[ball-1]) for ball in zone_balls]
        zone_scores.sort(key=lambda x: x[1], reverse=True)
        
        for ball, _ in zone_scores[:count]:
            selected_red.append(ball)
    
    red_balls = sorted(selected_red)
    blue_ball = int(np.argmax(blue_scores)) + 1
    
    return red_balls, blue_ball


def generate_predictions(csv_path='ssq_history_100.csv', n_groups=6):
    """生成多组区间平衡的预测"""
    engineer = SSQFeatureEngineer(csv_path)
    features = engineer.generate_feature_vector()
    data = engineer.data
    
    # 定义不同的区间分布模式
    zone_patterns = [
        (2, 2, 2),  # 均衡型
        (3, 2, 1),  # 偏态型
        (2, 3, 1),  # 偏态型
        (1, 2, 3),  # 偏态型
        (3, 1, 2),  # 偏态型
        (2, 1, 3),  # 偏态型
    ]
    
    pattern_names = [
        '均衡型(2-2-2)',
        '偏态型(3-2-1)',
        '偏态型(2-3-1)',
        '偏态型(1-2-3)',
        '偏态型(3-1-2)',
        '偏态型(2-1-3)'
    ]
    
    results = []
    for i, (pattern, name) in enumerate(zip(zone_patterns[:n_groups], pattern_names[:n_groups])):
        random.seed(100 + i * 100)
        np.random.seed(100 + i * 100)
        
        red, blue = balanced_predict(data, features, pattern)
        zone1 = sum(1 for x in red if x <= 11)
        zone2 = sum(1 for x in red if 12 <= x <= 22)
        zone3 = sum(1 for x in red if x >= 23)
        small = sum(1 for x in red if x <= 16)
        big = 6 - small
        
        results.append({
            'name': name,
            'red': red,
            'blue': blue,
            'zone_dist': f"{zone1}-{zone2}-{zone3}",
            'size_dist': f"{small}-{big}"
        })
    
    return results


def main():
    print("=" * 70)
    print("🎱 双色球区间平衡预测")
    print("=" * 70)
    print(f"预测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    import os
    workspace = os.path.expanduser('~/.openclaw/workspace')
    csv_path = os.path.join(workspace, 'ssq_history_100.csv')
    results = generate_predictions(csv_path=csv_path)
    
    print("\n🎯 预测结果:")
    print("-" * 70)
    
    for r in results:
        red_str = ' '.join([f'{x:02d}' for x in r['red']])
        print(f"\n{r['name']}")
        print(f"  红球: [{red_str}]")
        print(f"  蓝球: [{r['blue']:02d}]")
        print(f"  区间: {r['zone_dist']} (一区-二区-三区)")
        print(f"  大小: {r['size_dist']} (小号-大号)")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
