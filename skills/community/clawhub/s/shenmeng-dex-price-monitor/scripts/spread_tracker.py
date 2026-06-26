#!/usr/bin/env python3
"""
DEX价差追踪器
追踪和分析DEX间的价差历史，发现规律
"""

import json
import statistics
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import matplotlib.pyplot as plt
from collections import defaultdict

@dataclass
class SpreadRecord:
    """价差记录"""
    timestamp: datetime
    token_pair: str
    dex1: str
    dex2: str
    price1: float
    price2: float
    spread_pct: float
    direction: str  # 'positive' or 'negative'

class SpreadTracker:
    """价差追踪器"""
    
    def __init__(self):
        self.records: List[SpreadRecord] = []
        self.statistics: Dict = {}
    
    def add_record(self, record: SpreadRecord):
        """添加记录"""
        self.records.append(record)
    
    def load_from_file(self, filename: str):
        """从文件加载数据"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            for item in data:
                record = SpreadRecord(
                    timestamp=datetime.fromisoformat(item['timestamp']),
                    token_pair=item['token_pair'],
                    dex1=item['dex1'],
                    dex2=item['dex2'],
                    price1=item['price1'],
                    price2=item['price2'],
                    spread_pct=item['spread_pct'],
                    direction=item['direction']
                )
                self.records.append(record)
            
            print(f"✅ 已加载 {len(self.records)} 条记录")
        except FileNotFoundError:
            print(f"⚠️  文件 {filename} 不存在")
    
    def calculate_statistics(self, token_pair: Optional[str] = None) -> Dict:
        """计算统计信息"""
        records = self.records
        if token_pair:
            records = [r for r in records if r.token_pair == token_pair]
        
        if not records:
            return {}
        
        spreads = [r.spread_pct for r in records]
        
        stats = {
            'count': len(spreads),
            'mean': statistics.mean(spreads),
            'median': statistics.median(spreads),
            'stdev': statistics.stdev(spreads) if len(spreads) > 1 else 0,
            'min': min(spreads),
            'max': max(spreads),
            'p95': sorted(spreads)[int(len(spreads) * 0.95)],
            'p99': sorted(spreads)[int(len(spreads) * 0.99)]
        }
        
        return stats
    
    def analyze_by_time(self, token_pair: str, interval: str = 'hour') -> Dict:
        """按时间分析价差"""
        records = [r for r in self.records if r.token_pair == token_pair]
        
        if not records:
            return {}
        
        # 按时间分组
        grouped = defaultdict(list)
        
        for r in records:
            if interval == 'hour':
                key = r.timestamp.strftime('%H:00')
            elif interval == 'day':
                key = r.timestamp.strftime('%Y-%m-%d')
            else:
                key = r.timestamp.strftime('%Y-%m-%d %H:00')
            
            grouped[key].append(r.spread_pct)
        
        # 计算每组统计
        analysis = {}
        for key, spreads in sorted(grouped.items()):
            analysis[key] = {
                'count': len(spreads),
                'mean': statistics.mean(spreads),
                'max': max(spreads)
            }
        
        return analysis
    
    def find_best_opportunities(self, min_spread: float = 0.5, top_n: int = 10) -> List[SpreadRecord]:
        """找出最佳套利机会"""
        opportunities = [r for r in self.records if abs(r.spread_pct) >= min_spread]
        opportunities.sort(key=lambda x: abs(x.spread_pct), reverse=True)
        return opportunities[:top_n]
    
    def get_spread_distribution(self, token_pair: str, bins: int = 20) -> Tuple[List[float], List[int]]:
        """获取价差分布"""
        records = [r for r in self.records if r.token_pair == token_pair]
        spreads = [r.spread_pct for r in records]
        
        if not spreads:
            return [], []
        
        min_val = min(spreads)
        max_val = max(spreads)
        bin_width = (max_val - min_val) / bins
        
        bin_edges = [min_val + i * bin_width for i in range(bins + 1)]
        bin_counts = [0] * bins
        
        for spread in spreads:
            bin_idx = int((spread - min_val) / bin_width)
            bin_idx = min(bin_idx, bins - 1)
            bin_counts[bin_idx] += 1
        
        return bin_edges, bin_counts
    
    def calculate_arbitrage_frequency(self, threshold: float = 0.5) -> Dict:
        """计算套利频率"""
        total_records = len(self.records)
        opportunities = len([r for r in self.records if abs(r.spread_pct) >= threshold])
        
        return {
            'total_records': total_records,
            'opportunities': opportunities,
            'frequency': opportunities / total_records if total_records > 0 else 0,
            'threshold': threshold
        }
    
    def print_statistics(self, token_pair: Optional[str] = None):
        """打印统计信息"""
        stats = self.calculate_statistics(token_pair)
        
        if not stats:
            print("没有数据")
            return
        
        pair_str = f" ({token_pair})" if token_pair else ""
        
        print(f"\n{'='*70}")
        print(f"📊 价差统计{pair_str}")
        print(f"{'='*70}")
        print(f"样本数量: {stats['count']}")
        print(f"平均价差: {stats['mean']:.4f}%")
        print(f"中位数: {stats['median']:.4f}%")
        print(f"标准差: {stats['stdev']:.4f}%")
        print(f"最小值: {stats['min']:.4f}%")
        print(f"最大值: {stats['max']:.4f}%")
        print(f"95分位数: {stats['p95']:.4f}%")
        print(f"99分位数: {stats['p99']:.4f}%")
        print(f"{'='*70}\n")
    
    def print_time_analysis(self, token_pair: str, interval: str = 'hour'):
        """打印时间分析"""
        analysis = self.analyze_by_time(token_pair, interval)
        
        if not analysis:
            print("没有数据")
            return
        
        print(f"\n{'='*70}")
        print(f"⏰ {token_pair} 按{interval}分析")
        print(f"{'='*70}")
        print(f"{'时间':<15} {'次数':<10} {'平均价差':<15} {'最大价差':<15}")
        print(f"{'-'*70}")
        
        for time_key, data in sorted(analysis.items()):
            print(f"{time_key:<15} {data['count']:<10} {data['mean']:>12.4f}% {data['max']:>12.4f}%")
        
        print(f"{'='*70}\n")
    
    def plot_spread_history(self, token_pair: str, save_path: Optional[str] = None):
        """绘制价差历史"""
        try:
            import matplotlib
            matplotlib.use('Agg')  # 无GUI环境
            import matplotlib.pyplot as plt
        except ImportError:
            print("⚠️  需要安装matplotlib: pip install matplotlib")
            return
        
        records = [r for r in self.records if r.token_pair == token_pair]
        
        if not records:
            print("没有数据")
            return
        
        timestamps = [r.timestamp for r in records]
        spreads = [r.spread_pct for r in records]
        
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, spreads, linewidth=0.5)
        plt.axhline(y=0, color='r', linestyle='--', linewidth=0.5)
        plt.title(f'{token_pair} 价差历史')
        plt.xlabel('时间')
        plt.ylabel('价差 (%)')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            print(f"图表已保存到: {save_path}")
        else:
            plt.show()
    
    def export_report(self, filename: str):
        """导出报告"""
        # 获取所有交易对
        token_pairs = set(r.token_pair for r in self.records)
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_records': len(self.records),
                'unique_pairs': len(token_pairs)
            },
            'by_pair': {}
        }
        
        for pair in token_pairs:
            stats = self.calculate_statistics(pair)
            freq_05 = self.calculate_arbitrage_frequency(0.5)
            freq_10 = self.calculate_arbitrage_frequency(1.0)
            
            report['by_pair'][pair] = {
                'statistics': stats,
                'arbitrage_frequency_0.5%': freq_05,
                'arbitrage_frequency_1.0%': freq_10
            }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"报告已导出到: {filename}")


def generate_sample_data() -> List[SpreadRecord]:
    """生成示例数据"""
    import random
    
    records = []
    base_time = datetime.now() - timedelta(days=7)
    
    for i in range(1000):
        timestamp = base_time + timedelta(minutes=i * 10)
        
        # 模拟ETH/USDC在不同DEX的价格
        base_price = 3500 + random.gauss(0, 50)
        
        price1 = base_price * (1 + random.gauss(0, 0.001))
        price2 = base_price * (1 + random.gauss(0, 0.0015))
        
        spread = (price2 - price1) / price1 * 100
        
        record = SpreadRecord(
            timestamp=timestamp,
            token_pair='ETH/USDC',
            dex1='Uniswap V3',
            dex2='SushiSwap',
            price1=price1,
            price2=price2,
            spread_pct=spread,
            direction='positive' if spread > 0 else 'negative'
        )
        records.append(record)
    
    return records


def demo():
    """演示"""
    print("📈 DEX价差追踪器 - 演示")
    print("="*70)
    
    tracker = SpreadTracker()
    
    # 生成示例数据
    print("\n📝 生成示例数据...")
    records = generate_sample_data()
    for r in records:
        tracker.add_record(r)
    print(f"✅ 已生成 {len(records)} 条记录\n")
    
    # 统计信息
    tracker.print_statistics('ETH/USDC')
    
    # 套利频率
    print("\n📊 套利频率分析:")
    freq_05 = tracker.calculate_arbitrage_frequency(0.5)
    freq_10 = tracker.calculate_arbitrage_frequency(1.0)
    
    print(f"  价差 > 0.5%: {freq_05['frequency']*100:.2f}% ({freq_05['opportunities']}次)")
    print(f"  价差 > 1.0%: {freq_10['frequency']*100:.2f}% ({freq_10['opportunities']}次)")
    
    # 最佳机会
    print("\n🏆 最佳套利机会 (Top 5):")
    best = tracker.find_best_opportunities(min_spread=0.3, top_n=5)
    for i, opp in enumerate(best, 1):
        print(f"  {i}. {opp.timestamp.strftime('%m-%d %H:%M')} | "
              f"{opp.dex1} -> {opp.dex2} | {opp.spread_pct:.2f}%")
    
    # 导出报告
    print("\n💾 导出报告...")
    tracker.export_report('spread_analysis_report.json')
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
