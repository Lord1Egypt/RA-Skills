#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新工作项"""

import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yunxiao_api import load_config, update_workitem, get_workitem


def main():
    parser = argparse.ArgumentParser(description='更新云效工作项')
    parser.add_argument('workitem_id', type=str, help='工作项 ID')
    parser.add_argument('--subject', '-s', type=str, help='新标题')
    parser.add_argument('--status', type=str, help='新状态（待处理/进行中/已完成/已关闭）')
    parser.add_argument('--priority', type=str, choices=['低', '中', '高', '紧急'], help='优先级')
    parser.add_argument('--assignee', '-a', type=str, help='新负责人 userId')
    parser.add_argument('--desc', '-d', type=str, help='新描述')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    config = load_config()
    
    # 构建更新内容
    updates = {}
    
    if args.subject:
        updates['subject'] = args.subject
    
    if args.status:
        status_id = config.get('status_map', {}).get(args.status)
        if status_id:
            updates['status'] = status_id
        else:
            print(f"错误: 未知状态 '{args.status}'")
            print(f"可用状态: {', '.join(config.get('status_map', {}).keys())}")
            sys.exit(1)
    
    if args.priority:
        priority_id = config.get('priority_map', {}).get(args.priority)
        if priority_id:
            updates['priority'] = priority_id
    
    if args.assignee:
        updates['assignedTo'] = args.assignee
    
    if args.desc:
        updates['description'] = args.desc
    
    if not updates:
        print("错误: 未指定要更新的内容")
        print("使用 --subject, --status, --priority, --assignee, --desc 指定更新内容")
        sys.exit(1)
    
    try:
        # 先获取当前状态
        old_item = get_workitem(args.workitem_id)
        old_subject = old_item.get('subject', 'N/A')
        old_status = old_item.get('status', {}).get('displayName', 'N/A')
        
        # 执行更新
        update_workitem(args.workitem_id, updates)
        
        # 获取更新后的状态
        new_item = get_workitem(args.workitem_id)
        
        if args.json:
            print(json.dumps(new_item, ensure_ascii=False, indent=2))
        else:
            print(f"\n✓ 工作项更新成功!")
            print(f"  ID: {args.workitem_id}")
            print(f"  标题: {old_subject}")
            
            if args.status:
                print(f"  状态: {old_status} → {args.status}")
            if args.subject:
                print(f"  新标题: {args.subject}")
            if args.priority:
                print(f"  优先级: {args.priority}")
            if args.assignee:
                print(f"  新负责人 ID: {args.assignee}")
            
            print()
        
    except Exception as e:
        print(f"更新失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()