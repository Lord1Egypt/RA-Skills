#!/usr/bin/env python3
"""
不符合项录入脚本
功能:创建新的不符合项记录,包含条款/描述/证据等关键信息
"""
import json
import argparse
import sys
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "assets" / "nc_data.json"

def load_data():
    """加载现有数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"non_conformances": [], "audit_ids": []}

def save_data(data):
    """保存数据"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_nc_id(data):
    """生成唯一ID: NC-YYYYMMDD-NNN"""
    today = datetime.now().strftime("%Y%m%d")
    prefix = f"NC-{today}-"
    
    existing = [nc['id'] for nc in data['non_conformances'] if nc['id'].startswith(prefix)]
    if not existing:
        seq = 1
    else:
        seq = max(int(nc.split('-')[-1]) for nc in existing) + 1
    
    return f"{prefix}{seq:03d}"

def add_nc(args):
    """添加不符合项"""
    data = load_data()
    
    nc = {
        "id": generate_nc_id(data),
        "title": args.title,
        "clause": args.clause,
        "category": args.category or "minor",
        "description": args.description,
        "evidence": args.evidence if args.evidence else [],
        "root_cause": args.root_cause if hasattr(args, 'root_cause') and args.root_cause else "",
        "corrective_action": args.corrective_action if hasattr(args, 'corrective_action') and args.corrective_action else "",
        "verification": {
            "status": "open",
            "verifier": "",
            "verified_at": "",
            "result": ""
        },
        "audit_info": {
            "audit_id": args.audit_id if hasattr(args, 'audit_id') and args.audit_id else "",
            "auditor": args.auditor if hasattr(args, 'auditor') and args.auditor else "",
            "audit_date": datetime.now().strftime("%Y-%m-%d")
        },
        "created_at": datetime.now().isoformat()
    }
    
    data['non_conformances'].append(nc)
    
    if args.audit_id and args.audit_id not in data['audit_ids']:
        data['audit_ids'].append(args.audit_id)
    
    save_data(data)
    
    result = {
        "status": "success",
        "message": f"不符合项创建成功",
        "nc_id": nc["id"],
        "category": nc["category"],
        "clause": nc["clause"]
    }
    print(json.dumps(result, ensure_ascii=False))
    return result

def main():
    parser = argparse.ArgumentParser(description='录入不符合项')
    parser.add_argument('--title', required=True, help='不符合项标题')
    parser.add_argument('--clause', required=True, help='ISO条款编号')
    parser.add_argument('--description', required=True, help='不符合项描述')
    parser.add_argument('--evidence', nargs='*', help='证据列表')
    parser.add_argument('--category', choices=['major', 'minor', 'observation'], 
                        default='minor', help='不符合项类别')
    parser.add_argument('--root-cause', help='根本原因分析')
    parser.add_argument('--corrective-action', help='纠正措施')
    parser.add_argument('--audit-id', help='关联审核ID')
    parser.add_argument('--auditor', help='审核员姓名')
    
    args = parser.parse_args()
    add_nc(args)

if __name__ == "__main__":
    main()
