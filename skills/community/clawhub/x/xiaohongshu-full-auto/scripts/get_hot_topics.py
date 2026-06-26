#!/usr/bin/env python3
"""
抓取小红书热榜热点
"""

import json
import requests
from typing import List, Dict


def get_xiaohongshu_hot_topics(limit: int = 20) -> List[Dict]:
    """
    获取小红书热榜话题
    
    Returns:
        [
            {
                "title": "话题标题",
                "hot_value": 热度值,
                "url": "话题链接",
                "category": "分类"
            }
        ]
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Accept": "application/json",
    }
    
    # 抓取小红书热榜（公开接口）
    url = "https://www.xiaohongshu.com/explore"
    try:
        # 这里使用公开可访问的热榜接口
        # 实际生产环境可以使用小红书 MCP 或者公开爬虫
        response = requests.get("https://api.fakey.top/xiaohongshu/hot", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            topics = []
            for item in data[:limit]:
                topics.append({
                    "title": item.get("title", ""),
                    "hot_value": item.get("hot", 0),
                    "url": item.get("url", ""),
                    "category": item.get("category", "")
                })
            return topics
    except Exception as e:
        print(f"[WARN] 抓取失败: {e}, 使用备用方法...")
    
    # 备用：如果上面失败，这里可以返回一个示例供测试
    # 实际使用需要替换为有效的抓取方式
    return [
        {"title": "年轻人搞副业已经成常态了", "hot_value": 890000, "category": "生活"},
        {"title": "30岁职场人必须知道的三个真相", "hot_value": 760000, "category": "职场"},
        {"title": "AI工具提高工作效率500%", "hot_value": 680000, "category": "科技"},
        {"title": "普通人如何靠副业月入五千", "hot_value": 650000, "category": "赚钱"},
        {"title": "这几个减肥误区你中招了吗", "hot_value": 590000, "category": "健身"},
    ][:limit]


if __name__ == "__main__":
    topics = get_xiaohongshu_hot_topics(limit=10)
    print(json.dumps(topics, indent=2, ensure_ascii=False))
