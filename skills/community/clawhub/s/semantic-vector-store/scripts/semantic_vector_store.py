#!/usr/bin/env python3
"""
语义向量库 - 提供向量存储与语义搜索功能
优化版本：使用 sentence-transformers 嵌入模型 + FAISS 向量索引
"""

import json
import sqlite3
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
from datetime import datetime
import hashlib
import logging
import pickle
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    logger.warning("sentence-transformers 不可用，将使用随机向量（存根）")
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    logger.warning("FAISS 不可用，将使用线性扫描搜索")
    FAISS_AVAILABLE = False
    faiss = None

class EmbeddingModel:
    """嵌入模型（使用 sentence-transformers 或存根）"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        
        if SENTENCE_TRANSFORMERS_AVAILABLE and SentenceTransformer is not None:
            try:
                logger.info(f"加载 sentence-transformers 模型: {model_name}")
                self.model = SentenceTransformer(model_name)
                self.dimension = self.model.get_sentence_embedding_dimension()
                logger.info(f"模型加载成功，维度: {self.dimension}")
            except Exception as e:
                logger.error(f"加载 sentence-transformers 模型失败: {e}")
                self._fallback_to_stub()
        else:
            self._fallback_to_stub()
    
    def _fallback_to_stub(self):
        """回退到存根模型"""
        logger.warning("使用存根嵌入模型（随机向量）")
        self.model = None
        self.dimension = 384  # MiniLM-L6-v2 的维度
    
    def embed(self, text: str) -> List[float]:
        """将文本转换为向量"""
        if self.model is not None:
            # 使用真实模型
            vector = self.model.encode(text, normalize_embeddings=True).tolist()
            return vector
        else:
            # 存根：返回随机向量
            np.random.seed(hash(text) % 2**32)
            vector = np.random.randn(self.dimension).tolist()
            norm = np.linalg.norm(vector)
            if norm > 0:
                vector = (vector / norm).tolist()
            return vector
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量嵌入"""
        if self.model is not None and texts:
            vectors = self.model.encode(texts, normalize_embeddings=True).tolist()
            return vectors
        else:
            return [self.embed(text) for text in texts]

class FAISSIndex:
    """FAISS 向量索引管理器"""
    
    def __init__(self, dimension: int, index_type: str = "flat"):
        self.dimension = dimension
        self.index_type = index_type
        self.index = None
        self.vector_ids = []  # 存储每个向量对应的 memory_id
        self._init_index()
    
    def _init_index(self):
        """初始化 FAISS 索引"""
        if not FAISS_AVAILABLE or faiss is None:
            logger.warning("FAISS 不可用，使用空索引")
            self.index = None
            return
        
        try:
            if self.index_type == "flat":
                # 使用内积索引（向量已归一化，内积 = 余弦相似度）
                self.index = faiss.IndexFlatIP(self.dimension)
            else:
                # 回退到平面索引
                self.index = faiss.IndexFlatIP(self.dimension)
            
            logger.info(f"FAISS 索引初始化完成，维度: {self.dimension}, 类型: {self.index_type}")
        except Exception as e:
            logger.error(f"初始化 FAISS 索引失败: {e}")
            self.index = None
    
    def add_vectors(self, vectors: np.ndarray, vector_ids: List[str]):
        """添加向量到索引"""
        if self.index is None or vectors.shape[0] == 0:
            logger.warning(f"无法添加向量: index={self.index}, vectors.shape={vectors.shape if self.index else 'N/A'}")
            return False
        
        try:
            # 确保向量是 float32 类型
            vectors = vectors.astype(np.float32)
            before = self.index.ntotal
            self.index.add(vectors)
            after = self.index.ntotal
            self.vector_ids.extend(vector_ids)
            logger.info(f"FAISS 索引添加向量: {before} -> {after} (增加了 {after - before} 个), vector_ids 数量: {len(vector_ids)}")
            return True
        except Exception as e:
            logger.error(f"添加向量到 FAISS 索引失败: {e}")
            return False
    
    def search(self, query_vector: np.ndarray, k: int = 10) -> Tuple[List[List[int]], List[List[float]]]:
        """
        搜索相似向量
        
        Returns:
            (indices, scores): 索引列表和相似度分数列表
        """
        if self.index is None or self.index.ntotal == 0:
            return [], []
        
        try:
            query_vector = query_vector.astype(np.float32).reshape(1, -1)
            distances, indices = self.index.search(query_vector, min(k, self.index.ntotal))
            # 将距离转换为相似度分数（内积范围 [-1, 1]，归一化后为 [0, 1]）
            scores = [(dist + 1) / 2 for dist in distances[0]]
            return indices[0].tolist(), scores
        except Exception as e:
            logger.error(f"FAISS 搜索失败: {e}")
            return [], []
    
    def get_stats(self) -> Dict[str, Any]:
        """获取索引统计信息"""
        if self.index is None:
            return {"available": False, "total_vectors": 0}
        
        return {
            "available": True,
            "total_vectors": self.index.ntotal,
            "dimension": self.dimension,
            "index_type": self.index_type
        }
    
    def save(self, filepath: str):
        """保存索引到文件"""
        if self.index is None:
            return False
        
        try:
            faiss.write_index(self.index, filepath)
            # 同时保存向量ID映射
            id_map_file = Path(filepath).with_suffix('.ids.pkl')
            with open(id_map_file, 'wb') as f:
                pickle.dump(self.vector_ids, f)
            return True
        except Exception as e:
            logger.error(f"保存 FAISS 索引失败: {e}")
            return False
    
    def load(self, filepath: str):
        """从文件加载索引"""
        if not FAISS_AVAILABLE:
            return False
        
        try:
            self.index = faiss.read_index(filepath)
            # 加载向量ID映射
            id_map_file = Path(filepath).with_suffix('.ids.pkl')
            if id_map_file.exists():
                with open(id_map_file, 'rb') as f:
                    self.vector_ids = pickle.load(f)
            else:
                # 重建向量ID（假设顺序匹配）
                self.vector_ids = [f"vector_{i}" for i in range(self.index.ntotal)]
            return True
        except Exception as e:
            logger.error(f"加载 FAISS 索引失败: {e}")
            return False

class VectorStore:
    """向量存储（SQLite + FAISS 索引）"""
    
    def __init__(self, db_path: str = "~/.config/cortexgraph/semantic_vectors.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.embedder = EmbeddingModel()
        self.dimension = self.embedder.dimension
        
        # 初始化数据库
        self._init_db()
        
        # 初始化 FAISS 索引
        self.faiss_index = FAISSIndex(self.dimension, index_type="flat")
        self.faiss_index_path = self.db_path.with_suffix('.faiss')
        
        # 从数据库加载现有向量到索引
        self._load_vectors_to_index()
    
    def _init_db(self):
        """初始化 SQLite 数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建记忆表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                memory_id TEXT PRIMARY KEY,
                text_content TEXT NOT NULL,
                embedding BLOB,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_id ON memories(memory_id)")
        
        conn.commit()
        conn.close()
        logger.info(f"向量数据库已初始化: {self.db_path}")
    
    def _load_vectors_to_index(self):
        """从数据库加载向量到 FAISS 索引"""
        if not FAISS_AVAILABLE:
            return
        
        # 检查是否有保存的索引文件
        if self.faiss_index_path.exists():
            logger.info(f"从文件加载 FAISS 索引: {self.faiss_index_path}")
            if self.faiss_index.load(str(self.faiss_index_path)):
                logger.info(f"FAISS 索引加载成功，包含 {self.faiss_index.index.ntotal} 个向量")
                return
        
        # 否则从数据库加载
        logger.info("从数据库重建 FAISS 索引...")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT memory_id, embedding FROM memories WHERE embedding IS NOT NULL")
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            logger.info("数据库中没有向量数据")
            return
        
        vector_ids = []
        vectors = []
        
        for memory_id, embedding_blob in rows:
            try:
                # 反序列化向量
                vector = pickle.loads(embedding_blob)
                if len(vector) == self.dimension:
                    vector_ids.append(memory_id)
                    vectors.append(vector)
            except Exception as e:
                logger.warning(f"解析向量失败 {memory_id}: {e}")
        
        if vectors:
            vectors_np = np.array(vectors, dtype=np.float32)
            self.faiss_index.add_vectors(vectors_np, vector_ids)
            logger.info(f"FAISS 索引重建完成，添加了 {len(vectors)} 个向量")
            
            # 保存索引
            self.faiss_index.save(str(self.faiss_index_path))
    
    def add_memory(self, memory_id: str, text: str, metadata: Dict = None) -> Dict[str, Any]:
        """添加记忆到向量存储"""
        start_time = time.time()
        
        # 生成嵌入向量
        embedding = self.embedder.embed(text)
        embedding_blob = pickle.dumps(embedding)
        
        metadata_json = json.dumps(metadata or {})
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 插入或更新记录
            cursor.execute("""
                INSERT OR REPLACE INTO memories (memory_id, text_content, embedding, metadata, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (memory_id, text, embedding_blob, metadata_json))
            
            conn.commit()
            
            # 添加到 FAISS 索引
            if self.faiss_index.index is not None:
                vector_np = np.array(embedding, dtype=np.float32).reshape(1, -1)
                self.faiss_index.add_vectors(vector_np, [memory_id])
                # 保存索引以确保持久化
                self.faiss_index.save(str(self.faiss_index_path))
            
            elapsed = time.time() - start_time
            
            return {
                "success": True,
                "memory_id": memory_id,
                "dimension": self.dimension,
                "elapsed_seconds": elapsed
            }
            
        except Exception as e:
            conn.rollback()
            logger.error(f"添加记忆失败 {memory_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            conn.close()
    
    def add_memories_batch(self, memories: List[Dict]) -> Dict[str, Any]:
        """批量添加记忆"""
        if not memories:
            return {"success": True, "count": 0}
        
        start_time = time.time()
        
        # 准备批量数据
        texts = [mem.get('text', '') for mem in memories]
        memory_ids = [mem.get('memory_id') for mem in memories]
        metadata_list = [mem.get('metadata', {}) for mem in memories]
        
        # 批量生成嵌入
        embeddings = self.embedder.embed_batch(texts)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        success_count = 0
        errors = []
        
        try:
            for i, (memory_id, text, embedding, metadata) in enumerate(zip(memory_ids, texts, embeddings, metadata_list)):
                try:
                    embedding_blob = pickle.dumps(embedding)
                    metadata_json = json.dumps(metadata)
                    
                    cursor.execute("""
                        INSERT OR REPLACE INTO memories (memory_id, text_content, embedding, metadata, updated_at)
                        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """, (memory_id, text, embedding_blob, metadata_json))
                    
                    success_count += 1
                except Exception as e:
                    errors.append(f"{memory_id}: {e}")
            
            conn.commit()
            
            # 批量添加到 FAISS 索引
            if self.faiss_index.index is not None and success_count > 0:
                successful_embeddings = []
                successful_ids = []
                
                for i, (memory_id, embedding) in enumerate(zip(memory_ids, embeddings)):
                    if i < len(errors):  # 跳过错误的
                        continue
                    successful_embeddings.append(embedding)
                    successful_ids.append(memory_id)
                
                if successful_embeddings:
                    vectors_np = np.array(successful_embeddings, dtype=np.float32)
                    self.faiss_index.add_vectors(vectors_np, successful_ids)
            
            elapsed = time.time() - start_time
            
            return {
                "success": True,
                "count": success_count,
                "error_count": len(errors),
                "errors": errors if errors else None,
                "elapsed_seconds": elapsed,
                "avg_time_per_memory": elapsed / len(memories) if memories else 0
            }
            
        except Exception as e:
            conn.rollback()
            logger.error(f"批量添加记忆失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "count": 0,
                "error_count": len(memories)
            }
        finally:
            conn.close()
    
    def search(self, query: str, limit: int = 10, min_score: float = 0.0) -> List[Dict[str, Any]]:
        """语义搜索"""
        start_time = time.time()
        
        # 生成查询向量
        query_vector = self.embedder.embed(query)
        query_vector_np = np.array(query_vector, dtype=np.float32)
        
        results = []
        
        # 使用 FAISS 索引搜索
        if self.faiss_index.index is not None and self.faiss_index.index.ntotal > 0:
            indices, scores = self.faiss_index.search(query_vector_np, limit * 2)  # 多取一些用于过滤
            
            if indices:
                # 从数据库获取详细信息
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                try:
                    for idx, score in zip(indices, scores):
                        if idx < 0 or score < min_score:
                            continue
                        
                        memory_id = self.faiss_index.vector_ids[idx]
                        cursor.execute("""
                            SELECT text_content, metadata FROM memories WHERE memory_id = ?
                        """, (memory_id,))
                        row = cursor.fetchone()
                        
                        if row:
                            text_content, metadata_json = row
                            metadata = json.loads(metadata_json) if metadata_json else {}
                            
                            results.append({
                                "memory_id": memory_id,
                                "text": text_content,
                                "score": float(score),
                                "metadata": metadata
                            })
                        
                        if len(results) >= limit:
                            break
                finally:
                    conn.close()
        else:
            # 回退到线性扫描（仅用于小数据集或测试）
            logger.warning("FAISS 索引不可用，使用线性扫描搜索")
            results = self._linear_search(query_vector, limit, min_score)
        
        elapsed = time.time() - start_time
        
        # 按分数排序
        results.sort(key=lambda x: x["score"], reverse=True)
        
        logger.debug(f"搜索完成: 查询='{query[:50]}...', 结果数={len(results)}, 耗时={elapsed*1000:.1f}ms")
        
        return results
    
    def _linear_search(self, query_vector: List[float], limit: int, min_score: float) -> List[Dict]:
        """线性扫描搜索（回退方法）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT memory_id, text_content, embedding, metadata FROM memories WHERE embedding IS NOT NULL")
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        query_np = np.array(query_vector, dtype=np.float32)
        
        for memory_id, text_content, embedding_blob, metadata_json in rows:
            try:
                vector = pickle.loads(embedding_blob)
                vector_np = np.array(vector, dtype=np.float32)
                
                # 计算余弦相似度
                similarity = float(np.dot(query_np, vector_np))  # 向量已归一化
                
                if similarity >= min_score:
                    metadata = json.loads(metadata_json) if metadata_json else {}
                    results.append({
                        "memory_id": memory_id,
                        "text": text_content,
                        "score": similarity,
                        "metadata": metadata
                    })
            except Exception as e:
                logger.warning(f"线性搜索处理失败 {memory_id}: {e}")
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取向量存储统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 数据库统计
        cursor.execute("SELECT COUNT(*) FROM memories")
        total_memories = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM memories WHERE embedding IS NOT NULL")
        total_with_embeddings = cursor.fetchone()[0]
        
        conn.close()
        
        # FAISS 索引统计
        faiss_stats = self.faiss_index.get_stats()
        
        return {
            "summary": {
                "total_memories": total_memories,
                "total_with_embeddings": total_with_embeddings,
                "dimension": self.dimension,
                "embedding_model": self.embedder.model_name
            },
            "faiss_index": faiss_stats,
            "database_path": str(self.db_path)
        }
    
    def cleanup(self, older_than_days: int = 30) -> Dict[str, Any]:
        """清理旧数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM memories 
            WHERE julianday('now') - julianday(updated_at) > ?
        """, (older_than_days,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            # 需要重建索引
            self._load_vectors_to_index()
        
        return {
            "success": True,
            "deleted_count": deleted_count,
            "older_than_days": older_than_days
        }

    def health_check(self) -> Dict[str, Any]:
        """健康检查（适配器兼容性）"""
        stats = self.get_stats()
        return {
            "status": "healthy" if stats["summary"]["total_with_embeddings"] > 0 else "warning",
            "stats": stats
        }
    
    def embed(self, text: str) -> List[float]:
        """向量化文本（适配器兼容性）"""
        return self.embedder.embed(text)
    
    def add_vector(self, memory_id: str, vector: List[float], metadata: dict = None):
        """添加预计算向量（适配器兼容性）"""
        embedding_blob = pickle.dumps(vector)
        metadata_json = json.dumps(metadata or {})
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO memories (memory_id, text_content, embedding, metadata, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (memory_id, "", embedding_blob, metadata_json))
            conn.commit()
            
            # 添加到 FAISS 索引
            if self.faiss_index.index is not None:
                vector_np = np.array(vector, dtype=np.float32).reshape(1, -1)
                self.faiss_index.add_vectors(vector_np, [memory_id])
            
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @property
    def store(self):
        """存储对象（适配器兼容性）"""
        return self


def main():
    """测试函数"""
    store = VectorStore()
    
    print("=== 语义向量存储测试 ===")
    
    # 添加测试记忆
    test_memories = [
        {
            "memory_id": "test_1",
            "text": "OpenClaw 是一个智能助手平台",
            "metadata": {"type": "definition", "source": "test"}
        },
        {
            "memory_id": "test_2", 
            "text": "记忆系统包括共现图和语义向量存储",
            "metadata": {"type": "description", "source": "test"}
        },
        {
            "memory_id": "test_3",
            "text": "FAISS 是高效的向量相似度搜索库",
            "metadata": {"type": "definition", "source": "test"}
        }
    ]
    
    print("1. 添加测试记忆...")
    for mem in test_memories:
        result = store.add_memory(mem["memory_id"], mem["text"], mem["metadata"])
        print(f"   添加 {mem['memory_id']}: {'成功' if result['success'] else '失败'}")
    
    # 搜索测试
    print("\n2. 搜索测试...")
    queries = ["OpenClaw", "记忆系统", "向量搜索"]
    
    for query in queries:
        results = store.search(query, limit=3)
        print(f"   查询: '{query}' → 找到 {len(results)} 个结果")
        for i, res in enumerate(results[:2]):
            print(f"      {i+1}. {res['memory_id']} (分数: {res['score']:.3f})")
    
    # 统计信息
    print("\n3. 系统统计:")
    stats = store.get_stats()
    print(f"   总记忆数: {stats['summary']['total_memories']}")
    print(f"   向量维度: {stats['summary']['dimension']}")
    print(f"   FAISS 索引: {'可用' if stats['faiss_index']['available'] else '不可用'}")
    if stats['faiss_index']['available']:
        print(f"   索引向量数: {stats['faiss_index']['total_vectors']}")
    
    print("\n=== 测试完成 ===")

# 为了向后兼容性，提供 SemanticVectorStore 作为 VectorStore 的别名
SemanticVectorStore = VectorStore

if __name__ == "__main__":
    main()