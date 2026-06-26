#!/usr/bin/env python3
"""
fetch_iwencai_index.py - 使用 browser 工具获取同花顺问财指数数据

使用方式（由 generate_report.py 调用）：
1. browser navigate 到问财 URL
2. browser snapshot 获取页面内容
3. 解析 snapshot 提取数据
"""

import re
import json
from typing import Dict, Any, Optional, Tuple
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


def parse_index_from_snapshot(snapshot_text: str, index_name: str) -> Dict[str, Any]:
    """
    从 snapshot 文本中解析指数数据
    
    期望格式：
    - heading "上证指数 (000001)" [level=4]
    - generic [ref=e116]: 3957.05-49.50/-1.24%
    
    返回：
    {'point': 3957.05, 'change': -1.24}
    """
    # 模式 1：标准格式 - 点位 + 涨跌额/涨跌幅
    # 示例：3957.05-49.50/-1.24% 或 3957.05 -49.50 /-1.24%
    pattern1 = r'(\d{4}\.\d{2})\s*([+-]?\d+\.?\d*)\s*/\s*([+-]?\d+\.?\d*)\s*%'
    match = re.search(pattern1, snapshot_text)
    if match:
        point = float(match.group(1))
        change = float(match.group(3))
        return {'point': point, 'change': change}
    
    # 模式 2：宽松格式
    pattern2 = r'(\d{4}\.\d{2}).*?([+-]?\d+\.?\d*)\s*%'
    match = re.search(pattern2, snapshot_text)
    if match:
        point = float(match.group(1))
        change = float(match.group(2))
        return {'point': point, 'change': change}
    
    # 模式 3：带逗号格式 - 3,367.95 +0.99%
    pattern3 = rf'{index_name}.*?(\d{{1,3}},\d{{3}}\.\d{{2}})\s*([+-]?\d+\.?\d*)\s*%'
    match = re.search(pattern3, snapshot_text)
    if match:
        point_str = match.group(1).replace(',', '')
        point = float(point_str)
        change = float(match.group(2))
        return {'point': point, 'change': change}
    
    return {'point': None, 'change': None, 'error': '解析失败'}


def parse_sentiment_from_snapshot(snapshot_text: str) -> Dict[str, Optional[int]]:
    """
    从 snapshot 解析涨跌家数
    
    期望找到：
    - 上涨家数为 XXXX 家
    - 下跌家数为 XXXX 家
    
    返回：
    {'up': 1234, 'down': 4786}
    """
    result = {'up': None, 'down': None}
    
    # 解析上涨家数
    up_patterns = [
        r'上涨.*?为\s*(\d+)\s*家',
        r'上涨.*?:\s*(\d+)',
        r'上涨.*?\((\d+)\s*家\)',
    ]
    for pattern in up_patterns:
        match = re.search(pattern, snapshot_text, re.IGNORECASE)
        if match:
            result['up'] = int(match.group(1))
            break
    
    # 解析下跌家数
    down_patterns = [
        r'下跌.*?为\s*(\d+)\s*家',
        r'下跌.*?:\s*(\d+)',
        r'下跌.*?\((\d+)\s*家\)',
    ]
    for pattern in down_patterns:
        match = re.search(pattern, snapshot_text, re.IGNORECASE)
        if match:
            result['down'] = int(match.group(1))
            break
    
    return result


def fetch_indices_with_browser(browser_tool) -> Dict[str, Dict[str, Any]]:
    """
    使用 browser 工具获取所有指数数据
    
    Args:
        browser_tool: browser 工具对象（提供 navigate 和 snapshot 方法）
    
    Returns:
        {'shanghai': {...}, 'shenzhen': {...}, 'chinext': {...}}
    """
    results = {}
    
    for key, config in INDICES_CONFIG.items():
        name = config['name']
        query = config['query']
        url = build_iwencai_url(query)
        
        print(f"[INFO] 获取 {name} 数据...")
        
        try:
            # 导航
            browser_tool.navigate(targetUrl=url, timeoutMs=30000)
            
            # 获取 snapshot
            snapshot_result = browser_tool.snapshot(refs="aria", compact=True)
            snapshot_text = snapshot_result.get('content', '') if isinstance(snapshot_result, dict) else str(snapshot_result)
            
            # 解析
            data = parse_index_from_snapshot(snapshot_text, name)
            
            if data.get('point') is not None:
                print(f"[INFO] ✅ {name}: {data['point']} ({data['change']}%)")
            else:
                print(f"[WARN] ⚠ {name}: {data.get('error', '获取失败')}")
            
            results[key] = data
            
        except Exception as e:
            print(f"[ERROR] {name} 获取失败：{e}")
            results[key] = {'point': None, 'change': None, 'error': str(e)}
    
    return results


def fetch_sentiment_with_browser(browser_tool) -> Dict[str, Optional[int]]:
    """
    使用 browser 工具获取涨跌家数
    
    Args:
        browser_tool: browser 工具对象
    
    Returns:
        {'up': int, 'down': int}
    """
    # 获取上涨家数
    url_up = build_iwencai_url('A 股上涨家数')
    print(f"[INFO] 获取上涨家数...")
    
    try:
        browser_tool.navigate(targetUrl=url_up, timeoutMs=30000)
        snapshot_up = browser_tool.snapshot(refs="aria", compact=True)
        snapshot_text_up = snapshot_up.get('content', '') if isinstance(snapshot_up, dict) else str(snapshot_up)
        up_count = parse_sentiment_from_snapshot(snapshot_text_up).get('up')
        
        if up_count:
            print(f"[INFO] ✅ 上涨家数：{up_count}家")
        else:
            print(f"[WARN] ⚠ 上涨家数：解析失败")
    except Exception as e:
        print(f"[ERROR] 上涨家数获取失败：{e}")
        up_count = None
    
    # 获取下跌家数
    url_down = build_iwencai_url('A 股下跌家数')
    print(f"[INFO] 获取下跌家数...")
    
    try:
        browser_tool.navigate(targetUrl=url_down, timeoutMs=30000)
        snapshot_down = browser_tool.snapshot(refs="aria", compact=True)
        snapshot_text_down = snapshot_down.get('content', '') if isinstance(snapshot_down, dict) else str(snapshot_down)
        down_count = parse_sentiment_from_snapshot(snapshot_text_down).get('down')
        
        if down_count:
            print(f"[INFO] ✅ 下跌家数：{down_count}家")
        else:
            print(f"[WARN] ⚠ 下跌家数：解析失败")
    except Exception as e:
        print(f"[ERROR] 下跌家数获取失败：{e}")
        down_count = None
    
    return {'up': up_count, 'down': down_count}


# 以下为独立测试代码
def _mock_browser_tool():
    """模拟 browser 工具（用于测试解析逻辑）"""
    class MockBrowser:
        def navigate(self, targetUrl, timeoutMs):
            print(f"[MOCK] navigate: {targetUrl}")
            return True
        
        def snapshot(self, refs="aria", compact=True):
            # 模拟 snapshot 数据
            return {
                'content': '''
                heading "上证指数 (000001)" [level=4]
                generic [ref=e116]: 3367.95-20.50/-0.61%
                '''
            }
    
    return MockBrowser()


if __name__ == '__main__':
    # 测试解析逻辑
    print("=" * 60)
    print("测试指数数据解析")
    print("=" * 60)
    
    test_snapshots = [
        ("3367.95-20.50/-0.61%", "标准格式"),
        ("3,367.95 +0.99%", "带逗号格式"),
        ("3367.95 -0.61%", "宽松格式"),
    ]
    
    for snapshot, desc in test_snapshots:
        result = parse_index_from_snapshot(snapshot, "上证指数")
        print(f"{desc}: {result}")
    
    print("\n" + "=" * 60)
    print("测试涨跌家数解析")
    print("=" * 60)
    
    test_sentiment = "上涨家数为 1234 家，下跌家数为 4786 家"
    result = parse_sentiment_from_snapshot(test_sentiment)
    print(f"输入：{test_sentiment}")
    print(f"输出：{result}")
