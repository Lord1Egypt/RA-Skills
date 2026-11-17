#!/usr/bin/env python3
"""
隐患记录创建脚本
支持多维度隐患信息录入，保存至本地JSON文件
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


DATA_DIR = Path("./inspection_data")
INSPECTIONS_FILE = DATA_DIR / "inspections.json"
REMEDIATION_FILE = DATA_DIR / "remediations.json"


def load_inspections():
    """加载现有隐患记录"""
    if INSPECTIONS_FILE.exists():
        with open(INSPECTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_inspections(inspections):
    """保存隐患记录"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(INSPECTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(inspections, f, ensure_ascii=False, indent=2)


def generate_id(inspections):
    """生成唯一隐患ID"""
    if not inspections:
        return "HZD-001"
    max_num = 0
    for item in inspections:
        if item['id'].startswith('HZD-'):
            try:
                num = int(item['id'].split('-')[1])
                max_num = max(max_num, num)
            except ValueError:
                pass
    return f"HZD-{max_num + 1:03d}"


def validate_severity(severity):
    """验证严重等级"""
    valid_levels = ['low', 'medium', 'high', 'critical']
    if severity.lower() not in valid_levels:
        raise ValueError(f"无效的严重等级: {severity}，可选值: {', '.join(valid_levels)}")
    return severity.lower()


def validate_category(category):
    """验证隐患类别"""
    valid_categories = [
        '电气安全', '机械防护', '消防设施', '危化品管理',
        '个人防护', '作业环境', '特种设备', '安全基础管理'
    ]
    if category not in valid_categories:
        raise ValueError(f"隐患类别 '{category}' 不在标准分类中，请从以下类别中选择:\n{', '.join(valid_categories)}")
    return category


def main():
    parser = argparse.ArgumentParser(description='创建生产现场隐患记录')
    parser.add_argument('--location', required=True, help='隐患位置')
    parser.add_argument('--category', required=True, help='隐患类别（见清单模板）')
    parser.add_argument('--description', required=True, help='隐患详细描述')
    parser.add_argument('--severity', required=True, help='严重等级: low/medium/high/critical')
    parser.add_argument('--inspector', default='未知', help='检查人员')
    parser.add_argument('--found-date', default=None, help='发现日期（默认当天）')

    args = parser.parse_args()

    try:
        severity = validate_severity(args.severity)
        category = validate_category(args.category)
    except ValueError as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        sys.exit(1)

    inspections = load_inspections()
    new_id = generate_id(inspections)

    found_date = args.found_date or datetime.now().strftime('%Y-%m-%d')

    inspection_record = {
        "id": new_id,
        "location": args.location,
        "category": category,
        "description": args.description,
        "severity": severity,
        "severity_label": {
            "low": "一般",
            "medium": "较大",
            "high": "重大",
            "critical": "特大"
        }.get(severity, "未知"),
        "inspector": args.inspector,
        "found_date": found_date,
        "created_at": datetime.now().isoformat(),
        "status": "pending",
        "remediation_id": None
    }

    inspections.append(inspection_record)
    save_inspections(inspections)

    result = {
        "status": "success",
        "message": f"隐患记录创建成功",
        "data": {
            "id": new_id,
            "location": args.location,
            "severity": severity,
            "severity_label": inspection_record["severity_label"],
            "status": "pending"
        }
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
