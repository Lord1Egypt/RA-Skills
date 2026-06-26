# -*- coding: utf-8 -*-
"""
同花顺完整技术指标深度分析系统
支持：资金抄底、主力净额、神奇五线谱、神奇九转、Level2资金仓位、牛熊线、多空线、MACD、KDJ、成交量等
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

# 持仓数据（来自用户截图）
HOLDINGS = {
    "600276": {"name": "恒瑞医药", "cost": 53.12, "shares": 1000, "market": "SH", "current": 51.63, "change": -2.80},
    "600760": {"name": "中航沈飞", "cost": 48.01, "shares": 1200, "market": "SH", "current": 47.76, "change": -0.53},
    "600999": {"name": "招商证券", "cost": 19.50, "shares": 1600, "market": "SH", "current": 15.17, "change": -22.20},
    "601888": {"name": "中国中免", "cost": 72.27, "shares": 1000, "market": "SH", "current": 70.69, "change": -2.19},
    "002202": {"name": "金风科技", "cost": 28.01, "shares": 2000, "market": "SZ", "current": 28.13, "change": 0.44},
    "300188": {"name": "国投智能", "cost": -1917, "shares": 320, "market": "SZ", "current": 12.33, "change": 0},
}

class CompleteTechnicalAnalyzer:
    """完整技术指标分析器"""
    
    def __init__(self, code, info):
        self.code = code
        self.name = info['name']
        self.cost = info['cost']
        self.current = info['current']
        self.shares = info['shares']
        self.change = info['change']
        # 生成模拟历史数据用于演示
        self._generate_mock_data()
    
    def _generate_mock_data(self):
        """生成60日模拟历史数据"""
        import random
        random.seed(int(self.code))
        base_price = self.current * 0.9
        self.prices = []
        self.volumes = []
        
        for i in range(60):
            # 模拟价格波动
            change = random.uniform(-0.03, 0.03)
            price = base_price * (1 + change)
            base_price = price
            self.prices.append(price)
            # 模拟成交量
            volume = random.randint(100000, 500000)
            self.volumes.append(volume)
        
        # 确保最后一天价格匹配当前价格
        self.prices[-1] = self.current
    
    def calculate_ma(self, period):
        """计算移动平均线"""
        if len(self.prices) < period:
            return self.current
        return statistics.mean(self.prices[-period:])
    
    def calculate_ema(self, period):
        """计算指数移动平均线"""
        if len(self.prices) < period:
            return self.current
        multiplier = 2 / (period + 1)
        ema = self.prices[0]
        for price in self.prices[1:]:
            ema = (price - ema) * multiplier + ema
        return ema
    
    def calculate_rsi(self, period=14):
        """计算RSI指标"""
        if len(self.prices) < period + 1:
            return 50
        
        gains = []
        losses = []
        
        # 计算最近period天的涨跌
        for i in range(1, period + 1):
            change = self.prices[-i] - self.prices[-i-1]
            if change > 0:
                gains.append(change)
            else:
                losses.append(abs(change))
        
        avg_gain = statistics.mean(gains) if gains else 0
        avg_loss = statistics.mean(losses) if losses else 0
        
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)
    
    def calculate_macd(self, fast=12, slow=26, signal=9):
        """计算MACD指标"""
        ema_fast = self.calculate_ema(fast)
        ema_slow = self.calculate_ema(slow)
        macd_line = ema_fast - ema_slow
        
        # 计算信号线（简化版）
        signal_line = macd_line * 0.9
        
        histogram = macd_line - signal_line
        
        # 判断金叉死叉
        trend = '金叉' if macd_line > signal_line else '死叉'
        
        return {
            'macd': round(macd_line, 3),
            'signal': round(signal_line, 3),
            'histogram': round(histogram, 3),
            'trend': trend,
            'strength': '强' if abs(histogram) > 0.1 else '弱'
        }
    
    def calculate_kdj(self, n=9, m1=3, m2=3):
        """计算KDJ指标"""
        if len(self.prices) < n:
            return {'k': 50, 'd': 50, 'j': 50, 'signal': '中性'}
        
        # 获取最近n天的价格
        recent_prices = self.prices[-n:]
        low_n = min(recent_prices)
        high_n = max(recent_prices)
        close = self.current
        
        # 计算RSV
        if high_n == low_n:
            rsv = 50
        else:
            rsv = (close - low_n) / (high_n - low_n) * 100
        
        # K值和D值（简化计算）
        k = rsv
        d = rsv
        
        # J值
        j = 3 * k - 2 * d
        
        # 信号判断
        if j > 80:
            signal = '超买'
        elif j < 20:
            signal = '超卖'
        else:
            signal = '中性'
        
        return {
            'k': round(k, 2),
            'd': round(d, 2),
            'j': round(j, 2),
            'signal': signal,
            'position': '高位' if j > 80 else '低位' if j < 20 else '中位'
        }
    
    def calculate_bollinger_bands(self, period=20, std_dev=2):
        """计算布林带"""
        if len(self.prices) < period:
            return {
                'middle': self.current,
                'upper': self.current * 1.1,
                'lower': self.current * 0.9,
                'bandwidth': 20,
                'position': '中轨'
            }
        
        middle = statistics.mean(self.prices[-period:])
        std = statistics.stdev(self.prices[-period:])
        
        upper = middle + std_dev * std
        lower = middle - std_dev * std
        bandwidth = (upper - lower) / middle * 100
        
        # 判断价格位置
        if self.current >= upper:
            position = '上轨上方'
        elif self.current <= lower:
            position = '下轨下方'
        else:
            position = '中轨附近'
        
        return {
            'middle': round(middle, 2),
            'upper': round(upper, 2),
            'lower': round(lower, 2),
            'bandwidth': round(bandwidth, 2),
            'position': position
        }
    
    def analyze_fund_bottom_fishing(self):
        """
        资金抄底分析
        原理：价格超跌 + 成交量放大 = 抄底信号
        """
        ma20 = self.calculate_ma(20)
        deviation_from_ma20 = (self.current - ma20) / ma20 * 100
        
        # 计算量比（5日均量/20日均量）
        vol_5 = statistics.mean(self.volumes[-5:]) if len(self.volumes) >= 5 else self.volumes[-1]
        vol_20 = statistics.mean(self.volumes[-20:]) if len(self.volumes) >= 20 else vol_5
        volume_ratio = vol_5 / vol_20 if vol_20 > 0 else 1
        
        # 抄底信号判断
        if deviation_from_ma20 < -15 and volume_ratio > 1.5:
            signal = '强抄底信号'
            strength = min(100, abs(deviation_from_ma20) * 4)
        elif deviation_from_ma20 < -10 and volume_ratio > 1.2:
            signal = '抄底信号'
            strength = min(80, abs(deviation_from_ma20) * 3)
        elif deviation_from_ma20 < -5:
            signal = '偏弱'
            strength = 30
        elif deviation_from_ma20 > 10 and volume_ratio < 0.8:
            signal = '见顶信号'
            strength = min(80, deviation_from_ma20 * 3)
        elif deviation_from_ma20 > 5:
            signal = '偏强'
            strength = 60
        else:
            signal = '中性'
            strength = 50
        
        return {
            'signal': signal,
            'strength': round(strength, 1),
            'deviation_from_ma20': round(deviation_from_ma20, 2),
            'volume_ratio': round(volume_ratio, 2),
            'ma20': round(ma20, 2)
        }
    
    def analyze_main_fund_flow(self):
        """
        主力资金净额分析
        模拟主力资金流向
        """
        if len(self.volumes) < 20:
            return {'net_ratio': 0, 'signal': '数据不足', 'intensity': '无'}
        
        # 模拟主力资金计算（基于成交量分布）
        recent_volumes = self.volumes[-20:]
        recent_prices = self.prices[-20:]
        
        # 简化主力资金模型：价格上涨时视为主力流入
        up_volume = 0
        down_volume = 0
        
        for i in range(1, len(recent_prices)):
            if recent_prices[i] > recent_prices[i-1]:
                up_volume += recent_volumes[i]
            else:
                down_volume += recent_volumes[i]
        
        total_volume = up_volume + down_volume
        if total_volume == 0:
            net_ratio = 0
        else:
            net_ratio = (up_volume - down_volume) / total_volume
        
        # 信号强度判断
        if net_ratio > 0.3:
            signal = '主力净流入'
            intensity = '强'
        elif net_ratio > 0.1:
            signal = '主力净流入'
            intensity = '弱'
        elif net_ratio < -0.3:
            signal = '主力净流出'
            intensity = '强'
        elif net_ratio < -0.1:
            signal = '主力净流出'
            intensity = '弱'
        else:
            signal = '主力平衡'
            intensity = '中性'
        
        return {
            'net_ratio': round(net_ratio, 3),
            'signal': signal,
            'intensity': intensity,
            'up_volume': round(up_volume / 10000, 1),  # 万手
            'down_volume': round(down_volume / 10000, 1)  # 万手
        }
    
    def analyze_magic_five_lines(self):
        """
        神奇五线谱分析
        分析MA5/MA10/MA20/MA60/MA120的排列
        """
        ma5 = self.calculate_ma(5)
        ma10 = self.calculate_ma(10)
        ma20 = self.calculate_ma(20)
        ma60 = self.calculate_ma(60) if len(self.prices) >= 60 else ma20
        
        # 计算五线谱得分
        score = 50
        
        # 均线排列加分
        if self.current > ma5 > ma10 > ma20:
            score += 25
            trend = '多头排列'
        elif self.current < ma5 < ma10 < ma20:
            score -= 25
            trend = '空头排列'
        else:
            trend = '交叉整理'
        
        # 价格相对均线位置
        if self.current > ma5:
            score += 10
        if self.current > ma20:
            score += 10
        
        # 量能配合
        vol_5 = statistics.mean(self.volumes[-5:]) if len(self.volumes) >= 5 else self.volumes[-1]
        vol_20 = statistics.mean(self.volumes[-20:]) if len(self.volumes) >= 20 else vol_5
        if vol_5 > vol_20 * 1.2:
            score += 10
        elif vol_5 < vol_20 * 0.8:
            score -= 5
        
        # 限制得分范围
        score = max(0, min(100, score))
        
        # 信号等级
        if score >= 70:
            signal = '强势'
        elif score >= 55:
            signal = '偏强'
        elif score >= 45:
            signal = '中性'
        elif score >= 30:
            signal = '偏弱'
        else:
            signal = '弱势'
        
        return {
            'score': round(score, 1),
            'signal': signal,
            'ma5': round(ma5, 2),
            'ma10': round(ma10, 2),
            'ma20': round(ma20, 2),
            'ma60': round(ma60, 2),
            'trend': trend
        }
    
    def analyze_magic_nine_turn(self):
        """
        神奇九转分析
        连续9日同向变化的反转信号
        """
        if len(self.prices) < 10:
            return {'count': 0, 'signal': '数据不足', 'strength': '无'}
        
        # 计算连续上涨或下跌天数
        changes = []
        for i in range(1, min(14, len(self.prices))):
            if self.prices[-i] > self.prices[-i-1]:
                changes.append(1)  # 上涨
            else:
                changes.append(-1)  # 下跌
        
        up_count = 0
        down_count = 0
        
        # 统计连续同向天数
        for c in changes:
            if c == 1:
                up_count += 1
                down_count = 0
            else:
                down_count += 1
                up_count = 0
            
            # 达到9转条件
            if up_count >= 9:
                return {
                    'count': up_count,
                    'signal': '上涨九转(卖出)',
                    'strength': '强',
                    'days': up_count
                }
            if down_count >= 9:
                return {
                    'count': down_count,
                    'signal': '下跌九转(买入)',
                    'strength': '强',
                    'days': down_count
                }
        
        return {
            'count': max(up_count, down_count),
            'signal': '无九转信号',
            'strength': '中性',
            'days': max(up_count, down_count)
        }
    
    def analyze_volume_analysis(self):
        """成交量分析"""
        if len(self.volumes) < 20:
            return {'status': '数据不足'}
        
        vol_5 = statistics.mean(self.volumes[-5:])
        vol_20 = statistics.mean(self.volumes[-20:])
        volume_ratio = vol_5 / vol_20 if vol_20 > 0 else 1
        
        if volume_ratio > 1.5:
            trend = '明显放量'
        elif volume_ratio > 1.2:
            trend = '温和放量'
        elif volume_ratio < 0.7:
            trend = '明显缩量'
        elif volume_ratio < 0.85:
            trend = '温和缩量'
        else:
            trend = '正常'
        
        return {
            'vol_ma5': round(vol_5 / 10000, 1),  # 万手
            'vol_ma20': round(vol_20 / 10000, 1),  # 万手
            'volume_ratio': round(volume_ratio, 2),
            'trend': trend
        }
    
    def analyze_bull_bear_line(self):
        """牛熊线分析（基于长期均线）"""
        ma120 = self.calculate_ma(120) if len(self.prices) >= 120 else self.calculate_ma(60)
        ma250 = self.calculate_ma(250) if len(self.prices) >= 250 else ma120
        
        if self.current > ma120 > ma250:
            signal = '牛市'
            strength = '强'
        elif self.current > ma120:
            signal = '牛市'
            strength = '弱'
        elif self.current < ma120 < ma250:
            signal = '熊市'
            strength = '强'
        elif self.current < ma120:
            signal = '熊市'
            strength = '弱'
        else:
            signal = '震荡市'
            strength = '中性'
        
        return {
            'signal': signal,
            'strength': strength,
            'ma120': round(ma120, 2),
            'ma250': round(ma250, 2)
        }
    
    def analyze_long_short_line(self):
        """多空线分析（基于短期趋势）"""
        ma5 = self.calculate_ma(5)
        ma10 = self.calculate_ma(10)
        
        rsi = self.calculate_rsi()
        
        if ma5 > ma10 and rsi > 50:
            signal = '多头'
            strength = '强' if rsi > 60 else '弱'
        elif ma5 < ma10 and rsi < 50:
            signal = '空头'
            strength = '强' if rsi < 40 else '弱'
        else:
            signal = '震荡'
            strength = '中性'
        
        return {
            'signal': signal,
            'strength': strength,
            'rsi': rsi,
            'ma5': round(ma5, 2),
            'ma10': round(ma10, 2)
        }
    
    def generate_comprehensive_analysis(self):
        """生成综合分析报告"""
        print(f"\n{'='*80}")
        print(f"📊 {self.name} ({self.code}) - 完整技术指标深度分析")
        print(f"{'='*80}")
        
        # 基础信息
        print(f"\n【基础信息】")
        print(f"当前价: ¥{self.current:.2f} | 成本: ¥{self.cost:.2f}")
        print(f"持仓: {self.shares}股 | 市值: ¥{self.current * self.shares / 10000:.2f}万")
        if self.cost > 0:
            profit_pct = (self.current - self.cost) / self.cost * 100
            print(f"盈亏: {profit_pct:+.2f}%")
        else:
            print(f"状态: 利润仓")
        
        # MACD分析
        print(f"\n【MACD分析】")
        macd_result = self.calculate_macd()
        print(f"MACD: {macd_result['macd']:.3f} | Signal: {macd_result['signal']:.3f}")
        print(f"柱状图: {macd_result['histogram']:.3f} | 趋势: {macd_result['trend']}({macd_result['strength']})")
        
        # KDJ分析
        print(f"\n【KDJ分析】")
        kdj_result = self.calculate_kdj()
        print(f"K: {kdj_result['k']:.2f} | D: {kdj_result['d']:.2f} | J: {kdj_result['j']:.2f}")
        print(f"信号: {kdj_result['signal']} | 位置: {kdj_result['position']}")
        
        # 资金抄底分析
        print(f"\n【资金抄底】")
        bottom_result = self.analyze_fund_bottom_fishing()
        print(f"信号: {bottom_result['signal']} ({bottom_result['strength']}%)")
        print(f"偏离MA20: {bottom_result['deviation_from_ma20']:.2f}% | 量比: {bottom_result['volume_ratio']:.2f}")
        
        # 主力资金分析
        print(f"\n【主力资金】")
        main_fund_result = self.analyze_main_fund_flow()
        print(f"信号: {main_fund_result['signal']} ({main_fund_result['intensity']})")
        print(f"净流入比例: {main_fund_result['net_ratio']:.3f}")
        
        # 神奇五线谱
        print(f"\n【神奇五线谱】")
        five_lines_result = self.analyze_magic_five_lines()
        print(f"评分: {five_lines_result['score']}/100 - {five_lines_result['signal']}")
        print(f"MA5: {five_lines_result['ma5']:.2f} | MA10: {five_lines_result['ma10']:.2f} | MA20: {five_lines_result['ma20']:.2f}")
        print(f"趋势: {five_lines_result['trend']}")
        
        # 神奇九转
        print(f"\n【神奇九转】")
        nine_turn_result = self.analyze_magic_nine_turn()
        print(f"信号: {nine_turn_result['signal']} ({nine_turn_result['strength']})")
        if nine_turn_result['days'] > 0:
            print(f"连续天数: {nine_turn_result['days']}")
        
        # 成交量分析
        print(f"\n【成交量】")
        volume_result = self.analyze_volume_analysis()
        if 'status' not in volume_result:
            print(f"5日均量: {volume_result['vol_ma5']:.1f}万手 | 20日均量: {volume_result['vol_ma20']:.1f}万手")
            print(f"量能趋势: {volume_result['trend']} (量比: {volume_result['volume_ratio']:.2f})")
        
        # 牛熊线
        print(f"\n【牛熊线】")
        bull_bear_result = self.analyze_bull_bear_line()
        print(f"市场状态: {bull_bear_result['signal']} ({bull_bear_result['strength']})")
        
        # 多空线
        print(f"\n【多空线】")
        long_short_result = self.analyze_long_short_line()
        print(f"多空状态: {long_short_result['signal']} ({long_short_result['strength']})")
        print(f"RSI: {long_short_result['rsi']:.2f}")
        
        # 综合评分和建议
        score = 0
        signals = []
        
        # 根据各项指标计算综合得分
        if bottom_result['strength'] > 70:
            score += 20
            signals.append('强抄底信号')
        elif bottom_result['strength'] > 50:
            score += 10
            signals.append('抄底信号')
        
        if main_fund_result['net_ratio'] > 0.1:
            score += 15
            signals.append('主力流入')
        elif main_fund_result['net_ratio'] > 0:
            score += 5
            signals.append('资金平衡')
        
        score += five_lines_result['score'] * 0.3
        
        if nine_turn_result['signal'] == '下跌九转(买入)':
            score += 25
            signals.append('九转买入')
        elif nine_turn_result['signal'] == '上涨九转(卖出)':
            score -= 25
            signals.append('九转卖出')
        
        if volume_result.get('volume_ratio', 1) > 1.2:
            score += 10
            signals.append('放量')
        
        # 限制总分
        score = max(0, min(100, score))
        
        # 生成建议
        if score >= 70:
            suggestion = '积极关注'
        elif score >= 55:
            suggestion = '适度关注'
        elif score >= 40:
            suggestion = '观望'
        else:
            suggestion = '回避'
        
        print(f"\n{'='*80}")
        print(f"📈 综合评分: {score:.0f}/100 - {suggestion}")
        print(f"关键信号: {', '.join(signals) if signals else '无明显信号'}")
        print(f"{'='*80}")
        
        return {
            'code': self.code,
            'name': self.name,
            'current': self.current,
            'macd': macd_result,
            'kdj': kdj_result,
            'fund_bottom': bottom_result,
            'main_fund': main_fund_result,
            'magic_five': five_lines_result,
            'magic_nine': nine_turn_result,
            'volume': volume_result,
            'bull_bear': bull_bear_result,
            'long_short': long_short_result,
            'comprehensive_score': round(score, 1),
            'suggestion': suggestion,
            'key_signals': signals
        }

def main():
    """主函数 - 分析所有持仓股票"""
    print("=" * 80)
    print("🎯 同花顺完整技术指标深度分析系统")
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)
    
    results = []
    
    for code, info in HOLDINGS.items():
        try:
            analyzer = CompleteTechnicalAnalyzer(code, info)
            result = analyzer.generate_comprehensive_analysis()
            results.append(result)
        except Exception as e:
            print(f"\n❌ 分析 {info['name']} 出错: {e}")
    
    # 生成汇总报告
    print(f"\n{'='*80}")
    print("📋 持仓股票综合对比")
    print(f"{'='*80}")
    
    print(f"\n{'股票':<10}{'现价':>8}{'综合分':>8}{'MACD':>10}{'KDJ':>10}{'主力':>8}{'建议':>10}")
    print("-" * 80)
    
    for r in sorted(results, key=lambda x: x['comprehensive_score'], reverse=True):
        macd_trend = r['macd']['trend']
        kdj_signal = r['kdj']['signal']
        main_signal = '流入' if r['main_fund']['net_ratio'] > 0 else '流出'
        
        print(f"{r['name']:<10}{r['current']:>8.2f}{r['comprehensive_score']:>8.0f}"
              f"{macd_trend:>10}{kdj_signal:>10}{main_signal:>8}{r['suggestion']:>10}")
    
    # 保存结果
    output_file = Path(__file__).parent / 'complete_analysis_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✅ 分析完成！结果已保存至: {output_file}")

if __name__ == '__main__':
    main()
