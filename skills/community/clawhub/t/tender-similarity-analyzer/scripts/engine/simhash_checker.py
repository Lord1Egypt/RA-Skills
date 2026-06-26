# -*- coding: utf-8 -*-
"""
SimHash文档级查重模块
使用SimHash和汉明距离进行整体文档查重
"""

import hashlib
import numpy as np
from typing import List, Tuple, Dict
from collections import Counter
import re


class SimHashChecker:
    """
    SimHash 文档级查重器
    
    使用SimHash算法进行整体文档相似度检测
    适用于快速判断两个文档的整体重复率
    """
    
    def __init__(self, hash_size: int = 64):
        """
        @param hash_size: SimHash位数（64或128）
        """
        self.hash_size = hash_size
        
    def _tokenize(self, text: str) -> List[str]:
        """
        分词（简单的字符级分词）
        
        @param text: 原始文本
        @return: 词语列表
        """
        # 预处理
        text = re.sub(r'\s+', '', text)
        text = text.lower()
        
        # 字符级分词
        tokens = []
        for i in range(len(text) - 2):
            tokens.append(text[i:i + 3])  # 3-gram
            
        return tokens
        
    def _hash_token(self, token: str) -> int:
        """
        计算token的哈希值
        
        @param token: 词语
        @return: 哈希值
        """
        if self.hash_size == 64:
            return int(hashlib.md5(token.encode()).hexdigest()[:16], 16)
        else:
            return int(hashlib.sha256(token.encode()).hexdigest()[:32], 16)
            
    def compute_hash(self, text: str) -> int:
        """
        计算文本的SimHash值
        
        @param text: 原始文本
        @return: SimHash值
        """
        tokens = self._tokenize(text)
        
        if not tokens:
            return 0
            
        # 统计每个token的哈希
        v = np.zeros(self.hash_size, dtype=np.float64)
        
        for token in tokens:
            hash_val = self._hash_token(token)
            
            # 根据哈希值更新向量
            for i in range(self.hash_size):
                bit = (hash_val >> i) & 1
                if bit:
                    v[i] += 1
                else:
                    v[i] -= 1
                    
        # 生成最终哈希
        hash_val = 0
        for i in range(self.hash_size):
            if v[i] > 0:
                hash_val |= (1 << i)
                
        return hash_val
        
    def hamming_distance(self, hash1: int, hash2: int) -> int:
        """
        计算两个哈希值之间的汉明距离
        
        @param hash1: 哈希值1
        @param hash2: 哈希值2
        @return: 汉明距离
        """
        xor = hash1 ^ hash2
        return bin(xor).count('1')
        
    def similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的相似度
        
        @param text1: 文本1
        @param text2: 文本2
        @return: 相似度 [0, 1]
        """
        hash1 = self.compute_hash(text1)
        hash2 = self.compute_hash(text2)
        
        distance = self.hamming_distance(hash1, hash2)
        
        # 汉明距离转相似度
        similarity = 1 - (distance / self.hash_size)
        
        return max(0.0, min(1.0, similarity))
        
    def find_similar_documents(self, documents: Dict[str, str], 
                               threshold: float = 0.8) -> List[Dict]:
        """
        在文档集合中找出相似的文档对
        
        @param documents: 文档字典 {名称: 文本}
        @param threshold: 相似度阈值
        @return: 相似文档对列表
        """
        # 计算所有文档的哈希
        hashes = {}
        for name, text in documents.items():
            hashes[name] = self.compute_hash(text)
            
        # 两两比较
        names = list(documents.keys())
        similar_pairs = []
        
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                name1, name2 = names[i], names[j]
                distance = self.hamming_distance(hashes[name1], hashes[name2])
                similarity = 1 - (distance / self.hash_size)
                
                if similarity >= threshold:
                    similar_pairs.append({
                        'doc1': name1,
                        'doc2': name2,
                        'similarity': similarity,
                        'hamming_distance': distance
                    })
                    
        return similar_pairs
        
    def get_hash_features(self, text: str, top_k: int = 10) -> List[Dict]:
        """
        获取文本的SimHash特征（最重要的词语）
        
        @param text: 原始文本
        @param top_k: 返回前k个特征
        @return: 特征词语列表
        """
        tokens = self._tokenize(text)
        token_counts = Counter(tokens)
        
        # 计算每个token的权重
        features = []
        for token, count in token_counts.most_common(100):
            hash_val = self._hash_token(token)
            
            # 计算这个token对各位的贡献
            v = np.zeros(self.hash_size)
            for i in range(self.hash_size):
                bit = (hash_val >> i) & 1
                v[i] = count * (1 if bit else -1)
                
            features.append({
                'token': token,
                'count': count,
                'weight': float(np.sum(v))
            })
            
        # 按权重排序
        features.sort(key=lambda x: x['weight'], reverse=True)
        
        return features[:top_k]
