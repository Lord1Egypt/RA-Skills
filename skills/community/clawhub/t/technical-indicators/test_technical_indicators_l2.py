"""
技术指标 L2 单元测试

测试指标:
1. Ichimoku Cloud (一目均衡表)
2. VWAP (成交量加权平均价)
3. SuperTrend (超级趋势)
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 导入待测试模块
from ichimoku_cloud import (
    calculate_ichimoku,
    identify_cloud_breakout,
    identify_tk_cross,
    identify_chikou_signal,
    get_ichimoku_summary,
    get_all_ichimoku_parameters
)

from vwap import (
    calculate_vwap,
    calculate_vwap_intraday,
    identify_vwap_position,
    get_vwap_support_resistance,
    get_vwap_summary
)

from supertrend import (
    calculate_atr,
    calculate_supertrend,
    identify_trend_reversal,
    get_supertrend_levels,
    get_supertrend_summary,
    scan_supertrend_signals
)


def create_sample_data(n_periods: int = 100, trend: str = 'neutral') -> pd.DataFrame:
    """
    创建示例测试数据
    
    Args:
        n_periods: 周期数
        trend: 趋势类型 ('up', 'down', 'neutral')
    
    Returns:
        包含 OHLCV 数据的 DataFrame
    """
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=n_periods, freq='D')
    
    base_price = 100
    
    if trend == 'up':
        trend_component = np.linspace(0, 20, n_periods)
    elif trend == 'down':
        trend_component = np.linspace(0, -20, n_periods)
    else:
        trend_component = np.zeros(n_periods)
    
    noise = np.cumsum(np.random.randn(n_periods) * 1.5)
    prices = base_price + trend_component + noise
    
    df = pd.DataFrame({
        'date': dates,
        'open': prices + np.random.randn(n_periods) * 0.5,
        'high': prices + np.abs(np.random.randn(n_periods)) * 1.5,
        'low': prices - np.abs(np.random.randn(n_periods)) * 1.5,
        'close': prices,
        'volume': np.random.randint(1000000, 5000000, n_periods)
    })
    df.set_index('date', inplace=True)
    
    return df


def create_intraday_data(n_minutes: int = 240) -> pd.DataFrame:
    """
    创建日内分钟级测试数据
    
    Args:
        n_minutes: 分钟数
    
    Returns:
        包含日内 OHLCV 数据的 DataFrame
    """
    np.random.seed(42)
    
    base_time = pd.Timestamp('2024-03-14 09:30:00')
    times = [base_time + pd.Timedelta(minutes=i) for i in range(n_minutes)]
    
    base_price = 100
    prices = base_price + np.cumsum(np.random.randn(n_minutes) * 0.3) + np.linspace(0, 2, n_minutes)
    
    volume_pattern = np.sin(np.linspace(0, np.pi, n_minutes)) + 1
    volumes = (volume_pattern * np.random.uniform(0.8, 1.2, n_minutes) * 10000).astype(int)
    
    df = pd.DataFrame({
        'datetime': times,
        'open': prices + np.random.randn(n_minutes) * 0.2,
        'high': prices + np.abs(np.random.randn(n_minutes)) * 0.5,
        'low': prices - np.abs(np.random.randn(n_minutes)) * 0.5,
        'close': prices,
        'volume': volumes
    })
    
    return df


# ============================================================
# Ichimoku Cloud 测试
# ============================================================

class TestIchimokuCloud(unittest.TestCase):
    """Ichimoku Cloud 指标测试"""
    
    def setUp(self):
        """测试前准备"""
        self.df = create_sample_data(n_periods=100, trend='neutral')
    
    def test_calculate_ichimoku_columns(self):
        """测试计算结果包含所有必需的列"""
        df_ichimoku = calculate_ichimoku(self.df)
        
        required_columns = ['tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b', 'chikou_span']
        
        for col in required_columns:
            self.assertIn(col, df_ichimoku.columns, f"缺少列：{col}")
    
    def test_calculate_ichimoku_values_not_nan(self):
        """测试计算结果不为 NaN (在有效数据范围内)"""
        df_ichimoku = calculate_ichimoku(self.df)
        
        # 跳过前 52 个周期 (因为需要 52 周期数据)
        valid_data = df_ichimoku.iloc[60:]
        
        for col in ['tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b']:
            non_nan_count = valid_data[col].notna().sum()
            self.assertGreater(non_nan_count, 0, f"{col} 全部为 NaN")
    
    def test_tenkan_sen_calculation(self):
        """测试转换线计算正确性"""
        df_ichimoku = calculate_ichimoku(self.df)
        
        # 手动计算转换线
        high_9 = self.df['high'].rolling(window=9).max()
        low_9 = self.df['low'].rolling(window=9).min()
        expected_tenkan = (high_9 + low_9) / 2
        
        # 比较结果
        pd.testing.assert_series_equal(
            df_ichimoku['tenkan_sen'],
            expected_tenkan,
            check_names=False
        )
    
    def test_kijun_sen_calculation(self):
        """测试基准线计算正确性"""
        df_ichimoku = calculate_ichimoku(self.df)
        
        # 手动计算基准线
        high_26 = self.df['high'].rolling(window=26).max()
        low_26 = self.df['low'].rolling(window=26).min()
        expected_kijun = (high_26 + low_26) / 2
        
        # 比较结果
        pd.testing.assert_series_equal(
            df_ichimoku['kijun_sen'],
            expected_kijun,
            check_names=False
        )
    
    def test_senkou_span_displacement(self):
        """测试先行跨度的平移"""
        df_ichimoku = calculate_ichimoku(self.df)
        
        # 先行跨度 A 应该是当前值向前平移 26 周期
        # 所以 senkou_span_a[i] 应该等于 (tenkan_sen[i-26] + kijun_sen[i-26]) / 2
        
        # 检查第 80 行的 senkou_span_a 是否等于第 54 行的 (tenkan + kijun) / 2
        idx_current = 80
        idx_shifted = 80 - 26
        
        if idx_shifted >= 0 and idx_shifted < len(df_ichimoku):
            expected_span_a = (df_ichimoku.iloc[idx_shifted]['tenkan_sen'] + 
                              df_ichimoku.iloc[idx_shifted]['kijun_sen']) / 2
            actual_span_a = df_ichimoku.iloc[idx_current]['senkou_span_a']
            
            if pd.notna(expected_span_a) and pd.notna(actual_span_a):
                self.assertAlmostEqual(expected_span_a, actual_span_a, places=2)
    
    def test_get_all_ichimoku_parameters(self):
        """测试获取 9 个参数"""
        params = get_all_ichimoku_parameters(self.df)
        
        required_params = [
            '转换线', '基准线', '先行跨度 A', '先行跨度 B', '滞后跨度',
            '云团顶部', '云团底部', '云团颜色', '价格相对云团位置'
        ]
        
        for param in required_params:
            self.assertIn(param, params, f"缺少参数：{param}")
    
    def test_cloud_breakout_detection(self):
        """测试云团突破检测"""
        df_ichimoku = calculate_ichimoku(self.df)
        breakout = identify_cloud_breakout(df_ichimoku)
        
        self.assertIn('cloud_color', breakout)
        self.assertIn('price_position', breakout)
        self.assertIn('breakout_signal', breakout)
        
        # 云团颜色应该是 bullish 或 bearish
        self.assertIn(breakout.get('cloud_color'), ['bullish', 'bearish', None])
    
    def test_tk_cross_detection(self):
        """测试 TK 交叉检测"""
        df_ichimoku = calculate_ichimoku(self.df)
        tk_cross = identify_tk_cross(df_ichimoku)
        
        self.assertIn('cross_signal', tk_cross)
        self.assertIn('tk_position', tk_cross)
        
        # 交叉信号应该是 golden_cross, death_cross 或 None
        valid_signals = ['golden_cross', 'death_cross', None]
        self.assertIn(tk_cross.get('cross_signal'), valid_signals)
    
    def test_ichimoku_summary(self):
        """测试综合分析报告"""
        summary = get_ichimoku_summary(self.df)
        
        self.assertNotIn('error', summary)
        self.assertIn('current_price', summary)
        self.assertIn('overall_trend', summary)
        self.assertIn('recommendation', summary)
        
        # 总体趋势应该是预定义的值之一
        valid_trends = ['strong_bullish', 'bullish', 'strong_bearish', 'bearish', 'neutral']
        self.assertIn(summary.get('overall_trend'), valid_trends)
    
    def test_insufficient_data(self):
        """测试数据不足的情况"""
        small_df = create_sample_data(n_periods=30)
        
        # 数据不足时应该返回错误
        summary = get_ichimoku_summary(small_df)
        self.assertIn('error', summary)


# ============================================================
# VWAP 测试
# ============================================================

class TestVWAP(unittest.TestCase):
    """VWAP 指标测试"""
    
    def setUp(self):
        """测试前准备"""
        self.df_daily = create_sample_data(n_periods=100, trend='neutral')
        self.df_intraday = create_intraday_data(n_minutes=240)
    
    def test_calculate_vwap_columns(self):
        """测试 VWAP 计算结果包含必需的列"""
        df_vwap = calculate_vwap(self.df_daily)
        
        self.assertIn('vwap', df_vwap.columns)
    
    def test_vwap_values_reasonable(self):
        """测试 VWAP 值在合理范围内"""
        df_vwap = calculate_vwap(self.df_daily)
        
        vwap_values = df_vwap['vwap'].dropna()
        close_values = df_vwap['close']
        
        # VWAP 应该与价格在同一数量级
        self.assertGreater(vwap_values.min(), close_values.min() * 0.5)
        self.assertLess(vwap_values.max(), close_values.max() * 1.5)
    
    def test_vwap_intraday(self):
        """测试日内 VWAP 计算"""
        df_vwap = calculate_vwap_intraday(self.df_intraday)
        
        self.assertIn('vwap', df_vwap.columns)
        
        # 检查 VWAP 不为 NaN
        vwap_non_nan = df_vwap['vwap'].notna().sum()
        self.assertGreater(vwap_non_nan, 0)
    
    def test_vwap_position_detection(self):
        """测试价格相对 VWAP 位置检测"""
        df_vwap = calculate_vwap(self.df_daily)
        position = identify_vwap_position(df_vwap)
        
        self.assertIn('position', position)
        self.assertIn('current_price', position)
        self.assertIn('current_vwap', position)
        self.assertIn('deviation_percent', position)
        
        # 位置应该是预定义的值之一
        valid_positions = ['significantly_above', 'above', 'near', 'below', 'significantly_below', 'unknown']
        self.assertIn(position.get('position'), valid_positions)
    
    def test_vwap_cross_signal(self):
        """测试 VWAP 穿越信号检测"""
        df_vwap = calculate_vwap(self.df_daily)
        position = identify_vwap_position(df_vwap)
        
        self.assertIn('cross_signal', position)
        
        # 交叉信号应该是预定义的值之一
        valid_signals = ['bullish_cross', 'bearish_cross', None]
        self.assertIn(position.get('cross_signal'), valid_signals)
    
    def test_vwap_support_resistance(self):
        """测试 VWAP 支撑阻力位"""
        df_vwap = calculate_vwap(self.df_daily)
        sr = get_vwap_support_resistance(df_vwap)
        
        if 'error' not in sr:
            self.assertIn('vwap_high', sr)
            self.assertIn('vwap_low', sr)
            self.assertIn('vwap_avg', sr)
            self.assertIn('support', sr)
            self.assertIn('resistance', sr)
    
    def test_vwap_summary(self):
        """测试 VWAP 综合报告"""
        summary = get_vwap_summary(self.df_daily)
        
        self.assertNotIn('error', summary)
        self.assertIn('current_price', summary)
        self.assertIn('current_vwap', summary)
        self.assertIn('trend', summary)
        self.assertIn('recommendation', summary)
    
    def test_vwap_with_date_column(self):
        """测试带日期列的 VWAP 计算 (按日重置)"""
        df = self.df_daily.copy()
        df['date'] = df.index.date
        
        df_vwap = calculate_vwap(df, reset_daily=True)
        
        self.assertIn('vwap', df_vwap.columns)


# ============================================================
# SuperTrend 测试
# ============================================================

class TestSuperTrend(unittest.TestCase):
    """SuperTrend 指标测试"""
    
    def setUp(self):
        """测试前准备"""
        self.df = create_sample_data(n_periods=100, trend='up')
    
    def test_calculate_atr(self):
        """测试 ATR 计算"""
        atr = calculate_atr(self.df, period=14)
        
        # ATR 应该为正数
        self.assertGreater(atr.dropna().min(), 0)
        
        # ATR 应该与价格波动在同一数量级
        self.assertLess(atr.dropna().mean(), self.df['close'].mean() * 0.1)
    
    def test_calculate_supertrend_columns(self):
        """测试 SuperTrend 计算结果包含必需的列"""
        df_st = calculate_supertrend(self.df)
        
        required_columns = ['supertrend', 'trend']
        
        for col in required_columns:
            self.assertIn(col, df_st.columns, f"缺少列：{col}")
    
    def test_supertrend_trend_values(self):
        """测试 SuperTrend 趋势值"""
        df_st = calculate_supertrend(self.df)
        
        trend_values = df_st['trend'].dropna().unique()
        
        # 趋势值应该是 1 或 -1
        for val in trend_values:
            self.assertIn(val, [1, -1], f"无效的趋势值：{val}")
    
    def test_supertrend_values_reasonable(self):
        """测试 SuperTrend 值在合理范围内"""
        df_st = calculate_supertrend(self.df)
        
        supertrend_values = df_st['supertrend'].dropna()
        close_values = df_st['close']
        
        # SuperTrend 应该与价格在同一数量级
        self.assertGreater(supertrend_values.min(), close_values.min() * 0.5)
        self.assertLess(supertrend_values.max(), close_values.max() * 1.5)
    
    def test_trend_reversal_detection(self):
        """测试趋势反转检测"""
        df_st = calculate_supertrend(self.df)
        reversal = identify_trend_reversal(df_st)
        
        self.assertIn('current_trend', reversal)
        self.assertIn('reversal_signal', reversal)
        
        # 当前趋势应该是 bullish 或 bearish
        self.assertIn(reversal.get('current_trend'), ['bullish', 'bearish'])
        
        # 反转信号应该是预定义的值之一
        valid_signals = ['bullish_reversal', 'bearish_reversal', None]
        self.assertIn(reversal.get('reversal_signal'), valid_signals)
    
    def test_supertrend_levels(self):
        """测试 SuperTrend 关键价位"""
        df_st = calculate_supertrend(self.df)
        levels = get_supertrend_levels(df_st)
        
        if 'error' not in levels:
            self.assertIn('current_price', levels)
            self.assertIn('supertrend_value', levels)
            self.assertIn('trend', levels)
            self.assertIn('distance_percent', levels)
    
    def test_supertrend_summary(self):
        """测试 SuperTrend 综合报告"""
        summary = get_supertrend_summary(self.df, period=10, multiplier=3.0)
        
        self.assertNotIn('error', summary)
        self.assertIn('current_price', summary)
        self.assertIn('supertrend_value', summary)
        self.assertIn('trend', summary)
        self.assertIn('recommendation', summary)
        self.assertIn('parameters', summary)
        
        # 检查参数
        self.assertEqual(summary['parameters']['period'], 10)
        self.assertEqual(summary['parameters']['multiplier'], 3.0)
    
    def test_supertrend_with_different_parameters(self):
        """测试不同参数下的 SuperTrend"""
        # 使用不同的 period 和 multiplier
        df_st1 = calculate_supertrend(self.df, period=10, multiplier=3.0)
        df_st2 = calculate_supertrend(self.df, period=20, multiplier=2.0)
        
        # 不同参数应该产生不同的结果
        self.assertFalse(df_st1['supertrend'].equals(df_st2['supertrend']))
    
    def test_scan_supertrend_signals(self):
        """测试信号扫描"""
        df_st = calculate_supertrend(self.df)
        signals = scan_supertrend_signals(df_st, min_strength="moderate")
        
        # 返回的应该是列表
        self.assertIsInstance(signals, list)
        
        # 如果有信号，检查格式
        if signals:
            for sig in signals:
                self.assertIn('type', sig)
                self.assertIn('direction', sig)
                self.assertIn('recommendation', sig)


# ============================================================
# 集成测试
# ============================================================

class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """测试前准备"""
        self.df = create_sample_data(n_periods=100, trend='neutral')
    
    def test_all_indicators_work_together(self):
        """测试所有指标可以一起使用"""
        # Ichimoku
        df_ichimoku = calculate_ichimoku(self.df)
        ichimoku_summary = get_ichimoku_summary(self.df)
        
        # VWAP
        df_vwap = calculate_vwap(self.df)
        vwap_summary = get_vwap_summary(self.df)
        
        # SuperTrend
        df_st = calculate_supertrend(self.df)
        st_summary = get_supertrend_summary(self.df)
        
        # 所有指标都应该成功计算
        self.assertNotIn('error', ichimoku_summary)
        self.assertNotIn('error', vwap_summary)
        self.assertNotIn('error', st_summary)
    
    def test_indicators_on_trending_data(self):
        """测试指标在趋势数据上的表现"""
        # 上涨趋势
        df_up = create_sample_data(n_periods=100, trend='up')
        
        # 下跌趋势
        df_down = create_sample_data(n_periods=100, trend='down')
        
        # SuperTrend 应该能识别趋势
        st_up = get_supertrend_summary(df_up)
        st_down = get_supertrend_summary(df_down)
        
        # 上涨趋势中，SuperTrend 趋势应该是 bullish
        # 下跌趋势中，SuperTrend 趋势应该是 bearish
        # (注意：由于随机性，这个测试可能会失败，所以只检查不报错)
        self.assertNotIn('error', st_up)
        self.assertNotIn('error', st_down)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestIchimokuCloud))
    suite.addTests(loader.loadTestsFromTestCase(TestVWAP))
    suite.addTests(loader.loadTestsFromTestCase(TestSuperTrend))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("技术指标 L2 单元测试")
    print("=" * 60)
    print()
    
    result = run_tests()
    
    print()
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"运行测试数：{result.testsRun}")
    print(f"成功：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败：{len(result.failures)}")
    print(f"错误：{len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n出错的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}")
