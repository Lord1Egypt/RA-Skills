#!/usr/bin/env python3
"""
Twitter KOL Fetcher - Filter & Score
过滤和评分脚本

[优化]
- 加入话题聚类逻辑（基于关键词相似度）
- 聚类后的话题更易于生成内参
"""

import json
import re
from datetime import datetime
from collections import defaultdict

# AI 关键词（用于过滤）
AI_KEYWORDS = [
    "GPT", "Claude", "Gemini", "Sora", "Codex", "ChatGPT",
    "Llama", "Mistral", "Grok", "Perplexity", "Copilot",
    "Agent", "MCP", "Computer Use", "RAG", "Fine-tuning",
    "Prompt", "Embedding", "Vector", "LLM", "API",
    "o1", "o3", "GPT-5", "GPT-4", "Claude 4", "Gemini 2",
    "OpenAI", "Anthropic", "Google", "Meta", "xAI", "Cohere",
    "AGI", "Safety", "Security", "Alignment", "Regulation",
    "Benchmark", "Training", "Inference", "Model"
]

# 热门人物（用于兜底）
VIP_USERS = [
    "sama", "elonmusk", "DarioAmodei", "AndrewYNg", "ylecun",
    "JeffDean", "pmarca", "cdixon", "polynoamial", "mitchellh"
]

# 降低热度阈值
MIN_HOTNESS = 500  # 保持原值，平衡精确度和覆盖面
REPORT_TRIGGER_KEYWORDS = [
    "launch", "release", "announce", "debut",
    "funding", "Series", "round", "acquisition", "acqui",
    "safety", "security", "vulnerability", "breach", "hack",
    "policy", "regulation", "government", "ban", "export control"
]

def is_ai_related(text):
    """判断是否与 AI 相关"""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in AI_KEYWORDS)

def calculate_hotness(tweet):
    """计算热度分数"""
    likes = tweet.get("likes", 0)
    retweets = tweet.get("retweets", 0)
    views = tweet.get("views", 0)

    # 权重: 转发 > 点赞 > 浏览
    score = likes * 1 + retweets * 2 + views * 0.001
    return score

def is_report_worthy(text):
    """判断是否可能值得写内参"""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in REPORT_TRIGGER_KEYWORDS)

def should_always_include(tweet, vip_users):
    """兜底机制：这些情况必须包含（避免漏抓）"""
    text = tweet.get("text", "").lower()
    username = tweet.get("username", "").lower()

    # 1. VIP 用户发的 → 强制纳入
    if username in [u.lower() for u in vip_users]:
        return True

    # 2. 包含明确的发布关键词 → 强制纳入
    for kw in ["launching", "releasing", "announcing", "new", "breaking", "just released"]:
        if kw in text:
            return True

    # 3. 互动量极高 → 强制纳入
    if tweet.get("likes", 0) > 5000 or tweet.get("retweets", 0) > 500:
        return True

    return False

def extract_topic(tweets):
    """从推文中提取话题（单个）"""
    # 按热度排序
    sorted_tweets = sorted(tweets, key=lambda x: calculate_hotness(x), reverse=True)

    topics = []
    processed_ids = set()

    for tweet in sorted_tweets:
        if tweet["id"] in processed_ids:
            continue

        hotness = calculate_hotness(tweet)

        # 兜底机制：即使热度低，VIP 用户或重要事件也纳入
        if hotness < MIN_HOTNESS and not should_always_include(tweet, VIP_USERS):
            continue

        text = tweet["text"]
        author = tweet["username"]

        # 提取话题（简单方式：取前 50 个字符）
        topic_preview = text[:50].replace("\n", " ")

        topics.append({
            "topic": topic_preview,
            "hotness": hotness,
            "authors": [author],
            "tweets": [tweet],
            "key_tweet": tweet
        })

        processed_ids.add(tweet["id"])

    return topics


def extract_topic_keywords(text):
    """从文本中提取关键词（用于聚类）"""
    # 产品/公司关键词
    product_keywords = [
        "GPT", "Claude", "Gemini", "Sora", "Codex", "ChatGPT",
        "Llama", "Mistral", "Grok", "Perplexity", "Copilot", "Cursor",
        "Windsurf", "Cline", "Trae", "Devin", "Manus", "AlphaFold",
        "o1", "o3", "o4", "o5", "GPT-5", "GPT-4", "Claude 4", "Claude 3.5",
        "Gemini 2", "Gemini 1.5", "Llama 4", "DeepSeek", "V4", "V3",
    ]
    
    event_keywords = [
        "launch", "release", "announce", "debut", "unveil", "ship",
        "funding", "Series", "round", "acquisition", "valuation",
        "safety", "security", "vulnerability", "breach", "hack",
        "policy", "regulation", "government", "export control",
        "layoff", "hire", "resign", "join", "leave",
    ]
    
    all_keywords = product_keywords + event_keywords
    
    found = []
    text_lower = text.lower()
    for kw in all_keywords:
        if kw.lower() in text_lower:
            found.append(kw)
    
    return found if found else ["general"]


def cluster_topics(topics):
    """
    [新增] 将相似话题聚类
    基于关键词重叠度进行简单聚类
    """
    if not topics:
        return []
    
    clusters = []  # 每个元素是一个 cluster
    
    for topic in topics:
        topic_keywords = set(extract_topic_keywords(topic.get("key_tweet", {}).get("text", "")))
        
        placed = False
        for cluster in clusters:
            # 检查与现有 cluster 的重叠度
            cluster_keywords = cluster.get("keywords", set())
            overlap = topic_keywords & cluster_keywords
            
            # 如果有共同关键词且重叠度 >= 1，加入该 cluster
            if len(overlap) >= 1:
                # 更新 cluster
                cluster["keywords"] = cluster_keywords | topic_keywords
                cluster["hotness"] += topic.get("hotness", 0)
                cluster["authors"].extend(topic.get("authors", []))
                cluster["tweets"].append(topic.get("key_tweet", {}))
                cluster["all_topic_previews"].append(topic.get("topic", ""))
                
                # 更新主要话题名称（取最热门的）
                if topic.get("hotness", 0) > cluster.get("hotness", 0):
                    cluster["topic"] = topic.get("topic", "")
                    cluster["key_tweet"] = topic.get("key_tweet", {})
                
                placed = True
                break
        
        # 如果没有合适的 cluster，新建一个
        if not placed:
            clusters.append({
                "topic": topic.get("topic", ""),  # 主要话题
                "topic_preview": topic.get("topic", "")[:80],  # 话题摘要
                "keywords": topic_keywords,
                "hotness": topic.get("hotness", 0),
                "authors": list(set(topic.get("authors", []))),
                "tweets": [topic.get("key_tweet", {})],
                "all_topic_previews": [topic.get("topic", "")],
                "key_tweet": topic.get("key_tweet", {})
            })
    
    # 重新按热度排序
    clusters.sort(key=lambda x: x.get("hotness", 0), reverse=True)
    
    return clusters

def filter_and_score(input_file):
    """主函数：过滤和评分"""
    # 读取数据
    with open(input_file, "r", encoding="utf-8") as f:
        tweets = json.load(f)

    print(f"原始数据: {len(tweets)} 条推文")

    # 过滤 AI 相关
    ai_tweets = [t for t in tweets if is_ai_related(t.get("text", ""))]
    print(f"AI 相关: {len(ai_tweets)} 条")

    # 计算热度
    for tweet in ai_tweets:
        tweet["hotness"] = calculate_hotness(tweet)

    # 排序
    ai_tweets.sort(key=lambda x: x["hotness"], reverse=True)

    # 提取话题（单个）
    raw_topics = extract_topic(ai_tweets)
    print(f"原始热门话题: {len(raw_topics)} 个")

    # [新增] 话题聚类
    clustered_topics = cluster_topics(raw_topics)
    print(f"聚类后话题: {len(clustered_topics)} 个")

    # 输出
    output = {
        "all_ai_tweets": ai_tweets,
        "raw_topics": raw_topics,  # 保留原始话题（向后兼容）
        "topics": clustered_topics,  # 聚类后的主题
        "timestamp": datetime.now().isoformat()
    }

    output_file = input_file.replace(".json", "_filtered.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"过滤后数据已保存到: {output_file}")
    return output_file

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else f"/tmp/kol_tweets_{datetime.now().strftime('%Y%m%d')}.json"
    filter_and_score(input_file)
