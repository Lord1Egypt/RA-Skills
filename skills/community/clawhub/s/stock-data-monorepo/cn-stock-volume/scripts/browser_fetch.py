#!/usr/bin/env python3
"""
browser_fetch.py - 使用 OpenClaw browser 工具获取同花顺问财数据

提供函数：
- fetch_index_data(index_name): 获取指数数据
- fetch_sentiment_data(): 获取涨跌家数数据

注意：此脚本通过 subprocess 调用 OpenClaw CLI 来使用 browser 工具
"""

import json
import re
import sys
import subprocess
import os
from typing import Dict, Any, Optional, Tuple

# 问财 URL 配置
IWENCAI_BASE_URL = "https://www.iwencai.com/unifiedwap/result"

INDEX_QUERIES = {
    'shanghai': '上证指数',
    'shenzhen': '深证成指',
    'chinext': '创业板指',
}

SENTIMENT_QUERIES = {
    'up': 'A 股上涨家数',
    'down': 'A 股下跌家数',
}


def browser_navigate(url: str, timeout_ms: int = 30000) -> Tuple[bool, Optional[str]]:
    """
    使用 OpenClaw browser 工具导航到 URL
    
    Returns:
        (success, targetId): 导航是否成功，以及页面 targetId
    """
    try:
        # 尝试多种 openclaw 命令路径
        commands_to_try = [
            ['openclaw', 'browser', 'navigate', '--url', url],
            ['npx', 'openclaw', 'browser', 'navigate', '--url', url],
            ['node', '/usr/local/lib/node_modules/openclaw/dist/cli.js', 'browser', 'navigate', '--url', url],
        ]
        
        for cmd in commands_to_try:
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout_ms // 1000,
                    env={**os.environ, 'PATH': '/usr/local/bin:/usr/bin:/bin:' + os.environ.get('PATH', '')}
                )
                
                if result.returncode == 0:
                    # 解析输出获取 targetId
                    output = result.stdout.strip()
                    # 尝试从输出中提取 targetId（JSON 格式或纯文本）
                    if 'targetId' in output:
                        match = re.search(r'targetId["\s:]+([A-F0-9]+)', output, re.IGNORECASE)
                        if match:
                            return True, match.group(1)
                    return True, None
                else:
                    print(f"[DEBUG] 命令 {' '.join(cmd[:3])} 失败：{result.stderr[:100]}")
            except FileNotFoundError:
                continue
        
        print(f"[ERROR] 所有 openclaw 命令路径均失败")
        return False, None
        
    except Exception as e:
        print(f"[ERROR] browser navigate 异常：{e}")
        return False, None


def browser_snapshot(target_id: str = None, refs: str = "aria", timeout_ms: int = 10000) -> Optional[str]:
    """
    使用 OpenClaw browser 工具获取页面 snapshot
    
    Returns:
        snapshot 文本内容，失败返回 None
    """
    try:
        cmd = ['openclaw', 'browser', 'snapshot', '--refs', refs]
        if target_id:
            cmd.extend(['--target-id', target_id])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_ms // 1000
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"[ERROR] browser snapshot 失败：{result.stderr}")
            return None
    except Exception as e:
        print(f"[ERROR] browser snapshot 异常：{e}")
        return None


def build_iwencai_url(query: str) -> str:
    """构建同花顺问财 URL"""
    # URL encode the query
    from urllib.parse import quote
    encoded_query = quote(query)
    return f"{IWENCAI_BASE_URL}?w={encoded_query}&querytype=zhishu"


def parse_index_snapshot(snapshot_text: str, index_name: str) -> Dict[str, Any]:
    """
    解析指数数据 snapshot
    
    期望格式（aria snapshot）：
    heading "上证指数 (000001)" [level=4]
    generic [ref=e116]: 3957.05-49.50/-1.24%
    
    返回：
    {'point': 3957.05, 'change': -1.24}
    """
    # 模式 1：标准格式 - 点位 + 涨跌额/涨跌幅
    # 示例：3957.05-49.50/-1.24% 或 3957.05 -49.50 /-1.24%
    pattern1 = r'(\d{4}\.\d{2})\s*([+-]?\d+\.?\d*)\s*/\s*([+-]?\d+\.?\d*)\s*%'
    match = re.search(pattern1, snapshot_text)
    if match:
        point = float(match.group(1))
        change = float(match.group(3))  # 涨跌幅
        return {'point': point, 'change': change}
    
    # 模式 2：宽松格式 - 只提取点位和涨跌幅
    pattern2 = r'(\d{4}\.\d{2}).*?([+-]?\d+\.?\d*)\s*%'
    match = re.search(pattern2, snapshot_text)
    if match:
        point = float(match.group(1))
        change = float(match.group(2))
        return {'point': point, 'change': change}
    
    # 模式 3：查找包含指数名称的行
    # 示例：上证指数 3,367.95 +0.99%
    pattern3 = rf'{index_name}.*?(\d{{1,3}},?\d{{3}}\.\d{{2}})\s*([+-]?\d+\.?\d*)\s*%'
    match = re.search(pattern3, snapshot_text)
    if match:
        point_str = match.group(1).replace(',', '')
        point = float(point_str)
        change = float(match.group(2))
        return {'point': point, 'change': change}
    
    return {'point': None, 'change': None, 'error': '解析失败'}


def parse_sentiment_snapshot(snapshot_text: str, data_type: str) -> Dict[str, Any]:
    """
    解析涨跌家数 snapshot
    
    期望格式：
    上涨家数为 1234 家
    下跌家数为 4785 家
    
    或：
    上涨家数：1234
    下跌家数：4785
    
    返回：
    {'count': 1234}
    """
    # 模式 1：标准格式 - "XX 家数为 XXXX 家"
    pattern1 = rf'{data_type}.*?为\s*(\d+)\s*家'
    match = re.search(pattern1, snapshot_text, re.IGNORECASE)
    if match:
        return {'count': int(match.group(1))}
    
    # 模式 2：冒号格式 - "XX 家数：XXXX"
    pattern2 = rf'{data_type}\s*:\s*(\d+)'
    match = re.search(pattern2, snapshot_text, re.IGNORECASE)
    if match:
        return {'count': int(match.group(1))}
    
    # 模式 3：括号格式 - "上涨 (1234 家)"
    pattern3 = rf'{data_type}.*?\((\d+)\s*家\)'
    match = re.search(pattern3, snapshot_text, re.IGNORECASE)
    if match:
        return {'count': int(match.group(1))}
    
    # 模式 4：宽松匹配 - 查找数字 + 家
    pattern4 = r'(\d+)\s*家'
    matches = re.findall(pattern4, snapshot_text)
    if matches:
        return {'count': int(matches[0])}
    
    return {'count': None, 'error': '解析失败'}


def fetch_index_data(index_key: str, index_name: str, use_cache: bool = True) -> Dict[str, Any]:
    """
    获取指数数据
    
    Args:
        index_key: 索引键（shanghai/shenzhen/chinext）
        index_name: 指数名称（中文）
        use_cache: 是否使用缓存（避免重复请求）
    
    Returns:
        {'point': float, 'change': float} 或 {'point': None, 'change': None, 'error': str}
    """
    query = INDEX_QUERIES.get(index_key, index_name)
    url = build_iwencai_url(query)
    
    print(f"[INFO] 获取 {index_name} 数据...")
    print(f"[DEBUG] URL: {url}")
    
    # 导航到页面
    success, target_id = browser_navigate(url, timeout_ms=30000)
    if not success:
        return {'point': None, 'change': None, 'error': '导航失败'}
    
    # 获取 snapshot
    snapshot = browser_snapshot(target_id=target_id, refs="aria", timeout_ms=10000)
    if not snapshot:
        return {'point': None, 'change': None, 'error': 'snapshot 获取失败'}
    
    # 解析数据
    result = parse_index_snapshot(snapshot, index_name)
    
    if 'error' in result:
        print(f"[WARN] {index_name} 解析失败，snapshot 片段：{snapshot[:200]}")
    
    return result


def fetch_sentiment_data(data_type: str, query: str) -> Dict[str, Any]:
    """
    获取涨跌家数数据
    
    Args:
        data_type: 数据类型（上涨家数/下跌家数）
        query: 查询语句
    
    Returns:
        {'count': int} 或 {'count': None, 'error': str}
    """
    url = build_iwencai_url(query)
    
    print(f"[INFO] 获取 {data_type} 数据...")
    print(f"[DEBUG] URL: {url}")
    
    # 导航到页面
    success, target_id = browser_navigate(url, timeout_ms=30000)
    if not success:
        return {'count': None, 'error': '导航失败'}
    
    # 获取 snapshot
    snapshot = browser_snapshot(target_id=target_id, refs="aria", timeout_ms=10000)
    if not snapshot:
        return {'count': None, 'error': 'snapshot 获取失败'}
    
    # 解析数据
    result = parse_sentiment_snapshot(snapshot, data_type)
    
    if 'error' in result:
        print(f"[WARN] {data_type} 解析失败，snapshot 片段：{snapshot[:200]}")
    
    return result


def fetch_all_with_browser(date: str = None) -> Dict[str, Any]:
    """
    使用浏览器获取所有数据
    
    Returns:
        完整数据字典
    """
    from datetime import datetime
    
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"[INFO] 开始获取 {date} 数据...")
    
    # 获取指数数据
    indices = {}
    for key, name in INDEX_QUERIES.items():
        result = fetch_index_data(key, name)
        indices[key] = result
        print(f"[DEBUG] {name}: {result}")
    
    # 获取涨跌家数
    sentiment = {}
    for key, query in SENTIMENT_QUERIES.items():
        result = fetch_sentiment_data(key, query)
        count = result.get('count')
        sentiment[key] = count
        print(f"[DEBUG] {key}: {count}")
    
    # 计算涨跌比
    up = sentiment.get('up')
    down = sentiment.get('down')
    
    if up is not None and down is not None and up > 0:
        ratio_value = down / up
        ratio = f"1:{ratio_value:.1f}"
        
        if up > down * 2:
            desc = "上涨显著多于下跌"
        elif down > up * 2:
            desc = "下跌显著多于上涨"
        else:
            desc = "涨跌相当"
    else:
        ratio = "待补充"
        desc = "待补充"
    
    sentiment['ratio'] = ratio
    sentiment['description'] = desc
    
    # 构建完整数据
    data = {
        'date': date,
        'indices': indices,
        'sentiment': sentiment,
        'volume': {
            'today': None,
            'previous': None,
        },
        '_from_cache': False,
        'dataSource': 'iwencai-browser',
        'manualDataRequired': [
            'volume.today',
            'volume.previous',
        ],
    }
    
    return data


def main():
    """命令行测试入口"""
    print("=" * 60)
    print("cn-stock-volume 浏览器调用测试")
    print("=" * 60)
    
    data = fetch_all_with_browser()
    
    print("\n" + "=" * 60)
    print("获取结果:")
    print("=" * 60)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
