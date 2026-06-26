#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社交媒体内容排期器
"""
import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="社交媒体内容排期器")
    parser.add_argument("--topic", default="AI写作", help="内容主题")
    parser.add_argument("--platform", default="xiaohongshu", help="平台")
    parser.add_argument("--count", type=int, default=3, help="生成数量")
    args = parser.parse_args()

    results = []
    for i in range(args.count):
        results.append({
            "id": i+1,
            "platform": args.platform,
            "topic": f"{args.topic}内容{i+1}",
            "title": f"关于{args.topic}的第{i+1}篇",
            "tags": ["#干货", "#分享", f"#{args.topic}"]
        })

    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    # Fix Windows UTF-8 output
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    main()
