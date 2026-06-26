#!/usr/bin/env python3
"""
股票扫描器 v2 - 基于右侧交易法则 + 多周期共振
结合 MACD、量价分析、支撑压力位
多周期趋势共振确认买卖信号
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class StockScanner:
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.daily_df = None
        self.weekly_df = None
        self.monthly_df = None
        self.multi_timeframe = {}
        
    def fetch_data(self, periods=None):
        """获取多周期历史数据"""
        if periods is None:
            # 确保各周期都有足够数据
            periods = {
                'daily': '1y',    # 1年日线 -> 52周, 12月
                'weekly': '2y',  # 2年周线 -> 104周, 24月  
                'monthly': '5y'  # 5年月线 -> 60月
            }
        
        stock = yf.Ticker(self.symbol)
        
        # 直接获取更长周期的数据再resample
        # 日线用1年
        self.daily_df = stock.history(period=periods['daily'])
        
        # 周线从日线resample（需要更长的原始数据）
        # 获取2年数据用于周线计算
        stock_2y = yf.Ticker(self.symbol)
        daily_2y = stock_2y.history(period=periods['weekly'])
        self.weekly_df = daily_2y.resample('W').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()
        
        # 月线同样需要更长的原始数据
        stock_5y = yf.Ticker(self.symbol)
        daily_5y = stock_5y.history(period=periods['monthly'])
        self.monthly_df = daily_5y.resample('ME').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()
        
        return len(self.daily_df) > 0
    
    # ==================== 单周期趋势 ====================
    def get_trend_single(self, df):
        """判断单个周期的趋势"""
        if df is None or len(df) < 20:
            return "数据不足", 0, 0
        
        ma5 = df['Close'].rolling(5).mean().iloc[-1]
        ma20 = df['Close'].rolling(20).mean().iloc[-1]
        ma60 = df['Close'].rolling(60).mean().iloc[-1] if len(df) >= 60 else ma20
        
        current_price = df['Close'].iloc[-1]
        
        # 多均线多头排列判断
        if current_price > ma5 and ma5 > ma20 and ma20 > ma60:
            trend = "上升趋势 📈"
            trend_score = 2
        elif current_price < ma5 and ma5 < ma20 and ma20 < ma60:
            trend = "下降趋势 📉"
            trend_score = -2
        elif current_price > ma5 and ma5 > ma20:
            trend = "短期上升 ↗️"
            trend_score = 1
        elif current_price < ma5 and ma5 < ma20:
            trend = "短期下降 ↘️"
            trend_score = -1
        elif current_price > ma20:
            trend = "震荡偏强 ↔️📈"
            trend_score = 0.5
        elif current_price < ma20:
            trend = "震荡偏弱 ↔️📉"
            trend_score = -0.5
        else:
            trend = "震荡整理 ↔️"
            trend_score = 0
        
        # 均线发散程度（趋势强度）
        ma_divergence = abs(ma5 - ma20) / ma20 * 100 if ma20 > 0 else 0
        
        return trend, trend_score, ma_divergence
    
    # ==================== 多周期共振 ====================
    def analyze_multitimeframe(self):
        """多周期共振分析"""
        if self.daily_df is None:
            return None
        
        # 获取各周期趋势
        daily_trend, daily_score, daily_div = self.get_trend_single(self.daily_df)
        weekly_trend, weekly_score, weekly_div = self.get_trend_single(self.weekly_df)
        monthly_trend, monthly_score, monthly_div = self.get_trend_single(self.monthly_df)
        
        # 存储数据（兼容可能的数据不足情况）
        self.multi_timeframe = {
            'daily': {'trend': daily_trend, 'score': daily_score, 'divergence': daily_div},
            'weekly': {'trend': weekly_trend, 'score': weekly_score, 'divergence': weekly_div},
            'monthly': {'trend': monthly_trend, 'score': monthly_score, 'divergence': monthly_div}
        }
        
        # 共振分析
        total_score = daily_score * 0.5 + weekly_score * 0.3 + monthly_score * 0.2
        
        # 共振强度
        if daily_score == weekly_score and weekly_score == monthly_score:
            resonance = "完美共振 🌟🌟🌟"
            resonance_bonus = 3
        elif daily_score == weekly_score and daily_score * monthly_score > 0:
            resonance = "双周期共振 🌟🌟"
            resonance_bonus = 2
        elif daily_score == weekly_score or weekly_score == monthly_score:
            resonance = "部分共振 🌟"
            resonance_bonus = 1
        elif daily_score * weekly_score > 0:
            resonance = "日周同向 👍"
            resonance_bonus = 0.5
        elif daily_score * weekly_score < 0:
            resonance = "日周矛盾 ⚠️"
            resonance_bonus = -0.5
        else:
            resonance = "方向混乱 ❌"
            resonance_bonus = -1
        
        # 最终趋势评分（含共振加成）
        final_score = total_score + resonance_bonus
        
        return {
            'daily': self.multi_timeframe['daily'],
            'weekly': self.multi_timeframe['weekly'],
            'monthly': self.multi_timeframe['monthly'],
            'resonance': resonance,
            'resonance_bonus': resonance_bonus,
            'total_score': round(total_score, 2),
            'final_score': round(final_score, 2)
        }
    
    # ==================== MACD 多周期 ====================
    def calculate_macd_multiframe(self, df, fast=12, slow=26, signal=9):
        """计算单周期MACD"""
        if df is None or len(df) < 30:
            return None
        
        ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        current_macd = macd_line.iloc[-1]
        current_signal = signal_line.iloc[-1]
        current_hist = histogram.iloc[-1]
        prev_hist = histogram.iloc[-2] if len(histogram) > 1 else 0
        
        if current_macd > current_signal and current_hist > 0:
            status = "多头 🐂"
        elif current_macd < current_signal and current_hist < 0:
            status = "空头 🐻"
        else:
            status = "中性 ⚖️"
        
        crossover = None
        if len(histogram) >= 2:
            if prev_hist < 0 and current_hist > 0:
                crossover = "金叉 ✅"
            elif prev_hist > 0 and current_hist < 0:
                crossover = "死叉 ❌"
        
        return {
            'macd': round(current_macd, 4),
            'signal': round(current_signal, 4),
            'histogram': round(current_hist, 4),
            'status': status,
            'crossover': crossover
        }
    
    def analyze_macd_all(self):
        """MACD多周期分析"""
        daily_macd = self.calculate_macd_multiframe(self.daily_df)
        weekly_macd = self.calculate_macd_multiframe(self.weekly_df)
        monthly_macd = self.calculate_macd_multiframe(self.monthly_df)
        
        return {
            'daily': daily_macd,
            'weekly': weekly_macd,
            'monthly': monthly_macd
        }
    
    # ==================== 量价分析 ====================
    def analyze_volume_price(self):
        """量价分析"""
        df = self.daily_df
        
        vol_ma20 = df['Volume'].rolling(20).mean().iloc[-1]
        current_vol = df['Volume'].iloc[-1]
        vol_ratio = current_vol / vol_ma20 if vol_ma20 > 0 else 1
        
        price_change_1d = df['Close'].pct_change(1).iloc[-1] * 100
        price_change_5d = df['Close'].pct_change(5).iloc[-1] * 100
        
        if vol_ratio > 1.5 and price_change_1d > 1:
            vol_status = "放量上涨 📈🔥"
        elif vol_ratio > 1.5 and price_change_1d < -1:
            vol_status = "放量下跌 📉🔥"
        elif vol_ratio < 0.7 and abs(price_change_1d) < 1:
            vol_status = "缩量整理 ➖"
        elif vol_ratio > 1.5 and abs(price_change_1d) < 1:
            vol_status = "放量不涨 ⚠️"
        else:
            vol_status = "正常量价 ✅"
        
        return {
            'volume_ratio': round(vol_ratio, 2),
            'price_change_1d': round(price_change_1d, 2),
            'price_change_5d': round(price_change_5d, 2),
            'status': vol_status
        }
    
    # ==================== 支撑压力位 ====================
    def find_support_resistance(self, lookback=60):
        """寻找支撑压力位"""
        df = self.daily_df[-lookback:].copy()
        
        highs = df['High'].values
        lows = df['Low'].values
        closes = df['Close'].values
        current_price = closes[-1]
        
        def find_peaks(data, threshold=0.02):
            peaks = []
            for i in range(1, len(data)-1):
                if data[i] > data[i-1] and data[i] > data[i+1]:
                    if len(peaks) == 0 or abs(float(data[i]) - float(peaks[-1][1]))/float(peaks[-1][1]) > threshold:
                        peaks.append((i, float(data[i])))
            return peaks
        
        peak_highs = find_peaks(highs)
        peak_lows = find_peaks(lows)
        
        resistance_levels = [price for idx, price in peak_highs if price > current_price]
        support_levels = [price for idx, price in peak_lows if price < current_price]
        
        nearest_resistance = min(resistance_levels) if resistance_levels else current_price * 1.05
        nearest_support = max(support_levels) if support_levels else current_price * 0.95
        
        dist_to_resistance = (nearest_resistance - current_price) / current_price * 100
        dist_to_support = (current_price - nearest_support) / current_price * 100
        
        return {
            'nearest_resistance': round(nearest_resistance, 2),
            'dist_to_resistance': round(dist_to_resistance, 2),
            'nearest_support': round(nearest_support, 2),
            'dist_to_support': round(dist_to_support, 2)
        }
    
    # ==================== 综合信号 ====================
    def generate_signal(self):
        """生成综合买卖信号"""
        mt = self.analyze_multitimeframe()
        macd_all = self.analyze_macd_all()
        vol_price = self.analyze_volume_price()
        sr_levels = self.find_support_resistance()
        
        current_price = self.daily_df['Close'].iloc[-1]
        
        # 计分
        score = 0
        reasons_buy = []
        reasons_sell = []
        
        # 1. 多周期共振评分
        score += mt['final_score']
        if mt['final_score'] > 1:
            reasons_buy.append(f"✓ 多周期共振 ({mt['resonance']})")
        elif mt['final_score'] < -1:
            reasons_sell.append(f"✗ 空头共振 ({mt['resonance']})")
        
        # 2. 各周期趋势加分
        for tf, data in [('日线', mt['daily']), ('周线', mt['weekly']), ('月线', mt['monthly'])]:
            if '上升' in data['trend'] or '偏强' in data['trend']:
                reasons_buy.append(f"✓ {tf}{data['trend']}")
            elif '下降' in data['trend'] or '偏弱' in data['trend']:
                reasons_sell.append(f"✗ {tf}{data['trend']}")
        
        # 3. MACD信号（日线为主）
        daily_macd = macd_all['daily']
        if daily_macd:
            if daily_macd['crossover'] == "金叉 ✅":
                score += 2
                reasons_buy.append("✓ 日线MACD金叉")
            elif daily_macd['crossover'] == "死叉 ❌":
                score -= 2
                reasons_sell.append("✗ 日线MACD死叉")
            
            if daily_macd['status'] == "多头 🐂":
                score += 1
            elif daily_macd['status'] == "空头 🐻":
                score -= 1
        
        # 4. 周线MACD共振
        weekly_macd = macd_all['weekly']
        if weekly_macd and weekly_macd['status'] == daily_macd['status']:
            score += 0.5
            reasons_buy.append("✓ 周日MACD同向")
        
        # 5. 量价配合
        if "放量上涨" in vol_price['status']:
            score += 2
            reasons_buy.append("✓ 放量上涨")
        elif "放量下跌" in vol_price['status']:
            score -= 2
            reasons_sell.append("✗ 放量下跌")
        
        # 6. 支撑压力
        if sr_levels['dist_to_support'] < 2:
            score += 1
            reasons_buy.append(f"✓ 接近支撑 ${sr_levels['nearest_support']}")
        
        if sr_levels['dist_to_resistance'] < 1.5:
            score -= 1
            reasons_sell.append(f"⚠️ 接近压力 ${sr_levels['nearest_resistance']}")
        
        # 最终信号
        if score >= 5:
            signal = "💎强烈买入"
        elif score >= 3:
            signal = "✅买入"
        elif score <= -5:
            signal = "🔴强烈卖出"
        elif score <= -3:
            signal = "❌卖出"
        else:
            signal = "👀观望"
        
        return {
            'signal': signal,
            'score': round(score, 1),
            'current_price': round(current_price, 2),
            'multitimeframe': mt,
            'macd': macd_all,
            'volume': vol_price,
            'support_resistance': sr_levels,
            'reasons_buy': reasons_buy,
            'reasons_sell': reasons_sell
        }
    
    # ==================== 完整报告 ====================
    def full_report(self):
        """生成完整分析报告"""
        if self.daily_df is None:
            return f"无法获取 {self.symbol} 的数据"
        
        sig = self.generate_signal()
        mt = sig['multitimeframe']
        
        report = f"""
╔══════════════════════════════════════════════════╗
║        📊 {self.symbol} 多周期共振分析报告              ║
╠══════════════════════════════════════════════════╣
║  当前价格: ${sig['current_price']}                               ║
╠══════════════════════════════════════════════════╣
║  🌟 多周期共振分析                              ║
║  ────────────────────────────────────────────   ║
║  月线趋势: {mt['monthly']['trend']:<10}  (权重20%)            ║
║  周线趋势: {mt['weekly']['trend']:<10}  (权重30%)            ║
║  日线趋势: {mt['daily']['trend']:<10}  (权重50%)            ║
║                                                  ║
║  共振状态: {mt['resonance']:<18}                  ║
║  趋势评分: {mt['total_score']:>5} (含共振加成: {mt['resonance_bonus']:+.1f})    ║
╠══════════════════════════════════════════════════╣
║  📈 MACD 指标 (日/周/月)                        ║
║  ────────────────────────────────────────────   ║
║  日线: {sig['macd']['daily']['status']:<8} | {'金叉' if sig['macd']['daily']['crossover']=='金叉 ✅' else '死叉' if sig['macd']['daily']['crossover']=='死叉 ❌' else '无交叉'}         ║
║  周线: {sig['macd']['weekly']['status'] if sig['macd']['weekly'] else 'N/A':<8}                        ║
║  月线: {sig['macd']['monthly']['status'] if sig['macd']['monthly'] else 'N/A':<8}                        ║
╠══════════════════════════════════════════════════╣
║  📦 量价分析                                    ║
║  ────────────────────────────────────────────   ║
║  量比: {sig['volume']['volume_ratio']:>4}x  | 今日涨跌: {sig['volume']['price_change_1d']:>5}%       ║
║  状态: {sig['volume']['status']:<18}              ║
╠══════════════════════════════════════════════════╣
║  🎯 支撑压力位                                  ║
║  ────────────────────────────────────────────   ║
║  压力: ${sig['support_resistance']['nearest_resistance']} ({sig['support_resistance']['dist_to_resistance']:+.1f}%)  │  支撑: ${sig['support_resistance']['nearest_support']} ({sig['support_resistance']['dist_to_support']:+.1f}%) ║
╠══════════════════════════════════════════════════╣
║  💡 信号: {sig['signal']:<10}  综合评分: {sig['score']:>5}             ║
║  ────────────────────────────────────────────   ║"""
        
        if sig['reasons_buy']:
            for r in sig['reasons_buy']:
                report += f"\n║    {r:<40}  ║"
        if sig['reasons_sell']:
            for r in sig['reasons_sell']:
                report += f"\n║    {r:<40}  ║"
        
        report += """
╚══════════════════════════════════════════════════╝
"""
        return report


def scan_stocks(symbols):
    """批量扫描"""
    print("\n" + "="*55)
    print("🚀 股票扫描开始 - 多周期共振版")
    print("="*55 + "\n")
    
    results = []
    
    for symbol in symbols:
        try:
            scanner = StockScanner(symbol)
            if scanner.fetch_data():
                report = scanner.full_report()
                print(report)
                sig = scanner.generate_signal()
                results.append((symbol, sig))
            else:
                print(f"⚠️  无法获取 {symbol} 的数据\n")
        except Exception as e:
            print(f"❌ {symbol} 分析出错: {e}\n")
    
    # 按评分排序
    results.sort(key=lambda x: x[1]['score'] if isinstance(x[1], dict) else 0, reverse=True)
    
    print("\n" + "="*55)
    print("📋 股票评分排行榜 (多周期共振)")
    print("="*55)
    print(f"{'股票':<8} {'信号':<12} {'评分':<6} {'共振状态':<18}")
    print("-"*55)
    for symbol, sig in results:
        if isinstance(sig, dict):
            mt = sig['multitimeframe']
            print(f"{symbol:<8} {sig['signal']:<12} {sig['score']:>5}   {mt['resonance']:<18}")
    
    return results


if __name__ == "__main__":
    import sys
    
    # 默认扫描
    symbols = ["TSM"]
    scan_stocks(symbols)
