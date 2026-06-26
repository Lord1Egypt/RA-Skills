from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StockInfo:
    """股票基本信息"""
    code: str
    name: str
    industry: str = ""
    market_cap: float = 0.0
    list_date: str = ""


@dataclass
class RealtimeQuote:
    """实时行情"""
    price: float = 0.0
    change_pct: float = 0.0
    change_amt: float = 0.0
    volume: float = 0.0
    turnover: float = 0.0
    high: float = 0.0
    low: float = 0.0
    open: float = 0.0
    prev_close: float = 0.0
    amplitude: float = 0.0
    turnover_rate: float = 0.0


@dataclass
class TechnicalIndicators:
    """技术指标"""
    ma5: float = 0.0
    ma10: float = 0.0
    ma20: float = 0.0
    ma60: float = 0.0
    is_bullish_alignment: bool = False
    bias: float = 0.0
    volume_ratio: float = 0.0
    recent_trend: str = ""


@dataclass
class ChipDistribution:
    """筹码分布"""
    profit_ratio: float = 0.0
    avg_cost: float = 0.0
    concentration: float = 0.0
    profit_90_cost: float = 0.0
    profit_10_cost: float = 0.0


@dataclass
class CapitalFlow:
    """主力资金流向"""
    super_large_net: float = 0.0
    large_net: float = 0.0
    medium_net: float = 0.0
    small_net: float = 0.0
    super_large_in: float = 0.0
    super_large_out: float = 0.0
    large_in: float = 0.0
    large_out: float = 0.0
    ddx: float = 0.0
    ddy: float = 0.0
    ddz: float = 0.0


@dataclass
class Valuation:
    """估值数据"""
    pe_ttm: float = 0.0
    pb: float = 0.0
    pe_percentile: float = 0.0
    pb_percentile: float = 0.0


@dataclass
class FinancialData:
    """核心财务指标"""
    net_profit: float = 0.0
    revenue: float = 0.0
    net_profit_yoy: float = 0.0
    revenue_yoy: float = 0.0
    roe: float = 0.0
    gross_margin: float = 0.0
    debt_ratio: float = 0.0
    forecast_profit: float = 0.0
    forecast_growth: float = 0.0
    institution_holding_pct: float = 0.0


@dataclass
class NewsItem:
    """新闻条目"""
    title: str = ""
    snippet: str = ""
    date: str = ""
    source: str = ""
    url: str = ""
    info_type: str = ""
    content: str = ""


@dataclass
class CheckItem:
    """操作检查清单项"""
    condition: str = ""
    status: str = ""
    detail: str = ""


@dataclass
class StockAnalysisResult:
    """个股分析结果"""
    stock_code: str = ""
    stock_name: str = ""
    core_conclusion: str = ""
    score: int = 0
    action: str = ""
    trend: str = ""
    buy_price: Optional[float] = None
    stop_loss_price: Optional[float] = None
    target_price: Optional[float] = None
    checklist: list[CheckItem] = field(default_factory=list)
    risk_alerts: list[str] = field(default_factory=list)
    positive_catalysts: list[str] = field(default_factory=list)
    strategy: str = ""
    raw_report: str = ""
    disclaimer: str = "仅供参考，不构成投资建议。股市有风险，投资需谨慎。"
    stock_info: Optional[StockInfo] = None
    realtime: Optional[RealtimeQuote] = None
    tech: Optional[TechnicalIndicators] = None
    chip: Optional[ChipDistribution] = None
    capital_flow: Optional[CapitalFlow] = None
    valuation: Optional[Valuation] = None
    financial: Optional[FinancialData] = None
    news: list[NewsItem] = field(default_factory=list)


@dataclass
class IndexData:
    """指数数据"""
    name: str = ""
    code: str = ""
    close: float = 0.0
    change_pct: float = 0.0
    change_amt: float = 0.0


@dataclass
class MarketStatistics:
    """市场统计"""
    up_count: int = 0
    down_count: int = 0
    flat_count: int = 0
    limit_up_count: int = 0
    limit_down_count: int = 0


@dataclass
class SectorData:
    """板块数据"""
    name: str = ""
    change_pct: float = 0.0
    lead_stock: str = ""


@dataclass
class MarketOverview:
    """市场概览"""
    indices: list[IndexData] = field(default_factory=list)
    statistics: MarketStatistics = field(default_factory=MarketStatistics)
    top_sectors: list[SectorData] = field(default_factory=list)
    bottom_sectors: list[SectorData] = field(default_factory=list)


@dataclass
class MarketAnalysisResult:
    """市场分析结果"""
    date: str = ""
    core_conclusion: str = ""
    indices: list[IndexData] = field(default_factory=list)
    statistics: MarketStatistics = field(default_factory=MarketStatistics)
    top_sectors: list[SectorData] = field(default_factory=list)
    bottom_sectors: list[SectorData] = field(default_factory=list)
    sentiment: str = ""
    strategy: str = ""
    raw_report: str = ""
    disclaimer: str = "仅供参考，不构成投资建议。股市有风险，投资需谨慎。"
