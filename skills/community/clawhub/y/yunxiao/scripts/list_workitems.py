#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查询工作项列表"""

import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yunxiao_api import load_config, list_workitems, get_workitem


def main():
    parser = argparse.ArgumentParser(description='查询云效工作项列表')
    parser.add_argument('--mine', action='store_true', help='只查询我负责的')
    parser.add_argument('--project', type=str, help='项目名称或 ID')
    parser.add_argument('--status', type=str, help='状态筛选')
    parser.add_argument('--type', type=str, help='类型筛选（任务/需求/缺陷/风险）')
    parser.add_argument('--id', type=str, help='查询单个工作项详情')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    config = load_config()
    
    # 查询单个工作项
    if args.id:
        try:
            item = get_workitem(args.id)
            if args.json:
                print(json.dumps(item, ensure_ascii=False, indent=2))
            else:
                print(f"\n{'='*60}")
                print(f"工作项: {item.get('subject', 'N/A')}")
                print(f"{'='*60}")
                print(f"编号: {item.get('serialNumber', 'N/A')}")
                print(f"状态: {item.get('status', {}).get('displayName', 'N/A')}")
                print(f"类型: {item.get('workitemType', {}).get('name', 'N/A')}")
                print(f"负责人: {item.get('assignedTo', {}).get('name', 'N/A')}")
                print(f"项目: {item.get('space', {}).get('name', 'N/A')}")
                print(f"描述: {item.get('description', 'N/A')}")
                
                # 优先级
                custom_fields = item.get('customFieldValues', [])
                for field in custom_fields:
                    if field.get('fieldName') == '优先级':
                        values = field.get('values', [])
                        if values:
                            print(f"优先级: {values[0].get('displayValue', 'N/A')}")
                
                # 创建时间
                import time
                gmt_create = item.get('gmtCreate')
                if gmt_create:
                    create_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(gmt_create / 1000))
                    print(f"创建时间: {create_time}")
                
                print(f"\nID: {item.get('id')}")
                print(f"{'='*60}")
            return
        except Exception as e:
            print(f"查询失败: {e}")
            sys.exit(1)
    
    # 构建查询条件
    kwargs = {}
    
    if args.mine:
        kwargs['assigned_to'] = config['user_id']
    
    if args.project:
        # 如果传入的是项目名称，尝试匹配项目 ID
        if args.project in config.get('default_project', ''):
            kwargs['space_id'] = config.get('default_project_id')
        else:
            kwargs['space_id'] = args.project
    
    if args.status:
        status_map = config.get('status_map', {})
        if args.status in status_map:
            kwargs['status'] = status_map[args.status]
        else:
            kwargs['status'] = args.status
    
    if args.type:
        type_map = config.get('workitem_types', {})
        if args.type in type_map:
            kwargs['workitem_type'] = type_map[args.type]
    
    try:
        items = list_workitems(**kwargs)
        
        if args.json:
            print(json.dumps(items, ensure_ascii=False, indent=2))
            return
        
        if not items:
            print("暂无工作项")
            return
        
        print(f"\n共 {len(items)} 个工作项:\n")
        print(f"{'编号':<12} {'标题':<30} {'状态':<8} {'类型':<6} {'负责人':<8}")
        print("-" * 70)
        
        for item in items:
            serial = item.get('serialNumber', 'N/A')
            subject = item.get('subject', 'N/A')[:28]
            status = item.get('status', {}).get('displayName', 'N/A')
            wtype = item.get('workitemType', {}).get('name', 'N/A')
            assignee = item.get('assignedTo', {}).get('name', 'N/A')
            
            print(f"{serial:<12} {subject:<30} {status:<8} {wtype:<6} {assignee:<8}")
        
        print()
        
    except Exception as e:
        print(f"查询失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()