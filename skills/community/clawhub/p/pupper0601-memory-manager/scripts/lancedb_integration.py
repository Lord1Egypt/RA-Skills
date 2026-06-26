#!/usr/bin/env python3
"""
lancedb_integration.py - LanceDB 向量索引集成

功能：
  1. HNSW 索引加速向量搜索
  2. 查询缓存避免重复搜索
  3. 并行 embedding 加速写入

安装依赖：
  pip install lancedb  # ~50MB

配置：
  # 方式1：环境变量
  export LANCEDB_ENABLED=true
  export LANCEDB_INDEX_TYPE=HNSW
  
  # 方式2：代码配置
  from lancedb_integration import LanceDBManager
  manager = LanceDBManager(enabled=True, index_type="HNSW")
"""

import os
import sqlite3
import json
import time
import hashlib
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Dict, Any

# LanceDB 懒加载（可选依赖）
LANCEDB_AVAILABLE = False
try:
    import lancedb
    import pyarrow as pa
    LANCEDB_AVAILABLE = True
except ImportError:
    lancedb = None
    pa = None

# ─────────────────────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────────────────────

# 是否启用 LanceDB（通过环境变量或代码控制）
ENABLED = os.environ.get("LANCEDB_ENABLED", "false").lower() == "true"

# HNSW 参数
HNSW_M = int(os.environ.get("HNSW_M", "16"))           # 每个节点的最大连接数
HNSW_EF_CONSTRUCTION = int(os.environ.get("HNSW_EF_CONSTRUCTION", "200"))  # 构建时候选集
HNSW_EF_SEARCH = int(os.environ.get("HNSW_EF_SEARCH", "100"))              # 搜索时候选集

# 并行 embedding 配置
PARALLEL_EMBED_ENABLED = os.environ.get("PARALLEL_EMBED", "true").lower() == "true"
PARALLEL_WORKERS = int(os.environ.get("PARALLEL_WORKERS", "4"))  # 并行线程数
EMBED_BATCH_SIZE = int(os.environ.get("EMBED_BATCH_SIZE", "20"))  # 每批大小

# 缓存配置
CACHE_ENABLED = os.environ.get("CACHE_ENABLED", "true").lower() == "true"
CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", "3600"))  # 缓存有效期
CACHE_DB_NAME = ".memory_search_cache.db"


# ─────────────────────────────────────────────────────────────
# LanceDB Manager
# ─────────────────────────────────────────────────────────────

class LanceDBManager:
    """
    LanceDB 向量索引管理器
    
    功能：
    - HNSW 索引加速搜索
    - 增量索引更新
    - 与 SQLite 向量库共存
    """
    
    def __init__(self, db_path: str, enabled: bool = None, index_type: str = "HNSW"):
        self.db_path = db_path
        self.enabled = enabled if enabled is not None else ENABLED
        self.index_type = index_type
        self.db = None
        self.table = None
        
        if self.enabled and not LANCEDB_AVAILABLE:
            print("[Warning] LanceDB not installed. Run: pip install lancedb")
            self.enabled = False
    
    def connect(self):
        """连接到 LanceDB"""
        if not self.enabled:
            return False
        
        try:
            # LanceDB 支持 SQLite 后端
            uri = f"sqlite:///{self.db_path}"
            self.db = lancedb.connect(uri)
            
            # 打开或创建表
            table_name = "memory_embeddings"
            if table_name in self.db.table_names():
                self.table = self.db.open_table(table_name)
            else:
                self.table = self._create_table()
            
            return True
        except Exception as e:
            print(f"[Warning] LanceDB connection failed: {e}")
            self.enabled = False
            return False
    
    def _create_table(self):
        """创建 LanceDB 表（含 HNSW 索引）"""
        # 定义 schema
        schema = pa.schema([
            pa.field("chunk_id", pa.string()),
            pa.field("uid", pa.string()),
            pa.field("scope", pa.string()),
            pa.field("level", pa.string()),
            pa.field("filepath", pa.string()),
            pa.field("section_idx", pa.int32()),
            pa.field("title", pa.string()),
            pa.field("semantic_key", pa.string()),
            pa.field("content", pa.string()),
            pa.field("raw_content", pa.string()),
            pa.field("content_hash", pa.string()),
            pa.field("mtime", pa.float64()),
            pa.field("created_at", pa.string()),
            pa.field("importance_score", pa.float32()),
            pa.field("related_ids", pa.string()),
            # 向量字段
            pa.field("vector", pa.list_(pa.float32())),
        ])
        
        tbl = self.db.create_table("memory_embeddings", schema=schema)
        
        # 创建 HNSW 索引
        tbl.create_index(
            vector_column_name="vector",
            index_type=self.index_type,
            metric="cosine",
            parameters={
                "M": HNSW_M,
                "efConstruction": HNSW_EF_CONSTRUCTION,
                "ef": HNSW_EF_SEARCH,
            }
        )
        
        return tbl
    
    def add_vectors(self, records: List[Dict]):
        """
        批量添加向量记录
        
        Args:
            records: List of dict with keys: chunk_id, uid, scope, level, 
                    filepath, title, semantic_key, content, vector, etc.
        """
        if not self.enabled or not self.table:
            return False
        
        try:
            self.table.add(records)
            return True
        except Exception as e:
            print(f"[Warning] LanceDB add failed: {e}")
            return False
    
    def search(self, query_vector: List[float], top_k: int = 10, 
                uid: str = None, scope: str = None, level: str = None,
                filter_str: str = None) -> List[Dict]:
        """
        HNSW 向量搜索
        
        Args:
            query_vector: 查询向量
            top_k: 返回数量
            uid/scope/level: 过滤条件
            
        Returns:
            搜索结果列表
        """
        if not self.enabled or not self.table:
            return []
        
        try:
            # 构建过滤条件
            where_parts = []
            if uid and uid != "*":
                where_parts.append(f"uid = '{uid}'")
            if scope and scope != "*":
                where_parts.append(f"scope = '{scope}'")
            if level:
                where_parts.append(f"level = '{level}'")
            where_clause = " AND ".join(where_parts) if where_parts else None
            
            # 执行搜索
            results = self.table.search(query_vector) \
                .limit(top_k) \
                .select(["chunk_id", "uid", "scope", "level", "filepath", 
                        "title", "semantic_key", "content", "importance_score", 
                        "related_ids"]) \
                .to_list()
            
            return results
        except Exception as e:
            print(f"[Warning] LanceDB search failed: {e}")
            return []
    
    def rebuild_index(self, sqlite_db_path: str):
        """
        从 SQLite 重建 LanceDB 索引
        
        Args:
            sqlite_db_path: SQLite 数据库路径
        """
        if not self.enabled:
            return False
        
        try:
            # 读取 SQLite 数据
            conn = sqlite3.connect(sqlite_db_path)
            c = conn.cursor()
            c.execute("SELECT chunk_id, uid, scope, level, filepath, section_idx, "
                     "title, semantic_key, content, raw_content, content_hash, mtime, "
                     "created_at, importance_score, related_ids, embedding "
                     "FROM memory_embeddings")
            
            records = []
            for row in c.fetchall():
                emb = row[15]
                # 转换 bytes 到 list
                import struct
                vec = list(struct.unpack('f' * (len(emb) // 4), emb))
                
                records.append({
                    "chunk_id": row[0],
                    "uid": row[1],
                    "scope": row[2],
                    "level": row[3],
                    "filepath": row[4],
                    "section_idx": row[5],
                    "title": row[6],
                    "semantic_key": row[7],
                    "content": row[8],
                    "raw_content": row[9],
                    "content_hash": row[10],
                    "mtime": row[11],
                    "created_at": row[12],
                    "importance_score": row[13] or 50.0,
                    "related_ids": row[14] or "[]",
                    "vector": vec,
                })
            conn.close()
            
            if not records:
                return True
            
            # 清空并重建
            self.table.delete()
            self.table.add(records)
            
            print(f"  [LanceDB] Indexed {len(records)} vectors")
            return True
        except Exception as e:
            print(f"[Warning] LanceDB rebuild failed: {e}")
            return False
    
    def close(self):
        """关闭连接"""
        if self.db:
            self.db.close()


# ─────────────────────────────────────────────────────────────
# 查询缓存
# ─────────────────────────────────────────────────────────────

class SearchCache:
    """
    SQLite 实现的查询缓存
    
    避免重复查询同一条搜索，节省 API 调用
    """
    
    def __init__(self, base_path: str):
        self.db_path = os.path.join(os.path.dirname(base_path), CACHE_DB_NAME)
        self._init_cache_db()
        self._lock = threading.Lock()
    
    def _init_cache_db(self):
        """初始化缓存数据库"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS search_cache (
                cache_key    TEXT PRIMARY KEY,
                query        TEXT NOT NULL,
                uid          TEXT,
                scope        TEXT,
                level        TEXT,
                results      TEXT NOT NULL,  -- JSON 序列化
                created_at   TEXT NOT NULL,
                hit_count    INTEGER DEFAULT 1
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_created ON search_cache(created_at)")
        conn.close()
    
    def _make_key(self, query: str, uid: str, scope: str, level: str) -> str:
        """生成缓存键"""
        raw = f"{query}|{uid}|{scope}|{level}"
        return hashlib.md5(raw.encode()).hexdigest()
    
    def get(self, query: str, uid: str = None, scope: str = None, 
            level: str = None) -> Optional[List[Dict]]:
        """获取缓存结果"""
        if not CACHE_ENABLED:
            return None
        
        key = self._make_key(query, uid, scope, level)
        
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT results, created_at, hit_count FROM search_cache WHERE cache_key = ?", (key,))
            row = c.fetchone()
            
            if row:
                results_json, created_at, hit_count = row
                created = datetime.fromisoformat(created_at)
                age = (datetime.now() - created).total_seconds()
                
                if age < CACHE_TTL_SECONDS:
                    # 更新命中次数
                    c.execute("UPDATE search_cache SET hit_count = hit_count + 1 WHERE cache_key = ?", (key,))
                    conn.commit()
                    conn.close()
                    return json.loads(results_json)
                else:
                    # 过期，删除
                    c.execute("DELETE FROM search_cache WHERE cache_key = ?", (key,))
            
            conn.close()
            return None
    
    def set(self, query: str, results: List[Dict], 
            uid: str = None, scope: str = None, level: str = None):
        """设置缓存"""
        if not CACHE_ENABLED:
            return
        
        key = self._make_key(query, uid, scope, level)
        
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO search_cache 
                (cache_key, query, uid, scope, level, results, created_at, hit_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            """, (key, query, uid, scope, level, json.dumps(results, ensure_ascii=False),
                  datetime.now().isoformat()))
            conn.close()
    
    def clear_expired(self):
        """清理过期缓存"""
        if not CACHE_ENABLED:
            return
        
        cutoff = (datetime.now() - timedelta(seconds=CACHE_TTL_SECONDS)).isoformat()
        
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("DELETE FROM search_cache WHERE created_at < ?", (cutoff,))
            deleted = c.rowcount
            conn.commit()
            conn.close()
        
        if deleted > 0:
            print(f"  [Cache] Cleared {deleted} expired entries")
    
    def stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        if not CACHE_ENABLED:
            return {"enabled": False}
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT COUNT(*), SUM(hit_count) FROM search_cache")
        total, hits = c.fetchone()
        conn.close()
        
        return {
            "enabled": True,
            "total_entries": total or 0,
            "total_hits": hits or 0,
            "ttl_seconds": CACHE_TTL_SECONDS,
        }


# ─────────────────────────────────────────────────────────────
# 并行 Embedding
# ─────────────────────────────────────────────────────────────

def parallel_embed(texts: List[str], get_embeddings_func, 
                  workers: int = None, batch_size: int = None) -> List:
    """
    并行执行 embedding
    
    Args:
        texts: 文本列表
        get_embeddings_func: embedding 函数 (接受 list 返回 list)
        workers: 并行线程数
        batch_size: 每批大小
        
    Returns:
        向量列表
    """
    if not PARALLEL_EMBED_ENABLED or len(texts) < 10:
        # 数据量小，直接串行
        return get_embeddings_func(texts)
    
    workers = workers or PARALLEL_WORKERS
    batch_size = batch_size or EMBED_BATCH_SIZE
    
    # 分批
    batches = [texts[i:i+batch_size] for i in range(0, len(texts), batch_size)]
    
    results = [None] * len(batches)
    
    def process_batch(batch_idx, batch_texts):
        vectors = get_embeddings_func(batch_texts)
        return batch_idx, vectors
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(process_batch, i, batch): i 
            for i, batch in enumerate(batches)
        }
        
        for future in as_completed(futures):
            batch_idx, vectors = future.result()
            results[batch_idx] = vectors
    
    # 合并结果
    all_vectors = []
    for vectors in results:
        all_vectors.extend(vectors)
    
    return all_vectors


# ─────────────────────────────────────────────────────────────
# 搜索入口（整合 LanceDB + 缓存）
# ─────────────────────────────────────────────────────────────

def smart_search(query_vector: List[float], query_text: str,
                 lancedb_manager: LanceDBManager,
                 search_cache: SearchCache,
                 uid: str = None, scope: str = None, level: str = None,
                 top_k: int = 10, use_cache: bool = True) -> List[Dict]:
    """
    智能搜索：优先使用 LanceDB + 缓存
    
    搜索流程：
    1. 检查缓存 → 命中直接返回
    2. LanceDB HNSW 搜索 → 快速准确
    3. 回退到 SQLite 全表扫描
    """
    # 1. 缓存查询
    if use_cache and CACHE_ENABLED:
        cached = search_cache.get(query_text, uid, scope, level)
        if cached:
            return cached
    
    # 2. LanceDB 搜索
    if lancedb_manager.enabled:
        results = lancedb_manager.search(
            query_vector, top_k, uid, scope, level
        )
        if results:
            if use_cache and CACHE_ENABLED:
                search_cache.set(query_text, results, uid, scope, level)
            return results
    
    # 3. 回退到 SQLite（返回空，让调用方处理）
    return []


# ─────────────────────────────────────────────────────────────
# 便捷函数
# ─────────────────────────────────────────────────────────────

def get_lancedb_manager(db_path: str) -> LanceDBManager:
    """获取 LanceDB 管理器（懒加载）"""
    return LanceDBManager(db_path)


def get_search_cache(base_path: str) -> SearchCache:
    """获取搜索缓存"""
    return SearchCache(base_path)


if __name__ == "__main__":
    # 测试
    print("LanceDB Integration Module")
    print(f"  LanceDB available: {LANCEDB_AVAILABLE}")
    print(f"  Enabled: {ENABLED}")
    print(f"  Parallel embed: {PARALLEL_EMBED_ENABLED}")
    print(f"  Cache enabled: {CACHE_ENABLED}")
    
    if LANCEDB_AVAILABLE:
        print("\nHNSW Parameters:")
        print(f"  M: {HNSW_M}")
        print(f"  efConstruction: {HNSW_EF_CONSTRUCTION}")
        print(f"  efSearch: {HNSW_EF_SEARCH}")
