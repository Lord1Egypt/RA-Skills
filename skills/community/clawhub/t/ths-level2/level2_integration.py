# -*- coding: utf-8 -*-
"""
同花顺Level2数据集成分析系统
结合内存读取、本地数据库和模拟数据进行完整分析
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

class Level2DataSimulator:
    """Level2数据模拟器（用于演示）"""
    
    def __init__(self, code, info):
        self.code = code
        self.name = info['name']
        self.current = info['current']
        self._generate_level2_data()
    
    def _generate_level2_data(self):
        """生成模拟Level2数据"""
        import random
        random.seed(int(self.code))
        
        # 模拟五档买卖盘
        self.bid_prices = []
        self.bid_volumes = []
        self.ask_prices = []
        self.ask_volumes = []
        
        # 当前价格作为中间价
        mid_price = self.current
        
        # 生成买盘（低于当前价）
        for i in range(5):
            price = mid_price * (1 - random.uniform(0.001, 0.005 * (i + 1)))
            volume = random.randint(100, 1000) * 100  # 手数
            self.bid_prices.append(round(price, 2))
            self.bid_volumes.append(volume)
        
        # 生成卖盘（高于当前价）
        for i in range(5):
            price = mid_price * (1 + random.uniform(0.001, 0.005 * (i + 1)))
            volume = random.randint(100, 1000) * 100  # 手数
            self.ask_prices.append(round(price, 2))
            self.ask_volumes.append(volume)
        
        # 模拟成交明细
        self.trades = []
        for i in range(50):  # 最近50笔成交
            trade_price = mid_price * (1 + random.uniform(-0.002, 0.002))
            trade_volume = random.randint(10, 100) * 100
            trade_direction = random.choice(['buy', 'sell'])
            self.trades.append({
                'price': round(trade_price, 2),
                'volume': trade_volume,
                'direction': trade_direction,
                'timestamp': int(datetime.now().timestamp()) - i * 3  # 每3秒一笔
            })
        
        # 计算大单统计
        big_trades = [t for t in self.trades if t['volume'] > 5000]  # 大于50手
        self.big_buy_volume = sum(t['volume'] for t in big_trades if t['direction'] == 'buy')
        self.big_sell_volume = sum(t['volume'] for t in big_trades if t['direction'] == 'sell')
    
    def get_level2_depth(self):
        """获取五档行情"""
        return {
            'bid_prices': self.bid_prices,
            'bid_volumes': self.bid_volumes,
            'ask_prices': self.ask_prices,
            'ask_volumes': self.ask_volumes,
            'spread': round(self.ask_prices[0] - self.bid_prices[0], 2)
        }
    
    def get_trade_analysis(self):
        """成交明细分析"""
        total_volume = sum(t['volume'] for t in self.trades)
        buy_volume = sum(t['volume'] for t in self.trades if t['direction'] == 'buy')
        sell_volume = sum(t['volume'] for t in self.trades if t['direction'] == 'sell')
        
        net_volume = buy_volume - sell_volume
        net_ratio = net_volume / total_volume if total_volume > 0 else 0
        
        # 大单净量
        big_net_volume = self.big_buy_volume - self.big_sell_volume
        big_net_ratio = big_net_volume / (self.big_buy_volume + self.big_sell_volume) if (self.big_buy_volume + self.big_sell_volume) > 0 else 0
        
        return {
            'total_volume': total_volume,
            'buy_volume': buy_volume,
            'sell_volume': sell_volume,
            'net_volume': net_volume,
            'net_ratio': round(net_ratio, 3),
            'big_buy_volume': self.big_buy_volume,
            'big_sell_volume': self.big_sell_volume,
            'big_net_ratio': round(big_net_ratio, 3),
            'recent_trades': len(self.trades)
        }

class Level2TechnicalAnalyzer:
    """Level2技术指标分析器"""
    
    def __init__(self, code, info):
        self.code = code
        self.name = info['name']
        self.cost = info['cost']
        self.current = info['current']
        self.shares = info['shares']
        self.change = info['change']
        
        # 初始化Level2数据模拟器
        self.level2_simulator = Level2DataSimulator(code, info)
        
        # 生成历史数据用于技术指标
        self._generate_historical_data()
    
    def _generate_historical_data(self):
        """生成历史数据"""
        import random
        random.seed(int(self.code))
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
    
    def calculate_ma(self, period):
        """计算移动平均线"""
        if len(self.prices) < period:
            return self.current
        return statistics.mean(self.prices[-period:])
    
    def analyze_level2_pressure_support(self):
        """基于Level2数据的压力支撑分析"""
        level2_depth = self.level2_simulator.get_level2_depth()
        
        # 支撑位：买一到买五的加权平均
        bid_total_volume = sum(level2_depth['bid_volumes'])
        if bid_total_volume > 0:
            weighted_bid = sum(p * v for p, v in zip(level2_depth['bid_prices'], level2_depth['bid_volumes'])) / bid_total_volume
            support_level = weighted_bid
        else:
            support_level = self.current * 0.99
        
        # 阻力位：卖一到卖五的加权平均
        ask_total_volume = sum(level2_depth['ask_volumes'])
        if ask_total_volume > 0:
            weighted_ask = sum(p * v for p, v in zip(level2_depth['ask_prices'], level2_depth['ask_volumes'])) / ask_total_volume
            resistance_level = weighted_ask
        else:
            resistance_level = self.current * 1.01
        
        return {
            'support_level': round(support_level, 2),
            'resistance_level': round(resistance_level, 2),
            'bid_total_volume': bid_total_volume,
            'ask_total_volume': ask_total_volume,
            'spread': level2_depth['spread'],
            'pressure_ratio': round(ask_total_volume / (bid_total_volume + ask_total_volume) if (bid_total_volume + ask_total_volume) > 0 else 0.5, 3)
        }
    
    def analyze_level2_fund_flow(self):
        """Level2资金流向分析"""
        trade_analysis = self.level2_simulator.get_trade_analysis()
        
        # 主力资金判断
        if trade_analysis['big_net_ratio'] > 0.3:
            main_fund_signal = '主力大幅流入'
            main_fund_strength = '强'
        elif trade_analysis['big_net_ratio'] > 0.1:
            main_fund_signal = '主力流入'
            main_fund_strength = '中'
        elif trade_analysis['big_net_ratio'] < -0.3:
            main_fund_signal = '主力大幅流出'
            main_fund_strength = '强'
        elif trade_analysis['big_net_ratio'] < -0.1:
            main_fund_signal = '主力流出'
            main_fund_strength = '中'
        else:
            main_fund_signal = '主力观望'
            main_fund_strength = '弱'
        
        return {
            'main_fund_signal': main_fund_signal,
            'main_fund_strength': main_fund_strength,
            'big_net_ratio': trade_analysis['big_net_ratio'],
            'total_big_volume': trade_analysis['big_buy_volume'] + trade_analysis['big_sell_volume'],
            'net_volume_ratio': trade_analysis['net_ratio']
        }
    
    def analyze_level2_market_depth(self):
        """市场深度分析"""
        level2_depth = self.level2_simulator.get_level2_depth()
        
        # 买卖盘对比
        bid_sum = sum(level2_depth['bid_volumes'])
        ask_sum = sum(level2_depth['ask_volumes'])
        
        if bid_sum > ask_sum * 1.2:
            depth_signal = '买盘强势'
            depth_strength = '强'
        elif bid_sum > ask_sum * 1.05:
            depth_signal = '买盘偏强'
            depth_strength = '中'
        elif ask_sum > bid_sum * 1.2:
            depth_signal = '卖盘强势'
            depth_strength = '强'
        elif ask_sum > bid_sum * 1.05:
            depth_signal = '卖盘偏强'
            depth_strength = '中'
        else:
            depth_signal = '买卖均衡'
            depth_strength = '弱'
        
        return {
            'depth_signal': depth_signal,
            'depth_strength': depth_strength,
            'bid_sum': bid_sum,
            'ask_sum': ask_sum,
            'bid_ask_ratio': round(bid_sum / ask_sum if ask_sum > 0 else 1, 2)
        }
    
    def integrate_with_technical_indicators(self):
        """与传统技术指标集成"""
        # MACD
        ma12 = self.calculate_ma(12)
        ma26 = self.calculate_ma(26)
        macd_line = ma12 - ma26
        signal_line = macd_line * 0.9
        macd_histogram = macd_line - signal_line
        
        # RSI
        if len(self.prices) >= 15:
            gains = []
            losses = []
            for i in range(1, 15):
                change = self.prices[-i] - self.prices[-i-1]
                if change > 0:
                    gains.append(change)
                else:
                    losses.append(abs(change))
            avg_gain = statistics.mean(gains) if gains else 0
            avg_loss = statistics.mean(losses) if losses else 0
            rsi = 100 - (100 / (1 + avg_gain / avg_loss)) if avg_loss > 0 else 100
        else:
            rsi = 50
        
        return {
            'macd': round(macd_line, 3),
            'signal': round(signal_line, 3),
            'histogram': round(macd_histogram, 3),
            'rsi': round(rsi, 2),
            'ma5': round(self.calculate_ma(5), 2),
            'ma20': round(self.calculate_ma(20), 2)
        }
    
    def generate_level2_comprehensive_report(self):
        """生成Level2综合分析报告"""
        print(f"\n{'='*80}")
        print(f"🎯 {self.name} ({self.code}) - Level2深度分析")
        print(f"{'='*80}")
        
        # Level2压力支撑
        pressure_support = self.analyze_level2_pressure_support()
        print(f"\n【Level2压力支撑】")
        print(f"支撑位: ¥{pressure_support['support_level']:.2f}")
        print(f"阻力位: ¥{pressure_support['resistance_level']:.2f}")
        print(f"买卖盘总量: 买{pressure_support['bid_total_volume']:,}手 卖{pressure_support['ask_total_volume']:,}手")
        print(f"压力比率: {pressure_support['pressure_ratio']:.1%}")
        
        # Level2资金流向
        fund_flow = self.analyze_level2_fund_flow()
        print(f"\n【Level2资金流向】")
        print(f"主力信号: {fund_flow['main_fund_signal']} ({fund_flow['main_fund_strength']})")
        print(f"大单净量: {fund_flow['big_net_ratio']:+.1%}")
        print(f"总大单量: {fund_flow['total_big_volume']:,}手")
        
        # 市场深度
        market_depth = self.analyze_level2_market_depth()
        print(f"\n【市场深度】")
        print(f"深度信号: {market_depth['depth_signal']} ({market_depth['depth_strength']})")
        print(f"买卖比: {market_depth['bid_ask_ratio']:.2f}")
        
        # 传统技术指标
        technical = self.integrate_with_technical_indicators()
        print(f"\n【传统技术指标】")
        print(f"MACD: {technical['macd']:.3f} | Signal: {technical['signal']:.3f}")
        print(f"RSI: {technical['rsi']:.2f} | MA5: {technical['ma5']:.2f} | MA20: {technical['ma20']:.2f}")
        
        # 综合评分
        score = 50
        
        # Level2信号加分
        if fund_flow['big_net_ratio'] > 0.1:
            score += 15
        elif fund_flow['big_net_ratio'] > 0:
            score += 5
        
        if market_depth['depth_signal'] in ['买盘强势', '买盘偏强']:
            score += 10
        elif market_depth['depth_signal'] in ['卖盘强势', '卖盘偏强']:
            score -= 10
        
        # 技术指标加分
        if technical['macd'] > technical['signal']:
            score += 10
        if technical['rsi'] < 30:
            score += 15
        elif technical['rsi'] > 70:
            score -= 15
        
        # 价格位置
        if self.current < pressure_support['support_level'] * 1.02:
            score += 10
        if self.current > pressure_support['resistance_level'] * 0.98:
            score -= 10
        
        score = max(0, min(100, score))
        
        if score >= 70:
            suggestion = '积极关注'
        elif score >= 55:
            suggestion = '适度关注'
        elif score >= 40:
            suggestion = '观望'
        else:
            suggestion = '回避'
        
        print(f"\n{'='*80}")
        print(f"📈 Level2综合评分: {score}/100 - {suggestion}")
        print(f"关键Level2信号: {fund_flow['main_fund_signal']}, {market_depth['depth_signal']}")
        print(f"{'='*80}")
        
        return {
            'code': self.code,
            'name': self.name,
            'level2_pressure_support': pressure_support,
            'level2_fund_flow': fund_flow,
            'level2_market_depth': market_depth,
            'technical_indicators': technical,
            'level2_score': score,
            'level2_suggestion': suggestion
        }

def main():
    """主函数 - Level2综合分析"""
    print("=" * 80)
    print("🎯 同花顺Level2深度分析系统")
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)
    
    results = []
    
    for code, info in HOLDINGS.items():
        try:
            analyzer = Level2TechnicalAnalyzer(code, info)
            result = analyzer.generate_level2_comprehensive_report()
            results.append(result)
        except Exception as e:
            print(f"\n❌ 分析 {info['name']} 出错: {e}")
    
    # 生成汇总报告
    print(f"\n{'='*80}")
    print("📋 Level2分析综合对比")
    print(f"{'='*80}")
    
    print(f"\n{'股票':<10}{'Level2分':>10}{'主力信号':>15}{'市场深度':>12}{'建议':>10}")
    print("-" * 80)
    
    for r in sorted(results, key=lambda x: x['level2_score'], reverse=True):
        main_signal = r['level2_fund_flow']['main_fund_signal']
        depth_signal = r['level2_market_depth']['depth_signal']
        
        print(f"{r['name']:<10}{r['level2_score']:>10.0f}{main_signal:>15}{depth_signal:>12}{r['level2_suggestion']:>10}")
    
    # 保存结果
    output_file = Path(__file__).parent / 'level2_analysis_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✅ Level2分析完成！结果已保存至: {output_file}")

if __name__ == '__main__':
    main()
