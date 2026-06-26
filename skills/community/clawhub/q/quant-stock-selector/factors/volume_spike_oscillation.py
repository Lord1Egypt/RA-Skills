#!/usr/bin/env python3
"""
成交量放大 + 震荡选股模块
识别 2 周内成交量放大几倍，然后短期震荡的股票
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from data.akshare_data import AKShareData


class VolumeSpikeOscillationCalculator:
    """成交量放大 + 震荡计算器"""
    
    def __init__(self):
        self.data = AKShareData()
    
    def detect_volume_spike(self, df_kline, window=10, spike_threshold=3):
        """
        检测成交量放大
        
        参数:
            df_kline: K 线数据
            window: 观察窗口（默认 10 个交易日，约 2 周）
            spike_threshold: 放大倍数阈值（默认 3 倍）
        
        返回:
            dict: 成交量放大检测结果
        """
        if df_kline.empty or len(df_kline) < window:
            return {'detected': False}
        
        # 取最近 window 天数据
        df = df_kline.tail(window).copy()
        
        # 计算均量线（5 日均量）
        df['volume_ma5'] = df['volume'].rolling(5).mean()
        
        # 找出成交量放大几倍的天
        volume_spikes = []
        
        for i in range(len(df)):
            if i < 5:  # 前 5 天无法计算 5 日均量
                continue
            
            current_volume = df.iloc[i]['volume']
            avg_volume = df.iloc[i]['volume_ma5']
            
            if avg_volume > 0:
                volume_ratio = current_volume / avg_volume
                
                if volume_ratio >= spike_threshold:
                    volume_spikes.append({
                        'date': df.index[i],
                        'volume': current_volume,
                        'avg_volume': avg_volume,
                        'ratio': volume_ratio,
                        'price': df.iloc[i]['close'],
                        'change_pct': df.iloc[i].get('change_pct', 0)
                    })
        
        if not volume_spikes:
            return {'detected': False}
        
        # 最近一次放量
        latest_spike = volume_spikes[-1]
        spike_index = df.index.tolist().index(latest_spike['date'])
        
        return {
            'detected': True,
            'spike_count': len(volume_spikes),
            'latest_spike': latest_spike,
            'max_ratio': max(s['ratio'] for s in volume_spikes),
            'spike_index': spike_index,
            'days_since_spike': len(df) - 1 - spike_index
        }
    
    def detect_oscillation(self, df_kline, days_after_spike=5):
        """
        检测放量后的震荡走势
        
        参数:
            df_kline: K 线数据
            days_after_spike: 放量后观察天数（默认 5 天）
        
        返回:
            dict: 震荡检测结果
        """
        if df_kline.empty or len(df_kline) < days_after_spike + 5:
            return {'detected': False}
        
        # 先检测放量
        spike_result = self.detect_volume_spike(df_kline, window=15)
        
        if not spike_result['detected']:
            return {'detected': False}
        
        # 获取放量后的 K 线
        spike_index = spike_result['spike_index']
        df = df_kline.tail(len(df_kline) - spike_index)
        
        if len(df) < days_after_spike:
            return {'detected': False}
        
        # 取放量后 days_after_spike 天数据
        post_spike_df = df.tail(days_after_spike)
        
        # 计算震荡指标
        highest_price = post_spike_df['high'].max()
        lowest_price = post_spike_df['low'].min()
        current_price = post_spike_df['close'].iloc[-1]
        spike_price = spike_result['latest_spike']['price']
        
        # 震荡幅度（最高 - 最低）/ 最低
        oscillation_range = (highest_price - lowest_price) / lowest_price * 100
        
        # 当前价格相对放量日的涨跌幅
        price_change = (current_price - spike_price) / spike_price * 100
        
        # 判断是否震荡（不是单边上涨或下跌）
        # 条件 1: 震荡幅度在 5-20% 之间
        # 条件 2: 当前价格相对放量日涨跌在 -10% 到 +15% 之间
        is_oscillation = (
            5 <= oscillation_range <= 25 and
            -10 <= price_change <= 15
        )
        
        # 计算震荡得分
        oscillation_score = 0
        
        # 震荡幅度适中（5-15%）：+40 分
        if 5 <= oscillation_range <= 15:
            oscillation_score += 40
        elif 5 <= oscillation_range <= 20:
            oscillation_score += 25
        elif 5 <= oscillation_range <= 25:
            oscillation_score += 10
        
        # 价格没有大幅下跌（> -5%）：+30 分
        if price_change > -5:
            oscillation_score += 30
        elif price_change > -10:
            oscillation_score += 15
        
        # 成交量萎缩（洗盘）：+30 分
        avg_volume_post = post_spike_df['volume'].mean()
        spike_volume = spike_result['latest_spike']['volume']
        volume_ratio = avg_volume_post / spike_volume
        
        if volume_ratio < 0.5:  # 缩量到放量时的 50% 以下
            oscillation_score += 30
        elif volume_ratio < 0.7:
            oscillation_score += 15
        
        return {
            'detected': is_oscillation,
            'score': min(100, oscillation_score),
            'oscillation_range': round(oscillation_range, 1),
            'price_change': round(price_change, 1),
            'volume_ratio': round(volume_ratio, 2),
            'highest_price': round(highest_price, 2),
            'lowest_price': round(lowest_price, 2),
            'current_price': round(current_price, 2),
            'spike_price': round(spike_price, 2),
            'days_since_spike': spike_result['days_since_spike'],
            'spike_ratio': round(spike_result['max_ratio'], 1)
        }
    
    def calculate_volume_oscillation_score(self, df_kline):
        """
        计算成交量放大 + 震荡综合得分
        
        返回:
            dict: 综合得分和详细数据
        """
        if df_kline.empty:
            return {'score': 0, 'details': {}}
        
        # 1. 检测成交量放大
        spike_result = self.detect_volume_spike(df_kline, window=10, spike_threshold=2)
        
        if not spike_result['detected']:
            return {'score': 0, 'details': {}}
        
        # 2. 检测震荡走势
        oscillation_result = self.detect_oscillation(df_kline, days_after_spike=5)
        
        # 3. 综合得分
        score = 0
        
        # 成交量放大倍数（2-5 倍）：+40 分
        spike_ratio = spike_result['max_ratio']
        if 3 <= spike_ratio <= 5:
            score += 40
        elif 2 <= spike_ratio <= 6:
            score += 25
        elif spike_ratio >= 2:
            score += 10
        
        # 震荡得分：+40 分
        if oscillation_result['detected']:
            score += oscillation_result['score'] * 0.4
        else:
            # 即使不是典型震荡，有放量也加分
            score += 20
        
        # 放量后时间短（<5 天）：+20 分
        days_since = spike_result['days_since_spike']
        if days_since < 3:
            score += 20
        elif days_since < 5:
            score += 10
        
        score = min(100, max(0, score))
        
        details = {
            'volume_spike_detected': True,
            'spike_ratio': round(spike_ratio, 1),
            'days_since_spike': days_since,
            'oscillation_detected': oscillation_result.get('detected', False),
            'oscillation_score': oscillation_result.get('score', 0),
            'oscillation_range': oscillation_result.get('oscillation_range', 0),
            'price_change': oscillation_result.get('price_change', 0),
            'volume_ratio': oscillation_result.get('volume_ratio', 0),
        }
        
        return {
            'score': round(score, 1),
            'details': details
        }


if __name__ == "__main__":
    # 测试
    print("=" * 70)
    print("📊 成交量放大 + 震荡检测测试")
    print("=" * 70)
    
    calculator = VolumeSpikeOscillationCalculator()
    
    # 获取测试股票 K 线
    test_stocks = [
        ("001207", "联科科技"),
        ("603032", "德新科技"),
        ("002326", "永太科技"),
    ]
    
    for code, name in test_stocks:
        print(f"\n测试 {name}({code})...")
        df_kline = calculator.data.get_history_kline(code)
        
        if not df_kline.empty:
            print(f"  ✅ 获取 K 线：{len(df_kline)}条")
            
            # 检测成交量放大
            spike_result = calculator.detect_volume_spike(df_kline, window=10, spike_threshold=2)
            
            if spike_result['detected']:
                print(f"  ✅ 检测到成交量放大")
                print(f"     放大倍数：{spike_result['max_ratio']:.1f}倍")
                print(f"     距今天数：{spike_result['days_since_spike']}天")
                
                # 检测震荡
                oscillation_result = calculator.detect_oscillation(df_kline, days_after_spike=5)
                
                if oscillation_result['detected']:
                    print(f"  ✅ 检测到震荡走势")
                    print(f"     震荡幅度：{oscillation_result['oscillation_range']:.1f}%")
                    print(f"     价格变化：{oscillation_result['price_change']:.1f}%")
                    print(f"     成交量比：{oscillation_result['volume_ratio']:.2f}")
                else:
                    print(f"  ⚠️ 未检测到典型震荡")
            else:
                print(f"  ❌ 未检测到成交量放大")
        else:
            print(f"  ❌ 获取 K 线失败")
    
    print("\n" + "=" * 70)
