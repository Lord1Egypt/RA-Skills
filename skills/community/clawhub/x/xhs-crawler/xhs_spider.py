#!/usr/bin/env python3
"""
小红书舆情爬虫 - 简易测试版
基于公开信息，仅供学习研究
"""

import json
import requests
import time

# 小红书搜索 API (网页版)
# 注意: 这些接口可能随时变化
XHS_SEARCH_URL = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.xiaohongshu.com/search_result",
}

def search_notes(keyword, page=1, page_size=20):
    """搜索小红书笔记"""
    
    payload = {
        "keyword": keyword,
        "page": page,
        "page_size": page_size,
        "search_id": f"search_{int(time.time() * 1000)}",
        "sort": "general",
        "note_type": 0,
    }
    
    try:
        response = requests.post(
            XHS_SEARCH_URL, 
            json=payload,
            headers=HEADERS,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"请求异常: {e}")
        return None


def parse_results(data):
    """解析搜索结果"""
    if not data or not data.get("data"):
        return []
    
    items = data.get("data", {}).get("items", [])
    results = []
    
    for item in items:
        note_card = item.get("note_card", {})
        if not note_card:
            continue
            
        result = {
            "title": note_card.get("title", ""),
            "desc": note_card.get("desc", ""),
            "user": note_card.get("user", {}).get("nickname", ""),
            "likes": note_card.get("liked_count", 0),
            "comments": note_card.get("comment_count", 0),
            "collects": note_card.get("collected_count", 0),
            "tags": [tag.get("name", "") for tag in note_card.get("tag_list", [])],
            "url": f"https://www.xiaohongshu.com/explore/{note_card.get('note_id', '')}",
        }
        results.append(result)
    
    return results


def analyze_sentiment(notes):
    """简单的情感分析 (基于点赞/评论比例)"""
    positive = 0
    neutral = 0
    negative = 0
    
    for note in notes:
        # 简单的启发式规则
        engagement = note.get("likes", 0) + note.get("comments", 0) + note.get("collects", 0)
        
        if engagement > 1000:
            positive += 1
        elif engagement > 100:
            neutral += 1
        else:
            negative += 1
    
    return {
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "total": len(notes)
    }


def main():
    """主函数"""
    # 测试关键词
    keywords = ["摩比爱识字", "摩比点读笔"]
    
    for keyword in keywords:
        print(f"\n{'='*50}")
        print(f"搜索关键词: {keyword}")
        print(f"{'='*50}")
        
        data = search_notes(keyword)
        
        if data:
            notes = parse_results(data)
            print(f"找到 {len(notes)} 条笔记:\n")
            
            for i, note in enumerate(notes[:10], 1):
                print(f"{i}. {note['title'][:50]}...")
                print(f"   👤 {note['user']} | 👍 {note['likes']} | 💬 {note['comments']} | ⭐ {note['collects']}")
                print(f"   🏷️ {', '.join(note['tags'][:3])}")
                print()
            
            # 舆情分析
            sentiment = analyze_sentiment(notes)
            print(f"📊 舆情分析:")
            print(f"   热度较高: {sentiment['positive']} 条")
            print(f"   热度一般: {sentiment['neutral']} 条")
            print(f"   热度较低: {sentiment['negative']} 条")
        else:
            print("未获取到数据，可能是接口变化或需要登录")
        
        time.sleep(2)  # 避免请求过快


if __name__ == "__main__":
    main()
