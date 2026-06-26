# Recall API

## VectorMindRecall

### 初始化

```python
from recall.recall import VectorMindRecall

recall = VectorMindRecall(
    brain_db_path="~/.local/share/neural-memory/brains.db",
    infinitydb_dir="memory/layers/infinitydb"
)
```

### search()

语义搜索接口

```python
results = recall.search(query: str, top_k: int = 10) -> list[dict]
```

返回:
```python
[
    {"id": "chunk_id", "content": "记忆内容", "score": 0.85, "memory_type": "task"},
    ...
]
```

### search_by_session()

按 session 搜索

```python
results = recall.search_by_session(session_id: str, max_hops: int = 3) -> dict[int, list]
```

## InfinityDBLite

### vector_search()

暴力向量搜索

```python
from recall.infinitydb_lite import InfinityDBLite

db = InfinityDBLite()
results = db.vector_search(query_vector: list[float], k: int = 10) -> list[tuple[str, float]]
```

### adjacency_bfs()

内存图遍历

```python
bfs = db.adjacency_bfs(start_id: str, max_hops: int = 3) -> dict[int, list[str]]
```

### combined_recall()

HNSW + BFS 组合召回

```python
combined = db.combined_recall(query_vector: list[float], max_hops: int = 3, k: int = 10)
```

## 性能对比

| 方法 | 延迟 | QPS | 适用场景 |
|------|------|-----|---------|
| Brain.db SQL | 0.02ms | 60,000 | 精确 ID 查找 |
| Adjacency BFS | 0.00ms | 437,000 | 图遍历 |
| Vector Search | 16.8ms | 59 | 小数据集 |
| Combined Recall | 16.9ms | 59 | 大规模语义搜索 |