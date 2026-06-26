#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查询项目列表"""

import sys
import os
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yunxiao_api import search_projects


def main():
    parser = argparse.ArgumentParser(description='查询云效项目列表')
    parser.add_argument('--name', '-n', type=str, help='项目名称（模糊搜索）')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    try:
        projects = search_projects(name=args.name)
        
        if args.json:
            print(json.dumps(projects, ensure_ascii=False, indent=2))
            return
        
        if not projects:
            print("暂无项目")
            return
        
        print(f"\n共 {len(projects)} 个项目:\n")
        print(f"{'项目名称':<25} {'编号':<8} {'状态':<8} {'创建者':<10}")
        print("-" * 60)
        
        for p in projects:
            name = p.get('name', 'N/A')[:23]
            code = p.get('customCode', 'N/A')
            status = p.get('status', {}).get('name', 'N/A')
            creator = p.get('creator', {}).get('name', 'N/A')[:8]
            
            print(f"{name:<25} {code:<8} {status:<8} {creator:<10}")
        
        print()
        
    except Exception as e:
        print(f"查询失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()