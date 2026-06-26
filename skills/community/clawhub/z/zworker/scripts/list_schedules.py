#!/usr/bin/env python3
"""
列出zworker定时计划
支持分页和名称过滤
"""

import json
import sys
import argparse
from zworker_api import get_schedule_list, ZworkerAPIError, format_schedule_list

def main():
    parser = argparse.ArgumentParser(description='列出zworker定时计划')
    parser.add_argument('--name', help='计划名称模糊匹配')
    parser.add_argument('--page', type=int, default=0, help='页码，从0开始 (默认: 0)')
    parser.add_argument('--limit', type=int, default=24, help='每页数量 (默认: 24)')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')
    
    args = parser.parse_args()
    
    try:
        result = get_schedule_list(name=args.name, page_number=args.page, limit=args.limit)
        
        schedules = result.get('schedules', [])
        total = result.get('total', 0)
        rep_page_number = result.get('pageNumber', 1)
        rep_limit = result.get('limit', 24)
        
        if args.json:
            output = {
                'schedules': schedules,
                'total': total,
                'pageNumber': rep_page_number,
                'limit': rep_limit,
                'has_more': (rep_page_number * rep_limit + len(schedules)) < total
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(format_schedule_list(schedules))
            print()
            
            # 分页信息
            start = rep_page_number * rep_limit + 1
            end = start + len(schedules) - 1
            print(f"显示计划: {start}-{end} (总共: {total})")
            
            if rep_page_number == 0 and len(schedules) < total:
                print("提示: 当前仅返回前24条计划数，如果需要获取更多可以继续跟我说，比如：获取下一页数据")
        
        sys.exit(0)
        
    except ZworkerAPIError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()