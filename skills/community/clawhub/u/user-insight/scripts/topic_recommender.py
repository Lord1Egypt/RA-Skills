#!/usr/bin/env python3
"""
Topic recommendation engine for user exploration.
Suggests conversation topics based on user profile and exploration history.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

# Topic categories with example topics
TOPIC_CATEGORIES = {
    "technology": {
        "name": "科技",
        "topics": [
            "AI最新进展", "量子计算", "新能源技术", "太空探索",
            "生物技术", "区块链应用", "智能家居", "未来交通"
        ],
        "opening_styles": {
            "direct": "刚看到个技术新闻挺有意思：{topic}，你觉得这种技术几年内能普及？",
            "curiosity": "最近在关注{topic}，发现个反直觉的现象...",
            "story": "朋友公司最近在用{topic}解决实际问题，效果出乎意料..."
        }
    },
    "current_events": {
        "name": "时事热点",
        "topics": [
            "国际局势变化", "经济趋势分析", "社会现象观察", "政策解读",
            "行业动态", "科技伦理讨论", "环境议题", "教育改革"
        ],
        "opening_styles": {
            "direct": "最近{topic}挺火的，想听听你的看法？",
            "analytical": "分析了下最近的{topic}，发现几个有意思的角度...",
            "connection": "你之前聊过XX，这次的{topic}感觉有关联..."
        }
    },
    "lifestyle": {
        "name": "生活方式",
        "topics": [
            "城市探索", "美食探店", "健身方法", "效率提升",
            "理财技巧", "旅行攻略", "家居布置", "穿搭风格"
        ],
        "opening_styles": {
            "casual": "最近试了{topic}，发现个挺实用的小技巧...",
            "question": "你在{topic}方面有什么心得吗？",
            "sharing": "挖到个关于{topic}的宝藏资源，分享给你..."
        }
    },
    "entertainment": {
        "name": "娱乐休闲",
        "topics": [
            "电影剧集推荐", "音乐分享", "游戏讨论", "书籍推荐",
            "综艺吐槽", "二次元文化", "体育赛事", "线下活动"
        ],
        "opening_styles": {
            "casual": "刚看完/听完{topic}，有点上头...",
            "recommendation": "根据你喜欢的XX，推荐个{topic}相关的...",
            "discussion": "想聊聊{topic}，有个点挺好奇你的看法..."
        }
    },
    "knowledge": {
        "name": "知识科普",
        "topics": [
            "历史趣闻", "心理学现象", "经济学原理", "科学新知",
            "哲学思考", "语言学", "认知科学", "未来学"
        ],
        "opening_styles": {
            "curiosity": "读到个关于{topic}的有趣研究...",
            "mind_blowing": "知道个{topic}的冷知识，可能会颠覆认知...",
            "practical": "学了个{topic}的概念，发现生活中到处能用..."
        }
    },
    "personal_growth": {
        "name": "个人成长",
        "topics": [
            "职业规划", "学习方法", "人际关系", "情绪管理",
            "习惯养成", "思维模型", "决策技巧", "创造力培养"
        ],
        "opening_styles": {
            "reflective": "最近在思考{topic}，想听听你的经验...",
            "sharing": "实践了{topic}一段时间，有些感悟...",
            "question": "遇到个{topic}方面的困惑，想请教下..."
        }
    }
}

def load_profile(profile_path: str = None) -> Dict:
    """Load user profile from file."""
    if profile_path is None:
        profile_path = Path.home() / ".openclaw/workspace/memory/user-profile.json"
    else:
        profile_path = Path(profile_path)
    
    if not profile_path.exists():
        return create_default_profile()
    
    with open(profile_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_default_profile() -> Dict:
    """Create a new default profile."""
    return {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "basic_info": {},
        "interests": [],
        "communication_style": {},
        "exploration_state": {
            "explored_categories": [],
            "pending_categories": list(TOPIC_CATEGORIES.keys()),
            "avoided_topics": []
        }
    }

def load_exploration_log(log_path: str = None) -> List[Dict]:
    """Load topic exploration history."""
    if log_path is None:
        log_path = Path.home() / ".openclaw/workspace/memory/topic-exploration.json"
    else:
        log_path = Path(log_path)
    
    if not log_path.exists():
        return []
    
    with open(log_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("exploration_log", [])

def calculate_topic_score(category: str, topic: str, profile: Dict, log: List[Dict]) -> float:
    """Calculate interest score for a topic (0-1)."""
    score = 0.5  # Base score
    
    # Check if already in interests
    for interest in profile.get("interests", []):
        if interest["topic"] == topic or interest.get("category") == category:
            score = interest.get("score", 0.5)
            return score
    
    # Check exploration history
    for entry in log:
        if entry.get("topic") == topic:
            if entry.get("interest_detected"):
                score += 0.2
            else:
                score -= 0.3
            break
    
    # Check if category was explored before
    explored = profile.get("exploration_state", {}).get("explored_categories", [])
    if category in explored:
        score += 0.1  # Slight preference for familiar territory
    
    # Check avoided topics
    avoided = profile.get("exploration_state", {}).get("avoided_topics", [])
    if topic in avoided or category in avoided:
        score = 0.1  # Low score but not zero (can retry after cooldown)
    
    return max(0.0, min(1.0, score))

def recommend_topic(profile: Dict, log: List[Dict], strategy: str = "mixed") -> Dict[str, Any]:
    """
    Recommend a conversation topic.
    
    Strategies:
    - "exploit": Focus on known high-interest topics
    - "explore": Try new categories
    - "mixed": 70% exploit + 30% explore (default)
    """
    
    # Get all candidate topics with scores
    candidates = []
    for cat_key, cat_data in TOPIC_CATEGORIES.items():
        for topic in cat_data["topics"]:
            score = calculate_topic_score(cat_key, topic, profile, log)
            candidates.append({
                "category_key": cat_key,
                "category_name": cat_data["name"],
                "topic": topic,
                "score": score,
                "opening_styles": cat_data["opening_styles"]
            })
    
    # Sort by score
    candidates.sort(key=lambda x: x["score"], reverse=True)
    
    # Apply strategy
    if strategy == "exploit":
        # Pick from top 30%
        top_candidates = candidates[:max(1, len(candidates) // 3)]
        selected = random.choice(top_candidates)
    elif strategy == "explore":
        # Pick from bottom 50% that haven't been tried
        unexplored = [c for c in candidates if c["score"] == 0.5]
        if unexplored:
            selected = random.choice(unexplored)
        else:
            # Fall back to middle range
            mid_start = len(candidates) // 3
            mid_end = 2 * len(candidates) // 3
            selected = random.choice(candidates[mid_start:mid_end])
    else:  # mixed
        if random.random() < 0.7:
            # Exploit
            top_candidates = candidates[:max(1, len(candidates) // 3)]
            selected = random.choice(top_candidates)
        else:
            # Explore
            unexplored = [c for c in candidates if c["score"] == 0.5]
            if unexplored:
                selected = random.choice(unexplored)
            else:
                selected = random.choice(candidates[len(candidates)//3:])
    
    # Generate opening message
    style = random.choice(list(selected["opening_styles"].keys()))
    opening_template = selected["opening_styles"][style]
    opening_message = opening_template.format(topic=selected["topic"])
    
    return {
        "category": selected["category_name"],
        "topic": selected["topic"],
        "confidence": selected["score"],
        "strategy_used": strategy,
        "opening_style": style,
        "suggested_opening": opening_message
    }

def should_explore_now(profile: Dict, log: List[Dict]) -> bool:
    """Determine if it's a good time to initiate topic exploration."""
    # Check last exploration time
    last_date_str = profile.get("exploration_state", {}).get("last_exploration_date")
    if last_date_str:
        last_date = datetime.fromisoformat(last_date_str)
        if datetime.now() - last_date < timedelta(hours=24):
            return False  # Don't be too aggressive
    
    # Check if we have enough unexplored categories
    pending = profile.get("exploration_state", {}).get("pending_categories", [])
    if len(pending) < 2:
        return False  # Most things explored
    
    return True

def main():
    """CLI entry point."""
    import sys
    
    profile = load_profile()
    log = load_exploration_log()
    
    strategy = "mixed"
    if len(sys.argv) > 1:
        strategy = sys.argv[1]
    
    recommendation = recommend_topic(profile, log, strategy)
    print(json.dumps(recommendation, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
