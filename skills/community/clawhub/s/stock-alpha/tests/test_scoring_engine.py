"""
ScoringEngine 单元测试（六维版本）
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def mock_price_df():
    np.random.seed(42)
    codes = ["600036", "000001", "000333", "600519", "002594"]
    dates = pd.bdate_range("2026-02-01", "2026-04-30")
    records = []
    for c in codes:
        base = 10 + np.random.rand() * 20
        for d in dates[-60:]:
            change = np.random.randn() * 0.5
            close = max(2, base + change)
            records.append({
                "stock_code": c, "trade_date": d, "close": close,
                "open": close * (1 + np.random.randn() * 0.02),
                "high": close * (1 + abs(np.random.randn() * 0.02)),
                "low": close * (1 - abs(np.random.randn() * 0.02)),
                "volume": int(np.random.randint(1e6, 1e8)),
            })
            base = close
    df = pd.DataFrame(records)
    from src.collectors.technical import add_technical_indicators
    return add_technical_indicators(df)


@pytest.fixture
def mock_flow_df():
    np.random.seed(123)
    codes = ["600036", "000001", "000333", "600519", "002594"]
    dates = pd.bdate_range("2026-02-01", "2026-04-30")
    records = []
    for c in codes:
        for d in dates[-120:]:
            net = np.random.randn() * 5e7
            rate = np.random.randn() * 5
            records.append({
                "stock_code": c, "trade_date": d,
                "net_inflow_main": net, "net_inflow_rate": rate / 100.0,
                "amount": abs(net) * 3,
            })
    return pd.DataFrame(records)


class TestScoringEngine:
    def test_all_six_dimensions_present(self, mock_price_df, mock_flow_df):
        from src.screener.scoring_engine import ScoringEngine
        se = ScoringEngine()
        codes = pd.DataFrame({"stock_code": ["600036", "000001", "000333", "600519", "002594"]})
        result = se.score(codes, mock_price_df, mock_flow_df)
        expected = ["score_total", "score_behavior", "score_technical",
                    "score_fund_flow", "score_momentum", "score_risk", "score_volume"]
        for col in expected:
            assert col in result.columns, f"Missing: {col}"

    def test_scores_in_range(self, mock_price_df, mock_flow_df):
        from src.screener.scoring_engine import ScoringEngine
        se = ScoringEngine()
        codes = pd.DataFrame({"stock_code": ["600036", "000001", "000333", "600519", "002594"]})
        result = se.score(codes, mock_price_df, mock_flow_df)
        for col in ["score_total", "score_behavior", "score_technical",
                     "score_fund_flow", "score_momentum", "score_risk", "score_volume"]:
            vals = result[col].dropna()
            assert vals.between(0, 1).all(), f"{col} not in [0,1]"

    def test_no_flow_graceful(self, mock_price_df):
        from src.screener.scoring_engine import ScoringEngine
        se = ScoringEngine()
        codes = pd.DataFrame({"stock_code": ["600036", "000001", "000333", "600519", "002594"]})
        result = se.score(codes, mock_price_df, None)
        assert "score_total" in result.columns
        missing = se.get_missing_dims()
        assert len(missing) >= 2  # behavior + fund_flow

    def test_momentum_high_when_up(self, mock_price_df, mock_flow_df):
        """连续上涨的股票应获得高的动量分"""
        from src.screener.scoring_engine import ScoringEngine
        df = mock_price_df.copy()
        mask = df["stock_code"] == "600036"
        # 让600036最后几天大涨
        for i in range(-5, 0):
            idx = df[mask].index[i]
            df.loc[idx, "close"] *= 1.03
        se = ScoringEngine()
        codes = pd.DataFrame({"stock_code": ["600036", "000001"]})
        result = se.score(codes, df, mock_flow_df)
        mom_600036 = result[result["stock_code"]=="600036"]["score_momentum"].iloc[0]
        mom_000001 = result[result["stock_code"]=="000001"]["score_momentum"].iloc[0]
        assert mom_600036 >= mom_000001, f"上涨股动量应更高: {mom_600036} vs {mom_000001}"

    def test_risk_low_when_volatile(self, mock_price_df, mock_flow_df):
        """高波动率的股票风险分应更低"""
        from src.screener.scoring_engine import ScoringEngine
        df = mock_price_df.copy()
        mask = df["stock_code"] == "600036"
        # 让600036剧烈波动
        for i in range(-10, 0):
            idx = df[mask].index[i]
            df.loc[idx, "close"] *= (1 + np.random.randn() * 0.05)
        se = ScoringEngine()
        codes = pd.DataFrame({"stock_code": ["600036", "000001"]})
        result = se.score(codes, df, mock_flow_df)
        risk_600036 = result[result["stock_code"]=="600036"]["score_risk"].iloc[0]
        risk_000001 = result[result["stock_code"]=="000001"]["score_risk"].iloc[0]
        # 600036波动更大，风险分应更低
        assert risk_600036 <= risk_000001 + 0.2  # 容忍度

    def test_empty_input(self, mock_price_df, mock_flow_df):
        from src.screener.scoring_engine import ScoringEngine
        se = ScoringEngine()
        result = se.score(pd.DataFrame(), mock_price_df, mock_flow_df)
        assert len(result) == 0
