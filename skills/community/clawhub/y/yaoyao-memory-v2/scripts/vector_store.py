#!/usr/bin/env python3
"""ChromaDB 向量存储集成 - yaoyao-memory
支持多向量方案：本地 ChromaDB + Gitee API
"""
import json
import os
import time
from pathlib import Path

# 配置
PERSIST_DIR = Path.home() / ".openclaw" / "workspace" / "memory" / "chroma_db"
COLLECTION_NAME = "yaoyao_memory"

# 全局客户端（延迟初始化）
_chroma_client = None
_collection = None

def _get_chroma():
    """获取或创建ChromaDB客户端（单例）- 延迟导入"""
    global _chroma_client, _collection
    if _chroma_client is None:
        # 延迟导入 chromadb（重量级库）
        import chromadb
        from chromadb.config import Settings
        
        PERSIST_DIR.mkdir(parents=True, exist_ok=True)
        # 使用 PersistentClient 以支持持久化
        _chroma_client = chromadb.PersistentClient(
            path=str(PERSIST_DIR),
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        _collection = _chroma_client.get_or_create_collection(COLLECTION_NAME)
    return _collection

class VectorStore:
    """ChromaDB 向量存储 - 多向量方案"""
    
    def __init__(self, persist_dir=None):
        self.persist_dir = Path(persist_dir) if persist_dir else PERSIST_DIR
        self.collection = _get_chroma()
        
    def add(self, texts, ids, metadata=None):
        """添加文档到向量存储"""
        if metadata is None:
            # ChromaDB requires metadata to have at least one key-value pair
            metadata = [{'_type': 'memory'} for _ in range(len(texts))]
        
        self.collection.add(
            documents=texts,
            ids=ids,
            metadatas=metadata
        )
        
    def search(self, query_texts, n_results=5):
        """搜索向量（使用ChromaDB内置embedding）"""
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results
        )
        return results
    
    def hybrid_search(self, query_text, gitee_embedding_func, n_results=5):
        """混合搜索：先用本地ChromaDB搜索，再用Gitee API重排序
        
        Args:
            query_text: 查询文本
            gitee_embedding_func: Gitee API embedding函数
            n_results: 返回数量
        """
        # 1. 本地快速搜索（ChromaDB内置模型all-MiniLM-L6-v2, 384维）
        local_results = self.search([query_text], n_results=n_results * 2)
        
        if not local_results.get('ids') or not local_results['ids'][0]:
            return local_results
        
        # 2. 用Gitee API获取高质量embedding进行重排序
        query_emb = gitee_embedding_func(query_text)
        if not query_emb:
            return local_results
        
        # 3. 对本地结果重排序
        reranked = []
        for i, doc_id in enumerate(local_results['ids'][0]):
            doc = local_results['documents'][0][i]
            # 使用Gitee embedding计算相似度
            doc_emb = gitee_embedding_func(doc)
            if doc_emb:
                score = self._cosine_sim(query_emb, doc_emb)
                reranked.append({
                    'id': doc_id,
                    'document': doc,
                    'score': score,
                    'metadata': local_results['metadatas'][0][i] if local_results['metadatas'] else {}
                })
        
        # 按分数排序
        reranked.sort(key=lambda x: -x['score'])
        return {
            'ids': [[r['id'] for r in reranked[:n_results]]],
            'documents': [[r['document'] for r in reranked[:n_results]]],
            'distances': [[r['score'] for r in reranked[:n_results]]],
            'metadatas': [[r['metadata'] for r in reranked[:n_results]]]
        }
    
    @staticmethod
    def _cosine_sim(a, b):
        """计算余弦相似度"""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0
    
    def get(self, ids):
        """获取指定ID的文档"""
        return self.collection.get(ids)
    
    def delete(self, ids):
        """删除指定ID的文档"""
        self.collection.delete(ids)
    
    def count(self):
        """获取文档数量"""
        return self.collection.count()
    
    def sync_from_memory(self, memory_items):
        """从memory.py的index同步数据到ChromaDB
        
        Args:
            memory_items: list of dicts with 'id', 'title', 'type', etc.
        """
        texts = []
        ids = []
        metadata = []
        
        for item in memory_items:
            title = item.get('title', '')
            if not title:
                continue
            texts.append(title)
            ids.append(item.get('id', title))
            metadata.append({
                'type': item.get('type', 'info'),
                'importance': item.get('importance', 'Normal'),
                'file': item.get('file', '')
            })
        
        if texts:
            self.add(texts, ids, metadata)
        
        return len(texts)

if __name__ == "__main__":
    vs = VectorStore()
    print(f"ChromaDB VectorStore initialized")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Documents: {vs.count()}")
