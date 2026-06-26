from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd

from src.models import (
    CapitalFlow,
    ChipDistribution,
    FinancialData,
    IndexData,
    MarketOverview,
    MarketStatistics,
    RealtimeQuote,
    StockInfo,
    Valuation,
)


class MarketDataProvider(ABC):
    """行情数据源抽象基类，预留其他数据源接入接口"""

    @abstractmethod
    async def get_stock_info(self, code: str) -> StockInfo:
        """获取股票基本信息"""

    @abstractmethod
    async def get_daily_data(self, code: str, days: int = 120) -> pd.DataFrame:
        """获取日K线数据，返回 DataFrame，列包含 open/high/low/close/volume/change_pct 等"""

    @abstractmethod
    async def get_realtime_quote(self, code: str) -> RealtimeQuote:
        """获取实时行情"""

    @abstractmethod
    async def get_chip_distribution(self, code: str) -> Optional[ChipDistribution]:
        """获取筹码分布，不支持时返回 None"""

    @abstractmethod
    async def get_market_overview(self) -> MarketOverview:
        """获取市场概览（主要指数 + 市场统计 + 板块涨跌）"""

    @abstractmethod
    async def get_sector_rankings(self) -> tuple[list, list]:
        """获取板块涨跌榜，返回 (领涨板块列表, 领跌板块列表)"""

    @abstractmethod
    async def get_market_statistics(self) -> MarketStatistics:
        """获取市场统计（涨跌家数、涨停跌停数）"""

    @abstractmethod
    async def get_indices(self) -> list[IndexData]:
        """获取主要指数数据"""

    async def get_capital_flow(self, code: str) -> Optional[CapitalFlow]:
        """获取主力资金流向，不支持时返回 None"""
        return None

    async def get_valuation(self, code: str) -> Optional[Valuation]:
        """获取估值数据（PE/PB等），不支持时返回 None"""
        return None

    async def get_financial_data(self, code: str) -> Optional[FinancialData]:
        """获取核心财务指标，不支持时返回 None"""
        return None

    def normalize_code(self, code: str) -> str:
        """标准化股票代码，去除可能的前缀后缀"""
        code = code.strip()
        for prefix in ("sh", "sz", "SH", "SZ", "SH.", "SZ."):
            if code.startswith(prefix):
                code = code[len(prefix):]
                break
        if "." in code:
            code = code.split(".")[0]
        return code
