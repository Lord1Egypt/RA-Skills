"""
K 线形态识别模块 - Candlestick Pattern Recognition
包含 8 种基础形态：4 种单 K 线形态 + 4 种双 K 线形态

Author: AITechnicals
Created: 2026-03-14
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum


class Trend(Enum):
    """趋势方向"""
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


@dataclass
class Candle:
    """K 线数据结构"""
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0
    
    @property
    def body_size(self) -> float:
        """实体大小"""
        return abs(self.close - self.open)
    
    @property
    def body_top(self) -> float:
        """实体顶部"""
        return max(self.open, self.close)
    
    @property
    def body_bottom(self) -> float:
        """实体底部"""
        return min(self.open, self.close)
    
    @property
    def upper_shadow(self) -> float:
        """上影线长度"""
        return self.high - self.body_top
    
    @property
    def lower_shadow(self) -> float:
        """下影线长度"""
        return self.body_bottom - self.low
    
    @property
    def total_range(self) -> float:
        """总振幅"""
        return self.high - self.low
    
    def is_bullish(self) -> bool:
        """是否为阳线"""
        return self.close > self.open
    
    def is_bearish(self) -> bool:
        """是否为阴线"""
        return self.close < self.open
    
    def is_doji(self, threshold: float = 0.1) -> bool:
        """是否为十字星（实体非常小）"""
        if self.total_range == 0:
            return False
        return (self.body_size / self.total_range) < threshold


# ============================================================================
# 单 K 线形态 (Single Candlestick Patterns)
# ============================================================================

def detect_hammer(candle: Candle, prev_trend: Trend, threshold: float = 0.33) -> bool:
    """
    锤子线 (Hammer)
    
    识别规则:
    1. 出现在下降趋势后
    2. 实体较小，位于 K 线的上端
    3. 下影线长度至少是实体长度的 2 倍
    4. 上影线很短或不存在
    5. 下影线长度至少是总范围的 2/3
    
    Args:
        candle: 当前 K 线
        prev_trend: 之前的趋势
        threshold: 实体占比阈值
    
    Returns:
        bool: 是否识别为锤子线
    """
    # 必须在下降趋势后
    if prev_trend != Trend.BEARISH:
        return False
    
    # 实体必须很小（不超过总范围的 1/3）
    if candle.total_range == 0:
        return False
    if (candle.body_size / candle.total_range) > threshold:
        return False
    
    # 下影线至少是实体的 2 倍
    if candle.lower_shadow < (2 * candle.body_size):
        return False
    
    # 下影线至少是总范围的 2/3
    if candle.lower_shadow < (0.66 * candle.total_range):
        return False
    
    # 上影线应该很短
    if candle.upper_shadow > candle.body_size:
        return False
    
    return True


def detect_hanging_man(candle: Candle, prev_trend: Trend, threshold: float = 0.33) -> bool:
    """
    吊颈线 (Hanging Man)
    
    识别规则:
    1. 出现在上升趋势后
    2. 实体较小，位于 K 线的上端
    3. 下影线长度至少是实体长度的 2 倍
    4. 上影线很短或不存在
    5. 与锤子线形态相同，但出现在不同趋势
    
    Args:
        candle: 当前 K 线
        prev_trend: 之前的趋势
        threshold: 实体占比阈值
    
    Returns:
        bool: 是否识别为吊颈线
    """
    # 必须在上升趋势后
    if prev_trend != Trend.BULLISH:
        return False
    
    # 实体必须很小（不超过总范围的 1/3）
    if candle.total_range == 0:
        return False
    if (candle.body_size / candle.total_range) > threshold:
        return False
    
    # 下影线至少是实体的 2 倍
    if candle.lower_shadow < (2 * candle.body_size):
        return False
    
    # 下影线至少是总范围的 2/3
    if candle.lower_shadow < (0.66 * candle.total_range):
        return False
    
    # 上影线应该很短
    if candle.upper_shadow > candle.body_size:
        return False
    
    return True


def detect_doji(candle: Candle, threshold: float = 0.1) -> bool:
    """
    十字星 (Doji)
    
    识别规则:
    1. 开盘价和收盘价非常接近（几乎相等）
    2. 实体大小不超过总范围的 10%
    3. 可以有不同长度的上下影线
    
    Args:
        candle: 当前 K 线
        threshold: 实体占比阈值（默认 10%）
    
    Returns:
        bool: 是否识别为十字星
    """
    if candle.total_range == 0:
        return False
    
    # 实体非常小
    return (candle.body_size / candle.total_range) < threshold


def detect_shooting_star(candle: Candle, prev_trend: Trend, threshold: float = 0.33) -> bool:
    """
    射击之星 (Shooting Star)
    
    识别规则:
    1. 出现在上升趋势后
    2. 实体较小，位于 K 线的下端
    3. 上影线长度至少是实体长度的 2 倍
    4. 下影线很短或不存在
    5. 上影线长度至少是总范围的 2/3
    
    Args:
        candle: 当前 K 线
        prev_trend: 之前的趋势
        threshold: 实体占比阈值
    
    Returns:
        bool: 是否识别为射击之星
    """
    # 必须在上升趋势后
    if prev_trend != Trend.BULLISH:
        return False
    
    # 实体必须很小（不超过总范围的 1/3）
    if candle.total_range == 0:
        return False
    if (candle.body_size / candle.total_range) > threshold:
        return False
    
    # 上影线至少是实体的 2 倍
    if candle.upper_shadow < (2 * candle.body_size):
        return False
    
    # 上影线至少是总范围的 2/3
    if candle.upper_shadow < (0.66 * candle.total_range):
        return False
    
    # 下影线应该很短
    if candle.lower_shadow > candle.body_size:
        return False
    
    return True


# ============================================================================
# 双 K 线形态 (Double Candlestick Patterns)
# ============================================================================

def detect_bullish_engulfing(candle1: Candle, candle2: Candle) -> bool:
    """
    看涨吞没 (Bullish Engulfing)
    
    识别规则:
    1. 第一根是阴线（下跌）
    2. 第二根是阳线（上涨）
    3. 第二根的实体完全吞没第一根的实体
       - 第二根的开盘价 < 第一根的收盘价
       - 第二根的收盘价 > 第一根的开盘价
    4. 出现在下降趋势中（隐含）
    
    Args:
        candle1: 第一根 K 线（前一根）
        candle2: 第二根 K 线（当前）
    
    Returns:
        bool: 是否识别为看涨吞没
    """
    # 第一根必须是阴线
    if not candle1.is_bearish():
        return False
    
    # 第二根必须是阳线
    if not candle2.is_bullish():
        return False
    
    # 第二根实体必须完全吞没第一根实体
    if candle2.open >= candle1.close:
        return False
    if candle2.close <= candle1.open:
        return False
    
    return True


def detect_bearish_engulfing(candle1: Candle, candle2: Candle) -> bool:
    """
    看跌吞没 (Bearish Engulfing)
    
    识别规则:
    1. 第一根是阳线（上涨）
    2. 第二根是阴线（下跌）
    3. 第二根的实体完全吞没第一根的实体
       - 第二根的开盘价 > 第一根的收盘价
       - 第二根的收盘价 < 第一根的开盘价
    4. 出现在上升趋势中（隐含）
    
    Args:
        candle1: 第一根 K 线（前一根）
        candle2: 第二根 K 线（当前）
    
    Returns:
        bool: 是否识别为看跌吞没
    """
    # 第一根必须是阳线
    if not candle1.is_bullish():
        return False
    
    # 第二根必须是阴线
    if not candle2.is_bearish():
        return False
    
    # 第二根实体必须完全吞没第一根实体
    if candle2.open <= candle1.close:
        return False
    if candle2.close >= candle1.open:
        return False
    
    return True


def detect_piercing_line(candle1: Candle, candle2: Candle, penetration_ratio: float = 0.5) -> bool:
    """
    曙光初现 (Piercing Line)
    
    识别规则:
    1. 第一根是长阴线（下降）
    2. 第二根是阳线（上涨）
    3. 第二根开盘价低于第一根最低价（向下跳空）
    4. 第二根收盘价深入第一根实体内部，超过 50%
       - 收盘价 > 第一根实体中点
    
    Args:
        candle1: 第一根 K 线（前一根）
        candle2: 第二根 K 线（当前）
        penetration_ratio: 穿透比例阈值（默认 50%）
    
    Returns:
        bool: 是否识别为曙光初现
    """
    # 第一根必须是阴线
    if not candle1.is_bearish():
        return False
    
    # 第二根必须是阳线
    if not candle2.is_bullish():
        return False
    
    # 第二根开盘价低于第一根最低价（跳空低开）
    if candle2.open >= candle1.low:
        return False
    
    # 计算第一根实体的中点
    candle1_midpoint = (candle1.open + candle1.close) / 2
    
    # 第二根收盘价必须超过第一根实体中点（穿透超过 50%）
    if candle2.close <= candle1_midpoint:
        return False
    
    # 第二根收盘价不能超过第一根开盘价（否则变成吞没）
    if candle2.close >= candle1.open:
        return False
    
    return True


def detect_dark_cloud_cover(candle1: Candle, candle2: Candle, penetration_ratio: float = 0.5) -> bool:
    """
    乌云盖顶 (Dark Cloud Cover)
    
    识别规则:
    1. 第一根是长阳线（上涨）
    2. 第二根是阴线（下跌）
    3. 第二根开盘价高于第一根最高价（向上跳空）
    4. 第二根收盘价深入第一根实体内部，超过 50%
       - 收盘价 < 第一根实体中点
    
    Args:
        candle1: 第一根 K 线（前一根）
        candle2: 第二根 K 线（当前）
        penetration_ratio: 穿透比例阈值（默认 50%）
    
    Returns:
        bool: 是否识别为乌云盖顶
    """
    # 第一根必须是阳线
    if not candle1.is_bullish():
        return False
    
    # 第二根必须是阴线
    if not candle2.is_bearish():
        return False
    
    # 第二根开盘价高于第一根最高价（跳空高开）
    if candle2.open <= candle1.high:
        return False
    
    # 计算第一根实体的中点
    candle1_midpoint = (candle1.open + candle1.close) / 2
    
    # 第二根收盘价必须低于第一根实体中点（穿透超过 50%）
    if candle2.close >= candle1_midpoint:
        return False
    
    # 第二根收盘价不能低于第一根开盘价（否则变成吞没）
    if candle2.close <= candle1.open:
        return False
    
    return True


# ============================================================================
# 批量检测函数
# ============================================================================

def detect_single_candle_patterns(candle: Candle, prev_trend: Trend) -> dict:
    """
    检测所有单 K 线形态
    
    Args:
        candle: K 线数据
        prev_trend: 之前的趋势
    
    Returns:
        dict: 各形态的检测结果
    """
    return {
        'hammer': detect_hammer(candle, prev_trend),
        'hanging_man': detect_hanging_man(candle, prev_trend),
        'doji': detect_doji(candle),
        'shooting_star': detect_shooting_star(candle, prev_trend)
    }


def detect_double_candle_patterns(candle1: Candle, candle2: Candle) -> dict:
    """
    检测所有双 K 线形态
    
    Args:
        candle1: 第一根 K 线（前一根）
        candle2: 第二根 K 线（当前）
    
    Returns:
        dict: 各形态的检测结果
    """
    return {
        'bullish_engulfing': detect_bullish_engulfing(candle1, candle2),
        'bearish_engulfing': detect_bearish_engulfing(candle1, candle2),
        'piercing_line': detect_piercing_line(candle1, candle2),
        'dark_cloud_cover': detect_dark_cloud_cover(candle1, candle2)
    }


# ============================================================================
# 测试用例
# ============================================================================

def run_tests():
    """运行所有测试用例"""
    print("=" * 60)
    print("K 线形态识别测试")
    print("=" * 60)
    
    test_count = 0
    pass_count = 0
    
    # --- 单 K 线形态测试 ---
    print("\n【单 K 线形态测试】\n")
    
    # 测试 1: 锤子线
    print("测试 1: 锤子线 (Hammer)")
    hammer_candle = Candle(open=10.0, high=10.2, low=9.0, close=10.1)
    result = detect_hammer(hammer_candle, Trend.BEARISH)
    print(f"  下降趋势后的锤子线：{result} (期望：True)")
    test_count += 1
    if result: pass_count += 1
    
    # 测试 2: 非锤子线（上升趋势）
    result = detect_hammer(hammer_candle, Trend.BULLISH)
    print(f"  上升趋势后的锤子线：{result} (期望：False)")
    test_count += 1
    if not result: pass_count += 1
    
    # 测试 3: 吊颈线
    print("\n测试 2: 吊颈线 (Hanging Man)")
    hanging_man_candle = Candle(open=10.0, high=10.2, low=9.0, close=10.1)
    result = detect_hanging_man(hanging_man_candle, Trend.BULLISH)
    print(f"  上升趋势后的吊颈线：{result} (期望：True)")
    test_count += 1
    if result: pass_count += 1
    
    # 测试 4: 十字星
    print("\n测试 3: 十字星 (Doji)")
    doji_candle = Candle(open=10.0, high=10.5, low=9.5, close=10.02)
    result = detect_doji(doji_candle)
    print(f"  十字星：{result} (期望：True)")
    test_count += 1
    if result: pass_count += 1
    
    # 测试 5: 非十字星
    normal_candle = Candle(open=10.0, high=11.0, low=9.0, close=10.8)
    result = detect_doji(normal_candle)
    print(f"  普通 K 线：{result} (期望：False)")
    test_count += 1
    if not result: pass_count += 1
    
    # 测试 6: 射击之星
    print("\n测试 4: 射击之星 (Shooting Star)")
    shooting_star_candle = Candle(open=10.0, high=11.0, low=9.9, close=9.95)
    result = detect_shooting_star(shooting_star_candle, Trend.BULLISH)
    print(f"  上升趋势后的射击之星：{result} (期望：True)")
    test_count += 1
    if result: pass_count += 1
    
    # --- 双 K 线形态测试 ---
    print("\n【双 K 线形态测试】\n")
    
    # 测试 7: 看涨吞没
    print("测试 5: 看涨吞没 (Bullish Engulfing)")
    candle1 = Candle(open=10.5, high=10.6, low=10.0, close=10.1)  # 阴线
    candle2 = Candle(open=10.0, high=10.7, low=9.9, close=10.6)   # 阳线，吞没
    result = detect_bullish_engulfing(candle1, candle2)
    print(f"  看涨吞没：{result} (期望：True)")
    test_count += 1
    if result: pass_count += 1
    
    # 测试 8: 看跌吞没
    print("\n测试 6: 看跌吞没 (Bearish Engulfing)")
    candle1 = Candle(open=10.0, high=10.6, low=10.0, close=10.5)  # 阳线
    candle2 = Candle(open=10.6, high=10.7, low=9.9, close=9.95)   # 阴线，吞没
    result = detect_bearish_engulfing(candle1, candle2)
    print(f"  看跌吞没：{result} (期望：True)")
    test_count += 1
    if result: pass_count += 1
    
    # 测试 9: 曙光初现
    print("\n测试 7: 曙光初现 (Piercing Line)")
    candle1 = Candle(open=10.5, high=10.6, low=10.0, close=10.1)  # 阴线
    candle2 = Candle(open=9.8, high=10.4, low=9.7, close=10.35)   # 阳线，穿透>50%
    result = detect_piercing_line(candle1, candle2)
    print(f"  曙光初现：{result} (期望：True)")
    test_count += 1
    if result: pass_count += 1
    
    # 测试 10: 乌云盖顶
    print("\n测试 8: 乌云盖顶 (Dark Cloud Cover)")
    candle1 = Candle(open=10.0, high=10.6, low=10.0, close=10.5)  # 阳线，实体中点=10.25
    candle2 = Candle(open=10.8, high=10.9, low=10.1, close=10.2)  # 阴线，收盘价 10.2 < 10.25 但>10.0
    result = detect_dark_cloud_cover(candle1, candle2)
    print(f"  乌云盖顶：{result} (期望：True)")
    test_count += 1
    if result: pass_count += 1
    
    # --- 批量检测测试 ---
    print("\n【批量检测测试】\n")
    
    print("测试 9: 批量检测单 K 线形态")
    patterns = detect_single_candle_patterns(doji_candle, Trend.NEUTRAL)
    print(f"  结果：{patterns}")
    test_count += 1
    if patterns['doji']: pass_count += 1
    
    print("\n测试 10: 批量检测双 K 线形态")
    patterns = detect_double_candle_patterns(
        Candle(open=10.5, high=10.6, low=10.0, close=10.1),
        Candle(open=10.0, high=10.7, low=9.9, close=10.6)
    )
    print(f"  结果：{patterns}")
    test_count += 1
    if patterns['bullish_engulfing']: pass_count += 1
    
    # --- 测试结果汇总 ---
    print("\n" + "=" * 60)
    print(f"测试结果：{pass_count}/{test_count} 通过")
    print(f"通过率：{pass_count/test_count*100:.1f}%")
    print("=" * 60)
    
    return pass_count == test_count


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
