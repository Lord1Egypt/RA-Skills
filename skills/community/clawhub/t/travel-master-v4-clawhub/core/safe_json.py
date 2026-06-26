"""
safe_json.py - 安全JSON解析器（本地实现，无外部API）
"""

import re
import json

def safe_parse_json(text: str, default=None):
    """
    安全解析JSON（本地正则提取，无LLM调用）
    
    Args:
        text: 输入文本
        default: 默认返回值
    
    Returns:
        解析后的dict/list或default
    """
    if not text:
        return default or {}
    
    try:
        # 尝试直接解析
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # 正则提取JSON块
    patterns = [
        r'\{[^{}]*\}',  # 单层对象
        r'\[[^\[\]]*\]',  # 单层数组
        r'\{.*?\}',  # 跨层对象
        r'\[.*?\]'  # 跨层数组
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
    
    return default or {}

def extract_key_value(text: str, key: str):
    """
    提取键值（本地正则）
    
    Args:
        text: 输入文本
        key: 键名
    
    Returns:
        值或None
    """
    pattern = rf'{key}["\s:=]+(["\']?)([^"\',\s\]}]+)\1'
    match = re.search(pattern, text)
    if match:
        return match.group(2)
    return None

def is_valid_json(text: str) -> bool:
    """检查是否为有效JSON"""
    try:
        json.loads(text)
        return True
    except:
        return False