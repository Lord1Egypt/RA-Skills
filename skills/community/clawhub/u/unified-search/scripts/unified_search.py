#!/usr/bin/env python3
"""
统一搜索脚本 - 智能融合百度和 DuckDuckGo
中文查询用百度，英文查询用 DDG，加密货币用 CoinGecko
"""
import sys
import io
import json
import re
import os

# 修复 Windows 控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加脚本路径以便导入
baidu_script_path = os.path.join(os.path.dirname(__file__))
if baidu_script_path not in sys.path:
    sys.path.insert(0, baidu_script_path)

def is_chinese_query(query):
    """判断是否为中文查询"""
    return any('\u4e00' <= char <= '\u9fff' for char in query)

def is_crypto_query(query):
    """判断是否是加密货币相关查询"""
    crypto_keywords = ['btc', 'bitcoin', '比特币', 'eth', 'ethereum', '以太坊',
                       'crypto', '加密货币', '价格', 'price', '行情']
    query_lower = query.lower()
    return any(kw in query_lower for kw in crypto_keywords)

def search_with_smart_script(query):
    """使用智能搜索脚本（支持加密货币和百度）"""
    try:
        import subprocess
        script_path = os.path.join(baidu_script_path, 'smart_search.py')
        result = subprocess.run(
            [sys.executable, script_path, query],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"智能搜索失败: {e}", file=sys.stderr)
    return []

def search_with_ddg(query):
    """使用 DuckDuckGo 搜索"""
    try:
        import subprocess
        ddg_path = os.path.join(
            os.path.dirname(os.path.dirname(baidu_script_path)),
            'ddg-search', 'scripts', 'ddg_search.py'
        )
        result = subprocess.run(
            [sys.executable, ddg_path, query],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            results = json.loads(result.stdout)
            # 添加来源标记
            for r in results:
                r['source'] = 'DuckDuckGo'
            return results
    except Exception as e:
        print(f"DDG搜索失败: {e}", file=sys.stderr)
    return []

def unified_search(query):
    """统一搜索入口"""
    print(f"🔍 统一搜索: {query}", file=sys.stderr)
    
    # 1. 检查是否是加密货币查询
    if is_crypto_query(query):
        print("检测到加密货币查询，使用智能搜索...", file=sys.stderr)
        results = search_with_smart_script(query)
        if results:
            return results
    
    # 2. 判断语言类型
    if is_chinese_query(query):
        print("检测到中文查询，使用百度搜索...", file=sys.stderr)
        results = search_with_smart_script(query)
        if results:
            return results
        # 百度失败，降级到 DDG
        print("百度搜索失败，尝试 DuckDuckGo...", file=sys.stderr)
        return search_with_ddg(query)
    else:
        print("检测到英文查询，使用 DuckDuckGo...", file=sys.stderr)
        results = search_with_ddg(query)
        if results:
            return results
        # DDG 失败，降级到百度
        print("DuckDuckGo 搜索失败，尝试百度...", file=sys.stderr)
        return search_with_smart_script(query)

def print_results_formatted(results):
    """格式化输出结果"""
    if not results:
        print("未找到搜索结果")
        return
        
    for i, result in enumerate(results, 1):
        if 'error' in result:
            print(f"❌ {result['error']}")
            if 'suggestion' in result:
                print(f"💡 {result['suggestion']}")
            continue
            
        source = result.get('source', '')
        source_tag = f" [{source}]" if source else ""
        
        print(f"\n{i}. {result.get('title', '无标题')}{source_tag}")
        if result.get('url'):
            print(f"   🔗 {result['url']}")
        if result.get('snippet'):
            snippet = result['snippet'][:250] + ('...' if len(result['snippet']) > 250 else '')
            print(f"   📝 {snippet}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Please provide a search query"}))
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    results = unified_search(query)
    
    if '--format' in sys.argv or '-f' in sys.argv:
        print_results_formatted(results)
    else:
        print(json.dumps(results, ensure_ascii=False))
