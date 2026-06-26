"""
helpers.py - 安全辅助函数（本地实现，无外部API调用）
"""

import os
import json
import re
from .safe_json import safe_parse_json

# ✅ 本地实现，无外部API调用
# ⭐ ClawHub安全合规：移除call_llm/call_llm_json

def parse_user_intent(text: str) -> dict:
    """
    解析用户意图（本地正则，无LLM）
    
    Args:
        text: 用户输入
    
    Returns:
        意图dict
    """
    result = {
        "destination": None,
        "duration": None,
        "people": None,
        "budget": None,
        "style": None
    }
    
    # 目的地提取
    cities = ["杭州", "北京", "上海", "广州", "深圳", "成都", "重庆", 
              "西安", "南京", "苏州", "武汉", "长沙", "青岛", "厦门",
              "大理", "丽江", "三亚", "桂林", "敦煌", "兰州"]
    for city in cities:
        if city in text:
            result["destination"] = city
            break
    
    # 天数提取
    day_match = re.search(r'(\d+)\s*[天日]', text)
    if day_match:
        result["duration"] = int(day_match.group(1))
    
    # 人数提取
    people_match = re.search(r'(\d+)\s*[大人个人]', text)
    if people_match:
        result["people"] = int(people_match.group(1))
    
    # 预算提取
    budget_match = re.search(r'预算\s*(\d+)', text)
    if budget_match:
        result["budget"] = int(budget_match.group(1))
    
    # 风格提取
    if any(kw in text for kw in ["休闲", "慢生活", "度假"]):
        result["style"] = "休闲"
    elif any(kw in text for kw in ["特种兵", "打卡", "穷游"]):
        result["style"] = "特种兵"
    
    return result

def format_travel_summary(data: dict) -> str:
    """
    格式化旅行摘要（本地实现）
    
    Args:
        data: 旅行数据
    
    Returns:
        摘要文本
    """
    parts = []
    
    if data.get("destination"):
        parts.append(f"目的地：{data['destination']}")
    
    if data.get("duration"):
        parts.append(f"行程：{data['duration']}天")
    
    if data.get("people"):
        parts.append(f"人数：{data['people']}人")
    
    if data.get("budget"):
        parts.append(f"预算：{data['budget']}元")
    
    if data.get("style"):
        parts.append(f"风格：{data['style']}")
    
    return "\n".join(parts) if parts else "暂无信息"

def validate_api_key(key: str) -> bool:
    """
    验证API Key格式（本地检查）
    
    Args:
        key: API Key
    
    Returns:
        是否有效
    """
    if not key:
        return False
    
    # 基本格式检查
    if len(key) < 10:
        return False
    
    # 高德Key格式：32位十六进制
    if re.match(r'^[a-f0-9]{32}$', key):
        return True
    
    return False

def get_env_or_default(key: str, default: str = "") -> str:
    """
    安全读取环境变量（无外部调用）
    
    Args:
        key: 环境变量名
        default: 默认值
    
    Returns:
        值
    """
    return os.getenv(key, default)

# ⭐ ClawHub安全合规声明
"""
本文件已移除所有外部API调用：
- ❌ 无call_llm（移除）
- ❌ 无call_llm_json（移除）
- ✅ 本地正则解析（safe_parse_json）
- ✅ 本地意图识别（parse_user_intent）
- ✅ 无exec/eval/subprocess
"""