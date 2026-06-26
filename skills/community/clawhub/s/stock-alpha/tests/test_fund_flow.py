"""
FundFlowCollector 单元测试
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import pandas as pd
import numpy as np


class TestFundFlowEstimation:
    """价量估算资金流测试"""

    @pytest.fixture
    def mock_price_df(self):
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
                "open": close * (1 + np.random.randn() * 0.01),
                "close": close,
                "high": close * (1 + abs(np.random.randn() * 0.01)),
                "low": close * (1 - abs(np.random.randn() * 0.01)),
                "volume": int(np.random.randint(1e6, 1e8)),
            })
            base = close
        return pd.DataFrame(records)

    def test_estimate_returns_required_columns(self, mock_price_df):
        from src.collectors.fund_flow_collector import FundFlowCollector
        fc = FundFlowCollector()
        result = fc._estimate_from_price("600036", mock_price_df)
        for col in ["stock_code", "trade_date", "net_inflow_main", "amount", "net_inflow_rate"]:
            assert col in result.columns, f"Missing column: {col}"

    def test_estimate_output_count(self, mock_price_df):
        from src.collectors.fund_flow_collector import FundFlowCollector
        fc = FundFlowCollector()
        result = fc._estimate_from_price("600036", mock_price_df)
        assert len(result) == len(mock_price_df)

    def test_estimate_net_inflow_bounds(self, mock_price_df):
        """net_inflow_main 应在合理范围内（不爆炸）"""
        from src.collectors.fund_flow_collector import FundFlowCollector
        fc = FundFlowCollector()
        result = fc._estimate_from_price("600036", mock_price_df)
        vals = result["net_inflow_main"].abs()
        assert vals.max() < 1e11, f"Value too large: {vals.max()}"

    def test_estimate_rate_bounds(self, mock_price_df):
        """net_inflow_rate 应在 [-0.3, 0.3] 范围内"""
        from src.collectors.fund_flow_collector import FundFlowCollector
        fc = FundFlowCollector()
        result = fc._estimate_from_price("600036", mock_price_df)
        rate = result["net_inflow_rate"]
        assert rate.min() >= -0.3, f"Rate too low: {rate.min()}"
        assert rate.max() <= 0.3, f"Rate too high: {rate.max()}"

    def test_batch_with_price_df(self, mock_price_df):
        """batch_fund_flow 应能处理多只股票"""
        from src.collectors.fund_flow_collector import FundFlowCollector

        df1 = mock_price_df.copy()
        df2 = mock_price_df.copy()
        df2["stock_code"] = "000001"
        # Shift prices for stock 2
        df2["close"] = df2["close"] * 1.1

        combined = pd.concat([df1, df2], ignore_index=True)
        fc = FundFlowCollector()
        result = fc.batch_fund_flow(["600036", "000001"], price_df=combined)
        assert len(result["stock_code"].unique()) == 2
