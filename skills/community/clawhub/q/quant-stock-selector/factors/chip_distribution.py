#!/usr/bin/env python3
"""
筹码峰计算模块
计算筹码分布、筹码峰位置、上方压力等
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from data.akshare_data import AKShareData


class ChipDistributionCalculator:
    """筹码分布计算器"""
    
    def __init__(self):
        self.data = AKShareData()
    
    def calculate_chip_distribution(self, df_kline, window=180):
        """
        计算筹码分布
        使用成交量加权平均成本法
        
        参数:
            df_kline: K 线数据（包含 open, high, low, close, volume）
            window: 计算窗口（默认 180 天）
        
        返回:
            dict: 筹码分布数据
        """
        if df_kline.empty or len(df_kline) < window:
            return {}
        
        # 取最近 window 天数据
        df = df_kline.tail(window).copy()
        
        # 计算典型价格（(高 + 低 + 收) / 3）
        df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
        
        # 计算成交量加权的典型价格
        df['volume_price'] = df['volume'] * df['typical_price']
        
        # 计算筹码分布（按价格区间分组）
        price_min = df['low'].min()
        price_max = df['high'].max()
        price_range = price_max - price_min
        
        if price_range <= 0:
            return {}
        
        # 分成 50 个价格区间
        num_bins = 50
        bin_size = price_range / num_bins
        
        chip_distribution = []
        
        for i in range(num_bins):
            bin_low = price_min + i * bin_size
            bin_high = price_min + (i + 1) * bin_size
            
            # 计算该价格区间的筹码量（成交量）
            mask = (df['low'] <= bin_high) & (df['high'] >= bin_low)
            chip_volume = df.loc[mask, 'volume'].sum()
            
            chip_distribution.append({
                'price_low': bin_low,
                'price_high': bin_high,
                'price_mid': (bin_low + bin_high) / 2,
                'chip_volume': chip_volume,
                'chip_pct': 0  # 稍后计算百分比
            })
        
        # 计算百分比
        total_volume = sum(c['chip_volume'] for c in chip_distribution)
        if total_volume > 0:
            for c in chip_distribution:
                c['chip_pct'] = c['chip_volume'] / total_volume * 100
        
        return {
            'distribution': chip_distribution,
            'price_min': price_min,
            'price_max': price_max,
            'current_price': df['close'].iloc[-1],
            'total_volume': total_volume
        }
    
    def find_chip_peaks(self, chip_distribution):
        """
        找出筹码峰（筹码密集区）
        
        返回:
            list: 筹码峰列表，每个峰包含价格区间和筹码比例
        """
        if not chip_distribution or 'distribution' not in chip_distribution:
            return []
        
        distribution = chip_distribution['distribution']
        peaks = []
        
        # 找出筹码比例>5% 的区间作为筹码峰
        for i, chip in enumerate(distribution):
            if chip['chip_pct'] > 5:  # 筹码比例>5%
                # 检查是否是局部最大值
                is_peak = True
                
                if i > 0 and distribution[i-1]['chip_pct'] > chip['chip_pct']:
                    is_peak = False
                if i < len(distribution)-1 and distribution[i+1]['chip_pct'] > chip['chip_pct']:
                    is_peak = False
                
                if is_peak:
                    peaks.append({
                        'price_low': chip['price_low'],
                        'price_high': chip['price_high'],
                        'price_mid': chip['price_mid'],
                        'chip_pct': chip['chip_pct']
                    })
        
        # 按筹码比例排序
        peaks.sort(key=lambda x: x['chip_pct'], reverse=True)
        
        return peaks
    
    def calculate_pressure_ratio(self, chip_distribution, current_price=None):
        """
        计算上方压力筹码比例
        
        参数:
            chip_distribution: 筹码分布数据
            current_price: 当前价格（默认使用分布中的当前价）
        
        返回:
            float: 上方压力筹码比例（0-100）
        """
        if not chip_distribution or 'distribution' not in chip_distribution:
            return 100
        
        if current_price is None:
            current_price = chip_distribution.get('current_price', 0)
        
        distribution = chip_distribution['distribution']
        
        # 计算当前价格上方的筹码比例
        pressure_volume = 0
        total_volume = chip_distribution.get('total_volume', 0)
        
        for chip in distribution:
            if chip['price_mid'] > current_price:
                pressure_volume += chip['chip_volume']
        
        if total_volume > 0:
            pressure_ratio = pressure_volume / total_volume * 100
        else:
            pressure_ratio = 100
        
        return pressure_ratio
    
    def calculate_profit_ratio(self, chip_distribution, current_price=None):
        """
        计算获利盘比例（当前价格下方的筹码比例）
        
        返回:
            float: 获利盘比例（0-100）
        """
        if not chip_distribution or 'distribution' not in chip_distribution:
            return 0
        
        if current_price is None:
            current_price = chip_distribution.get('current_price', 0)
        
        distribution = chip_distribution['distribution']
        
        # 计算当前价格下方的筹码比例
        profit_volume = 0
        total_volume = chip_distribution.get('total_volume', 0)
        
        for chip in distribution:
            if chip['price_mid'] < current_price:
                profit_volume += chip['chip_volume']
        
        if total_volume > 0:
            profit_ratio = profit_volume / total_volume * 100
        else:
            profit_ratio = 0
        
        return profit_ratio
    
    def calculate_recent_gain(self, df_kline, days=20):
        """
        计算近期涨幅
        
        参数:
            df_kline: K 线数据
            days: 计算天数（默认 20 天）
        
        返回:
            float: 近期涨幅（%）
        """
        if df_kline.empty or len(df_kline) < days:
            return 0
        
        recent_close = df_kline['close'].iloc[-1]
        past_close = df_kline['close'].iloc[-days]
        
        if past_close > 0:
            gain = (recent_close - past_close) / past_close * 100
        else:
            gain = 0
        
        return gain
    
    def calculate_concentration_90(self, chip_distribution):
        """
        计算 90% 筹码集中度
        
        定义：90% 的筹码集中在什么价格区间内
        区间越小，说明筹码越集中，主力控盘程度越高
        
        返回:
            float: 集中度百分比（越小越好）
        """
        if not chip_distribution or 'distribution' not in chip_distribution:
            return 100
        
        distribution = chip_distribution['distribution']
        total_volume = chip_distribution.get('total_volume', 0)
        
        if total_volume <= 0:
            return 100
        
        # 按筹码量排序，找出包含 90% 筹码的最小价格区间
        sorted_chips = sorted(distribution, key=lambda x: x['chip_volume'], reverse=True)
        
        accumulated_volume = 0
        price_min = float('inf')
        price_max = 0
        target_volume = total_volume * 0.9  # 90% 筹码
        
        for chip in sorted_chips:
            accumulated_volume += chip['chip_volume']
            price_min = min(price_min, chip['price_low'])
            price_max = max(price_max, chip['price_high'])
            
            if accumulated_volume >= target_volume:
                break
        
        # 计算集中度（价格区间 / 平均价格）
        avg_price = (price_min + price_max) / 2
        if avg_price > 0:
            concentration = (price_max - price_min) / avg_price * 100
        else:
            concentration = 100
        
        return round(concentration, 1)
    
    def calculate_chip_score(self, df_kline):
        """
        计算筹码峰得分（0-100）
        
        评分标准（新增 90% 集中度）:
        1. 上方压力筹码比例<20%：+35 分
        2. 获利盘比例>50%：+25 分
        3. 近期涨幅<30%：+20 分
        4. 90% 集中度<10%：+20 分 ⭐ 新增
        
        返回:
            dict: 筹码峰得分和详细数据
        """
        if df_kline.empty:
            return {'score': 0, 'details': {}}
        
        # 1. 计算筹码分布
        chip_dist = self.calculate_chip_distribution(df_kline, window=180)
        
        if not chip_dist:
            return {'score': 0, 'details': {}}
        
        # 2. 找出筹码峰
        peaks = self.find_chip_peaks(chip_dist)
        
        # 3. 计算上方压力比例
        current_price = chip_dist.get('current_price', 0)
        pressure_ratio = self.calculate_pressure_ratio(chip_dist, current_price)
        
        # 4. 计算获利盘比例
        profit_ratio = self.calculate_profit_ratio(chip_dist, current_price)
        
        # 5. 计算近期涨幅
        recent_gain = self.calculate_recent_gain(df_kline, days=20)
        
        # 6. 计算 90% 集中度 ⭐ 新增
        concentration_90 = self.calculate_concentration_90(chip_dist)
        
        # 7. 计算得分
        score = 0
        
        # 上方压力<20%：+35 分（原 40 分，调整为 35 分）
        if pressure_ratio < 20:
            score += 35
        elif pressure_ratio < 40:
            score += 20
        elif pressure_ratio < 60:
            score += 10
        
        # 获利盘>50%：+25 分（原 30 分，调整为 25 分）
        if profit_ratio > 50:
            score += 25
        elif profit_ratio > 30:
            score += 15
        
        # 近期涨幅<30%：+20 分（原 30 分，调整为 20 分）
        if recent_gain < 30:
            score += 20
        elif recent_gain < 50:
            score += 10
        
        # 90% 集中度<10%：+20 分 ⭐ 新增
        if concentration_90 < 10:
            score += 20
        elif concentration_90 < 15:
            score += 10
        elif concentration_90 < 20:
            score += 5
        
        # 筹码峰在下方：+10 分（额外加分，总分可能超过 100）
        if peaks and current_price > peaks[0]['price_mid']:
            score += 10
        
        # 限制在 0-100
        score = min(100, max(0, score))
        
        details = {
            'pressure_ratio': round(pressure_ratio, 1),
            'profit_ratio': round(profit_ratio, 1),
            'recent_gain': round(recent_gain, 1),
            'concentration_90': round(concentration_90, 1),  # ⭐ 新增
            'chip_peaks': len(peaks),
            'current_price': current_price,
            'peak_prices': [p['price_mid'] for p in peaks[:3]] if peaks else []
        }
        
        return {
            'score': score,
            'details': details
        }


if __name__ == "__main__":
    # 测试
    print("=" * 70)
    print("📊 筹码峰计算测试")
    print("=" * 70)
    
    calculator = ChipDistributionCalculator()
    
    # 获取测试股票 K 线
    print("\n获取测试股票 K 线...")
    df_kline = calculator.data.get_history_kline("001207")  # 联科科技
    
    if not df_kline.empty:
        print(f"✅ 获取 K 线：{len(df_kline)}条")
        
        # 计算筹码峰得分
        print("\n计算筹码峰得分...")
        result = calculator.calculate_chip_score(df_kline)
        
        print(f"\n筹码峰得分：{result['score']}分")
        print(f"上方压力：{result['details'].get('pressure_ratio', 0):.1f}%")
        print(f"获利盘：{result['details'].get('profit_ratio', 0):.1f}%")
        print(f"近期涨幅：{result['details'].get('recent_gain', 0):.1f}%")
        print(f"筹码峰数量：{result['details'].get('chip_peaks', 0)}")
        
        # 评分解读
        print("\n评分解读:")
        if result['score'] >= 70:
            print("✅ 筹码结构优秀（上方压力小，获利盘多，涨幅适中）")
        elif result['score'] >= 50:
            print("🟡 筹码结构良好")
        else:
            print("❌ 筹码结构一般（上方压力大或涨幅过大）")
    else:
        print("❌ 获取 K 线失败")
    
    print("\n" + "=" * 70)
