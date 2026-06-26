#!/usr/bin/env python3
"""
多语言支持模块 - v1.0.0
支持中英文记忆混合处理

功能：
1. 自动检测语言
2. 中英文分词
3. 跨语言搜索
4. 混合内容处理
"""

import re
from typing import Dict, List, Tuple, Optional, Set

# 常用中文停用词
ZH_STOPWORDS = {"的", "了", "是", "在", "我", "你", "他", "这", "那", "和", "与", "或", "以及", "对于", "关于", "一个", "一些", "什么", "怎么", "如何", "为什么", "现在", "今天", "昨天", "这个", "那个"}

# 英文停用词
EN_STOPWORDS = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "from", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "this", "that", "these", "those"}

# 中英文分词模式
ZH_PATTERN = re.compile(r'[\u4e00-\u9fff]+')
EN_PATTERN = re.compile(r'[a-zA-Z]+')

class MultilangProcessor:
    """多语言处理器"""
    
    def __init__(self):
        pass
    
    def detect_language(self, text: str) -> str:
        """
        自动检测语言
        返回: 'zh' | 'en' | 'mixed'
        """
        zh_chars = len(ZH_PATTERN.findall(text))
        en_words = len(EN_PATTERN.findall(text))
        
        if zh_chars > 0 and en_words > 0:
            return "mixed"
        elif zh_chars > en_words:
            return "zh"
        elif en_words > 0:
            return "en"
        else:
            return "unknown"
    
    def tokenize(self, text: str, remove_stopwords: bool = True) -> List[str]:
        """
        混合分词
        返回所有词（中文按词分，英文按单词分）
        """
        tokens = []
        
        # 中文分词（简单按字符）
        zh_segments = ZH_PATTERN.findall(text)
        for seg in zh_segments:
            for char in seg:
                if char not in ZH_STOPWORDS or not remove_stopwords:
                    tokens.append(char)
        
        # 英文分词
        en_words = EN_PATTERN.findall(text)
        for word in en_words:
            word_lower = word.lower()
            if word_lower not in EN_STOPWORDS or not remove_stopwords:
                tokens.append(word_lower)
        
        return tokens
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        提取关键词及其权重
        """
        tokens = self.tokenize(text)
        
        # 统计频率
        freq = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        
        # 计算权重
        total = len(tokens) if tokens else 1
        keywords = []
        
        for word, count in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_k]:
            # 中文单字给更高权重（信息密度高）
            if len(word) == 1 and '\u4e00' <= word <= '\u9fff':
                weight = count / total * 1.5
            else:
                weight = count / total
            
            keywords.append((word, round(weight, 4)))
        
        return keywords
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算两段文本的相似度（支持中英文混合）
        """
        tokens1 = set(self.tokenize(text1, remove_stopwords=True))
        tokens2 = set(self.tokenize(text2, remove_stopwords=True))
        
        if not tokens1 or not tokens2:
            return 0.0
        
        # Jaccard 相似度
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def search_crosslingual(self, query: str, documents: List[Dict]) -> List[Dict]:
        """
        跨语言搜索
        - query: 查询文本
        - documents: 文档列表 [{"content": ..., "title": ..., "id": ...}]
        - 返回按相关性排序的结果
        """
        lang = self.detect_language(query)
        
        # 提取查询关键词
        query_keywords = set(self.tokenize(query, remove_stopwords=True))
        
        results = []
        for doc in documents:
            content = doc.get("content", "")
            title = doc.get("title", "")
            
            # 检测文档语言
            doc_lang = self.detect_language(content)
            
            # 提取文档关键词
            doc_keywords = set(self.tokenize(content, remove_stopwords=True))
            
            # 计算匹配
            if lang == doc_lang or lang == "mixed":
                # 同语言：直接匹配
                matches = len(query_keywords & doc_keywords)
            else:
                # 跨语言：只计算词根匹配（简化处理）
                # 实际应该用翻译或词向量，这里简化处理
                matches = len(query_keywords & doc_keywords) // 2
            
            if matches > 0:
                # 计算相似度
                similarity = self.calculate_similarity(query, content)
                
                results.append({
                    **doc,
                    "matches": matches,
                    "similarity": round(similarity, 4),
                    "query_lang": lang,
                    "doc_lang": doc_lang
                })
        
        # 排序
        results.sort(key=lambda x: (x["matches"], x["similarity"]), reverse=True)
        
        return results
    
    def format_text(self, text: str, max_length: int = 100) -> str:
        """
        格式化文本显示
        """
        if len(text) <= max_length:
            return text
        
        return text[:max_length] + "..."
    
    def report(self) -> str:
        """生成报告"""
        return """🌐 多语言支持模块
========================================
功能：
1. 自动检测语言（中文/英文/混合）
2. 混合分词处理
3. 跨语言搜索
4. 中英文关键词提取

使用方法：
- detect_language(text) -> 'zh' | 'en' | 'mixed'
- tokenize(text) -> ['词', 'word', ...]
- extract_keywords(text) -> [('词', 0.5), ...]
- calculate_similarity(text1, text2) -> 0.85
- search_crosslingual(query, documents) -> sorted_results
"""
