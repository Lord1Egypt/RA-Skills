"""A 股投研体系 v5.1 - 散户级 Bloomberg + 深度智能"""
__version__ = "5.5.0"

# v4.x 核心
from . import (data_sources, indicators, analyzers, portfolio, renderers,
               realtime_analyzer, multi_timeframe, market_phase, main_line_tracker,
               end_wave_detector, multi_dim_analysis, shake_vs_break,
               business_quality, research_reports, announcements,
               smart_picker, price_watcher, disciplines, run_brief)

# v5.0 新增 7 大工具
from . import (dcf_calculator, sector_rotation, sell_signal, polaris_monitor,
               realtime_alerts, financial_parser, backtest_engine)

# v5.1 新增 4 大 深度智能
from . import (main_line_intel, weekly_report, missed_opportunity, multi_model_vote)

# v5.2 新增 持仓优化器
from . import portfolio_optimizer

# v5.3 新增 全市场 突破前高 监控
from . import breakthrough_scanner

# v5.4 Anthropic financial-services 精华融合
from . import thesis_tracker, catalyst_calendar, daily_morning_note

# v5.5 ai-berkshire 精华融合 (4 大师视角 + Thesis Drift + Quality Screen)
from . import thesis_drift, quality_screen, four_masters_vote

__all__ = [
    'data_sources', 'indicators', 'analyzers', 'portfolio', 'renderers',
    'realtime_analyzer', 'multi_timeframe', 'market_phase', 'main_line_tracker',
    'end_wave_detector', 'multi_dim_analysis', 'shake_vs_break',
    'business_quality', 'research_reports', 'announcements',
    'smart_picker', 'price_watcher', 'disciplines', 'run_brief',
    'dcf_calculator', 'sector_rotation', 'sell_signal', 'polaris_monitor',
    'realtime_alerts', 'financial_parser', 'backtest_engine',
    'main_line_intel', 'weekly_report', 'missed_opportunity', 'multi_model_vote',
    'portfolio_optimizer',
    'breakthrough_scanner',
    'thesis_tracker', 'catalyst_calendar', 'daily_morning_note',
    'thesis_drift', 'quality_screen', 'four_masters_vote',
]
