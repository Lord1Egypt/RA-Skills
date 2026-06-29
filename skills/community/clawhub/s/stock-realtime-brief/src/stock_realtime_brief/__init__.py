"""A 股投研体系 v5.0 - 散户级 Bloomberg"""
__version__ = "5.0.0"
__author__ = "Stock Realtime Brief Contributors"

# v4.x 核心
from . import (
    data_sources,
    indicators,
    analyzers,
    portfolio,
    renderers,
    realtime_analyzer,
    multi_timeframe,
    market_phase,
    main_line_tracker,
    end_wave_detector,
    multi_dim_analysis,
    shake_vs_break,
    business_quality,
    research_reports,
    announcements,
    smart_picker,
    price_watcher,
    disciplines,
    run_brief,
)

# v5.0 新增 7 大工具
from . import (
    dcf_calculator,
    sector_rotation,
    sell_signal,
    polaris_monitor,
    realtime_alerts,
    financial_parser,
    backtest_engine,
)

__all__ = [
    # v4.x
    'data_sources', 'indicators', 'analyzers', 'portfolio', 'renderers',
    'realtime_analyzer', 'multi_timeframe', 'market_phase', 'main_line_tracker',
    'end_wave_detector', 'multi_dim_analysis', 'shake_vs_break',
    'business_quality', 'research_reports', 'announcements',
    'smart_picker', 'price_watcher', 'disciplines', 'run_brief',
    # v5.0 新增
    'dcf_calculator', 'sector_rotation', 'sell_signal', 'polaris_monitor',
    'realtime_alerts', 'financial_parser', 'backtest_engine',
]
