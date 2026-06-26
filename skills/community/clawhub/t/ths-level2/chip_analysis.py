# -*- coding: utf-8 -*-
"""
同花顺筹码分析系统
包含：筹码分布、股东人数变化、筹码集中度分析
"""
import os
import sys
import json
import io
import statistics
from datetime import datetime, timedelta
from pathlib import Path

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

class ChipAnalyzer:
    """筹码分析器"""
    
    def __init__(self, code, info):
        self.code = code
        self.name = info['name']
        self.cost = info['cost']
        self.current = info['current']
        self.shares = info['shares']
        self.change = info['change']
        # 生成模拟历史数据
        self._generate_mock_data()
    
    def _generate_mock_data(self):
        """生成模拟筹码和股东数据"""
        import random
        random.seed(int(self.code))
        
        # 生成60日价格数据（用于筹码分布）
        base_price = self.current * 0.9
        self.prices = []
        self.volumes = []
        for i in range(60):
            change = random.uniform(-0.03, 0.03)
            price = base_price * (1 + change)
            base_price = price
            self.prices.append(price)
            volume = random.randint(100000, 500000)
            self.volumes.append(volume)
        self.prices[-1] = self.current
        
        # 生成模拟股东人数数据（最近8个季度）
        current_shareholders = random.randint(50000, 200000)
        self.shareholder_counts = []
        for i in range(8):
            # 模拟股东人数变化趋势
            if i == 0:
                count = current_shareholders
            else:
                # 随机变化，但总体趋势
                change_pct = random.uniform(-0.15, 0.15)
                count = int(self.shareholder_counts[-1] * (1 + change_pct))
                count = max(10000, count)  # 最少1万人
            self.shareholder_counts.append(count)
        
        # 确保最新数据在最后
        self.shareholder_counts.reverse()
    
    def analyze_chip_distribution(self):
        """
        筹码分布分析
        基于历史价格和成交量计算筹码分布
        """
        if len(self.prices) < 20:
            return {'status': '数据不足'}
        
        # 计算价格区间
        min_price = min(self.prices)
        max_price = max(self.prices)
        price_range = max_price - min_price
        
        if price_range == 0:
            return {'status': '价格无波动'}
        
        # 将价格分为10个区间
        interval_size = price_range / 10
        chip_distribution = [0] * 10
        
        # 根据成交量加权计算筹码分布
        for price, volume in zip(self.prices, self.volumes):
            if price_range > 0:
                interval_index = min(9, int((price - min_price) / interval_size))
                chip_distribution[interval_index] += volume
        
        # 找到筹码密集区
        max_chips = max(chip_distribution)
        dense_intervals = []
        for i, chips in enumerate(chip_distribution):
            if chips >= max_chips * 0.7:  # 筹码密集区定义为最大值的70%以上
                price_start = min_price + i * interval_size
                price_end = min_price + (i + 1) * interval_size
                dense_intervals.append({
                    'start': round(price_start, 2),
                    'end': round(price_end, 2),
                    'chips': chips,
                    'percentage': round(chips / sum(chip_distribution) * 100, 1)
                })
        
        # 计算当前价格位置
        if self.current <= min_price:
            current_position = '最低位'
        elif self.current >= max_price:
            current_position = '最高位'
        else:
            position_pct = (self.current - min_price) / price_range * 100
            if position_pct < 30:
                current_position = '低位'
            elif position_pct < 70:
                current_position = '中位'
            else:
                current_position = '高位'
        
        # 计算筹码集中度
        total_chips = sum(chip_distribution)
        top_3_intervals = sorted(chip_distribution, reverse=True)[:3]
        concentration_ratio = sum(top_3_intervals) / total_chips if total_chips > 0 else 0
        
        if concentration_ratio > 0.7:
            concentration_level = '高度集中'
        elif concentration_ratio > 0.5:
            concentration_level = '中度集中'
        elif concentration_ratio > 0.3:
            concentration_level = '分散'
        else:
            concentration_level = '极度分散'
        
        return {
            'min_price': round(min_price, 2),
            'max_price': round(max_price, 2),
            'current_position': current_position,
            'dense_intervals': dense_intervals[:3],  # 返回前3个密集区
            'concentration_ratio': round(concentration_ratio, 3),
            'concentration_level': concentration_level,
            'total_volume': sum(self.volumes)
        }
    
    def analyze_shareholder_trend(self):
        """
        股东人数变化分析
        股东人数减少 = 筹码集中，股东人数增加 = 筹码分散
        """
        if len(self.shareholder_counts) < 2:
            return {'status': '数据不足'}
        
        current_count = self.shareholder_counts[-1]
        previous_count = self.shareholder_counts[-2]
        
        # 计算变化率
        change_pct = (current_count - previous_count) / previous_count * 100
        
        # 判断趋势
        if change_pct < -10:
            trend = '显著减少'
            signal = '筹码高度集中'
            strength = '强'
        elif change_pct < -5:
            trend = '明显减少'
            signal = '筹码集中'
            strength = '中'
        elif change_pct < -2:
            trend = '小幅减少'
            signal = '筹码略集中'
            strength = '弱'
        elif change_pct > 10:
            trend = '显著增加'
            signal = '筹码高度分散'
            strength = '强'
        elif change_pct > 5:
            trend = '明显增加'
            signal = '筹码分散'
            strength = '中'
        elif change_pct > 2:
            trend = '小幅增加'
            signal = '筹码略分散'
            strength = '弱'
        else:
            trend = '基本稳定'
            signal = '筹码稳定'
            strength = '中性'
        
        # 分析长期趋势（最近4个季度）
        recent_trend = []
        for i in range(1, min(4, len(self.shareholder_counts))):
            quarterly_change = (self.shareholder_counts[-i] - self.shareholder_counts[-i-1]) / self.shareholder_counts[-i-1] * 100
            recent_trend.append(quarterly_change)
        
        avg_recent_change = statistics.mean(recent_trend) if recent_trend else 0
        
        if avg_recent_change < -5:
            long_term_trend = '持续集中'
        elif avg_recent_change > 5:
            long_term_trend = '持续分散'
        else:
            long_term_trend = '震荡整理'
        
        return {
            'current_count': current_count,
            'previous_count': previous_count,
            'change_pct': round(change_pct, 2),
            'trend': trend,
            'signal': signal,
            'strength': strength,
            'long_term_trend': long_term_trend,
            'recent_quarters': self.shareholder_counts[-4:]  # 最近4个季度
        }
    
    def calculate_profitable_ratio(self):
        """
        获利盘比例估算
        基于当前价格与历史成本分布
        """
        if len(self.prices) < 10:
            return {'status': '数据不足'}
        
        # 简单估算：当前价格高于历史多少比例的价格
        profitable_count = sum(1 for price in self.prices if self.current > price)
        total_count = len(self.prices)
        profitable_ratio = profitable_count / total_count * 100
        
        if profitable_ratio > 80:
            level = '多数获利'
        elif profitable_ratio > 60:
            level = '部分获利'
        elif profitable_ratio > 40:
            level = '盈亏平衡'
        elif profitable_ratio > 20:
            level = '部分套牢'
        else:
            level = '多数套牢'
        
        return {
            'profitable_ratio': round(profitable_ratio, 1),
            'level': level,
            'total_periods': total_count,
            'profitable_periods': profitable_count
        }
    
    def analyze_chip_pressure_support(self):
        """
        筹码压力位和支撑位分析
        基于筹码密集区
        """
        chip_dist = self.analyze_chip_distribution()
        if 'status' in chip_dist:
            return {'status': '数据不足'}
        
        dense_intervals = chip_dist['dense_intervals']
        if not dense_intervals:
            return {'status': '无密集区'}
        
        # 支撑位：当前价格下方最近的密集区高点
        support_levels = []
        resistance_levels = []
        
        for interval in dense_intervals:
            mid_price = (interval['start'] + interval['end']) / 2
            if mid_price < self.current:
                support_levels.append(interval['end'])  # 密集区上沿作为支撑
            else:
                resistance_levels.append(interval['start'])  # 密集区下沿作为阻力
        
        support = max(support_levels) if support_levels else chip_dist['min_price']
        resistance = min(resistance_levels) if resistance_levels else chip_dist['max_price']
        
        # 计算距离
        support_distance = (self.current - support) / self.current * 100
        resistance_distance = (resistance - self.current) / self.current * 100
        
        return {
            'support_level': round(support, 2),
            'resistance_level': round(resistance, 2),
            'support_distance': round(support_distance, 2),
            'resistance_distance': round(resistance_distance, 2),
            'dense_intervals': dense_intervals
        }
    
    def generate_chip_analysis_report(self):
        """生成完整的筹码分析报告"""
        print(f"\n{'='*80}")
        print(f"🎯 {self.name} ({self.code}) - 筹码深度分析")
        print(f"{'='*80}")
        
        # 筹码分布分析
        print(f"\n【筹码分布分析】")
        chip_dist = self.analyze_chip_distribution()
        if 'status' not in chip_dist:
            print(f"价格区间: ¥{chip_dist['min_price']:.2f} - ¥{chip_dist['max_price']:.2f}")
            print(f"当前价位: {chip_dist['current_position']}")
            print(f"筹码集中度: {chip_dist['concentration_level']} ({chip_dist['concentration_ratio']:.1%})")
            
            if chip_dist['dense_intervals']:
                print(f"筹码密集区:")
                for i, interval in enumerate(chip_dist['dense_intervals'][:2]):
                    print(f"  区间{i+1}: ¥{interval['start']:.2f}-{interval['end']:.2f} ({interval['percentage']:.1f}%)")
        else:
            print(f"状态: {chip_dist['status']}")
        
        # 股东人数分析
        print(f"\n【股东人数分析】")
        shareholder_trend = self.analyze_shareholder_trend()
        if 'status' not in shareholder_trend:
            print(f"当前股东数: {shareholder_trend['current_count']:,}户")
            print(f"上期股东数: {shareholder_trend['previous_count']:,}户")
            print(f"变化: {shareholder_trend['change_pct']:+.2f}% ({shareholder_trend['trend']})")
            print(f"信号: {shareholder_trend['signal']} ({shareholder_trend['strength']})")
            print(f"长期趋势: {shareholder_trend['long_term_trend']}")
        else:
            print(f"状态: {shareholder_trend['status']}")
        
        # 获利盘分析
        print(f"\n【获利盘分析】")
        profitable_ratio = self.calculate_profitable_ratio()
        if 'status' not in profitable_ratio:
            print(f"获利盘比例: {profitable_ratio['profitable_ratio']:.1f}%")
            print(f"市场状态: {profitable_ratio['level']}")
        else:
            print(f"状态: {profitable_ratio['status']}")
        
        # 压力支撑分析
        print(f"\n【压力支撑分析】")
        pressure_support = self.analyze_chip_pressure_support()
        if 'status' not in pressure_support:
            print(f"支撑位: ¥{pressure_support['support_level']:.2f} (距离: {pressure_support['support_distance']:.2f}%)")
            print(f"阻力位: ¥{pressure_support['resistance_level']:.2f} (距离: {pressure_support['resistance_distance']:.2f}%)")
        else:
            print(f"状态: {pressure_support['status']}")
        
        # 综合筹码信号
        print(f"\n{'='*80}")
        signals = []
        score = 50
        
        # 筹码集中度信号
        if chip_dist.get('concentration_ratio', 0) > 0.7:
            signals.append('筹码高度集中')
            score += 15
        elif chip_dist.get('concentration_ratio', 0) > 0.5:
            signals.append('筹码中度集中')
            score += 10
        
        # 股东人数信号
        if shareholder_trend.get('change_pct', 0) < -5:
            signals.append('股东大幅减少')
            score += 15
        elif shareholder_trend.get('change_pct', 0) < -2:
            signals.append('股东小幅减少')
            score += 5
        
        # 获利盘信号
        if profitable_ratio.get('profitable_ratio', 0) > 70:
            signals.append('多数获利')
            score += 10
        elif profitable_ratio.get('profitable_ratio', 0) < 30:
            signals.append('多数套牢')
            score -= 10
        
        # 压力支撑信号
        if pressure_support.get('support_distance', 100) < 5:
            signals.append('接近支撑位')
            score += 10
        if pressure_support.get('resistance_distance', 100) < 5:
            signals.append('接近阻力位')
            score -= 10
        
        score = max(0, min(100, score))
        
        if score >= 70:
            suggestion = '积极关注'
        elif score >= 55:
            suggestion = '适度关注'
        elif score >= 40:
            suggestion = '观望'
        else:
            suggestion = '谨慎'
        
        print(f"📈 筹码综合评分: {score}/100 - {suggestion}")
        print(f"关键信号: {', '.join(signals) if signals else '无明显信号'}")
        print(f"{'='*80}")
        
        return {
            'code': self.code,
            'name': self.name,
            'chip_distribution': chip_dist,
            'shareholder_trend': shareholder_trend,
            'profitable_ratio': profitable_ratio,
            'pressure_support': pressure_support,
            'chip_score': score,
            'chip_suggestion': suggestion,
            'chip_signals': signals
        }

def main():
    """主函数 - 分析所有持仓股票的筹码情况"""
    print("=" * 80)
    print("🎯 同花顺筹码深度分析系统")
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)
    
    results = []
    
    for code, info in HOLDINGS.items():
        try:
            analyzer = ChipAnalyzer(code, info)
            result = analyzer.generate_chip_analysis_report()
            results.append(result)
        except Exception as e:
            print(f"\n❌ 分析 {info['name']} 出错: {e}")
    
    # 生成汇总报告
    print(f"\n{'='*80}")
    print("📋 筹码分析综合对比")
    print(f"{'='*80}")
    
    print(f"\n{'股票':<10}{'筹码分':>8}{'股东趋势':>12}{'集中度':>10}{'获利盘':>10}{'建议':>10}")
    print("-" * 80)
    
    for r in sorted(results, key=lambda x: x['chip_score'], reverse=True):
        shareholder_trend = r['shareholder_trend'].get('trend', 'N/A')
        concentration = r['chip_distribution'].get('concentration_level', 'N/A')
        profitable = f"{r['profitable_ratio'].get('profitable_ratio', 0):.0f}%" if 'status' not in r['profitable_ratio'] else 'N/A'
        
        print(f"{r['name']:<10}{r['chip_score']:>8.0f}{shareholder_trend:>12}{concentration:>10}{profitable:>10}{r['chip_suggestion']:>10}")
    
    # 保存结果
    output_file = Path(__file__).parent / 'chip_analysis_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✅ 筹码分析完成！结果已保存至: {output_file}")

if __name__ == '__main__':
    main()
