#!/usr/bin/env python3
"""
V2EX 热门获取脚本
V2EX Hot Topics Fetcher
"""

import json
import sys
from datetime import datetime

def get_v2ex_hot(limit=10, node=None):
    """获取 V2EX 热门（模拟数据）"""
    mock_topics = [
        {"id": 1, "title": "2026 年该学什么编程语言？", "node": "programmer", "replies": 234, "author": "dev123", "url": "https://v2ex.com/t/1"},
        {"id": 2, "title": "MacBook Pro M4 值得买吗？", "node": "apple", "replies": 189, "author": "macfan", "url": "https://v2ex.com/t/2"},
        {"id": 3, "title": "远程办公两年后的感受", "node": "career", "replies": 176, "author": "remote_dev", "url": "https://v2ex.com/t/3"},
        {"id": 4, "title": "推荐几个好用的 VS Code 插件", "node": "programmer", "replies": 156, "author": "vscoder", "url": "https://v2ex.com/t/4"},
        {"id": 5, "title": "大家都在用什么机械键盘？", "node": "hardware", "replies": 143, "author": "keyboard_lover", "url": "https://v2ex.com/t/5"},
        {"id": 6, "title": "求推荐一个靠谱的云服务器", "node": "host", "replies": 132, "author": "cloud_user", "url": "https://v2ex.com/t/6"},
        {"id": 7, "title": "AI 编程助手对比：Cursor vs Copilot", "node": "programmer", "replies": 128, "author": "ai_coder", "url": "https://v2ex.com/t/7"},
        {"id": 8, "title": "iOS 18 体验报告", "node": "apple", "replies": 115, "author": "ios_dev", "url": "https://v2ex.com/t/8"},
        {"id": 9, "title": "独立开发者如何获取第一批用户？", "node": "creative", "replies": 98, "author": "indie_dev", "url": "https://v2ex.com/t/9"},
        {"id": 10, "title": "北京程序员租房经验分享", "node": "life", "replies": 87, "author": "beijing_dev", "url": "https://v2ex.com/t/10"},
    ]
    
    if node:
        mock_topics = [t for t in mock_topics if t["node"] == node]
    
    return mock_topics[:limit]

def format_output(data):
    output = "💬 V2EX 今日热门\n\n"
    for item in data:
        output += f"{item['id']}. {item['title']}\n"
        output += f"   📂 {item['node']} | 💬 {item['replies']} | @{item['author']}\n\n"
    return output

def main():
    limit = 10
    node = None
    
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)
        elif arg not in ["--json", "-j"]:
            node = arg
    
    data = get_v2ex_hot(limit=limit, node=node)
    
    if "--json" in sys.argv or "-j" in sys.argv:
        print(json.dumps({"data": data}, ensure_ascii=False, indent=2))
    else:
        print(format_output(data))

if __name__ == "__main__":
    main()
