"""
智能信号生成系统
功能：
1. 信号强度评分 (0-100 分)
   - 指标符合度 (40 分)
   - 形态确认度 (30 分)
   - 量价配合度 (20 分)
   - 趋势强度 (10 分)
2. 置信度计算
3. 目标价和止损位自动计算
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SignalResult:
    """信号结果数据类"""
    signal: str  # "BUY", "SELL", "HOLD"
    strength: int  # 0-100
    confidence: float  # 0.0-1.0
    reason: str
    target_price: float
    stop_loss: float


class SmartSignalGenerator:
    """智能信号生成器"""
    
    def __init__(self):
        """初始化信号生成器"""
        pass
    
    def calculate_indicator_alignment_score(self, data: pd.DataFrame) -> float:
        """
        计算指标符合度分数 (满分40分)
        
        Args:
            data: 包含技术指标的数据
            
        Returns:
            指标符合度分数 (0-40)
        """
        score = 0.0
        
        # MACD金叉死叉判断
        if len(data) >= 2:
            macd_current = data['macd'].iloc[-1]
            macd_signal = data['macd_signal'].iloc[-1]
            macd_prev = data['macd'].iloc[-2]
            macd_signal_prev = data['macd_signal'].iloc[-2]
            
            # 金叉情况
            if macd_prev <= macd_signal_prev and macd_current > macd_signal_current:
                score += 10  # 买入信号
            elif macd_prev >= macd_signal_prev and macd_current < macd_signal_current:
                score -= 10  # 卖出信号
                
        # RSI超买超卖判断
        if 'rsi' in data.columns:
            rsi = data['rsi'].iloc[-1]
            if 30 <= rsi <= 70:
                # RSI在正常范围，根据趋势调整分数
                if rsi < 50:  # 偏向超卖
                    score += min(10, (50 - rsi) / 5)  # 最多加10分
                else:  # 偏向超买
                    score -= min(10, (rsi - 50) / 5)  # 最多减10分
            elif rsi < 30:  # 超卖
                score += 15  # 强烈买入信号
            elif rsi > 70:  # 超买
                score -= 15  # 强烈卖出信号
        
        # KDJ指标
        if 'k' in data.columns and 'd' in data.columns:
            k = data['k'].iloc[-1]
            d = data['d'].iloc[-1]
            k_prev = data['k'].iloc[-2] if len(data) >= 2 else k
            d_prev = data['d'].iloc[-2] if len(data) >= 2 else d
            
            # KDJ金叉
            if k_prev <= d_prev and k > d:
                score += 8
            elif k_prev >= d_prev and k < d:
                score -= 8
                
            # KDJ位置
            if k < 20:  # 超卖
                score += 5
            elif k > 80:  # 超买
                score -= 5
        
        # 将分数限制在0-40范围内
        score = max(0, min(40, 20 + score))  # 基础分20分，根据指标表现调整
        
        return score
    
    def calculate_pattern_recognition_score(self, data: pd.DataFrame) -> float:
        """
        计算形态确认度分数 (满分30分)
        
        Args:
            data: 包含价格数据的DataFrame
            
        Returns:
            形态确认度分数 (0-30)
        """
        score = 0.0
        
        if len(data) < 3:
            return score
            
        # 获取最近几根K线的数据
        recent_data = data.tail(10)  # 取最近10根K线用于形态识别
        
        # 检查锤子线（底部反转信号）
        for i in range(len(recent_data)):
            high = recent_data['high'].iloc[i]
            low = recent_data['low'].iloc[i]
            open_price = recent_data['open'].iloc[i]
            close = recent_data['close'].iloc[i]
            
            body = abs(close - open_price)
            upper_shadow = high - max(open_price, close)
            lower_shadow = min(open_price, close) - low
            
            # 锤子线条件：下影线长度至少是实体长度的2倍，上影线很短或没有
            if lower_shadow >= 2 * body and upper_shadow <= 0.1 * body:
                score += 15  # 锤子线是一个较强的买入信号
                break
                
        # 检查上吊线（顶部反转信号）
        for i in range(len(recent_data)):
            high = recent_data['high'].iloc[i]
            low = recent_data['low'].iloc[i]
            open_price = recent_data['open'].iloc[i]
            close = recent_data['close'].iloc[i]
            
            body = abs(close - open_price)
            upper_shadow = high - max(open_price, close)
            lower_shadow = min(open_price, close) - low
            
            # 上吊线条件：下影线长度至少是实体长度的2倍，上影线很短或没有，在上升趋势中出现
            if lower_shadow >= 2 * body and upper_shadow <= 0.1 * body:
                # 如果在上升趋势中，可能是顶部反转信号
                if len(data) >= 20:
                    avg_price_past = data['close'].tail(20).mean()
                    current_price = data['close'].iloc[-1]
                    if current_price > avg_price_past * 1.02:  # 当前价格高于过去平均价2%
                        score -= 15  # 上吊线在上升趋势中是卖出信号
                break
        
        # 检查吞没形态
        if len(data) >= 2:
            # 当前K线
            curr_open = data['open'].iloc[-1]
            curr_close = data['close'].iloc[-1]
            # 前一根K线
            prev_open = data['open'].iloc[-2]
            prev_close = data['close'].iloc[-2]
            
            # 多头吞噬：当前阳线完全覆盖前一根阴线
            if curr_close > curr_open and prev_close < prev_open and \
               curr_open < prev_close and curr_close > prev_open:
                score += 12  # 强烈买入信号
                
            # 空头吞噬：当前阴线完全覆盖前一根阳线
            elif curr_close < curr_open and prev_close > prev_open and \
                 curr_open > prev_close and curr_close < prev_open:
                score -= 12  # 强烈卖出信号
        
        # 将分数限制在0-30范围内
        score = max(0, min(30, score))
        
        return score
    
    def calculate_volume_price_alignment_score(self, data: pd.DataFrame) -> float:
        """
        计算量价配合度分数 (满分20分)
        
        Args:
            data: 包含成交量和价格数据的DataFrame
            
        Returns:
            量价配合度分数 (0-20)
        """
        score = 0.0
        
        if len(data) < 5 or 'volume' not in data.columns:
            return score
            
        # 计算近期成交量均值
        vol_avg_recent = data['volume'].tail(5).mean()
        vol_avg_prev = data['volume'].tail(10).head(5).mean()  # 前5日均值
        
        # 计算价格变化
        price_change_pct = (data['close'].iloc[-1] - data['close'].iloc[-5]) / data['close'].iloc[-5]
        
        # 量增价涨：积极信号
        if price_change_pct > 0 and vol_avg_recent > vol_avg_prev:
            score += 10  # 支持上涨趋势
        # 量减价跌：消极但正常的信号
        elif price_change_pct < 0 and vol_avg_recent < vol_avg_prev:
            score += 5  # 正常回调
        # 量增价跌：警惕信号
        elif price_change_pct < 0 and vol_avg_recent > vol_avg_prev:
            score -= 5  # 可能有大量抛售
        # 量减价涨：需谨慎
        elif price_change_pct > 0 and vol_avg_recent < vol_avg_prev:
            score += 3  # 涨幅缺乏量能支持
        
        # 检查是否出现放量突破
        current_volume = data['volume'].iloc[-1]
        volume_sma = data['volume'].rolling(window=20).mean().iloc[-1]
        
        if current_volume > volume_sma * 1.5:  # 成交量放大超过50%
            # 如果同时价格上涨，则为强势突破
            if price_change_pct > 0:
                score += 5  # 强势突破
            else:
                score -= 3  # 放量下跌，需警惕
        
        # 将分数限制在0-20范围内
        score = max(0, min(20, 10 + score))  # 基础分10分，根据量价关系调整
        
        return score
    
    def calculate_trend_strength_score(self, data: pd.DataFrame) -> float:
        """
        计算趋势强度分数 (满分10分)
        
        Args:
            data: 包含价格数据的DataFrame
            
        Returns:
            趋势强度分数 (0-10)
        """
        score = 0.0
        
        if len(data) < 20:
            return score
            
        # 计算短期和长期移动平均线
        short_ma = data['close'].rolling(window=5).mean()
        long_ma = data['close'].rolling(window=20).mean()
        
        # 短期均线与长期均线的关系
        ma_relationship = short_ma.iloc[-1] - long_ma.iloc[-1]
        
        # 计算价格相对于20日均线的位置
        price_position = (data['close'].iloc[-1] - long_ma.iloc[-1]) / long_ma.iloc[-1]
        
        # 趋势方向和强度判断
        if ma_relationship > 0 and price_position > 0:  # 短期均线上穿长期均线，且价格在均线上方
            score += 4  # 多头趋势
        elif ma_relationship < 0 and price_position < 0:  # 短期均线下穿长期均线，且价格在均线下方
            score -= 4  # 空头趋势
        
        # 计算价格趋势斜率
        recent_prices = data['close'].tail(10).values
        x = np.arange(len(recent_prices))
        slope, _ = np.polyfit(x, recent_prices, 1)
        
        # 根据斜率判断趋势强度
        normalized_slope = slope / data['close'].iloc[-1]  # 归一化处理
        trend_strength = min(abs(normalized_slope) * 100, 3)  # 最多3分
        if normalized_slope > 0:
            score += trend_strength  # 上升趋势加分
        else:
            score -= trend_strength  # 下降趋势减分
        
        # 将分数限制在0-10范围内
        score = max(0, min(10, 5 + score))  # 基础分5分，根据趋势调整
        
        return score
    
    def calculate_confidence_level(self, strength: float) -> float:
        """
        根据信号强度计算置信度
        
        Args:
            strength: 信号强度 (0-100)
            
        Returns:
            置信度 (0.0-1.0)
        """
        if strength >= 90:
            return 0.95  # 极高置信度
        elif strength >= 70:
            return 0.80  # 高置信度
        elif strength >= 50:
            return 0.65  # 中等置信度
        else:
            return 0.40  # 低置信度
    
    def calculate_target_and_stoploss(self, 
                                   current_price: float, 
                                   signal: str, 
                                   strength: float) -> Tuple[float, float]:
        """
        计算目标价和止损位
        
        Args:
            current_price: 当前价格
            signal: 交易信号 ("BUY" 或 "SELL")
            strength: 信号强度
            
        Returns:
            (target_price, stop_loss)
        """
        if signal == "BUY":
            # 买入信号：计算上方目标位和下方止损位
            risk_reward_ratio = 2.0  # 风险收益比
            volatility_factor = strength / 100.0  # 根据信号强度调整
            
            # 根据信号强度计算波动率系数
            base_target_pct = 0.05 * volatility_factor  # 基础目标涨幅5% * 信号强度系数
            base_stop_pct = 0.025 * volatility_factor  # 基础止损跌幅2.5% * 信号强度系数
            
            target_price = current_price * (1 + base_target_pct)
            stop_loss = current_price * (1 - base_stop_pct)
            
        elif signal == "SELL":
            # 卖出信号：计算下方目标位和上方止损位
            risk_reward_ratio = 2.0  # 风险收益比
            volatility_factor = strength / 100.0  # 根据信号强度调整
            
            # 根据信号强度计算波动率系数
            base_target_pct = 0.05 * volatility_factor  # 基础目标跌幅5% * 信号强度系数
            base_stop_pct = 0.025 * volatility_factor  # 基础止损涨幅2.5% * 信号强度系数
            
            target_price = current_price * (1 - base_target_pct)
            stop_loss = current_price * (1 + base_stop_pct)
        else:
            # HOLD信号：不设置目标价和止损
            target_price = current_price
            stop_loss = current_price
        
        return round(target_price, 2), round(stop_loss, 2)
    
    def generate_signal(self, data: pd.DataFrame) -> SignalResult:
        """
        生成交易信号
        
        Args:
            data: 包含价格、成交量和技术指标的DataFrame
            
        Returns:
            SignalResult对象，包含完整的信号信息
        """
        # 计算各项评分
        indicator_score = self.calculate_indicator_alignment_score(data)
        pattern_score = self.calculate_pattern_recognition_score(data)
        volume_score = self.calculate_volume_price_alignment_score(data)
        trend_score = self.calculate_trend_strength_score(data)
        
        # 计算总信号强度
        total_strength = indicator_score + pattern_score + volume_score + trend_score
        
        # 限制总强度在0-100之间
        total_strength = max(0, min(100, total_strength))
        
        # 确定交易信号
        if total_strength > 60:
            # 强度大于60，看具体指标情况确定买卖方向
            if indicator_score > 20:  # 如果指标符合度较高
                signal = "BUY"
            else:
                signal = "SELL"
        elif total_strength < 40:
            # 强度小于40，可能是卖出信号
            signal = "SELL"
        else:
            # 中等强度，保持观望
            signal = "HOLD"
        
        # 计算置信度
        confidence = self.calculate_confidence_level(total_strength)
        
        # 生成原因描述
        reasons = []
        if indicator_score > 25:
            reasons.append("指标符合度高")
        elif indicator_score < 15:
            reasons.append("指标出现背离")
            
        if pattern_score > 20:
            reasons.append("形态确认度高")
        elif pattern_score < 10:
            reasons.append("形态不够明确")
            
        if volume_score > 15:
            reasons.append("量价配合良好")
        elif volume_score < 8:
            reasons.append("量价配合不佳")
            
        if trend_score > 7:
            reasons.append("趋势强度高")
        elif trend_score < 3:
            reasons.append("趋势不明朗")
        
        reason_str = " + ".join(reasons) if reasons else "市场震荡整理"
        
        # 获取当前价格并计算目标价和止损位
        current_price = data['close'].iloc[-1] if 'close' in data.columns else 0
        target_price, stop_loss = self.calculate_target_and_stoploss(
            current_price, signal, total_strength
        )
        
        return SignalResult(
            signal=signal,
            strength=int(total_strength),
            confidence=round(confidence, 2),
            reason=reason_str,
            target_price=target_price,
            stop_loss=stop_loss
        )


def generate_smart_signal(data: pd.DataFrame) -> Dict:
    """
    便捷函数：直接从数据生成智能信号
    
    Args:
        data: 包含价格、成交量和技术指标的DataFrame
        
    Returns:
        字典格式的信号结果
    """
    generator = SmartSignalGenerator()
    result = generator.generate_signal(data)
    
    return {
        "signal": result.signal,
        "strength": result.strength,
        "confidence": result.confidence,
        "reason": result.reason,
        "target_price": result.target_price,
        "stop_loss": result.stop_loss
    }


if __name__ == "__main__":
    # 示例用法
    print("智能信号生成系统已加载")
    print("使用 generate_smart_signal(data) 函数来生成信号")