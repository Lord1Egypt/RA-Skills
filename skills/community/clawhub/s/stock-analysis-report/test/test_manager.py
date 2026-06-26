from __future__ import annotations

import asyncio
from typing import Optional
from unittest.mock import AsyncMock

import pandas as pd
import pytest

from src.data.manager import DataProviderManager
from src.data.provider import MarketDataProvider
from src.models import (
    CapitalFlow,
    ChipDistribution,
    FinancialData,
    IndexData,
    MarketOverview,
    MarketStatistics,
    RealtimeQuote,
    SectorData,
    StockInfo,
    Valuation,
)


class _StubProvider(MarketDataProvider):
    """Minimal stub that raises NotImplementedError for every abstract method"""

    async def get_stock_info(self, code: str) -> StockInfo:
        raise NotImplementedError

    async def get_daily_data(self, code: str, days: int = 120) -> pd.DataFrame:
        raise NotImplementedError

    async def get_realtime_quote(self, code: str) -> RealtimeQuote:
        raise NotImplementedError

    async def get_chip_distribution(self, code: str) -> Optional[ChipDistribution]:
        raise NotImplementedError

    async def get_market_overview(self) -> MarketOverview:
        raise NotImplementedError

    async def get_sector_rankings(self) -> tuple[list[SectorData], list[SectorData]]:
        raise NotImplementedError

    async def get_market_statistics(self) -> MarketStatistics:
        raise NotImplementedError

    async def get_indices(self) -> list[IndexData]:
        raise NotImplementedError


def _make_provider(**overrides) -> AsyncMock:
    provider = AsyncMock(spec=_StubProvider)
    for method_name in (
        "get_stock_info", "get_daily_data", "get_realtime_quote",
        "get_chip_distribution", "get_market_overview",
        "get_sector_rankings", "get_market_statistics", "get_indices",
        "get_capital_flow", "get_valuation", "get_financial_data",
        "normalize_code",
    ):
        if method_name not in overrides:
            setattr(provider, method_name, AsyncMock(side_effect=NotImplementedError))
    for name, value in overrides.items():
        setattr(provider, name, value)
    provider.normalize_code = lambda code: code
    return provider


class TestRaceProvidersSignatureFix:
    """Verify _race_providers correctly handles methods with and without code parameter"""

    def test_get_indices_no_code_parameter(self):
        provider = _make_provider(
            get_indices=AsyncMock(return_value=[
                IndexData(name="上证指数", code="000001", close=3200.0, change_pct=0.5),
            ]),
        )
        manager = DataProviderManager([provider])

        result = asyncio.run(manager.get_indices())
        assert len(result) == 1
        assert result[0].name == "上证指数"
        assert result[0].close == 3200.0
        provider.get_indices.assert_awaited_once_with()

    def test_get_sector_rankings_no_code_parameter(self):
        top = [SectorData(name="半导体", change_pct=3.2)]
        bottom = [SectorData(name="房地产", change_pct=-1.5)]
        provider = _make_provider(
            get_sector_rankings=AsyncMock(return_value=(top, bottom)),
        )
        manager = DataProviderManager([provider])

        result_top, result_bottom = asyncio.run(manager.get_sector_rankings())
        assert len(result_top) == 1
        assert result_top[0].name == "半导体"
        assert len(result_bottom) == 1
        assert result_bottom[0].name == "房地产"
        provider.get_sector_rankings.assert_awaited_once_with()

    def test_get_market_statistics_no_code_parameter(self):
        provider = _make_provider(
            get_market_statistics=AsyncMock(return_value=MarketStatistics(
                up_count=3000, down_count=1500, flat_count=200,
                limit_up_count=50, limit_down_count=10,
            )),
        )
        manager = DataProviderManager([provider])

        result = asyncio.run(manager.get_market_statistics())
        assert result.up_count == 3000
        assert result.down_count == 1500
        assert result.limit_up_count == 50
        provider.get_market_statistics.assert_awaited_once_with()

    def test_get_stock_info_with_code_parameter(self):
        provider = _make_provider(
            get_stock_info=AsyncMock(return_value=StockInfo(
                code="600519", name="贵州茅台", industry="白酒",
            )),
        )
        manager = DataProviderManager([provider])

        result = asyncio.run(manager.get_stock_info("600519"))
        assert result.name == "贵州茅台"
        assert result.code == "600519"
        provider.get_stock_info.assert_awaited_once_with("600519")

    def test_get_realtime_quote_with_code_parameter(self):
        provider = _make_provider(
            get_realtime_quote=AsyncMock(return_value=RealtimeQuote(
                price=1800.0, change_pct=1.5,
            )),
        )
        manager = DataProviderManager([provider])

        result = asyncio.run(manager.get_realtime_quote("600519"))
        assert result.price == 1800.0
        assert result.change_pct == 1.5
        provider.get_realtime_quote.assert_awaited_once_with("600519")

    def test_get_capital_flow_with_code_parameter(self):
        provider = _make_provider(
            get_capital_flow=AsyncMock(return_value=CapitalFlow(
                super_large_net=5e8, ddx=0.26,
            )),
        )
        manager = DataProviderManager([provider])

        result = asyncio.run(manager.get_capital_flow("600519"))
        assert result is not None
        assert result.super_large_net == 5e8
        provider.get_capital_flow.assert_awaited_once_with("600519")

    def test_get_valuation_with_code_parameter(self):
        provider = _make_provider(
            get_valuation=AsyncMock(return_value=Valuation(
                pe_ttm=28.5, pb=8.2,
            )),
        )
        manager = DataProviderManager([provider])

        result = asyncio.run(manager.get_valuation("600519"))
        assert result is not None
        assert result.pe_ttm == 28.5
        provider.get_valuation.assert_awaited_once_with("600519")

    def test_get_financial_data_with_code_parameter(self):
        provider = _make_provider(
            get_financial_data=AsyncMock(return_value=FinancialData(
                net_profit=5.5e10, roe=30.5,
            )),
        )
        manager = DataProviderManager([provider])

        result = asyncio.run(manager.get_financial_data("600519"))
        assert result is not None
        assert result.roe == 30.5
        provider.get_financial_data.assert_awaited_once_with("600519")


class TestRaceProvidersFallback:
    """Verify _race_providers falls through to next provider on failure"""

    def test_first_provider_fails_second_succeeds(self):
        failing = _make_provider(
            get_indices=AsyncMock(side_effect=ConnectionError("timeout")),
        )
        succeeding = _make_provider(
            get_indices=AsyncMock(return_value=[
                IndexData(name="上证指数", code="000001", close=3200.0),
            ]),
        )
        manager = DataProviderManager([failing, succeeding])

        result = asyncio.run(manager.get_indices())
        assert len(result) == 1
        assert result[0].name == "上证指数"

    def test_all_providers_fail_returns_none_for_indices(self):
        failing1 = _make_provider(
            get_indices=AsyncMock(side_effect=ConnectionError("fail")),
        )
        failing2 = _make_provider(
            get_indices=AsyncMock(side_effect=RuntimeError("error")),
        )
        manager = DataProviderManager([failing1, failing2])

        result = asyncio.run(manager.get_indices())
        assert result == []

    def test_all_providers_fail_returns_empty_for_sector_rankings(self):
        failing = _make_provider(
            get_sector_rankings=AsyncMock(side_effect=Exception("fail")),
        )
        manager = DataProviderManager([failing])

        top, bottom = asyncio.run(manager.get_sector_rankings())
        assert top == []
        assert bottom == []

    def test_all_providers_fail_returns_default_for_market_statistics(self):
        failing = _make_provider(
            get_market_statistics=AsyncMock(side_effect=Exception("fail")),
        )
        manager = DataProviderManager([failing])

        result = asyncio.run(manager.get_market_statistics())
        assert result.up_count == 0
        assert result.down_count == 0

    def test_first_provider_raises_second_returns_data(self):
        provider1 = _make_provider(
            get_chip_distribution=AsyncMock(side_effect=RuntimeError("unsupported")),
        )
        provider2 = _make_provider(
            get_chip_distribution=AsyncMock(return_value=ChipDistribution(
                profit_ratio=75.0, avg_cost=1720.0,
            )),
        )
        manager = DataProviderManager([provider1, provider2])

        result = asyncio.run(manager.get_chip_distribution("600519"))
        assert result is not None
        assert result.profit_ratio == 75.0


class TestRaceProvidersPriority:
    """Verify _race_providers returns the first successful result (priority order)"""

    def test_first_provider_wins(self):
        provider1 = _make_provider(
            get_indices=AsyncMock(return_value=[
                IndexData(name="上证指数", code="000001", close=3200.0),
            ]),
        )
        provider2 = _make_provider(
            get_indices=AsyncMock(return_value=[
                IndexData(name="上证指数", code="000001", close=3300.0),
            ]),
        )
        manager = DataProviderManager([provider1, provider2])

        result = asyncio.run(manager.get_indices())
        assert result[0].close == 3200.0


class TestGetStockInfoFallback:
    """Verify get_stock_info returns StockInfo(code=code, name=code) on total failure"""

    def test_all_providers_fail_returns_fallback(self):
        failing = _make_provider(
            get_stock_info=AsyncMock(side_effect=Exception("fail")),
        )
        manager = DataProviderManager([failing])

        result = asyncio.run(manager.get_stock_info("600519"))
        assert result.code == "600519"
        assert result.name == "600519"


class TestGetRealtimeQuoteFallback:
    """Verify get_realtime_quote returns empty RealtimeQuote on failure"""

    def test_all_providers_fail_returns_empty(self):
        failing = _make_provider(
            get_realtime_quote=AsyncMock(side_effect=Exception("fail")),
        )
        manager = DataProviderManager([failing])

        result = asyncio.run(manager.get_realtime_quote("600519"))
        assert result.price == 0.0

    def test_price_zero_treated_as_failure(self):
        provider = _make_provider(
            get_realtime_quote=AsyncMock(return_value=RealtimeQuote(price=0.0)),
        )
        manager = DataProviderManager([provider])

        result = asyncio.run(manager.get_realtime_quote("600519"))
        assert result.price == 0.0


class TestGetDailyDataBestResult:
    """Verify get_daily_data picks the result with the most rows"""

    def test_selects_longest_dataframe(self):
        df_short = pd.DataFrame({"close": [10.0, 11.0, 12.0]})
        df_long = pd.DataFrame({"close": range(20)})

        provider1 = _make_provider(
            get_daily_data=AsyncMock(return_value=df_short),
        )
        provider2 = _make_provider(
            get_daily_data=AsyncMock(return_value=df_long),
        )
        manager = DataProviderManager([provider1, provider2])

        result = asyncio.run(manager.get_daily_data("600519"))
        assert len(result) == 20

    def test_all_providers_fail_returns_empty_df(self):
        failing = _make_provider(
            get_daily_data=AsyncMock(side_effect=Exception("fail")),
        )
        manager = DataProviderManager([failing])

        result = asyncio.run(manager.get_daily_data("600519"))
        assert result.empty


class TestGetMarketOverview:
    """Verify get_market_overview aggregates results from sub-methods"""

    def test_aggregates_parallel_results(self):
        provider = _make_provider(
            get_indices=AsyncMock(return_value=[
                IndexData(name="上证指数", code="000001", close=3200.0),
            ]),
            get_market_statistics=AsyncMock(return_value=MarketStatistics(
                up_count=3000, down_count=1500,
            )),
            get_sector_rankings=AsyncMock(return_value=(
                [SectorData(name="半导体", change_pct=3.2)],
                [SectorData(name="房地产", change_pct=-1.5)],
            )),
        )
        manager = DataProviderManager([provider])

        result = asyncio.run(manager.get_market_overview())
        assert len(result.indices) == 1
        assert result.statistics.up_count == 3000
        assert len(result.top_sectors) == 1
        assert len(result.bottom_sectors) == 1
