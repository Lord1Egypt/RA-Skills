"""
技术指标模块单元测试
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import pandas as pd
import numpy as np


class TestTechnicalIndicators:
    """技术指标计算测试"""

    @pytest.fixture
    def single_stock_df(self):
        """单只股票60日模拟行情"""
        np.random.seed(42)
        dates = pd.bdate_range("2026-02-01", "2026-04-30")
        base = 30.0
        records = []
        for d in dates[-60:]:
            change = np.random.randn() * 0.5
            close = max(10, base + change)
            records.append({
                "stock_code": "600036",
                "trade_date": d,
                "close": close,
                "open": close * (1 + np.random.randn() * 0.01),
                "high": close * (1 + abs(np.random.randn() * 0.01)),
                "low": close * (1 - abs(np.random.randn() * 0.01)),
                "volume": int(np.random.randint(1e6, 1e8)),
            })
            base = close
        return pd.DataFrame(records)

    def test_rsi_calculation(self, single_stock_df):
        """RSI应在[0,100]范围内"""
        from src.collectors.technical import add_technical_indicators

        result = add_technical_indicators(single_stock_df)
        assert "RSI_14" in result.columns
        rsi = result["RSI_14"].dropna()
        assert (rsi >= 0).all() and (rsi <= 100).all()

    def test_macd_columns(self, single_stock_df):
        """MACD应有DIF/DEA/柱三条线"""
        from src.collectors.technical import add_technical_indicators

        result = add_technical_indicators(single_stock_df)
        for col in ["MACD_DIF", "MACD_SIGNAL", "MACD"]:
            assert col in result.columns

    def test_ma_columns(self, single_stock_df):
        """均线应有5/20/60日"""
        from src.collectors.technical import add_technical_indicators

        result = add_technical_indicators(single_stock_df)
        for col in ["MA_5d", "MA_20d", "MA_60d", "MA_20d_DIFF"]:
            assert col in result.columns

    def test_output_row_count(self, single_stock_df):
        """输出行数应与输入一致"""
        from src.collectors.technical import add_technical_indicators

        result = add_technical_indicators(single_stock_df)
        assert len(result) == len(single_stock_df)

    def test_ma_20d_diff_range(self, single_stock_df):
        """MA_20d_DIFF应在合理范围"""
        from src.collectors.technical import add_technical_indicators

        result = add_technical_indicators(single_stock_df)
        diff = result["MA_20d_DIFF"].dropna()
        assert (diff.abs() < 1.0).all()
