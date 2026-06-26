"""
目标追踪分析 Skill

支持多层级（门店/城市/省份/区域/集团）、多周期（日/周/月）的目标达成追踪分析。

主要功能:
- analyze: 目标追踪分析主函数
- format_report: 格式化报告输出
- check_alerts: 主动告警检查
- check_alerts_batch: 批量告警检查
- fetch_actual_data: 获取实际业绩数据（支持多层级）
- parse_actual_metrics: 解析业绩指标（支持多层级）

示例:
    from target_tracking import analyze, format_report
    
    result = analyze(
        store_id="416759_1714379448487",
        store_code="530102063",
        period="monthly",
        current_date="2026-03-25"
    )
    print(format_report(result))
"""

from .analyze import (
    analyze,
    format_report,
    check_alerts,
    check_alerts_batch,
    fetch_actual_data,
    parse_actual_metrics,
    TrackingPeriod
)

__all__ = [
    'analyze',
    'format_report',
    'check_alerts',
    'check_alerts_batch',
    'fetch_actual_data',
    'parse_actual_metrics',
    'TrackingPeriod'
]

__version__ = '3.1.0'
