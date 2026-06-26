#!/usr/bin/env python3
"""
format_output.py - 格式化多平台分发结果
接收JSON格式的平台输出，输出易读的格式化文本
"""

import json
import sys
from typing import Dict, List

def format_platform(platform: str, data: Dict) -> str:
    """格式化单个平台输出"""
    hashtags = " ".join(data.get("hashtags", []))
    
    lines = [
        f"\n{'='*50}",
        f"📱 {platform.upper()}",
        f"{'='*50}",
        f"\n📌 标题：{data.get('title', '')}",
        f"\n🎯 封面文案：{data.get('cover_suggestion', '')}",
        f"\n📝 正文：\n{data.get('body', '')}",
        f"\n🏷️ 标签：{hashtags}",
        f"\n⏰ 发布建议：{data.get('publish_tips', '')}",
    ]
    return "\n".join(lines)

def format_distributor_result(results: List[Dict]) -> str:
    """格式化完整分发结果"""
    output = [
        "\n" + "🔥"*25,
        "多平台分发结果",
        "🔥"*25,
    ]
    
    platform_icons = {
        "小红书": "📕",
        "抖音": "📱",
        "B站": "📺",
        "公众号": "📰"
    }
    
    for r in results:
        platform = r.get("platform", "")
        icon = platform_icons.get(platform, "📌")
        output.append(f"\n{icon} {platform}")
        output.append(format_platform(platform, r))
    
    return "\n".join(output)

if __name__ == "__main__":
    # 从stdin读取JSON
    try:
        data = json.load(sys.stdin)
        if isinstance(data, list):
            print(format_distributor_result(data))
        else:
            print(format_platform(data.get("platform", ""), data))
    except json.JSONDecodeError:
        print("Error: Invalid JSON input")
        sys.exit(1)
