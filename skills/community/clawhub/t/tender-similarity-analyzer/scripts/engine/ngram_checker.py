# -*- coding: utf-8 -*-
"""
N-gram句子级查重模块
使用N-gram和Jaccard相似度进行快速初筛
"""

import re
from typing import List, Set, Tuple, Dict
from collections import Counter


class NgramChecker:
    """
    N-gram 句子级查重器
    
    使用字符级N-gram + Jaccard相似度
    适用于快速筛选疑似重复的段落
    """
    
    def __init__(self, n: int = 3):
        """
        @param n: N-gram的N值，建议3-5
        """
        self.n = n
        
    def get_ngrams(self, text: str) -> Set[str]:
        """
        获取文本的N-gram集合
        
        @param text: 输入文本
        @return: N-gram集合
        """
        # 清理文本
        text = self._preprocess(text)
        
        if len(text) < self.n:
            return set()
            
        ngrams = set()
        for i in range(len(text) - self.n + 1):
            ngram = text[i:i + self.n]
            ngrams.add(ngram)
            
        return ngrams
        
    def _preprocess(self, text: str) -> str:
        """
        预处理文本
        
        @param text: 原始文本
        @return: 预处理后的文本
        """
        # 去除空白字符
        text = re.sub(r'\s+', '', text)
        # 转小写
        text = text.lower()
        return text
        
    def jaccard_similarity(self, set1: Set, set2: Set) -> float:
        """
        计算Jaccard相似度
        
        @param set1: 集合1
        @param set2: 集合2
        @return: Jaccard相似度 [0, 1]
        """
        if not set1 or not set2:
            return 0.0
            
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
        
    def similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的相似度
        
        @param text1: 文本1
        @param text2: 文本2
        @return: 相似度 [0, 1]
        """
        ngrams1 = self.get_ngrams(text1)
        ngrams2 = self.get_ngrams(text2)
        
        return self.jaccard_similarity(ngrams1, ngrams2)
        
    def find_common_ngrams(self, text1: str, text2: str) -> List[str]:
        """
        找出两个文本的公共N-gram
        
        @param text1: 文本1
        @param text2: 文本2
        @return: 公共N-gram列表
        """
        ngrams1 = self.get_ngrams(text1)
        ngrams2 = self.get_ngrams(text2)
        
        return list(ngrams1 & ngrams2)
        
    def get_common_ngram_details(self, text1: str, text2: str) -> List[Dict]:
        """
        获取公共N-gram的详细信息
        
        @param text1: 文本1
        @param text2: 文本2
        @return: 包含位置信息的N-gram列表
        """
        common_ngrams = self.find_common_ngrams(text1, text2)
        details = []
        
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        for ngram in common_ngrams:
            positions1 = [i for i in range(len(text1_lower) - self.n + 1) 
                         if text1_lower[i:i + self.n] == ngram.lower()]
            positions2 = [i for i in range(len(text2_lower) - self.n + 1) 
                         if text2_lower[i:i + self.n] == ngram.lower()]
            
            details.append({
                'ngram': ngram,
                'positions_in_text1': positions1,
                'positions_in_text2': positions2,
                'count': len(positions1) + len(positions2)
            })
            
        return details
        
    def quick_check(self, text1: str, text2: str, threshold: float = 0.3) -> Tuple[bool, float]:
        """
        快速检查两个文本是否可能重复
        
        @param text1: 文本1
        @param text2: 文本2
        @param threshold: 判定阈值
        @return: (是否疑似重复, 相似度)
        """
        sim = self.similarity(text1, text2)
        return (sim >= threshold, sim)
        
    def batch_check(self, texts: List[str], threshold: float = 0.3) -> List[List[float]]:
        """
        批量检查多个文本之间的相似度
        
        @param texts: 文本列表
        @param threshold: 判定阈值
        @return: 相似度矩阵
        """
        n = len(texts)
        matrix = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                sim = self.similarity(texts[i], texts[j])
                matrix[i][j] = sim
                matrix[j][i] = sim
                
        return matrix
