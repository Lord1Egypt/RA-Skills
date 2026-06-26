#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-Trigger for Axiang (阿香) - Test Version
"""

import re
import sys
import io

# Set UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from typing import List, Dict, Any, Optional

# Memory-related trigger keywords (Chinese)
MEMORY_KEYWORDS = [
    "之前说过", "之前提过", "之前讲过", "之前提到",
    "我记得", "我有印象", "我好像说过",
    "上次", "上上次", "上一次",
    "以前", "过去", "曾经",
    "说过", "提过", "讲过",
    "我说过", "我提过", "我讲过",
    "你记得", "还记得", "有印象",
    "之前", "从前",
    "那个", "这个", "那些", "这些",
    "刚才", "刚刚", "之前聊",
    "瀑布", "天台", "TTS", "技能", "阿福", "虾虾",
]

MEMORY_PATTERN = re.compile('|'.join(re.escape(kw) for kw in MEMORY_KEYWORDS))


def should_trigger_search(user_message: str) -> bool:
    if MEMORY_PATTERN.search(user_message):
        return True
    
    if any(pattern in user_message for pattern in ["吗？", "吗?", "？", "?"]):
        if any(word in user_message for word in ["过", "记得", "印象", "之前", "上次"]):
            return True
    
    return False


def extract_search_query(user_message: str) -> str:
    """
    Extract search query from user message
    
    Strategy: Keep nouns and key topics, remove question words and pronouns
    """
    query = user_message
    
    # Remove question markers
    query = re.sub(r'[吗？?]', '', query)
    
    # Remove common filler words (but keep important ones like 过 for past tense context)
    fillers = ["我", "你", "他", "她", "它", "的", "了", "吗", "呢", "吧", "啊", "呀", "是", "在", "有", "这", "那"]
    for filler in fillers:
        query = query.replace(filler, '')
    
    # Remove common verbs that don't add search value
    verbs = ["说过", "提过", "讲过", "提到", "记得", "聊过", "问过"]
    for verb in verbs:
        query = query.replace(verb, '')
    
    # Clean up whitespace
    query = ' '.join(query.split())
    
    # If query is too short, use original message (minus question marks)
    if len(query) < 2:
        query = re.sub(r'[吗？?]', '', user_message).strip()
    
    # Limit length but prefer the end (where the topic usually is)
    if len(query) > 30:
        query = query[-30:]
    
    return query.strip()


def search_and_format(query: str, k: int = 3) -> str:
    try:
        sys.path.insert(0, r"C:\Users\Xiabi\.openclaw\workspace\skills\rag_search\src")
        from search import search_memories
        
        results = search_memories(query, k=k)
        
        if not results:
            return ""
        
        formatted = []
        for i, result in enumerate(results, 1):
            source = result.get('source', 'Unknown')
            if '\\' in source:
                source = source.split('\\')[-1]
            preview = result.get('preview', '')[:150]
            similarity = result.get('similarity', 0)
            formatted.append(f"{i}. [{source}] (相似度：{similarity})\n   {preview}")
        
        return "\n\n".join(formatted)
    
    except Exception as e:
        print(f"[ERROR] Search failed: {e}")
        return ""


def auto_search(user_message: str, k: int = 3) -> Optional[Dict[str, Any]]:
    if not should_trigger_search(user_message):
        return None
    
    query = extract_search_query(user_message)
    
    if not query or len(query) < 2:
        return None
    
    results_str = search_and_format(query, k=k)
    
    if not results_str:
        return None
    
    return {
        "triggered": True,
        "query": query,
        "results": results_str,
        "message": f"找到了 {k} 条相关记忆"
    }


if __name__ == "__main__":
    test_messages = [
        "我之前说过瀑布的事情吗？",
        "我记得上次聊过 TTS",
        "你记得阿福吗？",
        "今天天气不错",
        "之前提过的技能安装流程",
        "虾虾在吗？",
    ]
    
    print("=" * 60)
    print("Auto-Trigger Test")
    print("=" * 60)
    
    for msg in test_messages:
        print(f"\nMessage: {msg}")
        result = auto_search(msg, k=2)
        
        if result:
            print(f"  [OK] Triggered! Query: {result['query']}")
            print(f"  {result['message']}")
        else:
            print(f"  [SKIP] Not triggered")
    
    print("\n" + "=" * 60)
