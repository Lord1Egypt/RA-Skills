"""
门店核心基线分析 Skill (Store POScore Baseline Analysis)

基于Agent API（数据库视图），提供多周期（13周/26周/52周/12月）基线+四分位分析，
支持波动归因和异常检测。

主要功能:
- analyze: 计算多指标基线（销售额、订单数、客单价、连带率）
- analyze_current_vs_baseline: 对比当前业绩与基线，自动归因波动
- calculate_baseline: 计算四分位统计量
- fetch_daily_data/fetch_weekly_data/fetch_monthly_data: 数据获取

示例:
    from store_poscore_baseline import analyze, analyze_current_vs_baseline
    
    # 计算基线
    baseline = analyze(
        store_id="416759_1714379448487",
        baseline_type="weekday",
        period="13w"
    )
    
    # 波动归因
    findings = analyze_current_vs_baseline(
        store_id="416759_1714379448487",
        current_date="2026-03-25"
    )
"""

from .analyze import (
    analyze,
    analyze_current_vs_baseline,
    calculate_baseline,
    fetch_daily_data,
    fetch_weekly_data,
    fetch_monthly_data,
    BaselineType,
    BaselinePeriod,
    BaselineMetrics
)

__all__ = [
    'analyze',
    'analyze_current_vs_baseline',
    'calculate_baseline',
    'fetch_daily_data',
    'fetch_weekly_data',
    'fetch_monthly_data',
    'BaselineType',
    'BaselinePeriod',
    'BaselineMetrics'
]

__version__ = '1.0.0'
