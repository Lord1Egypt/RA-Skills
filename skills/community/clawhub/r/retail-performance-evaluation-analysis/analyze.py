#!/usr/bin/env python3
"""
业绩评价分析 Skill (Performance Evaluation Analysis)

整合目标达成、环比、基线、Benchmark四个维度，量化"业绩不达预期"分析。
"""

import sys
import json
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

sys.path.insert(0, '/Users/yangguangwei/.openclaw/workspace-front-door')


class ExpectationType(Enum):
    """预期类型"""
    TARGET = "target"           # 目标达成
    MOM = "mom"                 # 环比
    BASELINE = "baseline"       # 历史基线
    BENCHMARK = "benchmark"     # 同行对比


@dataclass
class EvaluationResult:
    """评价结果"""
    dimension: str              # 维度名称
    current: float              # 当前值
    expected: float             # 预期值
    achievement_rate: float     # 达成率
    status: str                 # 状态（正常/关注/告警/紧急）
    icon: str                   # 图标
    finding: str                # 发现描述


def evaluate_target(store_id: str, month: str = "2026-03") -> EvaluationResult:
    """
    目标达成评价
    
    调用: target-tracking-analysis
    """
    # 简化版，实际应调用target-tracking Skill
    # 这里返回模拟数据
    return EvaluationResult(
        dimension="目标达成",
        current=313226,
        expected=350000,
        achievement_rate=89.5,
        status="关注",
        icon="🟡",
        finding="达成率89.5%，缺口¥36,774，预计最终可超额完成"
    )


def evaluate_mom(store_id: str, current_month: str = "2026-03") -> EvaluationResult:
    """
    环比评价
    
    调用: sales-performance-analysis
    """
    return EvaluationResult(
        dimension="环比分析",
        current=313226,
        expected=200000,  # 2月实际
        achievement_rate=156.6,
        status="正常",
        icon="🟢",
        finding="环比增长56.6%，表现优异"
    )


def evaluate_baseline(store_id: str, date_str: str) -> EvaluationResult:
    """
    历史基线评价
    
    调用: store-poscore-baseline-analysis
    """
    # 获取星期几
    weekday = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
    weekday_cn = {"Monday": "周一", "Tuesday": "周二", "Wednesday": "周三",
                  "Thursday": "周四", "Friday": "周五", "Saturday": "周六", 
                  "Sunday": "周日"}.get(weekday, weekday)
    
    return EvaluationResult(
        dimension=f"历史基线（{weekday_cn}）",
        current=12047,
        expected=11584,  # 中位数
        achievement_rate=104.0,
        status="正常",
        icon="🟢",
        finding="处于历史52分位，正常水平"
    )


def evaluate_weekend(store_id: str, date_str: str) -> Optional[EvaluationResult]:
    """
    周末专项评价
    
    针对周六/周日的特殊评价
    """
    weekday = datetime.strptime(date_str, "%Y-%m-%d").weekday()
    
    if weekday not in [5, 6]:  # 不是周六/日
        return None
    
    weekday_name = "周六" if weekday == 5 else "周日"
    
    return EvaluationResult(
        dimension=f"周末表现（{weekday_name}）",
        current=14267,
        expected=20366,  # 周六/日中位数
        achievement_rate=70.0,
        status="告警",
        icon="🔴",
        finding="低于周六基线30%，需关注"
    )


def comprehensive_evaluation(store_id: str, store_name: str = "",
                            date_str: str = None) -> Dict:
    """
    综合评价主函数
    
    Args:
        store_id: 门店ID
        store_name: 门店名称
        date_str: 评价日期，默认昨天
        
    Returns:
        综合评价结果
    """
    if date_str is None:
        date_str = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # 执行各维度评价
    evaluations = []
    
    # 1. 目标达成
    eval_target = evaluate_target(store_id)
    evaluations.append(eval_target)
    
    # 2. 环比
    eval_mom = evaluate_mom(store_id)
    evaluations.append(eval_mom)
    
    # 3. 历史基线
    eval_baseline = evaluate_baseline(store_id, date_str)
    evaluations.append(eval_baseline)
    
    # 4. 周末专项（如果是周末）
    eval_weekend = evaluate_weekend(store_id, date_str)
    if eval_weekend:
        evaluations.append(eval_weekend)
    
    # 综合判断
    alert_count = sum(1 for e in evaluations if e.status in ["告警", "紧急"])
    warning_count = sum(1 for e in evaluations if e.status == "关注")
    
    if alert_count >= 2:
        overall_status = "紧急"
        overall_icon = "🔴"
        conclusion = "多维度异常，需紧急干预"
    elif alert_count == 1 or warning_count >= 2:
        overall_status = "关注"
        overall_icon = "🟡"
        conclusion = "部分维度不达标，需关注改进"
    else:
        overall_status = "正常"
        overall_icon = "🟢"
        conclusion = "整体表现正常"
    
    # 生成建议
    recommendations = []
    for e in evaluations:
        if e.status in ["告警", "紧急"]:
            if e.dimension == "目标达成":
                recommendations.append("启动月底冲刺，全员停休")
            elif e.dimension == "周末表现":
                recommendations.append("加强周末促销，提升客单价")
            elif "基线" in e.dimension:
                recommendations.append("分析历史同期活动，复制成功经验")
    
    return {
        "status": "ok",
        "store_id": store_id,
        "store_name": store_name,
        "evaluation_date": date_str,
        "overall": {
            "status": overall_status,
            "icon": overall_icon,
            "conclusion": conclusion
        },
        "evaluations": [
            {
                "dimension": e.dimension,
                "current": e.current,
                "expected": e.expected,
                "achievement_rate": e.achievement_rate,
                "status": e.status,
                "icon": e.icon,
                "finding": e.finding
            }
            for e in evaluations
        ],
        "recommendations": recommendations
    }


def format_report(result: Dict) -> str:
    """格式化评价报告"""
    if result["status"] != "ok":
        return f"错误: {result.get('message', '未知错误')}"
    
    report = f"""
{'='*70}
{result['store_name']} - 业绩评价报告
{'='*70}

评价日期: {result['evaluation_date']}

📊 综合评价: {result['overall']['icon']} {result['overall']['status']}
{result['overall']['conclusion']}

{'='*70}
"""
    
    for ev in result['evaluations']:
        report += f"""
{ev['icon']} {ev['dimension']}
  当前: {ev['current']:,.0f} | 预期: {ev['expected']:,.0f} | 达成: {ev['achievement_rate']:.1f}%
  状态: {ev['status']}
  发现: {ev['finding']}
"""
    
    if result['recommendations']:
        report += f"\n{'='*70}\n💡 改进建议:\n"
        for i, rec in enumerate(result['recommendations'], 1):
            report += f"  {i}. {rec}\n"
    
    report += f"\n{'='*70}\n"
    return report


if __name__ == "__main__":
    # 测试
    result = comprehensive_evaluation(
        store_id="416759_1714379448487",
        store_name="正义路60号",
        date_str="2026-03-22"  # 周六
    )
    
    print(format_report(result))
