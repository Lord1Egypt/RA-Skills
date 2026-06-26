"""
业绩评价分析 Skill (Performance Evaluation Analysis)

整合目标达成、环比、基线、Benchmark四个维度，量化"业绩不达预期"分析。

主要功能:
- comprehensive_evaluation: 综合评价（目标+环比+基线+周末专项）
- format_report: 格式化报告输出
- evaluate_target/evaluate_mom/evaluate_baseline: 单维度评价

示例:
    from performance_evaluation import comprehensive_evaluation, format_report
    
    result = comprehensive_evaluation(
        store_id="416759_1714379448487",
        store_name="正义路60号",
        date_str="2026-03-22"
    )
    
    print(format_report(result))
"""

from .analyze import (
    comprehensive_evaluation,
    format_report,
    evaluate_target,
    evaluate_mom,
    evaluate_baseline,
    evaluate_weekend,
    ExpectationType,
    EvaluationResult
)

__all__ = [
    'comprehensive_evaluation',
    'format_report',
    'evaluate_target',
    'evaluate_mom',
    'evaluate_baseline',
    'evaluate_weekend',
    'ExpectationType',
    'EvaluationResult'
]

__version__ = '1.0.0'
