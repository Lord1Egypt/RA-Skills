#!/usr/bin/env python3
"""
隐患记录查询脚本
支持多条件筛选查询隐患列表
"""

import argparse
import json
import sys
from pathlib import Path


DATA_DIR = Path("./inspection_data")
INSPECTIONS_FILE = DATA_DIR / "inspections.json"


def load_inspections():
    """加载隐患记录"""
    if not INSPECTIONS_FILE.exists():
        return []
    with open(INSPECTIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def filter_inspections(inspections, severity=None, category=None, inspector=None, status=None):
    """多条件筛选"""
    result = inspections
    filters_applied = []

    if severity:
        result = [item for item in result if item.get('severity') == severity.lower()]
        filters_applied.append(f"严重等级={severity}")

    if category:
        result = [item for item in result if item.get('category') == category]
        filters_applied.append(f"类别={category}")

    if inspector:
        result = [item for item in result if inspector in item.get('inspector', '')]
        filters_applied.append(f"检查人包含'{inspector}'")

    if status:
        result = [item for item in result if item.get('status') == status]
        filters_applied.append(f"状态={status}")

    return result, filters_applied


def format_list_item(item):
    """格式化单条记录显示"""
    return {
        "id": item['id'],
        "location": item['location'],
        "category": item['category'],
        "severity": f"{item['severity']} ({item.get('severity_label', '')})",
        "status": item['status'],
        "inspector": item['inspector'],
        "found_date": item['found_date']
    }


def main():
    parser = argparse.ArgumentParser(description='查询隐患记录')
    parser.add_argument('--severity', help='按严重等级筛选: low/medium/high/critical')
    parser.add_argument('--category', help='按隐患类别筛选')
    parser.add_argument('--inspector', help='按检查人员筛选（模糊匹配）')
    parser.add_argument('--status', help='按状态筛选: pending/in_progress/completed')
    parser.add_argument('--format', choices=['list', 'detail', 'count'], default='list',
                        help='输出格式: list=简洁列表, detail=完整详情, count=数量统计')

    args = parser.parse_args()

    inspections = load_inspections()

    if not inspections:
        result = {
            "status": "success",
            "message": "暂无隐患记录",
            "data": {"total": 0, "items": []}
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    filtered, filters_applied = filter_inspections(
        inspections,
        severity=args.severity,
        category=args.category,
        inspector=args.inspector,
        status=args.status
    )

    if args.format == 'count':
        result = {
            "status": "success",
            "filters": filters_applied if filters_applied else ["无"],
            "total": len(filtered)
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.format == 'detail':
        output_items = filtered
    else:
        output_items = [format_list_item(item) for item in filtered]

    result = {
        "status": "success",
        "message": f"共找到 {len(filtered)} 条记录" + (f"，筛选条件: {', '.join(filters_applied)}" if filters_applied else ""),
        "total": len(filtered),
        "items": output_items
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
