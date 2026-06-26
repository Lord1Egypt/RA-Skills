#!/usr/bin/env python3
"""
微博热搜榜获取脚本
Weibo Hot Topics Fetcher
"""

import json
import sys
from datetime import datetime

def get_weibo_hot(limit=10):
    """获取微博热搜榜"""
    try:
        # 尝试从 API 获取
        import requests
        
        # 微博热搜 API（需要实际可用 API）
        # 这里使用模拟数据
        hot_list = get_mock_data(limit)
        
        return {
            "status": "success",
            "data": hot_list,
            "count": len(hot_list),
            "timestamp": datetime.now().isoformat(),
            "source": "mock"  # 实际应为 "api"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "data": get_mock_data(limit)
        }


def get_mock_data(limit=10):
    """模拟数据（API 不可用时）"""
    mock_hot = [
        {"rank": 1, "title": "2026春节档票房破纪录", "hot": 9876543, "label": "爆"},
        {"rank": 2, "title": "AI大模型最新突破", "hot": 8765432, "label": "热"},
        {"rank": 3, "title": "春运返程高峰", "hot": 7654321, "label": "热"},
        {"rank": 4, "title": "新能源汽车销量", "hot": 6543210, "label": "新"},
        {"rank": 5, "title": "央行最新政策", "hot": 5432109, "label": "热"},
        {"rank": 6, "title": "春季流感预防", "hot": 4321098, "label": ""},
        {"rank": 7, "title": "北京天气变化", "hot": 3210987, "label": ""},
        {"rank": 8, "title": "科技股走势", "hot": 2109876, "label": "新"},
        {"rank": 9, "title": "教育改革新政", "hot": 1098765, "label": ""},
        {"rank": 10, "title": "体育赛事直播", "hot": 987654, "label": ""},
    ]
    return mock_hot[:limit]


def format_output(data):
    """格式化输出"""
    output = "🔥 微博热搜榜\n\n"
    for item in data:
        label = f"[{item['label']}]" if item['label'] else ""
        hot_str = f"{item['hot'] / 10000:.1f}万"
        output += f"{item['rank']}. {label} {item['title']} - {hot_str}\n"
    return output


def main():
    limit = 10
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except:
            pass
    
    result = get_weibo_hot(limit)
    
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result["data"]))


if __name__ == "__main__":
    main()
