#!/usr/bin/env python3
"""
Extract user insights from conversation text.
Analyzes messages to identify preferences, interests, and patterns.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Interest keywords mapping
INTEREST_CATEGORIES = {
    "technology": ["编程", "代码", "技术", "软件", "硬件", "AI", "人工智能", "区块链", "算法"],
    "finance": ["股票", "投资", "理财", "经济", "金融", "基金", "比特币", "加密货币"],
    "news": ["新闻", "局势", "政治", "国际", "军事", "战争", "冲突"],
    "sports": ["足球", "篮球", "体育", "运动", "健身", "跑步"],
    "entertainment": ["电影", "音乐", "游戏", "综艺", "娱乐", "明星"],
    "education": ["学习", "考试", "备考", "读书", "知识", "课程"],
    "travel": ["旅游", "旅行", "景点", "酒店", "机票"],
    "food": ["美食", "餐厅", "烹饪", "菜谱", "吃"],
    "health": ["健康", "医疗", "养生", "保健", "心理"]
}

def detect_interests(text: str) -> List[str]:
    """Detect user interests from text."""
    interests = []
    text_lower = text.lower()
    
    for category, keywords in INTEREST_CATEGORIES.items():
        for keyword in keywords:
            if keyword in text or keyword in text_lower:
                interests.append(category)
                break
    
    return list(set(interests))

def detect_preferences(text: str) -> Dict[str, Any]:
    """Detect communication preferences."""
    prefs = {}
    
    # Length preference
    if len(text) < 50:
        prefs["response_length"] = "concise"
    elif len(text) > 200:
        prefs["response_length"] = "detailed"
    
    # Tone indicators
    if any(word in text for word in ["哈哈", "😂", "😄", "有趣"]):
        prefs["tone"] = "casual"
    elif any(word in text for word in ["请", "谢谢", "麻烦"]):
        prefs["tone"] = "polite"
    
    # Directness
    if any(word in text for word in ["直接", "简洁", "简单说", "一句话"]):
        prefs["communication_style"] = "direct"
    elif any(word in text for word in ["详细", "展开", "具体", "解释"]):
        prefs["communication_style"] = "elaborate"
    
    return prefs

def extract_entities(text: str) -> Dict[str, List[str]]:
    """Extract named entities (simple version)."""
    entities = {
        "names": [],
        "locations": [],
        "organizations": []
    }
    
    # Simple pattern matching for Chinese names (2-4 characters)
    name_pattern = r'[\u4e00-\u9fa5]{2,4}(?=说|提到|认为|表示)'
    entities["names"] = list(set(re.findall(name_pattern, text)))
    
    return entities

def analyze_message(message: str, timestamp: str = None) -> Dict[str, Any]:
    """Analyze a single message and extract insights."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    insights = {
        "timestamp": timestamp,
        "interests": detect_interests(message),
        "preferences": detect_preferences(message),
        "entities": extract_entities(message),
        "message_length": len(message),
        "has_question": "?" in message or "？" in message,
        "topics": []
    }
    
    return insights

def merge_insights(existing: Dict, new_insights: Dict) -> Dict:
    """Merge new insights into existing profile."""
    if not existing:
        return {
            "interests": {cat: 1 for cat in new_insights["interests"]},
            "preferences": new_insights["preferences"],
            "interaction_count": 1,
            "first_seen": new_insights["timestamp"],
            "last_updated": new_insights["timestamp"],
            "topics": new_insights.get("topics", [])
        }
    
    # Merge interests with frequency count
    for interest in new_insights["interests"]:
        existing["interests"][interest] = existing["interests"].get(interest, 0) + 1
    
    # Update preferences (latest wins for conflicting values)
    existing["preferences"].update(new_insights["preferences"])
    
    # Update metadata
    existing["interaction_count"] = existing.get("interaction_count", 0) + 1
    existing["last_updated"] = new_insights["timestamp"]
    
    return existing

def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: extract_insights.py '<message>' [timestamp]", file=sys.stderr)
        sys.exit(1)
    
    message = sys.argv[1]
    timestamp = sys.argv[2] if len(sys.argv) > 2 else datetime.now().isoformat()
    
    insights = analyze_message(message, timestamp)
    print(json.dumps(insights, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
