#!/usr/bin/env python3
"""
隐患整改任务管理脚本
支持创建、查询、更新整改任务
"""

import argparse
import json
import sys
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


def save_remediations(remediations):
    """保存整改任务"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(REMEDIATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(remediations, f, ensure_ascii=False, indent=2)


def update_inspection_status(inspection_id, remediation_id):
    """更新隐患状态"""
    if not INSPECTIONS_FILE.exists():
        return False

    with open(INSPECTIONS_FILE, 'r', encoding='utf-8') as f:
        inspections = json.load(f)

    for item in inspections:
        if item['id'] == inspection_id:
            item['status'] = 'in_progress'
            item['remediation_id'] = remediation_id
            break

    with open(INSPECTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(inspections, f, ensure_ascii=False, indent=2)

    return True


def generate_remediation_id(remediations):
    """生成整改任务ID"""
    if not remediations:
        return "REM-001"
    max_num = 0
    for item in remediations:
        if item['id'].startswith('REM-'):
            try:
                num = int(item['id'].split('-')[1])
                max_num = max(max_num, num)
            except ValueError:
                pass
    return f"REM-{max_num + 1:03d}"


def create_remediation(args, inspections):
    """创建整改任务"""
    # 验证隐患是否存在
    target_inspection = None
    for item in inspections:
        if item['id'] == args.inspection_id:
            target_inspection = item
            break

    if not target_inspection:
        print(json.dumps({
            "status": "error",
            "message": f"未找到隐患记录: {args.inspection_id}"
        }, ensure_ascii=False))
        sys.exit(1)

    _, remediations = load_data()
    new_id = generate_remediation_id(remediations)

    remediation = {
        "id": new_id,
        "inspection_id": args.inspection_id,
        "inspection_location": target_inspection['location'],
        "inspection_description": target_inspection['description'],
        "severity": target_inspection['severity'],
        "assignee": args.assignee,
        "deadline": args.deadline,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "completed_at": None,
        "notes": args.notes or ""
    }

    remediations.append(remediation)
    save_remediations(remediations)
    update_inspection_status(args.inspection_id, new_id)

    print(json.dumps({
        "status": "success",
        "message": "整改任务创建成功",
        "data": {
            "id": new_id,
            "inspection_id": args.inspection_id,
            "assignee": args.assignee,
            "deadline": args.deadline,
            "status": "pending"
        }
    }, ensure_ascii=False, indent=2))


def list_remediations(args):
    """列出整改任务"""
    _, remediations = load_data()

    if not remediations:
        print(json.dumps({
            "status": "success",
            "message": "暂无整改任务",
            "total": 0,
            "items": []
        }, ensure_ascii=False, indent=2))
        return

    # 筛选
    filtered = remediations
    if args.status:
        filtered = [r for r in filtered if r['status'] == args.status]
    if args.assignee:
        filtered = [r for r in filtered if args.assignee in r['assignee']]

    output = []
    for r in filtered:
        output.append({
            "id": r['id'],
            "inspection_id": r['inspection_id'],
            "location": r['inspection_location'],
            "assignee": r['assignee'],
            "deadline": r['deadline'],
            "status": r['status'],
            "created_at": r['created_at']
        })

    print(json.dumps({
        "status": "success",
        "message": f"共找到 {len(output)} 条整改任务",
        "total": len(output),
        "items": output
    }, ensure_ascii=False, indent=2))


def update_remediation(args):
    """更新整改任务"""
    _, remediations = load_data()

    target = None
    for r in remediations:
        if r['id'] == args.task_id:
            target = r
            break

    if not target:
        print(json.dumps({
            "status": "error",
            "message": f"未找到整改任务: {args.task_id}"
        }, ensure_ascii=False))
        sys.exit(1)

    # 更新字段
    if args.status:
        target['status'] = args.status
        if args.status == 'completed':
            target['completed_at'] = datetime.now().isoformat()
    if args.notes:
        target['notes'] = args.notes

    target['updated_at'] = datetime.now().isoformat()

    # 更新隐患状态
    if args.status == 'completed':
        if INSPECTIONS_FILE.exists():
            with open(INSPECTIONS_FILE, 'r', encoding='utf-8') as f:
                inspections = json.load(f)
            for item in inspections:
                if item['id'] == target['inspection_id']:
                    item['status'] = 'completed'
                    break
            with open(INSPECTIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump(inspections, f, ensure_ascii=False, indent=2)

    save_remediations(remediations)

    print(json.dumps({
        "status": "success",
        "message": f"整改任务 {args.task_id} 已更新",
        "data": {
            "id": target['id'],
            "status": target['status'],
            "updated_at": target['updated_at']
        }
    }, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description='整改任务管理')
    subparsers = parser.add_subparsers(dest='action', help='操作类型')

    # create 子命令
    create_parser = subparsers.add_parser('create', help='创建整改任务')
    create_parser.add_argument('--inspection-id', required=True, help='关联的隐患ID')
    create_parser.add_argument('--assignee', required=True, help='整改责任人')
    create_parser.add_argument('--deadline', required=True, help='整改期限 (YYYY-MM-DD)')
    create_parser.add_argument('--notes', help='备注信息')

    # list 子命令
    list_parser = subparsers.add_parser('list', help='列出整改任务')
    list_parser.add_argument('--status', help='按状态筛选: pending/in_progress/completed')
    list_parser.add_argument('--assignee', help='按责任人筛选')

    # update 子命令
    update_parser = subparsers.add_parser('update', help='更新整改任务')
    update_parser.add_argument('--task-id', required=True, help='整改任务ID')
    update_parser.add_argument('--status', choices=['pending', 'in_progress', 'completed'],
                               help='新状态')
    update_parser.add_argument('--notes', help='追加备注')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    inspections, _ = load_data()

    if args.action == 'create':
        create_remediation(args, inspections)
    elif args.action == 'list':
        list_remediations(args)
    elif args.action == 'update':
        update_remediation(args)


if __name__ == "__main__":
    main()
