# L3 检索流程

## 入口
`src/l3/l3_cron.py` (每两天 03:00)

## 流程

```
init_brain_db()  # SQLite schema
    ↓
load_l2_chunks()  # 扫描所有日期 L2 文件
    ↓
L3Processor.write_chunks()
    ↓
Step1: session 分组
Step2: 分批写入 neurons (SQLITE_BATCH_SIZE=200)
Step3: schema 生成 (session≥5 chunks → TF-IDF 关键词)
Step4: 批量写入 synapses
Step5: commit
    ↓
sync_to_infinitydb()
    ├→ _pending_neurons → brain.graph + brain.vec + brain.hnsw
    └→ _pending_relations → adj 邻接表（双向存储）
    ↓
rebuild_hnsw()  # index.jsonl 备份
    ↓
update_recall_config()  # brains.config
    ↓
mark_l2_graph_written()  # 扫描所有日期
```

## 关键修复

| 修复 | 内容 |
|------|------|
| OllamaEncoder | 批量 input:texts（之前逐条） |
| 零向量 | 跳过，不写入 Brain.db / InfinityDB |
| schema threshold | ≥5 chunks（之前≥10） |
| schema priority | 4（之前 6，过度优先） |
| load_l2_chunks | 扫描所有日期（之前只当天） |
| mark | 扫描所有日期 written_ids（之前只当天） |
| encode_batch | id() 映射保持顺序（之前去重导致错位） |
| written_ids | 只含成功写入（零向量不误删） |

## 召回 API

```python
from recall.infinitydb_lite import InfinityDBLite

db = InfinityDBLite()

# 1. 向量搜索
results = db.vector_search(query_vector, k=10)

# 2. 图遍历
bfs = db.adjacency_bfs(chunk_id, max_hops=3)
# 返回: {1: [nid1, nid2], 2: [nid3], 3: []}

# 3. 组合召回（HNSW + BFS）
combined = db.combined_recall(query_vector, max_hops=2, k=10)
# 返回: [{"id": "...", "activation": 0.85}, ...]
```

## 数据路径

- Brain.db: `~/.local/share/neural-memory/brains.db`
- InfinityDB: `memory/layers/infinitydb/`
  - brain.graph.json（邻接表）
  - brain.vec.fvec（二进制向量）
  - brain.hnsw（HNSW 索引）