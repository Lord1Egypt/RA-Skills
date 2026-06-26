# Agent Memory 渐进式升级路线图

> v8.4 → v8.5 → v8.6 → v8.7 → v8.8 → v8.9 → v9.0 全版本完成
>
> 基线: v8.3（147 项测试全通过，LLM 全链路达验证）

---

## 总览

```
v8.3 ──→ v8.4 ──→ v8.5 ──→ v8.6 ──→ v8.7 ──→ v8.8 ──→ v8.9 ──→ v9.0
基线    基础设施   性能     架构      生态      生产就绪   记忆引擎   智能体平台
147 测   CI/CD     BM25     PG 迁移   pip 包    异步鉴权    生命周期   GraphRAG
试全过   覆盖率    混合检索  模块拆分   可视化    多租户MQ    gRPC/TS    多模态
         Python   Embedding 记忆蒸馏   插件系统   SSE 流式    LLM 优化   分布式存储
         3.10+    对标      冷热分层   OpenAPI   API v3     决策引擎    6D 瓶颈全突破
```

---

# Phase 1: v8.4 — 工程基础设施与稳定性

> 目标: 补齐工程地基，建立自动化质量防线
> 周期: 2 周
> 优先级: 🔴 P0

## 1.1 架构升级方向

当前 v8.3 的短板不在功能，而在**工程可靠性**：
- 无 CI/CD，每次改动靠人工验证
- 无类型检查，Python 3.7 兼容性问题仅在运行时暴露
- 无覆盖率报告，不知道哪些代码路径从未被测试
- API key 硬编码在测试文件中

v8.4 不引入新功能，**专注工程基础设施零缺陷**。

## 1.2 关键技术点

### 1.2.1 Python 3.10+ 升级

| 项 | 当前 | 目标 |
|----|------|------|
| Python 版本 | 3.7.7 | 3.10+ |
| 类型注解 | `from __future__` 补丁 | 原生 `list[dict]` |
| `match/case` | 不可用 | 可替代深层 if/elif 链 |
| 性能 | 基线 | `str`/`bytes`/`dict` 均有加速 |

实施步骤:
1. 移除所有 `from __future__ import annotations`（36 个文件）
2. 更新 `pyproject.toml` 的 `requires-python = ">=3.10"`
3. 验证 `match/case` 可用于 `emotion.py` 的 nuance 判定逻辑
4. 更新 CI 的 Python matrix 为 `["3.10", "3.11", "3.12"]`

### 1.2.2 CI/CD 流水线

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: mypy agent_memory/
      - run: pytest tests/ -v --cov=agent_memory --cov-report=term
      - run: python real_world_test.py
```

验收标准:
- 每次 push 自动触发
- `ruff` 零错误
- `mypy` 零错误（至少 core 模块：store/encoder/emotion/pipeline/recall）
- 单元测试覆盖率 ≥ 80%
- `real_world_test.py` 40/40 通过

### 1.2.3 测试覆盖扩展

当前盲区必须补上（见 [ANALYSIS.md](file:///d:/Github/agent_memory_v8.3/agent_memory/ANALYSIS.md) §2.4）:

| 新测试文件 | 覆盖模块 | 目标用例数 | 前置条件 |
|-----------|---------|-----------|---------|
| `tests/test_recall.py` | `recall.py` | ≥ 25 | sqlite-vec |
| `tests/test_reranker.py` | `reranker.py` | ≥ 15 | sentence-transformers |
| `tests/test_semantic_topic.py` | `semantic_topic.py` | ≥ 12 | sentence-transformers |
| `tests/test_embedding_store.py` | `embedding_store.py` | ≥ 20 | sqlite-vec |
| `tests/test_server.py` | `server.py` HTTP API | ≥ 10 | FastAPI TestClient |

### 1.2.4 代码质量工具链

```
[tool.ruff]
line-length = 120
target-version = "py310"

[tool.mypy]
python_version = "3.10"
strict = false
warn_return_any = true
warn_unused_configs = true
```

### 1.2.5 环境依赖补齐

```
pip install sqlite-vec>=0.1.9
pip install sentence-transformers>=2.2.0
pip install FlagEmbedding>=1.2.0
```

同时确保 FTS5 trigram tokenizer 可用（编译或发行版 SQLite）。

### 1.2.6 API Key 安全

- 将 `llm_test.py` / `real_world_test.py` / `test_llm_conn.py` 中的硬编码 key 移至 `.env`
- 已通过 `.gitignore` 排除这些文件

## 1.3 资源需求

| 资源 | 说明 |
|------|------|
| 人力 | 1 人 × 2 周 |
| CI 运行环境 | GitHub Actions（免费额度足够） |
| Python 环境 | 3.10/3.11/3.12 多版本 |
| 外部依赖 | sqlite-vec wheels for Windows/Linux/macOS |

## 1.4 验收标准

| 检查项 | 通过条件 |
|--------|---------|
| Python 版本 | 3.10+，`from __future__` 已全部移除 |
| CI 绿钩 | push/PR 均自动触发，全 green |
| 覆盖率 | `pytest --cov` ≥ 80%（新增 5 个测试模块 ~82 用例） |
| ruff | 零 warning |
| mypy | core 模块零 error |
| sqlite-vec | `python -c "import sqlite_vec; print('OK')"` 成功 |
| LLM 全链路 | `python llm_test.py` 20/20 通过 |

---

# Phase 2: v8.5 — 检索性能与语义增强

> 目标: 检索质量达到生产级，性能与竞品对标
> 周期: 3 周
> 优先级: 🔴 P0（检索是记忆系统的核心价值）

## 2.1 架构升级方向

```
v8.4 检索管道:
  FTS5 LIKE ──┐
              ├── RRF 融合 ──→ reranker ──→ MMR 重排 ──→ 最终结果
  向量检索 ───┘

v8.5 检索管道:
  BM25 稀疏 ──┐
  向量检索 ───┼── 加权融合 ──→ multi-reranker ──→ diversity ──→ 最终结果
  关键词匹配 ─┘                                   ^            ^
                                                 CrossEnc    MMR+DPP
```

**核心变化**: 从双路 → 三路检索，引入稀疏-稠密混合，BM25 弥补中文语义检索弱点。

## 2.2 关键技术点

### 2.2.1 BM25 混合检索

实施步骤:
1. 新增 `bm25_index.py`，基于 `rank_bm25` 库
2. 为每条记忆构建 BM25 索引（字段：content + topics + tools）
3. 查询时并行执行 BM25 + 向量检索
4. 三路融合公式变为: `score = α·BM25 + β·Vector + γ·Keyword`，默认 α=0.4, β=0.4, γ=0.2
5. 支持动态权重：短查询提高 BM25 权重，长查询提高 Vector 权重

### 2.2.2 多 Embedding 模型热插拔

```python
# 新增 embedding_registry.py
EMBEDDING_MODELS = {
    "bge-large-zh": {"dim": 1024, "provider": "BAAI/bge-large-zh-v1.5"},
    "bge-m3":       {"dim": 1024, "provider": "BAAI/bge-m3"},
    "m3e-base":     {"dim": 768,  "provider": "moka-ai/m3e-base"},
    "gte-large-zh": {"dim": 1024, "provider": "thenlper/gte-large-zh"},
    "text2vec":     {"dim": 768,  "provider": "shibing624/text2vec-base-chinese"},
}
```

实施步骤:
1. 新增 `EmbeddingRegistry` 类，支持模型注册和切换
2. `embedding_store.py` 重构为 `EmbeddingStore(..., model="bge-large-zh")`
3. 记录每条记忆的 `embedding_model` 字段，用于模型迁移时重新编码
4. 添加模型切换 CLI: `python -m agent_memory.migrate --new-model bge-m3`

### 2.2.3 检索质量 Benchmark 套件

新增 `benchmarks/` 目录:

| Benchmark | 指标 | 对标 |
|-----------|------|------|
| `retrieval_accuracy.py` | Precision@k, Recall@k, MRR, NDCG@10 | BEIR 简化版 |
| `latency_bench.py` | p50/p95/p99 检索延迟 | 10K/100K/1M 数据集 |
| `embedding_quality.py` | 余弦相似度 vs 人工标注 | 100 对 (query, 正例, 负例) |
| `chinese_bench.py` | 中文检索专项 | CLTC/ViT 格式 |

验收标准:
- Precision@10 ≥ 0.85（v8.4 基线 ~0.70 LIKE 模式）
- p95 检索延迟 ≤ 200ms（10K 数据集）
- 中文检索 MRR ≥ 0.75
- 各 benchmark 结果写入 `benchmarks/results/v8.5.json`

### 2.2.4 中文 NLP 增强

实施步骤:
1. 引入 `jieba` 分词，替代仅靠 trigram tokenizer
2. 新增 `chinese_tokenizer.py`，支持:
   - 分词 + 停用词过滤
   - 同义词扩展（"开心" → "高兴/愉快/喜悦"）
   - 领域词典（技术词汇：微服务、向量化、RAG 等）
3. 情感词典 [emotion.py](file:///d:/Github/agent_memory_v8.3/agent_memory/emotion.py) 扩充至 500+ 中英双语条目

## 2.3 资源需求

| 资源 | 说明 |
|------|------|
| 人力 | 1 人 × 3 周 |
| 计算资源 | 下载 3-5 个 Embedding 模型 (~5-15GB) |
| Benchmark 数据集 | 构造 500 条记忆 + 100 组 query/正例/负例 |
| 外部库 | rank-bm25, jieba, FlagEmbedding, scipy |

## 2.4 验收标准

| 检查项 | 通过条件 |
|--------|---------|
| BM25 三路融合 | Precision@10 提升 ≥ 15%（vs v8.4 基线） |
| 模型热插拔 | 2 个模型切换后检索结果一致性 ≥ 90% |
| Benchmark CI | 每次 PR 自动运行 benchmark，不退化 |
| 检索延迟 | p95 ≤ 200ms（10K 数据集） |
| 中文分词 | 中文查询精确匹配率 ≥ +20%（vs 仅 trigram） |

---

# Phase 3: v8.6 — 架构重构与可扩展性

> 目标: 消除技术债，支持百万级记忆规模
> 周期: 4 周
> 优先级: 🟡 P1

## 3.1 架构升级方向

v8.5 的架构承载上限约 50 万条记忆。v8.6 的目标是 **百万条级别**，需要：
- 存储层可替换（SQLite → PostgreSQL）
- 核心模块拆分（降低单文件复杂度）
- 多 Agent 协作记忆共享
- 自动记忆蒸馏（减少膨胀）

## 3.2 关键技术点

### 3.2.1 存储后端抽象层

新增 `storage/` 包:

```
storage/
├── __init__.py
├── base.py           # AbstractMemoryStore (接口)
├── sqlite_store.py   # SQLite 实现（当前 store.py 重构）
├── pg_store.py       # PostgreSQL 实现
└── connection.py     # 连接池抽象
```

实施步骤:
1. 从 `store.py` 提取 `AbstractMemoryStore` 接口（~20 个抽象方法）
2. 实现 `SqliteMemoryStore`（当前代码迁移）
3. 实现 `PostgresMemoryStore`（基于 `asyncpg` + `pgvector`）
4. 新增 `ConnectionPool` 抽象，支持 SQLite WAL / PG 连接池
5. 通过环境变量 `MEMORY_STORE_BACKEND=postgres` 切换
6. 所有现有测试在两种后端上运行

### 3.2.2 核心模块拆分

| 当前 | 拆分后 | 行数变化 |
|------|--------|---------|
| `memory_system.py` (~1600 行) | `memory_system.py` (~200 行) | -87% |
| | `memory_builder.py` (AgentMemory 构造函数) | ~150 行 |
| | `memory_components.py` (组件注册表) | ~100 行 |
| `metacognition.py` (~750 行) | `meta_evaluation.py` (评估数据类 + 评分) | ~200 行 |
| | `reflection_engine.py` (反思 + 查询修正) | ~300 行 |
| | `metacognition.py` (MetacognitiveEngine 入口) | ~150 行 |

实施步骤:
1. `memory_system.py`: 引入 Builder 模式
   ```python
   am = (AgentMemory.builder()
         .with_db("memory.db")
         .with_llm(llm_fn)
         .with_semantic(True)
         .build())
   ```
2. 构造函数从 ~120 行缩减至 ~20 行
3. `metacognition.py`: 提取 `MetaEvaluation` 和 `ReflectionEngine` 为独立模块
4. 所有导入保持向后兼容（`from memory_system import AgentMemory` 不变）

### 3.2.3 记忆冷热分层 + 自动蒸馏

新增 `distill.py` 增强:

| 功能 | 触发条件 | 效果 |
|------|---------|------|
| 短期 → 长期压缩 | 同类记忆 ≥ 5 条 | LLM 摘要为 1 条 |
| 热点缓存 | 近 7 天被检索 ≥ 3 次 | 常驻内存 LRU cache |
| 冷数据迁移 | 30 天未被检索 | SQLite → 归档数据库 |
| 自动过期 | custom_ttl 到期 | 软删除 + 可选永久删除 |

### 3.2.4 多 Agent 协作记忆

新增 `agent_team.py`:

```python
team = AgentTeam("engineering-team")
team.add_agent("alice", role="backend")
team.add_agent("bob", role="frontend")
team.share_memory("数据库已从 MySQL 迁移到 PostgreSQL")
# → 自动广播到 team 成员的可读范围
```

实施步骤:
1. 基于现有 `agent_id` + `visibility` 字段扩展
2. 新增 `team_id` 级别共享记忆池
3. 新增 RBAC 权限: `read` / `write` / `share` 三级

## 3.3 资源需求

| 资源 | 说明 |
|------|------|
| 人力 | 1-2 人 × 4 周 |
| PostgreSQL 环境 | Docker 或云服务（用于 pg_store 开发和测试） |
| Embedding 模型 | 同上 v8.5 |
| 记忆蒸馏 LLM | 需要稳定的 LLM API（蒸馏会频繁调用） |

## 3.4 验收标准

| 检查项 | 通过条件 |
|--------|---------|
| 存储后端双实现 | 所有 106 个单元测试在 SQLite + PG 上均通过 |
| Builder 模式 | `AgentMemory.builder().build()` 可完全替代旧构造函数 |
| 模块拆分 | memory_system.py ≤ 250 行，metacognition.py ≤ 200 行 |
| 冷热分层 | 100K 条记忆下，热点检索延迟 p95 ≤ 100ms（vs 基线 200ms） |
| 记忆蒸馏 | 10 条同类记忆 → 1 条摘要，LLM prompt 长度减少 ≥ 60% |
| 后向兼容 | 所有现有测试无需修改即可通过 |

---

# Phase 4: v8.7 — 生态打磨与发布就绪

> 目标: 从内部项目变为可公开发布的 v1.0.0
> 周期: 3 周
> 优先级: 🔵 P2

## 4.1 架构升级方向

```
v8.6 架构:
  agent_memory/ (内部 Python 包)
  └── cli.py (基础 CLI)

v8.7 架构:
  agent_memory/            ← pip install agent-memory
  ├── server.py            ← FastAPI 生产级 HTTP API
  ├── dashboard/           ← Web UI 可视化面板
  ├── plugins/             ← 插件系统
  └── docs/                ← 完整文档站 (MkDocs)
```

## 4.2 关键技术点

### 4.2.1 pip 打包发布

```
agent-memory/
├── pyproject.toml         # 增强: classifiers, urls, scripts
├── LICENSE                # MIT
├── README.md              # 英文 + 中文双语
└── agent_memory/
    ├── __init__.py        # 顶层 API 导出
    └── ...
```

```toml
[project]
name = "agent-memory"
version = "8.7.0"
description = "Human-like memory system for AI Agents"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]

[project.scripts]
agent-memory = "agent_memory.cli:main"
agent-memory-server = "agent_memory.server:main"

[project.optional-dependencies]
web = ["fastapi", "uvicorn"]
pg = ["asyncpg", "pgvector"]
all = ["agent-memory[web,pg]"]
```

验收: `pip install agent-memory` 一键安装，`agent-memory --help` 输出帮助。

### 4.2.2 HTTP API 重构

基于 [server.py](file:///d:/Github/agent_memory_v8.3/agent_memory/server.py) 重写:

```
POST /v1/memories           # 写入记忆
GET  /v1/memories/{id}      # 获取记忆
POST /v1/recall             # 检索记忆
GET  /v1/agents/{id}/profile # 获取 Agent 人格画像
GET  /v1/health             # 健康检查
GET  /v1/metrics            # Prometheus metrics
GET  /docs                  # Swagger UI
```

新增:
- 请求验证（Pydantic v2）
- 速率限制（每 agent 100 req/min）
- 分页（offset/limit）
- 结构化错误响应（RFC 7807）

### 4.2.3 可视化仪表盘

新增 `dashboard/` (纯静态 HTML + JS，不引入前端框架):

| 页面 | 功能 |
|------|------|
| `memory-graph.html` | 记忆网络图（D3.js 力导向图，节点=记忆，连线=语义相似度） |
| `timeline.html` | 时间线视图（按天/周/月聚合，颜色=情感 valence） |
| `emotion-dashboard.html` | 情感仪表盘（8 维雷达图 + valence/arousal 散点图） |
| `agent-profile.html` | Agent 人格画像卡片 |

数据通过 API 获取，仪表盘纯静态部署。

### 4.2.4 插件系统

新增 `plugins/`:

```python
# plugins/base.py
class MemoryPlugin(ABC):
    name: str
    version: str

    @abstractmethod
    def on_ingest(self, memory: dict) -> dict: ...
    @abstractmethod
    def on_recall(self, query: str, results: list) -> list: ...
```

内置插件:
- `AutoTagger`: 自动给记忆打标签
- `SentimentMonitor`: 情感异常告警（连续 5 条负面 → 通知）
- `SlackNotifier`: 重要记忆推送到 Slack
- `ObsidianSync`: 同步到 Obsidian vault（已有 `obsidian_sync.py`，改为插件）

### 4.2.5 文档站点

新增 `docs/` (MkDocs + Material theme):

```
docs/
├── index.md            # 概览
├── quickstart.md       # 5 分钟上手
├── architecture.md     # 架构图 + 数据流
├── api/                # OpenAPI 自动生成
├── guides/             # 使用指南
└── contributing.md     # 贡献指南
```

## 4.3 资源需求

| 资源 | 说明 |
|------|------|
| 人力 | 1 人 × 3 周 |
| MkDocs | `pip install mkdocs-material` |
| API 文档 | FastAPI 自带 Swagger，零额外成本 |
| 仪表盘 | D3.js CDN，零额外依赖 |
| PyPI | https://pypi.org 账号 |

## 4.4 验收标准

| 检查项 | 通过条件 |
|--------|---------|
| pip 安装 | `pip install agent-memory` 成功，3 分钟内可跑通 quickstart |
| HTTP API | 所有端点有 Swagger 文档，`pytest tests/test_server.py` 通过 |
| 仪表盘 | 4 个 HTML 页面可打开，数据从 API 实时加载 |
| 插件系统 | 3 个内置插件可用，第三方插件可通过 `pip install agent-memory-plugin-xxx` 注册 |
| 文档站 | `mkdocs serve` 可本地浏览，架构图不是占位符 |
| 后向兼容 | v8.3 → v8.8 数据迁移脚本通过 |

---

# Phase 5: v8.9 — ✅ 已完成 — 记忆生命周期 + 跨语言 SDK + 记忆驱动决策

> 目标: 从"高性能记忆存储"进化为"会演化的记忆引擎"，并面向多语言生态开放
> 周期: 4 周
> 优先级: 🔴 P0（当前开发焦点）
> 依赖: v8.8 异步架构 + 多租户体系

## 5.1 v8.9 定位

v8.8 解决的问题: **Agent 如何在高并发下安全地读写记忆？**（异步 + 鉴权 + 多租户 + Worker）

v8.9 要解决的问题: **记忆如何持续演化？如何让更多语言的开发者使用？如何让记忆直接参与决策？**

```
v8.8:  记忆 = 高并发安全的分布式存储
v8.9:  记忆 = 有生命周期的实体 + 跨语言可调用 + 驱动 Agent 行为
```

## 5.2 记忆生命周期引擎 (`memory_lifecycle.py`)

### 5.2.1 核心设计

v8.6 的 `memory_tier.py` 实现了冷热分层（物理层生命周期），v8.9 新增**语义层生命周期**——记忆写入后不是静态的，而是持续演化：

```python
# agent_memory/memory_lifecycle.py — v8.9 新增
class MemoryLifecycle:
    def on_create(self, memory: dict):
        """写入时触发：初始化生命周期状态"""
        memory["lifecycle_state"] = "active"
        memory["version"] = 1
        return memory

    def on_contradict(self, old: dict, new: dict) -> dict:
        """新记忆与旧记忆矛盾时触发
        例: 旧记忆"用户偏好 MySQL"，新记忆"用户已迁移到 PostgreSQL"
        → 旧记忆标记为 superseded，新记忆标记为 current
        """
        old["lifecycle_state"] = "superseded"
        old["superseded_by"] = new["memory_id"]
        new["lifecycle_state"] = "current"
        new["supersedes"] = old["memory_id"]
        return new

    def on_reinforce(self, memory: dict, times: int):
        """被频繁检索 → 强化重要性
        例: 同一记忆被查询 ≥ 10 次 → importance 从 medium 升为 high
        """
        if times >= 10 and memory.get("importance") == "medium":
            memory["importance"] = "high"
            memory["reinforced_at"] = int(time.time())
        return memory

    def on_decay(self, memory: dict, days_since_access: int):
        """长期未访问 → 衰减
        例: 记忆 90 天未被召回 → confidence 衰减 50%
        """
        if days_since_access > 90:
            memory["confidence"] = max(0.0, memory.get("confidence", 1.0) * 0.5)
            memory["lifecycle_state"] = "decaying"
        return memory

    def on_merge(self, memories: list[dict]) -> dict:
        """N 条高度相似的记忆 → LLM 融合为 1 条
        触发条件: N ≥ 5 且内容相似度 > 0.85
        """
        merged_content = self._llm_summarize(memories)
        merged = {
            "memory_id": self._gen_merged_id(memories),
            "content": merged_content,
            "merged_from": [m["memory_id"] for m in memories],
            "lifecycle_state": "merged",
            "version": max(m.get("version", 1) for m in memories) + 1,
        }
        return merged

    def on_evolve(self, memory: dict, new_evidence: dict):
        """基于新证据更新记忆内容
        不覆盖原始记忆，创建新版本文档
        """
        evolved = dict(memory)
        evolved["memory_id"] = f"{memory['memory_id']}_v{memory.get('version',1)+1}"
        evolved["content"] = self._llm_update(memory["content"], new_evidence)
        evolved["version"] = memory.get("version", 1) + 1
        memory["lifecycle_state"] = "superseded"
        memory["evolved_to"] = evolved["memory_id"]
        return evolved

    def get_lifecycle_history(self, memory_id: str) -> list[dict]:
        """查询一条记忆的完整演化链
        返回: [v1(原始), v2(反驳修改), v3(融合), v4(当前)]
        """
```

### 5.2.2 生命周期状态机

```
                    ┌──────────┐
              ┌────→│  active  │─────┐
              │     └────┬─────┘     │
        reinforcement  │        decay│
              │     ┌───▼───┐     ┌──▼────┐
              └─────│reinforced│   │decaying│──→(长期衰减)→ deleted
                    └─────────┘   └───────┘
              ┌──────────┐
              │superseded│← 被新证据版本取代
              └──────────┘
              ┌──────────┐
              │  merged  │← N条融合 → 新记忆替代原N条
              └──────────┘
```

### 5.2.3 演进线追踪 API

```python
# 查询因果演进链（结合坐标编码 + lifecycle 版本链）
lifecycle.trace("memory_id") → [
    {"version": 1, "state": "active",     "event": "created",      "ts": 1700},
    {"version": 1, "state": "reinforced",  "event": "频繁检索强化",  "ts": 1701},
    {"version": 2, "state": "current",     "event": "新证据更新",    "ts": 1702},
    {"version": 2, "state": "active",      "event": "当前版本",      "ts": 1702},
]
```

实施步骤:
1. `memory_lifecycle.py`: 实现上述 7 个生命周期方法，构建在 `memory_tier.py` 之上
2. `lifecycle_events.py`: 生命周期事件触发器——定时扫描器检查 decay/merge 条件
3. `store.py` 扩展: 新增 `lifecycle_state`, `version`, `superseded_by`, `merged_from` 字段
4. `api_v3.py` 扩展: `GET /v1/memories/{id}/trace` → 返回完整演化链

## 5.3 gRPC + WebSocket API + TypeScript SDK

### 5.3.1 gRPC 服务定义

v8.8 的 `api_v3.py` 是纯 FastAPI HTTP。v8.9 新增 gRPC 协议（Protocol Buffers）：

```protobuf
// agent_memory/proto/memory_service.proto
service MemoryService {
  rpc WriteMemory(WriteRequest) returns (WriteResponse);
  rpc RecallMemory(RecallRequest) returns (RecallResponse);
  rpc StreamEvents(StreamRequest) returns (stream MemoryEvent);  // gRPC streaming
  rpc GetLifecycleTrace(TraceRequest) returns (TraceResponse);
}

message WriteRequest {
  string content = 1;
  string owner_agent_id = 2;
  string importance = 3;
  repeated string topics = 4;
  string visibility = 5;
  string tenant_id = 6;
}

message RecallResponse {
  repeated MemoryResult results = 1;
  float latency_ms = 2;
  int32 total_count = 3;
}
```

实施:
- `proto/memory_service.proto` — 完整 Protocol Buffers 定义
- `grpc_server.py` — gRPC 服务端，复用 `api_v3.py` 的业务逻辑
- `grpc_gateway.py` — gRPC ↔ HTTP 双向网关（同一端口或独立端口）

### 5.3.2 WebSocket 服务

```python
# agent_memory/ws_server.py — v8.9 新增
@app.websocket("/v1/ws/{tenant_id}")
async def memory_websocket(websocket, tenant_id):
    """WebSocket 双向通信:
    客户端发送 → {action: "recall", query: "...", top_k: 10}
    服务端返回 → {action: "recall_result", results: [...], latency_ms: 12.3}
    
    同时也推送实时事件:
    → {event: "memory.created", data: {...}}
    → {event: "alert.sentiment", data: {...}}
    """
```

WebSocket 事件类型:
- `memory.created/updated/deleted` — 记忆 CRUD 通知
- `recall.completed` — 检索完成 + 结果
- `lifecycle.state_change` — 生命周期状态变更
- `alert.sentiment` — 情感告警
- `team.shared` — 团队共享通知

### 5.3.3 TypeScript/JavaScript SDK

```typescript
// agent_memory/sdk/typescript/agent-memory-client.ts — v8.9 新增
class AgentMemoryClient {
  constructor(options: {
    host: string;       // "localhost:8988" or gRPC endpoint
    tenantId: string;
    apiKey: string;
    protocol?: "http" | "grpc" | "ws";  // default: "http"
  })

  // 同步记忆操作
  async remember(content: string, options?: RememberOptions): Promise<MemoryResult>
  async recall(query: string, topK?: number): Promise<MemoryResult[]>
  async get(id: string): Promise<MemoryResult | null>

  // WebSocket 实时模式
  connect(): Promise<void>
  on(event: "memory.created" | "memory.updated" | "alert.sentiment", 
     callback: (data: MemoryEvent) => void): void
  disconnect(): void

  // 生命周期追踪
  async trace(id: string): Promise<LifecycleNode[]>
}

// 使用示例
const client = new AgentMemoryClient({
  host: "localhost:8988",
  tenantId: "my-app",
  apiKey: "sk-xxx",
  protocol: "ws",
});

await client.connect();
client.on("memory.created", (event) => {
  console.log(`新记忆: ${event.data.content}`);
});

const result = await client.recall("用户偏好", 5);
```

SDK 交付物:
- `sdk/typescript/agent-memory-client.ts` — TypeScript SDK（~300 行）
- `sdk/typescript/package.json` — npm 包配置
- `sdk/typescript/README.md` — 5 分钟上手文档
- npm 发布: `@agent-memory/client`（TypeScript 优先，含 `.d.ts` 类型声明）

## 5.4 记忆驱动决策 (`memory_decision.py`)

### 5.4.1 设计

v8.x 的记忆是**被动的**——Agent 问 → 检索 → 返回，Agent 自己决策。
v8.9 的记忆开始**主动参与决策**——记忆系统分析历史行为模式，提供结构化建议：

```python
# agent_memory/memory_decision.py — v8.9 新增
class MemoryDecisionEngine:
    def analyze_pattern(self, agent_id: str, topic: str, 
                        context: dict = None) -> DecisionAdvice:
        """基于历史记忆分析行为模式，返回决策建议
        
        输入:  agent_id="agent-42", topic="数据库选型"
        
        内部流程:
          1. 坐标交叉检索: topic + person + tool 维度交叉
          2. 情感趋势分析: 过往类似决策的情感 valence
          3. 生命周期追溯: 相关记忆是否被 superseded/merged
          4. 生成建议: 推荐 + 置信度 + 依据 + 风险
        
        返回:
          DecisionAdvice {
            recommendation: "PostgreSQL",
            confidence: 0.87,
            evidence: [
              "3次成功迁移经验 (person=alice, topic=database, valence>0.7)",
              "团队偏好：过去6个月新项目均选择PostgreSQL",
              "风险：首次使用 pgvector 扩展（1条记忆标记为 superseded）"
            ],
            alternatives: ["MySQL 8.0", "MongoDB 6.0"],
            risk_factors: ["pgvector 扩展运维经验不足（追溯到 2024-03-15 的记忆）"]
          }
        """
```

### 5.4.2 决策追溯

与纯 embedding "相似度 0.87" 不同，v8.9 的决策建议**每条都有坐标溯源**：

```
推荐 "PostgreSQL" 的主要原因:
  ├── topic=database + person=alice → 3次迁移成功 (time维度: 2024-Q3)
  ├── topic=practice + tool=postgresql → 团队积极评价 (emotion维度: valence>0.7)
  └── topic=risk + tool=pgvector → 运维经验不足 (lifecycle: 1条记忆已 superseded)
  
每一个判断都可以追溯到具体的坐标编码记忆 → 满足合规审计要求
```

实施步骤:
1. `memory_decision.py`: DecisionAdvice 数据类 + MemoryDecisionEngine
2. 坐标交叉分析: 利用 N 维坐标自动发现 topic+person+tool 交叉模式
3. 情感加权: 历史上相似场景的情感 valence 加权置信度
4. `api_v3.py` 扩展: `POST /v1/decide` 端点

## 5.5 资源需求

| 资源 | 说明 |
|------|------|
| 人力 | 1-2 人 × 4 周 |
| gRPC | `pip install grpcio grpcio-tools` |
| Proto 编译器 | `protoc` (protobuf compiler) |
| WebSocket | FastAPI 原生支持 `WebSocket`，零额外依赖 |
| TypeScript SDK | 纯 TS 文件，npm publish |
| 生命周期触发器 | 基于 v8.8 的 `message_queue.py` Worker 调度 |

## 5.6 验收标准

| 模块 | 通过条件 |
|------|---------|
| 记忆生命周期 | 7 个生命周期方法单元测试全部通过；`trace()` 返回 ≥ 1 条演化链 |
| gRPC 服务 | protobuf 编译成功；Python + TypeScript 客户端调用 `WriteMemory` + `RecallMemory` |
| WebSocket | 客户端 connect → 收到 `memory.created` 事件；断开重连机制 |
| TypeScript SDK | `npm run build` 成功；示例代码 30 秒内可跑通 |
| 记忆驱动决策 | `analyze_pattern()` 返回 DecisionAdvice 含 evidence + risk_factors；API 端点返回 200 |

---

# Phase 6: v9.0 — ✅ 已完成 — 突破性战略规划

> 目标: 从"记忆引擎"进化为"记忆智能体平台"
> 周期: 战略规划阶段（不设硬性 deadline）
> 优先级: 🟡 P2（v8.9 完成后启动专项研讨）
> 依赖: v8.9 记忆生命周期 + 记忆驱动决策

## 6.1 v9.0 定位

v8.x 系列解决的问题: **Agent 如何记住？如何安全高效地存取？如何让记忆持续演化？**

v9.0 要解决的问题: **Agent 如何理解自己的记忆？如何让记忆跨越模态和语言的边界？如何将记忆变成可推理的知识？**

```
v8.9:  记忆 = 有生命周期的实体 + 跨语言 SDK + 记忆驱动决策
v9.0:  记忆 = 可推理的知识图谱 + 多模态理解 + 云原生行为引擎
```

## 6.2 架构瓶颈分析（v9.0 全部解决 ✅）

v8.9 已解决记忆生命周期 + 跨语言API + 决策基础，v9.0 解决剩余三大瓶颈：

| 瓶颈 | 根因 | v9.0 突破方向 |
|------|------|-------------------|
| **线性检索天花板** | RRF/BM25/向量都是"查询 → 匹配"模式，无法跨记忆推理 | ✅ v9.0 GraphRAG: 记忆 → 实体/关系图 → 多跳推理 |
| **文本单一模态** | 仅处理文本，但真实 Agent 交互包含图片、音频、视频 | ✅ v9.0 多模态记忆: 图片/音频/视频一等记忆公民 |
| **单机扩展上限** | SQLite/单 PostgreSQL 实例，无法水平扩展 | ✅ v9.0 分布式向量存储: 一致性哈希 + 仲裁副本 |
| **静态记忆更新** | 记忆一旦写入，只有删除/覆盖，缺少持续演化能力 | ✅ **v8.9 记忆生命周期**: 更新/反驳/增强/融合/衰减 |
| **孤立记忆系统** | 记忆与 Agent 决策/规划/工具调用完全解耦 | ✅ **v8.9 记忆驱动决策**: Agent 行为记忆化 + 决策追溯 |
| **开发者友好度** | 纯 Python API，非 Python Agent 使用困难 | ✅ **v8.9 gRPC/WebSocket API + TypeScript SDK** |

> **v9.0 总结**: 全部 6 项架构瓶颈已在 v8.9 + v9.0 版本中全部解决。系统已实现从"高性能记忆存储"到"记忆智能体平台"的完整跃迁。

## 6.3 颠覆性技术引入

### 6.3.1 记忆知识图谱 (GraphRAG)

```
v8.x:  "用户喜欢用 Python" ──存储──→ SQLite 行
                                  ↓
                              检索时返回该行

v9.0:  "用户喜欢用 Python" ──实体抽取──→ [用户: 偏好] ──关系──→ [Python: 编程语言]
                                          ↓
                                     多跳推理: 用户偏好 → Python → 可能偏好 FastAPI, Pydantic...
                                          ↓
                                     推荐: 建议用户试试 Ruff 替代 Flake8
```

实施路径:
1. 引入 `neo4j` 或 `networkx` 作为图存储层
2. 每写入一条记忆，LLM 自动抽取实体和关系 → 增量更新图
3. 检索时支持 Cypher 图查询 + 自然语言 → 图查询的 NL2Cypher
4. 图上的 PageRank 用于记忆重要性排序

### 5.3.2 多模态记忆

```python
# v9.0 API
memory.remember(
    content="用户分享了一张架构图",
    image=b"...",          # 图片 bytes
    audio=b"...",         # 音频 bytes
    modalities=["text", "image"],
)
# → 图片通过 CLIP/ViT 编码为向量
# → 音频通过 Whisper 转写为文本
# → 多模态向量融合后存入统一向量空间
```

关键组件:
- `multimodal_encoder.py`: 整合 CLIP(图)、Whisper(音)、VideoMAE(视频)
- `cross_modal_retrieval.py`: "找一张关于数据库架构的图" → 文本查图片
- `media_summarizer.py`: LLM 驱动的图片/音频自动描述

### 6.3.3 云原生架构

```
                    ┌─────────────┐
                    │  API Gateway │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │ Memory API  │ │ Recall API  │ │ Admin API   │
    │ (Stateless) │ │ (Stateless) │ │ (Stateless) │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
    ┌──────▼───────────────▼───────────────▼──────┐
    │              Message Queue (NATS/Kafka)      │
    └──────────────────────┬──────────────────────┘
           ┌───────────────┼───────────────┐
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │   Embedder  │ │  Indexer    │ │  Archiver   │
    │   Worker    │ │  Worker     │ │  Worker     │
    └─────────────┘ └─────────────┘ └─────────────┘
           │               │               │
    ┌──────▼───────────────▼───────────────▼──────┐
    │           Storage Layer (S3 + PGVector)      │
    └─────────────────────────────────────────────┘
```

- 无状态 API 层：水平自动扩展
- 异步 Worker 层：写入/索引/归档解耦
- 对象存储：大文件（图片/音频）+ 冷记忆归档
- 向量数据库：Milvus/Qdrant 替代 sqlite-vec

### 6.3.4 记忆生命周期增强（v8.9 已实现基础版）

v8.9 的 `memory_lifecycle.py` 已实现 7 种生命周期事件（create/contradict/reinforce/decay/merge/evolve/trace）。
v9.0 在此基础上增强：

```python
# v8.9 已有: on_create, on_contradict, on_reinforce, on_decay, on_merge, on_evolve, trace
# v9.0 新增: 生命周期与知识图谱联动
class GraphLifecycle(MemoryLifecycle):
    def on_contradict(self, old, new):
        super().on_contradict(old, new)
        # v9.0 新增: 在知识图谱中标记矛盾边
        self.graph.add_edge(old["memory_id"], new["memory_id"], 
                           relation="CONTRADICTS", confidence=0.9)

    def on_merge(self, memories):
        merged = super().on_merge(memories)
        # v9.0 新增: 将被融合的记忆在图中聚合为单个节点
        self.graph.merge_nodes(
            [m["memory_id"] for m in memories],
            target_id=merged["memory_id"]
        )
        return merged
```

### 6.3.5 记忆驱动决策增强（v8.9 已实现基础版）

v8.9 的 `memory_decision.py` 已实现 `analyze_pattern()` 基础决策追溯。
v9.0 在此基础上增强：

```
v8.9:  Agent 调用 memory.decide("数据库选型")
           ↓
       基于坐标交叉 + 生命周期追溯 → 返回结构化建议

v9.0:  Agent 调用 memory.decide("数据库选型", context={...})
           ↓
       + 知识图谱多跳推理（"PostgreSQL → 需要 → pgvector → 团队 × 经验不足"）
       + 跨模态证据（"用户上次发的架构图里用了 Postgres"）
       + 实时情感加权（"团队最近对 PostgreSQL 的情绪正在上升"）
           ↓
       返回: {
         "recommendation": "PostgreSQL",
         "confidence": 0.92,  # 较 v8.9 提升（多跳推理贡献）
         "based_on": ["3次迁移经验", "团队偏好", "架构图证据", "情感上升趋势"],
         "graph_path": ["PostgreSQL → pgvector → 团队经验不足"],
         "cross_modal": ["图片证据: 2024-03 架构图中使用 PostgreSQL"],
         "emotional_trend": "团队 valence 从 0.3 → 0.7, 信心上升"
       }
```

## 6.4 生态系统建设

### 6.4.1 多语言 SDK（TypeScript 已在 v8.9 完成）

| SDK | 优先级 | 状态 | 核心能力 |
|-----|--------|------|---------|
| Python (内置) | P0 | ✅ v8.8 完成 | 全部功能 + gRPC |
| TypeScript/JavaScript | P1 | ✅ v8.9 完成 | `remember` + `recall` + `decide` + WebSocket |
| Go | P2 | v9.0 新增 | `remember` + `recall`（高性能场景） |
| Rust | P3 | v9.0 新增 | 嵌入式 SDK（边缘设备） |

### 6.4.2 社区与生态

| 里程碑 | 目标 |
|--------|------|
| GitHub Stars | 1,000+ |
| 外部贡献者 | ≥ 5 人 |
| 社区插件 | ≥ 10 个第三方插件 |
| 案例研究 | 3 篇博客/论文引用 |
| 集成生态 | LangChain/LlamaIndex/AutoGPT 官方集成 |

### 6.4.3 商业化路径（可选）

```
开源核心 (MIT)              →  社区版（永远免费）
Mem0 Cloud (SaaS)            →  托管记忆服务，按 API 调用计费
Enterprise                    →  私有部署 + SLA + 审计日志
Skill Marketplace             →  记忆分析技能市场（30% 分成）
```

## 6.5 v9.0 专项研讨会议议程

在 v8.9 发布后组织，建议议程：

```
Day 1: 当前状态回顾
  - v8.9 性能报告（gRPC vs REST 延迟对比 + TypeScript SDK 反馈）
  - 用户反馈汇总（GitHub Issues + npm 下载量）
  - 竞品分析更新（Mem0/Letta/LangChain 2026 最新动态）

Day 2: 技术决策
  - GraphRAG vs 纯向量检索：何时引入图存储？
  - 多模态优先级：先做图片 OCR 还是先做 CLIP 语义检索？
  - 云原生选型：Kubernetes vs Serverless vs Fly.io？
  - 是否引入 Rust 重写坐标编码核心层？
  - v8.9 生命周期引擎是否需要分布式事务支持？

Day 3: 路线决策
  - v9.0 MVP 范围定义（"must have" = GraphRAG + 多模态基础, "nice to have" = 云原生 + Go SDK）
  - v8.9 反馈中暴露的最大痛点（决定 v9.0 优先级排序）
  - 商业化 vs 纯开源路线
  - 团队扩展计划
  - v9.0 发布 target date
```

---

# 附录: 版本里程碑总表

| 版本 | 主题 | 周期 | 核心交付 | 测试目标 | 发布标准 |
|------|------|------|---------|---------|---------|
| **v8.3** | 基线修复 | ✅ 已完成 | 4 致命Bug + 147 测试 | 40 rule + 20 LLM + 87 unit | 全部通过 |
| **v8.4** | 基础设施 | ✅ 已完成 | CI/CD + pyproject.toml + 覆盖率 80% | 61 new tests | CI 绿钩 |
| **v8.5** | 检索增强 | ✅ 已完成 | BM25 + Chinese Tokenizer + Embedding Registry | Benchmark 套件 | P@10 ≥ 0.80 |
| **v8.6** | 架构重构 | ✅ 已完成 | 存储抽象层 + 冷热分层 + 多 Agent 协作 | 64 tests | 双后端全通过 |
| **v8.7** | 生态发布 | ✅ 已完成 | pip 包 + REST API v2 + 仪表盘 + 插件系统 | 47 tests | 全量通过 |
| **v8.8** | 生产就绪 | ✅ 已完成 | 异步架构 + JWT 鉴权 + 多租户 + 消息队列 + SSE | 145 tests | 全量通过 |
| **v8.9** | ✅ 已完成 | 4 周 | 记忆生命周期 + gRPC/WebSocket + TypeScript SDK + 记忆驱动决策 + LLM Token 优化 + 容量评估 | 41 tests | 7 生命周期 + 5 层 LLM 优化 + TS SDK |
| **v9.0** | ✅ 已完成 | 战略阶段 | GraphRAG 知识图谱 + 多模态记忆 + 分布式向量存储 | 72 tests | GraphRAG + 多模态 + 分布式三模块全通过 |
| **v10.0** | 未来规划 | 探索阶段 | 待定 — 基于 v9.0 反馈决定 | — | — |

---

*本文档基于 v8.3 代码审查 + 430 项测试（v8.3-v9.0）的实证分析推导生成。*
*v9.0 已完成，全部 6 项架构瓶颈解决。v10.0 为未来探索阶段。*