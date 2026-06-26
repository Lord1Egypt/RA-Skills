#!/usr/bin/env python3
"""
关闭zworker定时计划
支持按ID或名称关闭
"""

import sys
import argparse
from zworker_api import set_schedule, ZworkerAPIError

def main():
    parser = argparse.ArgumentParser(description='关闭zworker定时计划')
    parser.add_argument('--id', type=int, help='计划ID')
    parser.add_argument('--name', help='计划名称')
    parser.add_argument('--quiet', action='store_true', help='安静模式，仅输出成功/失败')
    
    args = parser.parse_args()
    
    if not args.id and not args.name:
        print("错误: 必须提供 --id 或 --name 参数", file=sys.stderr)
        sys.exit(1)
    
    try:
        result = set_schedule(enable=False, schedule_id=args.id, schedule_name=args.name)
        
        if args.quiet:
            print("success")
        else:
            print("✅ 已成功关闭定时计划")
        
        sys.exit(0)
        
    except ZworkerAPIError as e:
        if args.quiet:
            print(f"error: {e}", file=sys.stderr)
        else:
            print(f"❌ 定时计划关闭失败: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.quiet:
            print(f"error: {e}", file=sys.stderr)
        else:
            print(f"❌ 未知错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()