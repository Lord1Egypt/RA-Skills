# paper2spec Architecture — Pipeline & Modes
# paper2spec 架构文档 — 管线与模式

> Version 0.3.0 | [English](#english) | [中文](#中文)

---

<a id="english"></a>
## English

### Overview

paper2spec converts quantitative finance research papers (PDF) into structured,
machine-readable strategy specifications through a two-stage pipeline:

```
PDF ──→ [Stage 1: Parser] ──→ PaperContent ──→ [Stage 2: Extractor] ──→ ExtractionResult
                                                                              │
                                                                    N × StrategySpec
```

**Stage 1 (Parser)** has two interchangeable modes — **Mode A** and **Mode B**.
**Stage 2 (Extractor)** uses a fixed 5-layer architecture (Layer 0–4).
Both stages output the same data models regardless of mode chosen.

---

### Stage 1: Parser (PDF → PaperContent)

The parser extracts three core sections from a paper: **methodology**,
**data description**, and **signal logic**. Title and abstract are extracted
via regex heuristics (no LLM cost).

#### Mode A — Builtin / Direct LLM (Default)

```
PDF ─→ pymupdf4llm (text extraction)
         │
         ▼
    Full Text (Markdown)
         │
         ├─ len ≤ 100K chars ──→ use full text as context
         │
         └─ len > 100K chars ──→ truncate: first 90K + last 10K
                                  (preserves methodology at front,
                                   results/tables at back)
         │
         ▼
   ┌─────────────────────────────────────────┐
   │       3 Parallel LLM Calls              │
   │  asyncio.gather(                        │
   │    methodology_prompt(context),          │
   │    data_description_prompt(context),     │
   │    signal_logic_prompt(context)          │
   │  )                                      │
   └─────────────────────────────────────────┘
         │
         ▼
    PaperContent {
      title, abstract,
      methodology, data_description, signal_logic,
      full_text
    }
```

**Key characteristics:**
- **Speed**: ~20–60s per paper (3 LLM calls in parallel)
- **Dependencies**: Only core deps (litellm + PyMuPDF)
- **Context window**: Sends up to 100K chars per LLM call
- **Best for**: Papers ≤ 100 pages (covers ~95% of quant finance papers)
- **Truncation strategy**: Head + tail preserves methodology sections
  (typically early in the paper) and results/tables (typically late)

#### Mode B — Agent / FAISS Semantic Retrieval

```
PDF ─→ pymupdf4llm (text extraction)
         │
         ▼
    Full Text (Markdown)
         │
         ▼
   RecursiveCharacterTextSplitter
   (chunk_size=1500, overlap=200)
         │
         ▼
   ┌──────────────────────────┐
   │  FAISS Index             │
   │  bge-small-en-v1.5       │
   │  (384-dim, CPU, normalized) │
   └──────────────────────────┘
         │
         ▼
   Per-section semantic retrieval:
   ┌─────────────────────────────────────────┐
   │  For each of 3 sections:                │
   │    5 domain-specific queries ──→ top-k   │
   │    chunks retrieved & deduplicated       │
   │                                          │
   │  asyncio.gather(                         │
   │    methodology: 5 queries → chunks → LLM │
   │    data_desc:   5 queries → chunks → LLM │
   │    signal_logic: 6 queries → chunks → LLM│
   │  )                                       │
   └─────────────────────────────────────────┘
         │
         ▼
    PaperContent { same schema as Mode A }
```

**Key characteristics:**
- **Speed**: ~60–120s per paper (embedding + retrieval + 3 LLM calls)
- **Dependencies**: Requires `pip install paper2spec[agent]`
  (langchain-community, sentence-transformers, faiss-cpu — ~500MB)
- **Context window**: Sends only relevant chunks, not full text
- **Best for**: Very long papers (>100 pages) or when Mode A misses details
- **Query banks**: 5–6 domain-specific queries per section, e.g.:
  - Methodology: "signal generation entry exit rules", "portfolio formation
    rebalancing weighting scheme"...
  - Data: "CRSP Compustat database time period", "stock selection market
    capitalization"...
  - Signal: "buy signal long position entry", "technical indicators
    threshold parameter formula"...

#### Mode Selection Rule

| Condition | Mode | Reason |
|-----------|------|--------|
| ≤ 60 pages | A (builtin) | Fast, no truncation needed |
| 60–100 pages | A (builtin) | Truncation preserves key sections |
| >100 pages | B (agent) | Semantic retrieval avoids context limits |
| User reports missing content | B (agent) | Better recall for buried details |

**Automatic — do not ask the user to choose.**

---

### Stage 2: Extractor (PaperContent → ExtractionResult)

The extractor uses a 5-layer architecture. Each layer is a focused LLM call
that builds on the previous layer's output.

```
PaperContent
     │
     ▼
┌──────────────────────────────────────────┐
│  Layer 0: Strategy Detection             │
│  Input: title + abstract + methodology   │
│         + signal_logic                   │
│  Output: List[StrategyBrief]             │
│    - N strategies detected               │
│    - name, type, description per strategy│
│    - differentiation & section hints     │
└──────────────────────────────────────────┘
     │
     ├── N = 1: single-strategy path (no context injection)
     │
     └── N > 1: multi-strategy path (parallel extraction)
                Each strategy gets a "strategy_focus" block
                injected into Layer 1–4 prompts
     │
     ▼
┌──────────────────────────────────────────────────────┐
│  Per-Strategy Extraction (serial within, parallel    │
│  across strategies when N > 1)                       │
│                                                      │
│  Layer 1: Metadata + Data Requirements               │
│    → strategy_name, type, asset_class, data_source,  │
│      lookback_period, expected_performance            │
│                                                      │
│  Layer 2: Indicators                                 │
│    → List[Indicator] with formula, inputs, params    │
│                                                      │
│  Layer 3: Logic Pipeline                             │
│    → List[LogicStep]: filter → rank → threshold →    │
│      composite signal → trade signal                 │
│                                                      │
│  Layer 4: Execution Plan + Risk Management           │
│    → List[ExecutionPlan]: trigger, action, sizing    │
│    → risk_management rules                           │
└──────────────────────────────────────────────────────┘
     │
     ▼
ExtractionResult {
  paper_title: str,
  num_detected: int,
  strategies: List[StrategySpec]
}
```

**Multi-strategy parallelization** (N > 1):

```
Layer 0 detects N strategies
    │
    ├── Strategy 1: L1 → L2 → L3 → L4  ─┐
    ├── Strategy 2: L1 → L2 → L3 → L4  ─┤  asyncio.gather()
    └── Strategy N: L1 → L2 → L3 → L4  ─┘
    │
    ▼
ExtractionResult (N specs)
```

Within each strategy, Layers 1–4 run **serially** (each depends on the previous).
Across strategies, all N extraction pipelines run **in parallel**.

---

### End-to-End Data Flow

```
┌─────────┐   pymupdf4llm   ┌──────────┐   Mode A or B   ┌──────────────┐
│  PDF    │ ─────────────→  │ Raw Text │ ─────────────→  │ PaperContent │
│  File   │                 │ (MD fmt) │   3 ∥ LLM calls  │  .json/.md   │
└─────────┘                 └──────────┘                  └──────────────┘
                                                                │
                                                                ▼
                                                          ┌──────────┐
                                                          │ Layer 0  │
                                                          │ Detect N │
                                                          └──────────┘
                                                                │
                                                    ┌───────────┼───────────┐
                                                    ▼           ▼           ▼
                                               Strategy 1  Strategy 2   ...N
                                               L1→L2→L3→L4 L1→L2→L3→L4
                                                    │           │           │
                                                    └───────────┼───────────┘
                                                                ▼
                                                     ┌──────────────────┐
                                                     │ ExtractionResult │
                                                     │   .json / .md    │
                                                     └──────────────────┘
```

### Performance Benchmarks

| Stage | Single Strategy | Multi (3 strategies) |
|-------|----------------|---------------------|
| Parser Mode A | ~20–60s | Same (parser is strategy-agnostic) |
| Parser Mode B | ~60–120s | Same |
| Extractor | ~50–70s | ~60–90s (parallel) |
| **Total (Mode A)** | **~70–130s** | **~80–150s** |

Benchmarked with DeepSeek Chat. GPT-4o / Claude are typically 1.5–3× slower.

### LLM Call Count

| Configuration | LLM Calls |
|---------------|-----------|
| Mode A, 1 strategy | 3 (parser) + 1 (L0) + 4 (L1-L4) = **8** |
| Mode A, N strategies | 3 + 1 + N×4 = **4 + 4N** |
| Mode B, 1 strategy | 3 (parser) + 1 + 4 = **8** |
| Mode B, N strategies | 3 + 1 + N×4 = **4 + 4N** |

---

<a id="中文"></a>
## 中文

### 概述

paper2spec 将量化金融研究论文 (PDF) 通过两阶段管线转换为结构化、机器可读的策略规格：

```
PDF ──→ [阶段1: Parser] ──→ PaperContent ──→ [阶段2: Extractor] ──→ ExtractionResult
                                                                          │
                                                                 N × StrategySpec
```

**阶段1 (Parser)** 有两种可互换模式 — **Mode A** 和 **Mode B**。
**阶段2 (Extractor)** 使用固定的5层架构 (Layer 0–4)。
两个阶段无论选择哪种模式，输出相同的数据模型。

---

### 阶段1：Parser（PDF → PaperContent）

解析器从论文中提取三个核心部分：**方法论 (methodology)**、**数据描述 (data description)** 和 **信号逻辑 (signal logic)**。标题和摘要通过正则表达式启发式提取（无 LLM 开销）。

#### Mode A — 内置 / 直接 LLM（默认）

```
PDF ─→ pymupdf4llm (文本提取)
         │
         ▼
    全文 (Markdown 格式)
         │
         ├─ 长度 ≤ 100K 字符 ──→ 使用全文作为上下文
         │
         └─ 长度 > 100K 字符 ──→ 截断：前 90K + 后 10K
                                  (保留前部方法论 + 尾部结果/表格)
         │
         ▼
   ┌─────────────────────────────────────────┐
   │       3 个并行 LLM 调用                  │
   │  asyncio.gather(                        │
   │    methodology_prompt(上下文),            │
   │    data_description_prompt(上下文),       │
   │    signal_logic_prompt(上下文)            │
   │  )                                      │
   └─────────────────────────────────────────┘
         │
         ▼
    PaperContent {
      title, abstract,
      methodology, data_description, signal_logic,
      full_text
    }
```

**核心特征：**
- **速度**：每篇论文约 20–60 秒（3 个 LLM 调用并行）
- **依赖**：仅核心依赖 (litellm + PyMuPDF)
- **上下文窗口**：每次 LLM 调用最多发送 100K 字符
- **适用**：≤ 100 页的论文（覆盖约 95% 的量化金融论文）
- **截断策略**：头 + 尾保留方法论部分（通常在论文前段）和结果/表格（通常在论文后段）

#### Mode B — Agent / FAISS 语义检索

```
PDF ─→ pymupdf4llm (文本提取)
         │
         ▼
    全文 (Markdown 格式)
         │
         ▼
   RecursiveCharacterTextSplitter
   (chunk_size=1500, overlap=200)
         │
         ▼
   ┌────────────────────────────┐
   │  FAISS 索引                │
   │  bge-small-en-v1.5         │
   │  (384维, CPU, 归一化)       │
   └────────────────────────────┘
         │
         ▼
   按节语义检索：
   ┌─────────────────────────────────────────┐
   │  每个部分:                               │
   │    5 个领域查询 ──→ top-k 相关片段       │
   │    片段去重                               │
   │                                          │
   │  asyncio.gather(                         │
   │    methodology: 5 查询 → 片段 → LLM      │
   │    data_desc:   5 查询 → 片段 → LLM      │
   │    signal_logic: 6 查询 → 片段 → LLM     │
   │  )                                       │
   └─────────────────────────────────────────┘
         │
         ▼
    PaperContent { 与 Mode A 相同的 schema }
```

**核心特征：**
- **速度**：每篇论文约 60–120 秒（embedding + 检索 + 3 个 LLM 调用）
- **依赖**：需要 `pip install paper2spec[agent]`
  (langchain-community, sentence-transformers, faiss-cpu — 约 500MB)
- **上下文窗口**：仅发送相关片段，而非全文
- **适用**：超长论文 (>100 页) 或 Mode A 遗漏细节时
- **查询库**：每部分 5-6 个领域特定查询

#### 模式选择规则

| 条件 | 模式 | 原因 |
|------|------|------|
| ≤ 60 页 | A (内置) | 快速，无需截断 |
| 60–100 页 | A (内置) | 截断保留关键部分 |
| >100 页 | B (agent) | 语义检索避免上下文限制 |
| 用户反馈内容缺失 | B (agent) | 更好的细节召回 |

**自动选择 — 不需要询问用户。**

---

### 阶段2：Extractor（PaperContent → ExtractionResult）

提取器使用5层架构。每层是一个聚焦的 LLM 调用，建立在前一层的输出之上。

```
PaperContent
     │
     ▼
┌──────────────────────────────────────────┐
│  Layer 0: 策略检测                        │
│  输入: title + abstract + methodology     │
│        + signal_logic                    │
│  输出: List[StrategyBrief]               │
│    - 检测到 N 个策略                      │
│    - 每个策略的名称、类型、描述            │
│    - 区分点和相关章节提示                  │
└──────────────────────────────────────────┘
     │
     ├── N = 1: 单策略路径（无上下文注入）
     │
     └── N > 1: 多策略路径（并行提取）
                每个策略注入 "strategy_focus" 块
                到 Layer 1-4 的 prompt 中
     │
     ▼
┌──────────────────────────────────────────────────────┐
│  逐策略提取（策略内串行，策略间并行 N>1）              │
│                                                      │
│  Layer 1: 元数据 + 数据需求                           │
│    → strategy_name, type, asset_class, data_source,  │
│      lookback_period, expected_performance            │
│                                                      │
│  Layer 2: 指标体系                                    │
│    → List[Indicator]，含公式、输入、参数               │
│                                                      │
│  Layer 3: 逻辑管线                                    │
│    → List[LogicStep]: 筛选 → 排名 → 阈值 →           │
│      复合信号 → 交易信号                              │
│                                                      │
│  Layer 4: 执行计划 + 风险管理                         │
│    → List[ExecutionPlan]: 触发、动作、仓位            │
│    → 风控规则                                        │
└──────────────────────────────────────────────────────┘
     │
     ▼
ExtractionResult {
  paper_title: str,
  num_detected: int,
  strategies: List[StrategySpec]
}
```

**多策略并行化** ( N > 1 ):

```
Layer 0 检测到 N 个策略
    │
    ├── 策略 1: L1 → L2 → L3 → L4  ─┐
    ├── 策略 2: L1 → L2 → L3 → L4  ─┤  asyncio.gather()
    └── 策略 N: L1 → L2 → L3 → L4  ─┘
    │
    ▼
ExtractionResult (N 个 specs)
```

每个策略内部 Layer 1–4 **串行**（每层依赖前层输出）。
多个策略之间 **并行** 提取 (asyncio.gather)。

---

### 端到端数据流

```
┌─────────┐   pymupdf4llm   ┌──────────┐   Mode A 或 B   ┌──────────────┐
│  PDF    │ ─────────────→  │ 原始文本 │ ─────────────→  │ PaperContent │
│  文件   │                 │ (MD格式) │   3 ∥ LLM调用    │  .json/.md   │
└─────────┘                 └──────────┘                  └──────────────┘
                                                                │
                                                                ▼
                                                          ┌──────────┐
                                                          │ Layer 0  │
                                                          │ 检测 N   │
                                                          └──────────┘
                                                                │
                                                    ┌───────────┼───────────┐
                                                    ▼           ▼           ▼
                                                 策略 1      策略 2       ...N
                                               L1→L2→L3→L4 L1→L2→L3→L4
                                                    │           │           │
                                                    └───────────┼───────────┘
                                                                ▼
                                                     ┌──────────────────┐
                                                     │ ExtractionResult │
                                                     │   .json / .md    │
                                                     └──────────────────┘
```

### 性能基准

| 阶段 | 单策略 | 多策略 (3 个) |
|------|--------|-------------|
| Parser Mode A | ~20–60s | 相同 (parser 与策略数无关) |
| Parser Mode B | ~60–120s | 相同 |
| Extractor | ~50–70s | ~60–90s (并行) |
| **总计 (Mode A)** | **~70–130s** | **~80–150s** |

基准测试使用 DeepSeek Chat。GPT-4o / Claude 通常慢 1.5–3 倍。

### LLM 调用次数

| 配置 | LLM 调用数 |
|------|-----------|
| Mode A, 1 策略 | 3 (parser) + 1 (L0) + 4 (L1-L4) = **8** |
| Mode A, N 策略 | 3 + 1 + N×4 = **4 + 4N** |
| Mode B, 1 策略 | 3 (parser) + 1 + 4 = **8** |
| Mode B, N 策略 | 3 + 1 + N×4 = **4 + 4N** |

---

### 数据模型参考

| 模型 | 位置 | 用途 |
|------|------|------|
| `PaperContent` | [paper2spec/models.py](../paper2spec/models.py) | 论文解析结果 |
| `StrategyBrief` | 同上 | Layer 0 检测的策略摘要 |
| `StrategySpec` | 同上 | 完整策略规格 (L1-L4 产物) |
| `ExtractionResult` | 同上 | 最终输出：N 个 StrategySpec |
| `Indicator` | 同上 | 指标定义 (L2) |
| `LogicStep` | 同上 | 逻辑步骤 (L3) |
| `ExecutionPlan` | 同上 | 执行计划 (L4) |

### JSON Schema 校验

```bash
# 校验 PaperContent
python -c "import json; from jsonschema import validate; \
  validate(json.load(open('content.json')), json.load(open('schemas/paper_content.schema.json')))"

# 校验 ExtractionResult
python -c "import json; from jsonschema import validate; \
  validate(json.load(open('spec.json')), json.load(open('schemas/strategy_spec.schema.json')))"
```
