# -*- coding: utf-8 -*-
"""
TF-IDF段落级查重模块
使用TF-IDF向量和余弦相似度进行精确查重
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from collections import Counter
import re

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    raise ImportError("scikit-learn >= 1.0.0 is required. Install: pip install scikit-learn")


class TFIDFChecker:
    """
    TF-IDF 段落级查重器
    
    使用字符级TF-IDF + 余弦相似度
    适用于精确检测段落级别的重复
    """
    
    def __init__(self, ngram_range: Tuple[int, int] = (2, 4), max_features: int = 50000):
        """
        @param ngram_range: N-gram范围
        @param max_features: 最大特征数
        """
        self.ngram_range = ngram_range
        self.max_features = max_features
        self.vectorizer = TfidfVectorizer(
            analyzer='char',      # 字符级分析（中文友好）
            ngram_range=ngram_range,
            max_features=max_features,
            min_df=1,
            sublinear_tf=True     # 使用对数TF
        )
        self._fitted = False
        
    def fit(self, texts: List[str]):
        """
        训练TF-IDF模型
        
        @param texts: 文本列表
        """
        cleaned_texts = [self._preprocess(t) for t in texts]
        self.vectorizer.fit(cleaned_texts)
        self._fitted = True
        
    def _preprocess(self, text: str) -> str:
        """
        预处理文本
        
        @param text: 原始文本
        @return: 预处理后的文本
        """
        # 去除空白字符
        text = re.sub(r'\s+', '', text)
        return text
        
    def transform(self, texts: List[str]) -> np.ndarray:
        """
        将文本转换为TF-IDF向量
        
        @param texts: 文本列表
        @return: TF-IDF向量矩阵
        """
        if not self._fitted:
            self.fit(texts)
            
        cleaned_texts = [self._preprocess(t) for t in texts]
        return self.vectorizer.transform(cleaned_texts).toarray()
        
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的余弦相似度
        
        @param text1: 文本1
        @param text2: 文本2
        @return: 余弦相似度 [0, 1]
        """
        vectors = self.transform([text1, text2])
        
        # 计算余弦相似度
        vec1 = vectors[0].reshape(1, -1)
        vec2 = vectors[1].reshape(1, -1)
        
        sim = cosine_similarity(vec1, vec2)[0][0]
        
        return float(sim)
        
    def compute_similarity_matrix(self, texts: List[str]) -> np.ndarray:
        """
        计算多个文本之间的相似度矩阵
        
        @param texts: 文本列表
        @return: 相似度矩阵
        """
        if len(texts) < 2:
            return np.array([[1.0]])
            
        vectors = self.transform(texts)
        
        # 计算余弦相似度矩阵
        sim_matrix = cosine_similarity(vectors)
        
        return sim_matrix
        
    def find_similar_pairs(self, texts: List[str], threshold: float = 0.3) -> List[Dict]:
        """
        找出所有相似度超过阈值的文本对
        
        @param texts: 文本列表
        @param threshold: 判定阈值
        @return: 相似文本对列表
        """
        if len(texts) < 2:
            return []
            
        sim_matrix = self.compute_similarity_matrix(texts)
        n = len(texts)
        pairs = []
        
        for i in range(n):
            for j in range(i + 1, n):
                if sim_matrix[i][j] >= threshold:
                    pairs.append({
                        'index1': i,
                        'index2': j,
                        'text1': texts[i][:100] + '...' if len(texts[i]) > 100 else texts[i],
                        'text2': texts[j][:100] + '...' if len(texts[j]) > 100 else texts[j],
                        'similarity': float(sim_matrix[i][j])
                    })
                    
        return pairs
        
    def get_similar_words(self, text1: str, text2: str, top_k: int = 20) -> List[Dict]:
        """
        获取两个文本中最相似的词语
        
        @param text1: 文本1
        @param text2: 文本2
        @param top_k: 返回前k个
        @return: 相似词语列表
        """
        if not self._fitted:
            self.fit([text1, text2])
            
        vectors = self.transform([text1, text2])
        
        # 获取特征名
        feature_names = self.vectorizer.get_feature_names_out()
        
        # 获取两个向量的差异
        diff = np.abs(vectors[0] - vectors[1])
        
        # 找出差异最小的特征（即相似的词）
        indices = np.argsort(diff)[:top_k]
        
        similar_words = []
        for idx in indices:
            if diff[idx] < 0.1:  # 只返回差异很小的
                similar_words.append({
                    'word': feature_names[idx],
                    'tfidf_1': float(vectors[0][idx]),
                    'tfidf_2': float(vectors[1][idx]),
                    'diff': float(diff[idx])
                })
                
        return similar_words
