#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查询单个工作项详情"""

import sys
import os
import json
import argparse
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yunxiao_api import get_workitem


def main():
    parser = argparse.ArgumentParser(description='查询云效工作项详情')
    parser.add_argument('workitem_id', type=str, help='工作项 ID')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    try:
        item = get_workitem(args.workitem_id)
        
        if args.json:
            print(json.dumps(item, ensure_ascii=False, indent=2))
            return
        
        print(f"\n{'='*60}")
        print(f"工作项详情")
        print(f"{'='*60}")
        print(f"编号: {item.get('serialNumber', 'N/A')}")
        print(f"标题: {item.get('subject', 'N/A')}")
        print(f"状态: {item.get('status', {}).get('displayName', 'N/A')}")
        print(f"类型: {item.get('workitemType', {}).get('name', 'N/A')}")
        print(f"负责人: {item.get('assignedTo', {}).get('name', 'N/A')}")
        print(f"创建者: {item.get('creator', {}).get('name', 'N/A')}")
        print(f"项目: {item.get('space', {}).get('name', 'N/A')}")
        
        # 描述
        description = item.get('description', '')
        if description:
            print(f"\n描述:\n{description}")
        
        # 自定义字段
        custom_fields = item.get('customFieldValues', [])
        for field in custom_fields:
            field_name = field.get('fieldName', '')
            values = field.get('values', [])
            if values:
                display_value = values[0].get('displayValue', '')
                if field_name and display_value:
                    print(f"{field_name}: {display_value}")
        
        # 时间信息
        gmt_create = item.get('gmtCreate')
        gmt_modified = item.get('gmtModified')
        
        if gmt_create:
            create_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(gmt_create / 1000))
            print(f"\n创建时间: {create_time}")
        
        if gmt_modified:
            modify_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(gmt_modified / 1000))
            print(f"修改时间: {modify_time}")
        
        # ID
        print(f"\n工作项 ID: {item.get('id')}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"查询失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()