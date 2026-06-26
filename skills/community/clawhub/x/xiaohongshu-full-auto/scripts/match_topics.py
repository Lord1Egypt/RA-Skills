#!/usr/bin/env python3
"""
根据垂类智能匹配选题
从热榜中选出和用户垂类最相关的话题
"""

import re
from typing import List, Dict


def topic_similarity(topic_title: str, niches: List[str]) -> float:
    """计算话题和垂类的相似度"""
    topic_lower = topic_title.lower()
    score = 0
    
    for niche in niches:
        niche_lower = niche.lower()
        # 完全匹配
        if niche_lower in topic_lower:
            score += 10
        # 分词匹配
        words = re.findall(r'[\w]+', niche_lower)
        for word in words:
            if len(word) > 1 and word in topic_lower:
                score += 2
    
    return score


def match_topics_by_niches(hot_topics: List[Dict], niches: List[str], count: int = 3) -> List[Dict]:
    """
    根据垂类匹配热点选题
    
    Args:
        hot_topics: 热榜话题列表
        niches: 用户垂类列表
        count: 返回几个
        
    Returns:
        排序后的选题列表
    """
    scored_topics = []
    
    for topic in hot_topics:
        score = topic_similarity(topic['title'], niches)
        # 热度乘以相似度作为总分
        total_score = score * (1 + topic.get('hot_value', 100000) / 1000000)
        scored_topics.append((total_score, topic))
    
    # 按得分排序
    scored_topics.sort(key=lambda x: x[0], reverse=True)
    
    # 返回前 count 个
    result = [t for (s, t) in scored_topics[:count]]
    return result


if __name__ == "__main__":
    sample_topics = [
        {"title": "年轻人搞副业已经成常态了", "hot_value": 890000},
        {"title": "30岁职场人必须知道的三个真相", "hot_value": 760000},
        {"title": "AI工具提高工作效率500%", "hot_value": 680000},
        {"title": "普通人如何靠副业月入五千", "hot_value": 650000},
        {"title": "这几个减肥误区你中招了吗", "hot_value": 590000},
    ]
    niches = ["副业", "职场", "AI工具"]
    result = match_topics_by_niches(sample_topics, niches, 3)
    for r in result:
        print(f"{r['title']} - 热度: {r['hot_value']}")
