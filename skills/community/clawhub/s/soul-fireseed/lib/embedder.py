#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
lib/embedder.py
火种·灵魂 v2.0 - 隐空间映射器

将化石文本映射到语义向量空间，支持相似度计算和检索。
"""

import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path

try:
    from .extractor import Fossil
except ImportError:
    from extractor import Fossil


class FossilEmbedder:
    """
    隐空间映射器
    
    使用预训练模型将化石文本转换为向量，支持语义检索和聚类分析。
    
    注意: 需要安装 sentence-transformers 库
    pip install sentence-transformers
    
    使用示例:
        >>> embedder = FossilEmbedder()
        >>> vec = embedder.embed("我喜欢冒险")
        >>> similar = embedder.find_similar("我对风险的看法", fossils)
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 cache_enabled: bool = True,
                 cache_path: str = "cache/embeddings/"):
        """
        初始化嵌入器
        
        参数:
            model_name: 预训练模型名称
            cache_enabled: 是否启用缓存
            cache_path: 缓存路径
        """
        self.model_name = model_name
        self.cache_enabled = cache_enabled
        self.cache_path = Path(cache_path)
        
        # 尝试加载模型
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            self.available = True
        except ImportError:
            print("警告: sentence-transformers 未安装，嵌入功能不可用")
            print("安装命令: pip install sentence-transformers")
            self.model = None
            self.available = False
        
        # 缓存
        self.embedding_cache: Dict[str, List[float]] = {}
        if cache_enabled:
            self.cache_path.mkdir(parents=True, exist_ok=True)
            self._load_cache()
    
    def embed(self, text: str) -> Optional[List[float]]:
        """
        将文本转换为向量
        
        参数:
            text: 输入文本
            
        返回:
            向量表示（列表），失败返回 None
        """
        if not self.available:
            return None
        
        # 检查缓存
        cache_key = self._get_cache_key(text)
        if cache_key in self.embedding_cache:
            return self.embedding_cache[cache_key]
        
        try:
            embedding = self.model.encode(text).tolist()
            
            # 缓存
            if self.cache_enabled:
                self.embedding_cache[cache_key] = embedding
                self._save_cache_item(cache_key, embedding)
            
            return embedding
        except Exception as e:
            print(f"嵌入失败: {e}")
            return None
    
    def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        计算两个向量的余弦相似度
        
        参数:
            vec1: 向量1
            vec2: 向量2
            
        返回:
            相似度 (0.0 - 1.0)
        """
        if not vec1 or not vec2:
            return 0.0
        
        # 余弦相似度
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def find_similar(self, query: str, fossils: List[Fossil], 
                    top_k: int = 10, threshold: float = 0.5) -> List[Tuple[Fossil, float]]:
        """
        检索与查询最相似的化石
        
        参数:
            query: 查询文本
            fossils: 候选化石列表
            top_k: 返回数量
            threshold: 相似度阈值
            
        返回:
            (化石, 相似度) 元组列表，按相似度降序排列
        """
        if not self.available or not fossils:
            return []
        
        # 编码查询
        query_vec = self.embed(query)
        if not query_vec:
            return []
        
        # 计算所有化石的相似度
        results = []
        for fossil in fossils:
            fossil_vec = self.embed(fossil.content)
            if fossil_vec:
                sim = self.similarity(query_vec, fossil_vec)
                if sim >= threshold:
                    results.append((fossil, sim))
        
        # 按相似度排序
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_k]
    
    def cluster(self, fossils: List[Fossil], n_clusters: int = 5) -> Dict[int, List[Fossil]]:
        """
        对化石进行聚类分析
        
        参数:
            fossils: 化石列表
            n_clusters: 聚类数量
            
        返回:
            {簇ID: 化石列表} 字典
        """
        if not self.available or len(fossils) < n_clusters:
            return {0: fossils}
        
        try:
            from sklearn.cluster import KMeans
            import numpy as np
            
            # 获取所有向量
            vectors = []
            valid_fossils = []
            for fossil in fossils:
                vec = self.embed(fossil.content)
                if vec:
                    vectors.append(vec)
                    valid_fossils.append(fossil)
            
            if not vectors:
                return {0: fossils}
            
            # K-Means 聚类
            X = np.array(vectors)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X)
            
            # 分组
            clusters: Dict[int, List[Fossil]] = {}
            for i, label in enumerate(labels):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(valid_fossils[i])
            
            return clusters
        
        except ImportError:
            print("警告: scikit-learn 未安装，聚类功能不可用")
            print("安装命令: pip install scikit-learn")
            return {0: fossils}
    
    def _get_cache_key(self, text: str) -> str:
        """生成缓存键"""
        import hashlib
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def _load_cache(self):
        """从磁盘加载缓存"""
        cache_file = self.cache_path / "embeddings.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self.embedding_cache = json.load(f)
            except Exception:
                pass
    
    def _save_cache_item(self, key: str, embedding: List[float]):
        """保存单个缓存项"""
        cache_file = self.cache_path / "embeddings.json"
        try:
            # 简化：每次保存全部（实际应增量保存）
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.embedding_cache, f)
        except Exception:
            pass
