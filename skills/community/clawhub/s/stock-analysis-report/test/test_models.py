from __future__ import annotations

import pytest

from src.models import (
    CapitalFlow,
    CheckItem,
    ChipDistribution,
    FinancialData,
    IndexData,
    MarketAnalysisResult,
    MarketStatistics,
    NewsItem,
    RealtimeQuote,
    SectorData,
    StockAnalysisResult,
    StockInfo,
    TechnicalIndicators,
    Valuation,
)


class TestStockInfo:
    def test_defaults(self):
        info = StockInfo(code="600519", name="贵州茅台")
        assert info.code == "600519"
        assert info.name == "贵州茅台"
        assert info.industry == ""
        assert info.market_cap == 0.0

    def test_full_init(self):
        info = StockInfo(code="000001", name="平安银行", industry="银行", market_cap=1e12)
        assert info.industry == "银行"
        assert info.market_cap == 1e12


class TestRealtimeQuote:
    def test_defaults(self):
        q = RealtimeQuote()
        assert q.price == 0.0
        assert q.change_pct == 0.0
        assert q.turnover_rate == 0.0


class TestTechnicalIndicators:
    def test_bullish_alignment_default(self):
        tech = TechnicalIndicators()
        assert tech.is_bullish_alignment is False


class TestChipDistribution:
    def test_defaults(self):
        chip = ChipDistribution()
        assert chip.profit_ratio == 0.0
        assert chip.avg_cost == 0.0


class TestCapitalFlow:
    def test_defaults(self):
        cf = CapitalFlow()
        assert cf.super_large_net == 0.0
        assert cf.ddx == 0.0


class TestStockAnalysisResult:
    def test_defaults(self):
        result = StockAnalysisResult()
        assert result.stock_code == ""
        assert result.score == 0
        assert result.checklist == []
        assert result.risk_alerts == []
        assert result.disclaimer != ""

    def test_with_data(self):
        result = StockAnalysisResult(
            stock_code="600519",
            stock_name="贵州茅台",
            score=75,
            action="买入",
            trend="看多",
        )
        assert result.stock_code == "600519"
        assert result.score == 75
        assert result.action == "买入"


class TestMarketAnalysisResult:
    def test_defaults(self):
        result = MarketAnalysisResult()
        assert result.date == ""
        assert result.indices == []
        assert result.sentiment == ""
        assert result.disclaimer != ""


class TestMarketStatistics:
    def test_defaults(self):
        stats = MarketStatistics()
        assert stats.up_count == 0
        assert stats.down_count == 0
        assert stats.limit_up_count == 0


class TestCheckItem:
    def test_init(self):
        item = CheckItem(condition="MA5 > MA10", status="✅", detail="均线多头")
        assert item.condition == "MA5 > MA10"
        assert item.status == "✅"


class TestNewsItem:
    def test_init(self):
        item = NewsItem(title="利好消息", snippet="摘要", date="2025-01-15")
        assert item.title == "利好消息"
        assert item.info_type == ""
