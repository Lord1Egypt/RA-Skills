
#!/usr/bin/env python3
"""
心理咨询师 Skill 生成器
"""

import os
import json
import argparse
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="心理咨询师 Skill 生成器")
    parser.add_argument("--action", choices=["create", "list", "update"], default="create", help="操作类型")
    parser.add_argument("--slug", help="咨询师代号")
    parser.add_argument("--base-dir", default="./counselors", help="基础目录")
    return parser.parse_args()

def list_counselors(base_dir):
    """列出所有已生成的咨询师"""
    if not os.path.exists(base_dir):
        print("暂无咨询师")
        return
    
    counselors = [d for d in os.listdir(base_dir) 
                  if os.path.isdir(os.path.join(base_dir, d)) 
                  and d != "versions" and d != "knowledge"]
    
    if not counselors:
        print("暂无咨询师")
        return
    
    print("已生成的咨询师：")
    for counselor in counselors:
        meta_file = os.path.join(base_dir, counselor, "meta.json")
        if os.path.exists(meta_file):
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
                print(f"  - {counselor}: {meta.get('name', '')} ({meta.get('theoretical_orientation', '')})")

def main():
    args = parse_args()
    
    if args.action == "list":
        list_counselors(args.base_dir)
    elif args.action == "create":
        print("创建功能将由 skill 主流程处理")
    elif args.action == "update":
        print("更新功能将由 skill 主流程处理")

if __name__ == "__main__":
    main()
