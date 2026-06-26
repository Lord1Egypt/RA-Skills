#!/usr/bin/env python3
"""
执行zworker任务
支持按ID或名称执行
"""

import sys
import argparse
from zworker_api import run_task, ZworkerAPIError

def main():
    parser = argparse.ArgumentParser(description='执行zworker任务')
    parser.add_argument('--id', type=int, help='任务ID')
    parser.add_argument('--name', help='任务名称')
    parser.add_argument('--quiet', action='store_true', help='安静模式，仅输出成功/失败')
    
    args = parser.parse_args()
    
    if not args.id and not args.name:
        print("错误: 必须提供 --id 或 --name 参数", file=sys.stderr)
        sys.exit(1)
    
    try:
        result = run_task(task_id=args.id, task_name=args.name)
        
        if args.quiet:
            print("success")
        else:
            print("✅ 已成功触发任务执行")
        
        sys.exit(0)
        
    except ZworkerAPIError as e:
        if args.quiet:
            print(f"error: {e}", file=sys.stderr)
        else:
            print(f"❌ 触发任务执行失败: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.quiet:
            print(f"error: {e}", file=sys.stderr)
        else:
            print(f"❌ 未知错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()