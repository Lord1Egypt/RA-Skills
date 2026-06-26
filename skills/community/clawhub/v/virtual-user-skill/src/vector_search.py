#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量检索模块 - 基于场景库的相似度搜索

功能：
1. 加载场景库数据
2. 计算问题与场景的相似度
3. 返回最相关的场景
"""

import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class VectorSearchEngine:
    """向量检索引擎"""
    
    def __init__(self, data_dir=None):
        """
        初始化检索引擎
        
        Args:
            data_dir: 数据目录路径，默认使用 skill 的 data 目录
        """
        if data_dir is None:
            # 默认使用 skill 的 data 目录
            self.data_dir = Path(__file__).parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)
        
        self.model = None
        self.scenarios = None
        self.embeddings = None
        self.loaded = False
    
    def load_model(self, model_name='shibing624/text2vec-base-chinese'):
        """加载向量化模型"""
        print(f"🤖 加载向量化模型：{model_name}")
        self.model = SentenceTransformer(model_name)
        print("✅ 模型加载完成")
    
    def load_scenarios(self, encrypted_file='scenario_library.json.enc'):
        """
        加载场景库数据
        
        Args:
            encrypted_file: 加密的场景库文件名
        """
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        from encrypt import EncryptManager
        
        encrypted_path = self.data_dir / encrypted_file
        
        if not encrypted_path.exists():
            raise FileNotFoundError(f"场景库文件不存在：{encrypted_path}")
        
        print(f"📂 加载场景库：{encrypted_path}")
        
        # 解密数据
        manager = EncryptManager()
        decrypted_json = manager.decrypt_file(encrypted_path)
        self.scenarios = json.loads(decrypted_json)
        
        print(f"✅ 场景库加载完成，共 {len(self.scenarios)} 条场景")
        self.loaded = True
    
    def load_embeddings(self, embeddings_file='scenario_embeddings.npy'):
        """
        加载预计算的向量
        
        Args:
            embeddings_file: 向量文件名
        """
        embeddings_path = self.data_dir / embeddings_file
        
        if not embeddings_path.exists():
            raise FileNotFoundError(f"向量文件不存在：{embeddings_path}")
        
        print(f"📂 加载向量：{embeddings_path}")
        self.embeddings = np.load(embeddings_path)
        print(f"✅ 向量加载完成，形状：{self.embeddings.shape}")
    
    def ensure_model_loaded(self):
        """确保模型已加载"""
        if self.model is None:
            self.load_model()
    
    def ensure_data_loaded(self):
        """确保数据已加载"""
        if not self.loaded:
            self.load_scenarios()
            self.load_embeddings()
    
    def encode_query(self, query):
        """将查询文本向量化"""
        self.ensure_model_loaded()
        embedding = self.model.encode([query], show_progress_bar=False)
        return embedding[0]
    
    def search(self, query, top_k=10):
        """
        搜索最相关的场景
        
        Args:
            query: 用户问题
            top_k: 返回最相关的 K 个场景
        
        Returns:
            list: 最相关的场景列表
        """
        self.ensure_data_loaded()
        
        # 计算查询向量
        query_embedding = self.encode_query(query)
        
        # 计算余弦相似度
        similarities = cosine_similarity(
            [query_embedding], 
            self.embeddings
        )[0]
        
        # 获取 top_k 个最相关的索引
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # 返回对应的场景
        results = []
        for idx in top_indices:
            scenario = self.scenarios[idx].copy()
            scenario['similarity_score'] = float(similarities[idx])
            results.append(scenario)
        
        return results
    
    def search_and_group(self, query, top_k=20, group_by='用户具体场景'):
        """
        搜索并分组场景（用于生成多样化的虚拟用户类型）
        
        Args:
            query: 用户问题
            top_k: 搜索的场景数量
            group_by: 分组字段
        
        Returns:
            dict: 按字段分组的场景
        """
        results = self.search(query, top_k=top_k)
        
        # 按指定字段分组
        groups = {}
        for scenario in results:
            key = scenario.get(group_by, '未知')
            if key not in groups:
                groups[key] = []
            groups[key].append(scenario)
        
        return groups


# 测试代码
if __name__ == "__main__":
    # 测试用（需要实际数据文件）
    print("向量检索模块测试")
    print("注意：需要实际的场景库数据文件才能运行完整测试")
