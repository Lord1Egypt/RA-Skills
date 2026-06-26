#!/usr/bin/env python3
"""
全网搜索工具 - 孙永乐开发的搜索接口
支持自然语言搜索，返回结构化结果
"""

import json
import requests
import sys
import argparse
import os

# 搜索接口配置
DEFAULT_SEARCH_URL = "https://49srjp57sf.coze.site/run"
DEFAULT_SEARCH_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0MWIxZTA3LWU0NjgtNGVkNS05ZGIwLWY0NjViMGQ5MmU4ZiJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIk5uZUN2TGgwaGl4RHFuNlk4ZTJ2YnI2aEFZenJWd1JIIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzcyNjAxMTEwLCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjEzMjU3NTc2OTE4MDI0MjMzIiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjEzMjYzNzk4ODE1Njg2NzA4In0.B5SHufj3jzhI54uc3218woi1KS6606Wg6Lelj6fK11rTQK8AibKkgjitbp1guhZNE8TpPyE-nFPH9cKYHL8G94t_2V0u3TbOw6na1AgbGKEQTpyokI_7QDqwIM0o82P8VLl_cYfpHbuglhS39MTt7gw8UI2LgdAaDC8QfoZwKJZ3CQvslOrOqf2bxxSTZ7XOpizB4ShajdbbvzJywCe3EjUh6rYvJEx_i_HPBM--APB09yMUVCzQrYdo5MTrkf4ZMK-Hej3huJJXkBwX0B-symujbxJLCi5EckAoP7uQLIuna_W6JypCtb7SdofJkK3oFYgek9iYg9DlKiC1TC-BGg"

# 从环境变量读取配置（如果有）
SEARCH_URL = os.environ.get("UNIVERSAL_SEARCH_URL", DEFAULT_SEARCH_URL)
SEARCH_TOKEN = os.environ.get("UNIVERSAL_SEARCH_TOKEN", DEFAULT_SEARCH_TOKEN)

SEARCH_HEADERS = {
    "Authorization": f"Bearer {SEARCH_TOKEN}",
    "Content-Type": "application/json",
}


def search(query, timeout=120):
    """
    执行全网搜索
    
    Args:
        query: 搜索关键词或问题
        timeout: 超时时间（秒）
    
    Returns:
        搜索结果（JSON格式）
    """
    payload = {
        "query": query
    }
    
    try:
        response = requests.post(
            SEARCH_URL, 
            headers=SEARCH_HEADERS, 
            json=payload, 
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"搜索错误: {e}", file=sys.stderr)
        return None


def print_summary(result):
    """打印搜索摘要"""
    if not result:
        return
    
    if "final_answer" in result:
        print("\n" + "="*80)
        print("📊 搜索结果摘要")
        print("="*80)
        print(result["final_answer"])
    
    if "verified_results" in result:
        print("\n" + "="*80)
        print("🔍 验证结果")
        print("="*80)
        for i, verified in enumerate(result["verified_results"], 1):
            print(f"\n[{i}] 可信度: ⭐ {verified.get('credibility_score', 'N/A')}/10")
            print(f"    来源: {verified.get('source_name', 'N/A')}")
            print(f"    原因: {verified.get('reason', 'N/A')}")
            content = verified.get('content', '')
            if len(content) > 200:
                content = content[:200] + "..."
            print(f"    内容: {content}")


def main():
    parser = argparse.ArgumentParser(description='全网搜索工具')
    parser.add_argument('query', nargs='+', help='搜索关键词或问题')
    parser.add_argument('--timeout', type=int, default=120, help='超时时间（秒）')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')
    
    args = parser.parse_args()
    query = ' '.join(args.query)
    
    print(f"🔍 正在搜索: {query}")
    print("请稍候，这可能需要一些时间...\n")
    
    result = search(query, args.timeout)
    
    if result:
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_summary(result)
    else:
        print("❌ 搜索失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
