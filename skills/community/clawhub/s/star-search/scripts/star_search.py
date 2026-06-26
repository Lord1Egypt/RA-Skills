#!/usr/bin/env python3
"""
Star Search - 百度搜索 via Camofox REST API
无需 API Key，免费绕过验证码
"""

import sys
import urllib.parse
import subprocess
import re
import json
import argparse
import time


def search(query, num=10, camofox_url="http://localhost:9377"):
    """通过 Camofox + 百度搜索"""
    
    # 1. 创建 tab
    tab_resp = subprocess.run([
        'curl', '-s', '-X', 'POST', 
        f'{camofox_url}/tabs',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({
            "userId": "star-search",
            "sessionKey": f"sess_{int(time.time())}",
            "url": f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}"
        })
    ], capture_output=True, text=True, timeout=15)
    
    try:
        tab_data = json.loads(tab_resp.stdout)
        tab_id = tab_data.get('tabId')
        if not tab_id:
            print(f"Error: Failed to create tab - {tab_data}")
            return []
    except json.JSONDecodeError:
        print(f"Error: Invalid response from Camofox")
        return []
    
    # 2. 等待页面加载
    time.sleep(3)
    
    # 3. 获取 snapshot
    snap_resp = subprocess.run([
        'curl', '-s', 
        f'{camofox_url}/tabs/{tab_id}/snapshot',
        '-G', '--data-urlencode', 'userId=star-search'
    ], capture_output=True, text=True, timeout=15)
    
    data = snap_resp.stdout
    if not data:
        print("Error: No snapshot received")
        return []
    
    # 4. 提取结果 - h3 headings
    pattern = r'heading "([^"]+)" \[level=3\]:.*?/url: (http://www\.baidu\.com/link\?url=[^\s\)]+)'
    matches = re.findall(pattern, data, re.DOTALL)
    
    results = []
    for title, url in matches[:num]:
        title = title.strip()[:100]
        results.append({'title': title, 'url': url})
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Star Search - 百度搜索 via Camofox')
    parser.add_argument('query', nargs='+', help='搜索关键词')
    parser.add_argument('-n', '--num', type=int, default=10, help='结果数量')
    parser.add_argument('--camofox', default='http://localhost:9377', help='Camofox URL')
    args = parser.parse_args()
    
    query = ' '.join(args.query)
    
    print(f"🔍 搜索: {query}")
    print(f"   引擎: 百度 + Camofox")
    print("-" * 60)
    
    results = search(query, args.num, args.camofox)
    
    if not results:
        print("未找到结果，请确认 Camofox 已启动:")
        print("  cd /tmp/camofox-browser && npm start")
        return
    
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   {r['url']}")
        print()
    
    print(f"共 {len(results)} 条结果")


if __name__ == "__main__":
    main()
