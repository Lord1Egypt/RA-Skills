"""
客户清单分析 Skill

基于Shop API客户清单数据，快速查询不同类型客户的数量、试用情况汇总、导购匹配情况。
"""

from .analyze import (
    analyze,
    format_report,
    fetch_customer_list,
    analyze_customer_types,
    analyze_badge_match,
    analyze_trial_summary,
    CUSTOMER_TYPE_MAP
)

__version__ = "1.0.0"
__all__ = [
    "analyze",
    "format_report",
    "fetch_customer_list",
    "analyze_customer_types",
    "analyze_badge_match",
    "analyze_trial_summary",
    "CUSTOMER_TYPE_MAP"
]
