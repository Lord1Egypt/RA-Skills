#!/usr/bin/env python3
"""
DEX历史价格分析器
分析历史价格数据，发现趋势和规律
"""

import json
import statistics
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

@dataclass
class PricePoint:
    """价格点"""
    timestamp: datetime
    price: float
    dex: Optional[str] = None
    volume: Optional[float] = None

class HistoricalAnalyzer:
    """历史价格分析器"""
    
    def __init__(self):
        self.price_data: Dict[str, List[PricePoint]] = defaultdict(list)
    
    def add_data(self, token_pair: str, point: PricePoint):
        """添加价格数据"""
        self.price_data[token_pair].append(point)
    
    def load_from_monitor_data(self, filename: str):
        """从监控数据加载"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            for pair, points in data.get('price_history', {}).items():
                for p in points:
                    point = PricePoint(
                        timestamp=datetime.fromisoformat(p['timestamp']),
                        price=p['price'],
                        dex=p.get('dex'),
                        volume=p.get('volume')
                    )
                    self.add_data(pair, point)
            
            print(f"✅ 已加载 {sum(len(v) for v in self.price_data.values())} 条记录")
        except FileNotFoundError:
            print(f"⚠️  文件 {filename} 不存在")
    
    def calculate_volatility(self, token_pair: str, window: int = 24) -> Dict:
        """计算波动率"""
        points = self.price_data.get(token_pair, [])
        
        if len(points) < 2:
            return {}
        
        prices = [p.price for p in points[-window:]]
        
        # 计算收益率
        returns = []
        for i in range(1, len(prices)):
            ret = (prices[i] - prices[i-1]) / prices[i-1]
            returns.append(ret)
        
        if not returns:
            return {}
        
        # 年化波动率
        hourly_vol = statistics.stdev(returns) if len(returns) > 1 else 0
        daily_vol = hourly_vol * (24 ** 0.5)
        annual_vol = daily_vol * (365 ** 0.5)
        
        return {
            'hourly_volatility': hourly_vol * 100,
            'daily_volatility': daily_vol * 100,
            'annual_volatility': annual_vol * 100,
            'mean_return': statistics.mean(returns) * 100 if returns else 0,
            'max_return': max(returns) * 100,
            'min_return': min(returns) * 100
        }
    
    def calculate_moving_average(self, token_pair: str, periods: List[int] = None) -> Dict[str, float]:
        """计算移动平均线"""
        if periods is None:
            periods = [7, 14, 30]
        
        points = self.price_data.get(token_pair, [])
        prices = [p.price for p in points]
        
        mas = {}
        for period in periods:
            if len(prices) >= period:
                ma = sum(prices[-period:]) / period
                mas[f'MA{period}'] = ma
        
        return mas
    
    def find_support_resistance(self, token_pair: str, window: int = 20) -> Dict:
        """找出支撑和阻力位"""
        points = self.price_data.get(token_pair, [])
        prices = [p.price for p in points[-window:]]
        
        if not prices:
            return {}
        
        # 简单方法：取高低点
        sorted_prices = sorted(prices)
        
        # 支撑位（20%低点）
        support_idx = int(len(sorted_prices) * 0.2)
        support = sorted_prices[support_idx]
        
        # 阻力位（80%高点）
        resistance_idx = int(len(sorted_prices) * 0.8)
        resistance = sorted_prices[resistance_idx]
        
        return {
            'support': support,
            'resistance': resistance,
            'current': prices[-1],
            'distance_to_support': (prices[-1] - support) / support * 100,
            'distance_to_resistance': (resistance - prices[-1]) / resistance * 100
        }
    
    def analyze_price_trend(self, token_pair: str) -> Dict:
        """分析价格趋势"""
        points = self.price_data.get(token_pair, [])
        
        if len(points) < 2:
            return {}
        
        prices = [p.price for p in points]
        
        # 计算各时间段变化
        current = prices[-1]
        
        trends = {
            'current_price': current,
            'price_1h_ago': prices[-2] if len(prices) >= 2 else None,
            'price_24h_ago': prices[-24] if len(prices) >= 24 else None,
        }
        
        if trends['price_1h_ago']:
            trends['change_1h'] = (current - trends['price_1h_ago']) / trends['price_1h_ago'] * 100
        
        if trends['price_24h_ago']:
            trends['change_24h'] = (current - trends['price_24h_ago']) / trends['price_24h_ago'] * 100
        
        # 趋势判断
        if 'change_24h' in trends:
            change = trends['change_24h']
            if change > 5:
                trends['trend'] = '强烈上涨 📈'
            elif change > 2:
                trends['trend'] = '上涨 ↗️'
            elif change > -2:
                trends['trend'] = '横盘 ➡️'
            elif change > -5:
                trends['trend'] = '下跌 ↘️'
            else:
                trends['trend'] = '强烈下跌 📉'
        
        return trends
    
    def calculate_price_statistics(self, token_pair: str) -> Dict:
        """计算价格统计"""
        points = self.price_data.get(token_pair, [])
        prices = [p.price for p in points]
        
        if not prices:
            return {}
        
        return {
            'count': len(prices),
            'mean': statistics.mean(prices),
            'median': statistics.median(prices),
            'stdev': statistics.stdev(prices) if len(prices) > 1 else 0,
            'min': min(prices),
            'max': max(prices),
            'range': max(prices) - min(prices),
            'current': prices[-1]
        }
    
    def detect_anomalies(self, token_pair: str, threshold: float = 3.0) -> List[PricePoint]:
        """检测异常价格"""
        points = self.price_data.get(token_pair, [])
        
        if len(points) < 10:
            return []
        
        prices = [p.price for p in points]
        mean = statistics.mean(prices)
        stdev = statistics.stdev(prices) if len(prices) > 1 else 0
        
        if stdev == 0:
            return []
        
        anomalies = []
        for p in points:
            z_score = abs(p.price - mean) / stdev
            if z_score > threshold:
                anomalies.append(p)
        
        return anomalies
    
    def get_hourly_pattern(self, token_pair: str) -> Dict[int, Dict]:
        """获取小时级模式"""
        points = self.price_data.get(token_pair, [])
        
        # 按小时分组
        hourly_data = defaultdict(list)
        for p in points:
            hour = p.timestamp.hour
            hourly_data[hour].append(p.price)
        
        pattern = {}
        for hour, prices in sorted(hourly_data.items()):
            if prices:
                pattern[hour] = {
                    'mean': statistics.mean(prices),
                    'count': len(prices),
                    'volatility': statistics.stdev(prices) if len(prices) > 1 else 0
                }
        
        return pattern
    
    def print_analysis(self, token_pair: str):
        """打印分析结果"""
        print(f"\n{'='*70}")
        print(f"📊 {token_pair} 历史价格分析")
        print(f"{'='*70}")
        
        # 基础统计
        stats = self.calculate_price_statistics(token_pair)
        if stats:
            print(f"\n📈 基础统计:")
            print(f"  数据点: {stats['count']}")
            print(f"  当前价格: ${stats['current']:,.2f}")
            print(f"  平均价格: ${stats['mean']:,.2f}")
            print(f"  中位数: ${stats['median']:,.2f}")
            print(f"  标准差: ${stats['stdev']:,.2f}")
            print(f"  最低: ${stats['min']:,.2f}")
            print(f"  最高: ${stats['max']:,.2f}")
        
        # 趋势分析
        trends = self.analyze_price_trend(token_pair)
        if trends:
            print(f"\n📉 趋势分析:")
            print(f"  当前: ${trends['current_price']:,.2f}")
            if 'change_1h' in trends:
                print(f"  1小时变化: {trends['change_1h']:+.2f}%")
            if 'change_24h' in trends:
                print(f"  24小时变化: {trends['change_24h']:+.2f}%")
            if 'trend' in trends:
                print(f"  趋势: {trends['trend']}")
        
        # 波动率
        vol = self.calculate_volatility(token_pair)
        if vol:
            print(f"\n📊 波动率:")
            print(f"  小时波动率: {vol['hourly_volatility']:.2f}%")
            print(f"  日波动率: {vol['daily_volatility']:.2f}%")
            print(f"  年波动率: {vol['annual_volatility']:.2f}%")
        
        # 支撑阻力
        sr = self.find_support_resistance(token_pair)
        if sr:
            print(f"\n🎯 支撑/阻力:")
            print(f"  支撑位: ${sr['support']:,.2f} ({sr['distance_to_support']:+.2f}%)")
            print(f"  阻力位: ${sr['resistance']:,.2f} ({sr['distance_to_resistance']:+.2f}%)")
        
        # 移动平均线
        mas = self.calculate_moving_average(token_pair)
        if mas:
            print(f"\n📊 移动平均线:")
            for name, value in mas.items():
                print(f"  {name}: ${value:,.2f}")
        
        # 异常检测
        anomalies = self.detect_anomalies(token_pair)
        if anomalies:
            print(f"\n⚠️  检测到 {len(anomalies)} 个异常价格点")
        
        print(f"{'='*70}\n")
    
    def export_report(self, filename: str):
        """导出分析报告"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'tokens': {}
        }
        
        for token_pair in self.price_data.keys():
            report['tokens'][token_pair] = {
                'statistics': self.calculate_price_statistics(token_pair),
                'volatility': self.calculate_volatility(token_pair),
                'trend': self.analyze_price_trend(token_pair),
                'support_resistance': self.find_support_resistance(token_pair),
                'moving_averages': self.calculate_moving_average(token_pair)
            }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"报告已导出到: {filename}")


def generate_sample_data() -> List[PricePoint]:
    """生成示例数据"""
    import random
    
    points = []
    base_time = datetime.now() - timedelta(days=7)
    base_price = 3500
    
    for i in range(168):  # 7天 * 24小时
        timestamp = base_time + timedelta(hours=i)
        
        # 随机游走
        change = random.gauss(0, 0.01)
        base_price *= (1 + change)
        
        # 添加趋势
        if i > 100:
            base_price *= 1.002  # 上涨趋势
        
        points.append(PricePoint(
            timestamp=timestamp,
            price=base_price,
            dex='Uniswap V3'
        ))
    
    return points


def demo():
    """演示"""
    print("📈 DEX历史价格分析器 - 演示")
    print("="*70)
    
    analyzer = HistoricalAnalyzer()
    
    # 生成示例数据
    print("\n📝 生成示例数据...")
    for point in generate_sample_data():
        analyzer.add_data('ETH/USDC', point)
    print(f"✅ 已生成数据\n")
    
    # 分析
    analyzer.print_analysis('ETH/USDC')
    
    # 小时模式
    print("\n⏰ 小时级价格模式:")
    pattern = analyzer.get_hourly_pattern('ETH/USDC')
    for hour, data in sorted(pattern.items())[:5]:  # 只显示前5个
        print(f"  {hour:02d}:00 - 平均: ${data['mean']:,.2f}, 波动: {data['volatility']:.2f}%")
    
    # 导出报告
    analyzer.export_report('historical_analysis_report.json')
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
