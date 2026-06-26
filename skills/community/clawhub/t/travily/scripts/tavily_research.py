#!/usr/bin/env python3
"""
Tavily Research API - 深度研究（带引用）
"""
import os
import sys
from pathlib import Path
import argparse
import json
import time

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


def research(input_text: str, model: str = 'mini', max_results: int = None) -> dict:
    """执行深度研究"""
    if not TAVILY_API_KEY:
        print("错误: 请在 .env 文件中设置 TAVILY_API_KEY")
        sys.exit(1)

    url = 'https://api.tavily.com/research'
    data = {'input': input_text, 'model': model}
    if max_results:
        data['max_results'] = max_results
    headers = {'Authorization': f'Bearer {TAVILY_API_KEY}', 'Content-Type': 'application/json'}

    try:
        print(f"正在研究: {input_text}")
        print(f"模型: {model}")
        print("这可能需要 30-120 秒...\n")

        response = requests.post(url, json=data, headers=headers, timeout=180)
        response.raise_for_status()
        result = response.json()

        if result.get('status') == 'pending':
            request_id = result.get('request_id')
            print("研究排队中，等待结果...")
            poll_url = f'https://api.tavily.com/research/{request_id}'
            attempt = 0
            while attempt < 60:
                time.sleep(2)
                poll_response = requests.get(poll_url, headers=headers, timeout=30)
                poll_result = poll_response.json()
                if poll_result.get('status') == 'completed':
                    return poll_result
                elif poll_result.get('status') == 'failed':
                    return poll_result
                attempt += 1
            print("\n等待超时。")
        return result
    except Exception as e:
        print(f"请求出错: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Tavily Research - 深度研究')
    parser.add_argument('topic', nargs='?', help='研究主题')
    parser.add_argument('--model', '-m', choices=['mini', 'pro', 'auto'], default='mini')
    parser.add_argument('--max-results', '-n', type=int)
    parser.add_argument('--output', '-o', help='输出文件')
    parser.add_argument('--json', '-j', action='store_true')

    args = parser.parse_args()
    if not args.topic:
        parser.print_help()
        sys.exit(1)

    results = research(args.topic, args.model, args.max_results)
    content = results.get('content', results.get('results', results))

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(str(content))
        print(f"已保存到: {args.output}")
    elif args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        if isinstance(content, dict):
            print("\n" + "=" * 60)
            print(f"研究: {args.topic}")
            print("=" * 60)
            if 'answer' in content:
                print("\n回答:\n")
                print(content['answer'])
            if 'sources' in content:
                print("\n来源:")
                for i, source in enumerate(content['sources'], 1):
                    print(f"  [{i}] {source}")
        else:
            print(content)


if __name__ == '__main__':
    main()
