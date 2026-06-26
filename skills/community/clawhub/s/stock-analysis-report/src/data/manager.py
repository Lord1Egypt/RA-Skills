from __future__ import annotations

import asyncio
import logging
import time
from typing import Optional

import pandas as pd

from src.data.provider import MarketDataProvider
from src.data.utils import calculate_chip_from_daily
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

logger = logging.getLogger(__name__)

_PROVIDER_TIMEOUT = 10.0


class DataProviderManager(MarketDataProvider):

    def __init__(self, providers: list[MarketDataProvider]):
        self.providers = providers
        provider_names = [p.__class__.__name__ for p in providers]
        logger.info("DataProviderManager 初始化: %s", " → ".join(provider_names))

    async def _race_providers(self, method_name: str, *args, **kwargs):
        tasks = []
        for provider in self.providers:
            method = getattr(provider, method_name)
            tasks.append(asyncio.wait_for(method(*args, **kwargs), timeout=_PROVIDER_TIMEOUT))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            provider_name = self.providers[i].__class__.__name__
            if isinstance(result, (asyncio.TimeoutError, asyncio.CancelledError)):
                logger.warning("[数据源] %s %s 超时(%.0fs)", provider_name, method_name, _PROVIDER_TIMEOUT)
                continue
            if isinstance(result, Exception):
                logger.warning("[数据源] %s %s 失败: %s", provider_name, method_name, result)
                continue
            logger.info("[数据源] %s %s 成功", provider_name, method_name)
            return result

        return None

    async def get_stock_info(self, code: str) -> StockInfo:
        code = self.normalize_code(code)
        start = time.monotonic()
        result = await self._race_providers("get_stock_info", code)
        if result and isinstance(result, StockInfo) and result.name and result.name != code:
            logger.debug("get_stock_info(%s) 完成 耗时%.2fs", code, time.monotonic() - start)
            return result
        logger.warning("get_stock_info(%s) 所有数据源均失败", code)
        return StockInfo(code=code, name=code)

    async def get_daily_data(self, code: str, days: int = 120) -> pd.DataFrame:
        code = self.normalize_code(code)
        start = time.monotonic()
        tasks = [
            asyncio.wait_for(provider.get_daily_data(code, days), timeout=_PROVIDER_TIMEOUT)
            for provider in self.providers
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        best_df = pd.DataFrame()
        best_len = 0
        for i, result in enumerate(results):
            provider_name = self.providers[i].__class__.__name__
            if isinstance(result, Exception):
                logger.warning("[数据源] %s get_daily_data 失败: %s", provider_name, result)
                continue
            if result is not None and not result.empty:
                result_len = len(result)
                logger.info("[数据源 %d/%d] %s 获取日K线: %d 条 (请求%d天)",
                            i + 1, len(self.providers), provider_name, result_len, days)
                if result_len > best_len:
                    best_df = result
                    best_len = result_len
            else:
                logger.warning("[数据源 %d/%d] %s 日K线数据为空",
                               i + 1, len(self.providers), provider_name)

        if not best_df.empty:
            logger.debug("get_daily_data(%s) 完成 耗时%.2fs (最佳:%d条)",
                         code, time.monotonic() - start, best_len)
        else:
            logger.warning("get_daily_data(%s) 所有数据源均失败", code)
        return best_df

    async def get_realtime_quote(self, code: str) -> RealtimeQuote:
        code = self.normalize_code(code)
        start = time.monotonic()
        result = await self._race_providers("get_realtime_quote", code)
        if result and isinstance(result, RealtimeQuote) and result.price > 0:
            logger.debug("get_realtime_quote(%s) 完成 耗时%.2fs", code, time.monotonic() - start)
            return result
        logger.warning("get_realtime_quote(%s) 所有数据源均失败", code)
        return RealtimeQuote()

    async def get_chip_distribution(self, code: str) -> Optional[ChipDistribution]:
        code = self.normalize_code(code)
        start = time.monotonic()
        result = await self._race_providers("get_chip_distribution", code)
        if result is not None:
            logger.debug("get_chip_distribution(%s) 完成 耗时%.2fs", code, time.monotonic() - start)
            return result

        logger.info("[筹码兜底] 所有数据源筹码接口未返回，尝试K线估算")
        try:
            df = await self.get_daily_data(code, 90)
        except Exception:
            logger.warning("[筹码兜底] K线数据获取失败，筹码分布不可用")
            return None
        result = calculate_chip_from_daily(df)
        if result:
            logger.info("[筹码兜底] K线估算筹码分布成功: 获利比例=%.1f%%, 平均成本=%.2f",
                        result.profit_ratio, result.avg_cost)
        else:
            logger.warning("[筹码兜底] K线估算筹码分布失败: 数据不足")
        logger.debug("get_chip_distribution(%s) 完成 耗时%.2fs", code, time.monotonic() - start)
        return result

    async def get_market_overview(self) -> MarketOverview:
        start = time.monotonic()
        logger.info("开始获取市场概览...")

        indices, statistics, sectors = await asyncio.gather(
            self.get_indices(),
            self.get_market_statistics(),
            self.get_sector_rankings(),
        )
        top_sectors, bottom_sectors = sectors if isinstance(sectors, tuple) else ([], [])

        overview = MarketOverview(
            indices=indices,
            statistics=statistics,
            top_sectors=top_sectors,
            bottom_sectors=bottom_sectors,
        )

        logger.info("市场概览获取完成: 指数%d个, 涨%d/跌%d/平%d, 领涨板块%d个, 领跌板块%d个, 耗时%.2fs",
                    len(indices), statistics.up_count, statistics.down_count,
                    statistics.flat_count, len(top_sectors), len(bottom_sectors),
                    time.monotonic() - start)
        return overview

    async def get_indices(self) -> list[IndexData]:
        result = await self._race_providers("get_indices")
        if result and isinstance(result, list):
            return result
        logger.warning("get_indices() 所有数据源均失败")
        return []

    async def get_sector_rankings(self) -> tuple[list[SectorData], list[SectorData]]:
        result = await self._race_providers("get_sector_rankings")
        if result and isinstance(result, tuple):
            return result
        logger.warning("get_sector_rankings() 所有数据源均失败")
        return [], []

    async def get_market_statistics(self) -> MarketStatistics:
        result = await self._race_providers("get_market_statistics")
        if result and isinstance(result, MarketStatistics) and (result.up_count > 0 or result.down_count > 0):
            return result
        logger.warning("get_market_statistics() 所有数据源均失败")
        return MarketStatistics()

    async def get_capital_flow(self, code: str) -> Optional[CapitalFlow]:
        code = self.normalize_code(code)
        result = await self._race_providers("get_capital_flow", code)
        if result is not None:
            return result
        logger.debug("get_capital_flow(%s) 所有数据源均不支持或失败", code)
        return None

    async def get_valuation(self, code: str) -> Optional[Valuation]:
        code = self.normalize_code(code)
        result = await self._race_providers("get_valuation", code)
        if result is not None:
            return result
        logger.debug("get_valuation(%s) 所有数据源均不支持或失败", code)
        return None

    async def get_financial_data(self, code: str) -> Optional[FinancialData]:
        code = self.normalize_code(code)
        result = await self._race_providers("get_financial_data", code)
        if result is not None:
            return result
        logger.debug("get_financial_data(%s) 所有数据源均不支持或失败", code)
        return None
