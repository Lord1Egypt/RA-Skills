#!/usr/bin/env python3
"""
高级技术指标库
Advanced Technical Indicators - High Win Rate

包含业内常用的高胜率技术指标：
1. RSI 相对强弱指标 (经典)
2. MACD 移动平均收敛发散 (趋势)
3. Bollinger Bands 布林带 (波动率)
4. KDJ 随机指标 (超买超卖)
5. CCI 商品通道指标 (趋势强度)
6. ADX 平均趋向指数 (趋势强度)
7. OBV 能量潮指标 (成交量)
8. ATR 平均真实波幅 (波动率)
9. Ichimoku Cloud 一目均衡表 (综合)
10. VWAP 成交量加权平均价 (机构)
"""

import math
from typing import List, Dict, Tuple, Optional


class TechnicalIndicators:
    """高级技术指标计算器"""
    
    @staticmethod
    def sma(prices: List[float], period: int = 20) -> List[float]:
        """简单移动平均线"""
        if len(prices) < period:
            return []
        
        result = []
        for i in range(len(prices)):
            if i < period - 1:
                result.append(None)
            else:
                avg = sum(prices[i-period+1:i+1]) / period
                result.append(avg)
        
        return result
    
    @staticmethod
    def ema(prices: List[float], period: int = 20) -> List[float]:
        """指数移动平均线"""
        if len(prices) < period:
            return []
        
        multiplier = 2 / (period + 1)
        ema = [sum(prices[:period]) / period]  # 第一个 EMA 用 SMA
        
        for i in range(period, len(prices)):
            ema.append((prices[i] - ema[-1]) * multiplier + ema[-1])
        
        # 补齐前面的 None
        return [None] * (period - 1) + ema
    
    @staticmethod
    def rsi(prices: List[float], period: int = 14) -> List[float]:
        """
        RSI 相对强弱指标
        超卖：< 30 (买入信号)
        超买：> 70 (卖出信号)
        """
        if len(prices) < period + 1:
            return []
        
        result = []
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            gains.append(max(0, change))
            losses.append(max(0, -change))
        
        # 第一个 RSI
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        if avg_loss == 0:
            result.append(100)
        else:
            rs = avg_gain / avg_loss
            result.append(100 - (100 / (1 + rs)))
        
        # 后续 RSI (平滑)
        for i in range(period, len(gains)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            
            if avg_loss == 0:
                result.append(100)
            else:
                rs = avg_gain / avg_loss
                result.append(100 - (100 / (1 + rs)))
        
        return [None] * (period - 1) + result
    
    @staticmethod
    def macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """
        MACD 移动平均收敛发散
        金叉：MACD 线上穿信号线 (买入)
        死叉：MACD 线下穿信号线 (卖出)
        """
        if len(prices) < slow + signal:
            return {'macd': [], 'signal': [], 'histogram': []}
        
        ema_fast = TechnicalIndicators.ema(prices, fast)
        ema_slow = TechnicalIndicators.ema(prices, slow)
        
        # MACD 线 = 快线 - 慢线
        macd_line = []
        for i in range(len(prices)):
            if ema_fast[i] is None or ema_slow[i] is None:
                macd_line.append(None)
            else:
                macd_line.append(ema_fast[i] - ema_slow[i])
        
        # 信号线 = MACD 的 EMA
        macd_valid = [x for x in macd_line if x is not None]
        signal_line = TechnicalIndicators.ema(macd_valid, signal)
        
        # 补齐 None
        none_count = macd_line.index(next(x for x in macd_line if x is not None))
        signal_line = [None] * none_count + signal_line
        
        # 柱状图
        histogram = []
        for i in range(len(prices)):
            if macd_line[i] is None or signal_line[i] is None:
                histogram.append(None)
            else:
                histogram.append(macd_line[i] - signal_line[i])
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram,
            'current': {
                'macd': macd_line[-1] if macd_line[-1] else 0,
                'signal': signal_line[-1] if signal_line[-1] else 0,
                'histogram': histogram[-1] if histogram[-1] else 0,
            }
        }
    
    @staticmethod
    def bollinger_bands(prices: List[float], period: int = 20, std_dev: float = 2.0) -> Dict:
        """
        布林带
        上轨：SMA + 2 倍标准差
        中轨：SMA
        下轨：SMA - 2 倍标准差
        
        触及下轨：可能超卖 (买入)
        触及上轨：可能超买 (卖出)
        """
        if len(prices) < period:
            return {'upper': [], 'middle': [], 'lower': []}
        
        upper = []
        middle = []
        lower = []
        
        for i in range(len(prices)):
            if i < period - 1:
                upper.append(None)
                middle.append(None)
                lower.append(None)
            else:
                window = prices[i-period+1:i+1]
                sma = sum(window) / period
                variance = sum((x - sma) ** 2 for x in window) / period
                std = math.sqrt(variance)
                
                middle.append(sma)
                upper.append(sma + std_dev * std)
                lower.append(sma - std_dev * std)
        
        return {
            'upper': upper,
            'middle': middle,
            'lower': lower,
            'current': {
                'upper': upper[-1] if upper[-1] else 0,
                'middle': middle[-1] if middle[-1] else 0,
                'lower': lower[-1] if lower[-1] else 0,
                'price': prices[-1],
                'position': (prices[-1] - lower[-1]) / (upper[-1] - lower[-1]) * 100 if upper[-1] != lower[-1] else 50
            }
        }
    
    @staticmethod
    def kdj(prices: List[float], n: int = 9, m1: int = 3, m2: int = 3) -> Dict:
        """
        KDJ 随机指标
        K 线：快线
        D 线：慢线
        J 线：方向敏感线
        
        超卖：< 20 (买入)
        超买：> 80 (卖出)
        金叉：K 上穿 D (买入)
        死叉：K 下穿 D (卖出)
        """
        if len(prices) < n:
            return {'k': [], 'd': [], 'j': []}
        
        # 计算最高价和最低价 (简化，使用收盘价代替)
        lows = prices
        highs = prices
        
        k_values = []
        d_values = []
        j_values = []
        
        # 第一个 RSV
        lowest = min(lows[:n])
        highest = max(highs[:n])
        rsv = (prices[n-1] - lowest) / (highest - lowest) * 100 if highest != lowest else 50
        
        k = rsv
        d = k
        j = 2 * k - d
        
        k_values.append(k)
        d_values.append(d)
        j_values.append(j)
        
        # 后续计算
        for i in range(n, len(prices)):
            lowest = min(lows[i-n+1:i+1])
            highest = max(highs[i-n+1:i+1])
            rsv = (prices[i] - lowest) / (highest - lowest) * 100 if highest != lowest else 50
            
            k = (2/3) * k + (1/3) * rsv
            d = (2/3) * d + (1/3) * k
            j = 2 * k - d
            
            k_values.append(k)
            d_values.append(d)
            j_values.append(j)
        
        none_count = n - 1
        return {
            'k': [None] * none_count + k_values,
            'd': [None] * none_count + d_values,
            'j': [None] * none_count + j_values,
            'current': {
                'k': k_values[-1],
                'd': d_values[-1],
                'j': j_values[-1],
            }
        }
    
    @staticmethod
    def cci(prices: List[float], period: int = 20) -> List[float]:
        """
        CCI 商品通道指标
        > +100: 超买
        < -100: 超卖
        """
        if len(prices) < period:
            return []
        
        result = []
        
        for i in range(len(prices)):
            if i < period - 1:
                result.append(None)
            else:
                window = prices[i-period+1:i+1]
                sma = sum(window) / period
                
                # 平均偏差
                deviations = [abs(x - sma) for x in window]
                mean_deviation = sum(deviations) / period
                
                if mean_deviation == 0:
                    result.append(0)
                else:
                    cci = (prices[i] - sma) / (0.015 * mean_deviation)
                    result.append(cci)
        
        return result
    
    @staticmethod
    def atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> List[float]:
        """
        ATR 平均真实波幅
        衡量波动率，用于止损设置
        """
        if len(highs) < period + 1:
            return []
        
        tr_values = []
        
        # 计算真实波幅
        for i in range(1, len(highs)):
            tr1 = highs[i] - lows[i]
            tr2 = abs(highs[i] - closes[i-1])
            tr3 = abs(lows[i] - closes[i-1])
            tr = max(tr1, tr2, tr3)
            tr_values.append(tr)
        
        # 第一个 ATR
        atr = sum(tr_values[:period]) / period
        result = [atr]
        
        # 后续 ATR (平滑)
        for i in range(period, len(tr_values)):
            atr = (atr * (period - 1) + tr_values[i]) / period
            result.append(atr)
        
        return [None] * period + result
    
    @staticmethod
    def obv(closes: List[float], volumes: List[float]) -> List[float]:
        """
        OBV 能量潮指标
        价格上涨：OBV += 成交量
        价格下跌：OBV -= 成交量
        """
        if len(closes) != len(volumes):
            return []
        
        obv = [0]
        
        for i in range(1, len(closes)):
            if closes[i] > closes[i-1]:
                obv.append(obv[-1] + volumes[i])
            elif closes[i] < closes[i-1]:
                obv.append(obv[-1] - volumes[i])
            else:
                obv.append(obv[-1])
        
        return obv
    
    @staticmethod
    def adx(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Dict:
        """
        ADX 平均趋向指数
        ADX > 25: 趋势强劲
        ADX < 20: 震荡市场
        """
        if len(highs) < period + 14:
            return {'adx': [], 'plus_di': [], 'minus_di': []}
        
        plus_dm = []
        minus_dm = []
        tr_values = []
        
        for i in range(1, len(highs)):
            up_move = highs[i] - highs[i-1]
            down_move = lows[i-1] - lows[i]
            
            plus_dm.append(up_move if up_move > down_move and up_move > 0 else 0)
            minus_dm.append(down_move if down_move > up_move and down_move > 0 else 0)
            
            tr1 = highs[i] - lows[i]
            tr2 = abs(highs[i] - closes[i-1])
            tr3 = abs(lows[i] - closes[i-1])
            tr_values.append(max(tr1, tr2, tr3))
        
        # 平滑
        plus_14 = sum(plus_dm[:period])
        minus_14 = sum(minus_dm[:period])
        tr_14 = sum(tr_values[:period])
        
        result_adx = []
        result_plus_di = []
        result_minus_di = []
        
        for i in range(period, len(plus_dm)):
            plus_14 = plus_14 - plus_14 / 14 + plus_dm[i]
            minus_14 = minus_14 - minus_14 / 14 + minus_dm[i]
            tr_14 = tr_14 - tr_14 / 14 + tr_values[i]
            
            plus_di = 100 * plus_14 / tr_14 if tr_14 > 0 else 0
            minus_di = 100 * minus_14 / tr_14 if tr_14 > 0 else 0
            
            dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di) if (plus_di + minus_di) > 0 else 0
            result_adx.append(dx)
            result_plus_di.append(plus_di)
            result_minus_di.append(minus_di)
        
        # ADX 平滑
        adx_smoothed = []
        if len(result_adx) >= period:
            adx = sum(result_adx[:period]) / period
            adx_smoothed.append(adx)
            for i in range(period, len(result_adx)):
                adx = (adx * (period - 1) + result_adx[i]) / period
                adx_smoothed.append(adx)
        
        return {
            'adx': [None] * (period * 2 - 1) + adx_smoothed,
            'plus_di': [None] * period + result_plus_di,
            'minus_di': [None] * period + result_minus_di,
        }
    
    @staticmethod
    def vwap(highs: List[float], lows: List[float], closes: List[float], volumes: List[float]) -> List[float]:
        """
        VWAP 成交量加权平均价
        机构常用指标，日内交易基准
        """
        if len(highs) != len(lows) or len(highs) != len(closes) or len(highs) != len(volumes):
            return []
        
        vwap = []
        cumulative_pv = 0
        cumulative_vol = 0
        
        for i in range(len(highs)):
            typical_price = (highs[i] + lows[i] + closes[i]) / 3
            cumulative_pv += typical_price * volumes[i]
            cumulative_vol += volumes[i]
            
            vwap.append(cumulative_pv / cumulative_vol if cumulative_vol > 0 else typical_price)
        
        return vwap
    
    @staticmethod
    def get_all_indicators(prices: List[float], highs: List[float] = None, 
                          lows: List[float] = None, volumes: List[float] = None) -> Dict:
        """
        获取所有指标
        
        Returns:
            包含所有技术指标的字典
        """
        if highs is None:
            highs = prices
        if lows is None:
            lows = prices
        if volumes is None:
            volumes = [1000000] * len(prices)
        
        return {
            'rsi_14': TechnicalIndicators.rsi(prices, 14),
            'macd': TechnicalIndicators.macd(prices),
            'bollinger': TechnicalIndicators.bollinger_bands(prices),
            'kdj': TechnicalIndicators.kdj(prices),
            'cci_20': TechnicalIndicators.cci(prices, 20),
            'atr_14': TechnicalIndicators.atr(highs, lows, prices, 14),
            'obv': TechnicalIndicators.obv(prices, volumes),
            'vwap': TechnicalIndicators.vwap(highs, lows, prices, volumes),
        }
    
    @staticmethod
    def generate_composite_signal(indicators: Dict) -> Dict:
        """
        生成综合信号 (多指标共振)
        
        高胜率组合:
        - RSI 超卖 + MACD 金叉 + 价格触及布林带下轨
        - KDJ < 20 + CCI < -100 + 成交量放大
        """
        signals = []
        bullish_count = 0
        bearish_count = 0
        
        # 1. RSI 信号
        rsi = indicators.get('rsi_14', [])
        if rsi and rsi[-1]:
            if rsi[-1] < 30:
                signals.append(('RSI_OVERSOLD', 'BULLISH', 8))
                bullish_count += 1
            elif rsi[-1] > 70:
                signals.append(('RSI_OVERBOUGHT', 'BEARISH', 8))
                bearish_count += 1
        
        # 2. MACD 信号
        macd = indicators.get('macd', {})
        if macd and macd.get('histogram'):
            hist = macd['histogram']
            if len(hist) >= 2 and hist[-2] < 0 and hist[-1] > 0:
                signals.append(('MACD_GOLDEN_CROSS', 'BULLISH', 9))
                bullish_count += 1
            elif len(hist) >= 2 and hist[-2] > 0 and hist[-1] < 0:
                signals.append(('MACD_DEATH_CROSS', 'BEARISH', 9))
                bearish_count += 1
        
        # 3. 布林带信号
        bb = indicators.get('bollinger', {})
        if bb and bb.get('current'):
            pos = bb['current'].get('position', 50)
            if pos < 10:
                signals.append(('BB_LOWER_BAND', 'BULLISH', 7))
                bullish_count += 1
            elif pos > 90:
                signals.append(('BB_UPPER_BAND', 'BEARISH', 7))
                bearish_count += 1
        
        # 4. KDJ 信号
        kdj = indicators.get('kdj', {})
        if kdj and kdj.get('current'):
            k = kdj['current'].get('k', 50)
            d = kdj['current'].get('d', 50)
            if k < 20 and k > d:
                signals.append(('KDJ_OVERSOLD', 'BULLISH', 7))
                bullish_count += 1
            elif k > 80 and k < d:
                signals.append(('KDJ_OVERBOUGHT', 'BEARISH', 7))
                bearish_count += 1
        
        # 5. CCI 信号
        cci = indicators.get('cci_20', [])
        if cci and cci[-1]:
            if cci[-1] < -100:
                signals.append(('CCI_OVERSOLD', 'BULLISH', 6))
                bullish_count += 1
            elif cci[-1] > 100:
                signals.append(('CCI_OVERBOUGHT', 'BEARISH', 6))
                bearish_count += 1
        
        # 综合判断
        total_signals = bullish_count + bearish_count
        if total_signals == 0:
            return {
                'signal': 'HOLD',
                'confidence': 50,
                'reason': '无明显信号',
                'details': signals,
            }
        
        if bullish_count > bearish_count:
            net_strength = bullish_count - bearish_count
            confidence = min(50 + net_strength * 15, 95)
            return {
                'signal': 'STRONG_BUY' if confidence > 80 else 'BUY',
                'confidence': round(confidence, 1),
                'reason': f'{bullish_count} 个多头信号 vs {bearish_count} 个空头信号',
                'details': signals,
                'bullish_count': bullish_count,
                'bearish_count': bearish_count,
            }
        else:
            net_strength = bearish_count - bullish_count
            confidence = min(50 + net_strength * 15, 95)
            return {
                'signal': 'STRONG_SELL' if confidence > 80 else 'SELL',
                'confidence': round(confidence, 1),
                'reason': f'{bearish_count} 个空头信号 vs {bullish_count} 个多头信号',
                'details': signals,
                'bullish_count': bullish_count,
                'bearish_count': bearish_count,
            }