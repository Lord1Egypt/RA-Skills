#!/usr/bin/env python3
"""
Soul Memory Module: Heartbeat Filter
v3.3.2 - 过滤 Heartbeat 自我报告，防止记忆污染

Author: Soul Memory System
Date: 2026-03-02
"""

import re
import json
from pathlib import Path
from typing import Tuple

# Heartbeat 过滤关键词
HEARTBEAT_FILTER_KEYWORDS = [
    "Heartbeat 自動提取",
    "Heartbeat 報告", 
    "蒙恬將軍邊防巡查",
    "記憶斥候回報",
    "烽火台檢查",
    "記憶邊防穩固",
    "Soul Memory Heartbeat 已成功發動",
    "Heartbeat 已成功啟動",
    "心跳自動提取",
    "檢視記憶檔案",
    "Soul Memory System.*運作分析報告",
]

# Heartbeat 过滤正则模式
HEARTBEAT_FILTER_PATTERNS = [
    r'🔥\s*\[.*?\].*?Heartbeat.*?自動提取',
    r'\*\*Heartbeat\s+摘要\*\*',
    r'##\s*\[.*?\]\s*.*?Heartbeat.*?自動提取',
    r'Soul Memory System.*?運作分析報告',
    r'蒙恬將軍.*?邊防巡查',
    r'記憶斥候回報',
    r'烽火台檢查',
]


def is_heartbeat_self_report(text: str) -> Tuple[bool, str]:
    """
    检查文本是否为 Heartbeat 自我报告
    
    Args:
        text: 要检查的文本
        
    Returns:
        Tuple[bool, str]: (是否为Heartbeat报告, 匹配的关键词)
    """
    if not text:
        return False, ""
    
    text_upper = text.upper()
    
    # 检查关键词
    for keyword in HEARTBEAT_FILTER_KEYWORDS:
        if keyword.upper() in text_upper:
            return True, f"keyword: {keyword}"
    
    # 检查正则模式
    for pattern in HEARTBEAT_FILTER_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            return True, f"pattern: {pattern}"
    
    # 额外检查：包含 "Heartbeat" + 特定动词组合
    heartbeat_indicators = ['自動提取', '報告', '巡查', '摘要', 'HEARTBEAT', '心跳']
    if 'HEARTBEAT' in text_upper or '心跳' in text or 'HEARTBEAT' in text:
        for indicator in heartbeat_indicators:
            if indicator.upper() in text_upper:
                return True, f"combo: HEARTBEAT + {indicator}"
    
    return False, ""


def should_filter_memory(user_query: str, assistant_response: str) -> Tuple[bool, str]:
    """
    检查是否应该过滤这条记忆
    
    Args:
        user_query: 用户查询
        assistant_response: 助手回复
        
    Returns:
        Tuple[bool, str]: (是否过滤, 原因)
    """
    # 检查用户查询
    is_hb_query, query_reason = is_heartbeat_self_report(user_query)
    if is_hb_query:
        return True, f"query contains Heartbeat: {query_reason}"
    
    # 检查助手回复
    is_hb_response, response_reason = is_heartbeat_self_report(assistant_response)
    if is_hb_response:
        return True, f"response contains Heartbeat: {response_reason}"
    
    return False, ""


class HeartbeatFilter:
    """Heartbeat 过滤器类"""
    
    def __init__(self, config_path: str = None):
        self.enabled = True
        self.filter_count = 0
        
        # 加载配置（如果存在）
        if config_path:
            config_file = Path(config_path)
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        self.enabled = config.get('enabled', True)
                except Exception as e:
                    print(f"⚠️ Heartbeat filter config load failed: {e}")
    
    def check(self, user_query: str, assistant_response: str) -> Tuple[bool, str]:
        """检查是否应该过滤"""
        if not self.enabled:
            return False, ""
        
        should_filter, reason = should_filter_memory(user_query, assistant_response)
        if should_filter:
            self.filter_count += 1
        return should_filter, reason
    
    def stats(self) -> dict:
        """返回过滤器统计"""
        return {
            "enabled": self.enabled,
            "total_filtered": self.filter_count
        }


# 便捷函数
def filter_heartbeat(user_query: str, assistant_response: str) -> Tuple[bool, str]:
    """便捷函数：过滤 Heartbeat"""
    return should_filter_memory(user_query, assistant_response)


if __name__ == "__main__":
    # 测试
    test_cases = [
        ("查看記憶", "🔥 [I] Heartbeat 自動提取..."),
        ("你好", "正常回復"),
        ("Heartbeat 報告", "系統運作正常"),
        ("邊防如何", "蒙恬將軍邊防巡查報告..."),
    ]
    
    print("🧪 Heartbeat Filter Test")
    print("=" * 50)
    
    for query, response in test_cases:
        should_filter, reason = filter_heartbeat(query, response)
        status = "🚫 FILTERED" if should_filter else "✅ PASSED"
        print(f"\nQuery: {query[:30]}...")
        print(f"Response: {response[:30]}...")
        print(f"Result: {status}")
        if should_filter:
            print(f"Reason: {reason}")
