#!/usr/bin/env python3
"""
隐患排查统计分析脚本
支持类型分布、趋势分析、汇总报告
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


DATA_DIR = Path("./inspection_data")
INSPECTIONS_FILE = DATA_DIR / "inspections.json"
REMEDIATIONS_FILE = DATA_DIR / "remediations.json"


def load_data():
    """加载隐患和整改数据"""
    inspections = []
    remediations = []

    if INSPECTIONS_FILE.exists():
        with open(INSPECTIONS_FILE, 'r', encoding='utf-8') as f:
            inspections = json.load(f)

    if REMEDIATIONS_FILE.exists():
        with open(REMEDIATIONS_FILE, 'r', encoding='utf-8') as f:
            remediations = json.load(f)

    return inspections, remediations


def analyze_distribution(inspections):
    """类型分布分析"""
    categories = [item['category'] for item in inspections]
    severities = [item['severity'] for item in inspections]
    locations = [item['location'] for item in inspections]

    # 按类别统计
    category_dist = dict(Counter(categories).most_common())
    # 按严重等级统计
    severity_dist = dict(Counter(severities))
    severity_labels = {
        "critical": "特大",
        "high": "重大",
        "medium": "较大",
        "low": "一般"
    }
    severity_dist_zh = {severity_labels.get(k, k): v for k, v in severity_dist.items()}

    return {
        "by_category": category_dist,
        "by_severity": severity_dist_zh,
        "top_locations": dict(Counter(locations).most_common(5))
    }


def analyze_trend(inspections):
    """时间趋势分析"""
    # 按月份统计
    monthly_stats = defaultdict(lambda: {"total": 0, "by_severity": {}})

    for item in inspections:
        try:
            date_str = item['found_date']
            month_key = date_str[:7]  # YYYY-MM

            monthly_stats[month_key]["total"] += 1

            severity = item['severity']
            if severity not in monthly_stats[month_key]["by_severity"]:
                monthly_stats[month_key]["by_severity"][severity] = 0
            monthly_stats[month_key]["by_severity"][severity] += 1
        except (KeyError, ValueError):
            continue

    return dict(sorted(monthly_stats.items()))


def analyze_summary(inspections, remediations):
    """综合汇总报告"""
    total = len(inspections)
    if total == 0:
        return {"total": 0, "message": "暂无数据"}

    # 状态统计
    status_counter = Counter(item['status'] for item in inspections)
    pending = status_counter.get('pending', 0)
    in_progress = status_counter.get('in_progress', 0)
    completed = status_counter.get('completed', 0)

    # 严重等级统计
    severity_counter = Counter(item['severity'] for item in inspections)
    high_critical = severity_counter.get('high', 0) + severity_counter.get('critical', 0)

    # 整改完成率
    remediation_map = {r['inspection_id']: r for r in remediations}
    completed_with_remediation = 0
    for item in inspections:
        if item['status'] == 'completed' and remediation_map.get(item['id']):
            completed_with_remediation += 1

    completion_rate = (completed / total * 100) if total > 0 else 0
    remediation_rate = (completed_with_remediation / total * 100) if total > 0 else 0

    # 高危隐患待整改数
    high_pending = len([i for i in inspections
                        if i['severity'] in ['high', 'critical'] and i['status'] != 'completed'])

    return {
        "total_inspections": total,
        "status_breakdown": {
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "pending_rate": f"{pending / total * 100:.1f}%"
        },
        "severity_alert": {
            "high_critical_count": high_critical,
            "high_critical_rate": f"{high_critical / total * 100:.1f}%"
        },
        "completion_metrics": {
            "inspection_completion_rate": f"{completion_rate:.1f}%",
            "remediation_rate": f"{remediation_rate:.1f}%"
        },
        "urgent_items": {
            "high_critical_pending": high_pending,
            "message": "需优先整改" if high_pending > 0 else "暂无紧急隐患"
        }
    }


def main():
    parser = argparse.ArgumentParser(description='隐患统计分析')
    parser.add_argument('--type', choices=['distribution', 'trend', 'summary', 'full'],
                        default='full', help='分析类型')

    args = parser.parse_args()

    inspections, remediations = load_data()

    if not inspections:
        print(json.dumps({
            "status": "success",
            "message": "暂无隐患数据",
            "data": {}
        }, ensure_ascii=False, indent=2))
        return

    if args.type == 'distribution':
        data = analyze_distribution(inspections)
    elif args.type == 'trend':
        data = analyze_trend(inspections)
    elif args.type == 'summary':
        data = analyze_summary(inspections, remediations)
    else:
        data = {
            "distribution": analyze_distribution(inspections),
            "trend": analyze_trend(inspections),
            "summary": analyze_summary(inspections, remediations)
        }

    result = {
        "status": "success",
        "type": args.type,
        "generated_at": datetime.now().isoformat(),
        "data": data
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
