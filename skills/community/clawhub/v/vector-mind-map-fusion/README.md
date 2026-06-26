# Vector-Mind Map-Fusion

三层向量记忆融合系统：L1 提取 → L2 整理 → L3 检索

> v1.2.0：方案A（cost tracker + checkpoint + manifest + warm-cold） 实施 — InfinityDB 单一数据源 + 并行搜索（HNSW 语义 + 关键词字面）

---

## 核心架构

```
用户输入
    ↓
L1 (Session Scanner + Classifier)
    ├─ ByteOffsetScanner: 扫描 session JSONL，断点续扫
    ├─ Stage1 过滤: 噪音/UUID/cron/metadata
    ├─ Classifier: 去噪→质量检查→分类→分块→向量
    └─ 输出: L2A/ (每日增量)
    ↓
L2 (Daily Consolidator)
    ├─ 加载 L2A: 扫描所有日期文件
    ├─ session 分组 + 滑动窗口
    ├─ 四级去重: content_hash → cosine → simhash → hnsw
    ├─ session graph: N-gram 中文分词
    ├─ transitive closure: 关系补全
    └─ 输出: L2/ (每日增量)
    ↓
L3 (Biweekly Consolidator)
    ├─ 加载 L2: 写入 InfinityDB（单一数据源）
    ├─ SCHEMA 生成: session≥5 → TF-IDF 摘要
    ├─ InfinityDB 同步: brain.graph(元数据) + brain.vec(向量) + brain.hnsw
    └─ 增量删除 L2 (written_ids 追踪)

Recall（检索）
    ├─ Path1: HNSW 向量搜索（语义查全）
    ├─ Path2: 关键词搜索（字面查准）
    ├─ merge_seeds(): 两者都命中得双倍权重
    ├─ spreading_activation: 图扩散
    ├─ dynamic_priority: 按 priority 加权
    └─ tier/type 过滤 → top-k 返回
```

---

## 数据存储（方案A：单一 InfinityDB）

```
memory/layers/infinitydb/
    brain.graph.json   # 神经元元数据 + 邻接关系（唯一数据源）
    brain.vec.fvec     # 二进制向量存储
    brain.vec.idx      # 向量 ID 索引
    brain.hnsw         # HNSW 索引（pickle）

brain.graph.json 结构：
{
  "neurons": {
    "neuron_id": {
      "content": "记忆内容...",
      "memory_type": "task",
      "priority": 3,
      "tier": "warm",
      "timestamp": "2026-04-26T...",
      "neighbors": { "other_id": 0.5 }
    }
  },
  "config": {
    "recall": { "max_spread_hops": 3, ... }
  }
}
```

---

## 环境准备

### 1. 安装 Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh
# Windows: https://ollama.com/download
```

### 2. 拉取向量模型

```bash
ollama pull bge-m3
ollama list  # 验证
```

### 3. 启动服务

```bash
ollama serve
curl http://localhost:11434/api/tags  # 验证
```

### 4. 安装 Python 依赖

```bash
pip install --break-system-packages httpx
# 无其他外部依赖（纯 Python 标准库实现）
```

---

## 快速使用

```bash
# 运行全部
python main.py run --all

# 只运行某一层
python main.py run --layer l1
python main.py run --layer l2
python main.py run --layer l3

# 搜索记忆
python main.py search "查询内容"
python src/recall/recall.py "查询内容" --top-k 5

# 按类型/层级过滤
python src/recall/recall.py "安装" --tier warm --type task

# 查看状态
python main.py stats
```

---

## Recall API

```python
from src.recall.recall import fusion_recall

# 基础检索（向量 + 关键词并行搜索）
results = fusion_recall("昨天安装了什么", top_k=10)

# 带过滤
results = fusion_recall(
    query="项目配置",
    top_k=10,
    tier="warm",           # 按层级过滤
    memory_type="task",    # 按类型过滤
    min_score=0.3          # 最低激活分
)

# 返回格式
# [{
#   "id": "neuron_id",
#   "content": "记忆内容",
#   "memory_type": "task",
#   "priority": 3,
#   "tier": "warm",
#   "activation_score": 0.6854
# }, ...]
```

---

## 项目结构

```
vector-mind-map-fusion/
├── README.md              # 本文件
├── SKILL.md               # OpenClaw skill 元数据
├── requirements.txt       # Python 依赖
├── main.py                # 项目入口
├── src/
│   ├── l1/                # L1 提取层
│   │   ├── l1_cron.py
│   │   ├── scan_sessions_incremental.py
│   │   └── l1_classifier.py
│   ├── l2/                # L2 整理层
│   │   ├── l2_cron.py
│   │   └── l2_daily.py
│   ├── l3/                # L3 检索层
│   │   ├── l3_cron.py
│   │   └── l3_biweekly_consolidate.py
│   └── recall/            # 召回工具
│       ├── recall.py          # SpreadingActivationRecall（并行搜索）
│       └── infinitydb_lite.py # InfinityDB 单一数据源
└── memory/
    └── layers/
        ├── l1a/           # L1 原始提取
        ├── l2a/           # L2 去重前
        ├── l2/            # L2 整理后
        └── infinitydb/     # L3 永久记忆（单一数据源）
```

---

## 触发条件

| 用户意图 | 对应层 | 说明 |
|---------|-------|------|
| "记住 XXX"、"存入记忆" | L1 | 立即提取 |
| "之前有没有"、"我的记忆里" | Recall | 语义 + 关键词并行查询 |
| "整理一下"、"归类" | L2 | 结构化整理 |
| "搜索记忆"、"语义搜索" | Recall | 向量召回 |
| 每日定时 | L1+L2 (00:30 CST) | 增量扫描 |
| 每两天定时 | L3 (03:00 CST) | 归档整理 |

---

## 质量保证

| 保证 | 实现 |
|------|------|
| 防断裂 | 50字 overlap、atomic write、byte offset |
| 防丢失 | tmp 保护、written_ids 追踪、graph_written 标记 |
| 防质量下降 | denoise→quality→classify 顺序、零向量过滤 |
| 防关系错乱 | session graph + transitive closure |
| 防索引混乱 | 四级去重、content_hash_index 隔离 |
| 单一数据源 | InfinityDB 唯一写入，无双写同步问题 |

---

## 性能指标

| 操作 | 速度 |
|------|------|
| L1 Scanner | ~87,000 条/秒 |
| L1 Classifier | ~32,000 条/秒 |
| L2 处理 | ~14,500 条/秒 |
| L3 InfinityDB 写入 | ~100 条/秒 |
| Vector Search (HNSW) | O(log n) |
| Adjacency BFS | <1ms/hop |
| Combined Recall | ~59 QPS |

---

## 版本历史

| 版本 | 更新内容 |
|------|---------|
| 1.0.5 | 初始版本 |
| 1.0.7 | 回滚 L3 dedup，L3 为纯写代理 |
| **1.1.0** | **方案A：InfinityDB 单一数据源 + 并行搜索（HNSW+关键词）** |

---

## 详细文档

- [L1 提取流程](docs/l1_flow.md)
- [L2 整理流程](docs/l2_flow.md)
- [L3 检索流程](docs/l3_flow.md)
- [Recall API](docs/recall_api.md)
- [修复清单](docs/fixes.md)
