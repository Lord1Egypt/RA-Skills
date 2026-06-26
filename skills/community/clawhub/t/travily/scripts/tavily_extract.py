#!/usr/bin/env python3
"""
Tavily Extract API - 从 URL 提取内容
"""
import os
import sys
from pathlib import Path
import argparse
import json

# 尝试从 .env 加载
ENV_FILE = Path(__file__).parent.parent / ".env"
if ENV_FILE.exists():
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

try:
    import requests
except ImportError:
    print("错误: 请先安装: pip install requests")
    sys.exit(1)

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")


def extract(url: str, extract_depth: str = 'basic') -> dict:
    """从 URL 提取内容"""
    if not TAVILY_API_KEY:
        print("错误: 请在 .env 文件中设置 TAVILY_API_KEY")
        sys.exit(1)

    url_api = 'https://api.tavily.com/extract'
    data = {'urls': [url], 'extract_depth': extract_depth}
    headers = {'Authorization': f'Bearer {TAVILY_API_KEY}', 'Content-Type': 'application/json'}

    try:
        print(f"正在提取: {url}")
        response = requests.post(url_api, json=data, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return result
    except Exception as e:
        print(f"请求出错: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Tavily Extract - URL 内容提取')
    parser.add_argument('url', nargs='?', help='要提取的 URL')
    parser.add_argument('--extract-depth', '-d', choices=['basic', 'deep'], default='basic')
    parser.add_argument('--output', '-o', help='输出文件')
    parser.add_argument('--json', '-j', action='store_true')

    args = parser.parse_args()
    if not args.url:
        parser.print_help()
        sys.exit(1)

    results = extract(args.url, args.extract_depth)
    content = results.get('content', results.get('raw_content', results))

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(str(content))
        print(f"已保存到: {args.output}")
    elif args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print("\n" + "=" * 60)
        print(f"提取自: {args.url}")
        print("=" * 60)
        print("\n")
        print(content)


if __name__ == '__main__':
    main()
