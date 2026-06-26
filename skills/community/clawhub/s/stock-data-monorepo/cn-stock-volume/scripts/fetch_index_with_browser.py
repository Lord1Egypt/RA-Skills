#!/usr/bin/env python3
"""
fetch_index_with_browser.py - 使用 OpenClaw browser 工具获取指数数据

此脚本通过 sessions_spawn 调用 browser 工具，获取同花顺问财的指数数据。

使用方式：
    python3 fetch_index_with_browser.py [--date YYYY-MM-DD] [--json]

输出：
    JSON 格式数据，包含三大指数点位和涨跌幅
"""

import sys
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import quote


# 指数配置
INDICES_CONFIG = {
    'shanghai': {'name': '上证指数', 'query': '上证指数'},
    'shenzhen': {'name': '深证成指', 'query': '深证成指'},
    'chinext': {'name': '创业板指', 'query': '创业板指'},
}


def build_iwencai_url(query: str) -> str:
    """构建同花顺问财 URL"""
    encoded_query = quote(query)
    return f"https://www.iwencai.com/unifiedwap/result?w={encoded_query}&querytype=zhishu"


def parse_index_from_text(text: str, index_name: str) -> Dict[str, Any]:
    """从文本中解析指数数据"""
    # 模式 1：标准格式 - 3367.95-20.50/-0.61%
    pattern1 = r'(\d{4}\.\d{2})\s*([+-]?\d+\.?\d*)\s*/\s*([+-]?\d+\.?\d*)\s*%'
    match = re.search(pattern1, text)
    if match:
        point = float(match.group(1))
        change = float(match.group(3))
        return {'point': point, 'change': change}
    
    # 模式 2：带逗号 - 3,367.95 +0.99%
    pattern2 = r'(\d{1,3},\d{3}\.\d{2})\s*([+-]?\d+\.?\d*)\s*%'
    match = re.search(pattern2, text)
    if match:
        point_str = match.group(1).replace(',', '')
        point = float(point_str)
        change = float(match.group(2))
        return {'point': point, 'change': change}
    
    # 模式 3：简单格式 - 3367.95 -0.61%
    pattern3 = r'(\d{4}\.\d{2})\s*([+-]?\d+\.?\d*)\s*%'
    match = re.search(pattern3, text)
    if match:
        point = float(match.group(1))
        change = float(match.group(2))
        return {'point': point, 'change': change}
    
    return {'point': None, 'change': None}


def fetch_with_sessions_spawn(query: str, index_name: str) -> Dict[str, Any]:
    """
    通过 sessions_spawn 调用 browser 工具获取数据
    
    由于这是同步脚本，我们使用一个简化的方法：
    1. 创建一个临时 task 文件
    2. 使用 openclaw sessions_spawn 执行
    3. 解析输出
    
    但更简单的方法是直接返回占位符，让用户手动补充
    或者使用 web_fetch 工具获取页面内容
    """
    # 尝试使用 web_fetch 工具
    url = build_iwencai_url(query)
    
    try:
        # 使用 web_fetch 获取页面内容
        result = subprocess.run(
            ['openclaw', 'web-fetch', url, '--extractMode', 'text'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = parse_index_from_text(result.stdout, index_name)
            if data.get('point'):
                return data
    except Exception as e:
        pass
    
    return {'point': None, 'change': None, 'error': '获取失败'}


def fetch_all_indices() -> Dict[str, Dict[str, Any]]:
    """获取所有指数数据"""
    results = {}
    
    for key, config in INDICES_CONFIG.items():
        name = config['name']
        query = config['query']
        
        print(f"[INFO] 获取 {name} 数据...")
        
        # 使用 web_fetch 获取
        url = build_iwencai_url(query)
        
        try:
            # 尝试 web_fetch
            result = subprocess.run(
                ['openclaw', 'web-fetch', url, '--extractMode', 'text', '--maxChars', '5000'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout.strip():
                data = parse_index_from_text(result.stdout, name)
                if data.get('point'):
                    print(f"[INFO] ✅ {name}: {data['point']} ({data['change']}%)")
                    results[key] = data
                    continue
            
            print(f"[WARN] ⚠ {name}: web_fetch 未获取到有效数据")
            results[key] = {'point': None, 'change': None, 'error': 'web_fetch 失败'}
            
        except subprocess.TimeoutExpired:
            print(f"[ERROR] {name}: 超时")
            results[key] = {'point': None, 'change': None, 'error': '超时'}
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            results[key] = {'point': None, 'change': None, 'error': str(e)}
    
    return results


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='获取 A 股指数数据')
    parser.add_argument('--date', default=None, help='日期 (YYYY-MM-DD)')
    parser.add_argument('--json', action='store_true', help='仅输出 JSON')
    
    args = parser.parse_args()
    
    date = args.date or datetime.now().strftime('%Y-%m-%d')
    
    if not args.json:
        print("=" * 60)
        print(f"获取 A 股指数数据 | {date}")
        print("=" * 60)
    
    # 获取数据
    indices = fetch_all_indices()
    
    # 构建输出
    output = {
        'date': date,
        'indices': indices,
        'sentiment': {
            'up': None,
            'down': None,
            'ratio': '待补充',
            'description': '待补充'
        },
        'volume': {
            'today': None,
            'previous': None
        },
        '_from_cache': False,
        'dataSource': 'iwencai-web-fetch',
    }
    
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print("\n" + "=" * 60)
        print("结果:")
        print("=" * 60)
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
