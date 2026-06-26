#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
starmemo v2.0 - 启发式召回模块
智能检索相关记忆
"""
import re
from typing import List, Dict, Optional
from pathlib import Path


class HeuristicRecall:
    """启发式召回系统"""
    
    def __init__(self, storage, ai_processor=None):
        self.storage = storage
        self.ai_processor = ai_processor
        
        # 召回触发词
        self.recall_triggers = [
            "之前", "上次", "以前", "刚才", "昨天", "前天",
            "说过", "提到", "讨论", "聊过", "记得",
            "那个", "什么来着", "怎么说的"
        ]
        
        # 上下文关键词权重
        self.keyword_weights = {}
    
    def should_recall(self, text: str) -> bool:
        """判断是否应该召回记忆"""
        # 检查触发词
        for trigger in self.recall_triggers:
            if trigger in text:
                return True
        
        # 检查问句模式
        question_patterns = [
            r"我.*什么",
            r"什么.*来着",
            r"是.*还是",
            r"有没有.*说过"
        ]
        
        for pattern in question_patterns:
            if re.search(pattern, text):
                return True
        
        return False
    
    def extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取
        # 移除常见停用词
        stopwords = {"的", "了", "是", "在", "我", "你", "他", "她", "它",
                     "这", "那", "有", "和", "与", "或", "但", "如果", "因为"}
        
        # 分词（简单按空格和标点分割）
        words = re.split(r'[\s,，。！？、；：""''（）【】]+', text)
        
        # 过滤
        keywords = []
        for word in words:
            word = word.strip()
            if len(word) >= 2 and word not in stopwords:
                keywords.append(word)
        
        return keywords
    
    def recall(self, text: str, limit: int = 3) -> Dict:
        """
        召回相关记忆
        
        Returns:
            dict: {
                "should_recall": bool,
                "daily_results": list,
                "knowledge_results": list,
                "combined_memory": str
            }
        """
        result = {
            "should_recall": False,
            "daily_results": [],
            "knowledge_results": [],
            "combined_memory": ""
        }
        
        # 判断是否需要召回
        if not self.should_recall(text):
            return result
        
        result["should_recall"] = True
        
        # 提取关键词
        keywords = self.extract_keywords(text)
        
        # 搜索每日记忆
        for keyword in keywords[:3]:  # 最多用前3个关键词
            daily = self.storage.search_daily(keyword, limit=2)
            result["daily_results"].extend(daily)
        
        # 搜索知识库
        for keyword in keywords[:3]:
            knowledge = self.storage.search_knowledge(keyword, limit=2)
            result["knowledge_results"].extend(knowledge)
        
        # 去重
        seen = set()
        unique_daily = []
        for item in result["daily_results"]:
            key = item.get("content", "")[:50]
            if key not in seen:
                seen.add(key)
                unique_daily.append(item)
        result["daily_results"] = unique_daily[:limit]
        
        seen = set()
        unique_knowledge = []
        for item in result["knowledge_results"]:
            key = item.get("title", "")
            if key not in seen:
                seen.add(key)
                unique_knowledge.append(item)
        result["knowledge_results"] = unique_knowledge[:limit]
        
        # 合并为上下文
        memory_parts = []
        
        if result["daily_results"]:
            memory_parts.append("【相关记忆】")
            for item in result["daily_results"][:2]:
                memory_parts.append(item["content"][:200])
        
        if result["knowledge_results"]:
            memory_parts.append("\n【相关知识】")
            for item in result["knowledge_results"][:2]:
                memory_parts.append(f"- {item.get('title', '')}: {item.get('content', '')[:100]}")
        
        result["combined_memory"] = "\n".join(memory_parts)
        
        return result
    
    def learn_keywords(self, text: str, importance: int = 1):
        """学习关键词权重"""
        keywords = self.extract_keywords(text)
        for kw in keywords:
            self.keyword_weights[kw] = self.keyword_weights.get(kw, 0) + importance
    
    def get_important_keywords(self, top_n: int = 10) -> List[tuple]:
        """获取重要关键词"""
        sorted_kw = sorted(self.keyword_weights.items(), key=lambda x: x[1], reverse=True)
        return sorted_kw[:top_n]
