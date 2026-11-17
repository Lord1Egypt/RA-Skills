---
name: rag-optimization
description: 完整的RAG系统优化方案，涵盖21+种策略（Self-RAG、命题分块、上下文压缩、引用溯源、查询意图等）；提供诊断工具、实现代码与评估框架；当用户需要优化知识库问答、提升检索准确率、降低幻觉或评估RAG效果时使用
dependency:
  python:
    - python-dotenv>=1.0
    - sentence-transformers>=2.2.0
    - numpy>=1.21.0
    - pdfplumber>=0.7.0
    - pypdf>=3.0.0
    - python-docx>=0.8.11
    - beautifulsoup4>=4.9.0
    - lxml>=4.6.0
    - pytesseract>=0.3.8
    - Pillow>=8.0.0
    - openpyxl>=3.0.0
    - networkx>=3.0
    - requests>=2.0
---

# RAG检索优化技能

## 技能概述

本技能提供完整的RAG系统优化方案，涵盖21+种优化策略，帮助构建高准确率、生产级的RAG应用。

**核心价值**：
- 准确率可从 0.3 提升至 0.85+
- 提供可落地的实施代码与配置模板
- 包含完整的评估框架

> 注意：**效果数字说明**——本文档与策略详解中引用的效果数据（如准确率 0.30→0.85、幻觉率↓30-50% 等）均为**社区基准/经验参考值**，具体提升幅度取决于你的文档类型、查询分布与基线水平。请务必使用 [scripts/evaluate.py](scripts/evaluate.py) 在自有数据上建立基准并对比验证，勿将参考值当作保证值。

**适用场景**：构建知识库问答、优化检索准确率、解决检索噪音、降低幻觉问题

**环境准备与配置**：详见 [全局操作说明](references/global-operations.md)

### 架构约束

> 注意：以下架构限制在使用前需要了解：

| 约束 | 说明 |
|------|------|
| **同步架构** | 所有操作为同步执行，一个 LLM 调用阻塞整个线程。高并发场景需要外部封装异步层 |
| **LLM 依赖** | Self-RAG、Reranking、上下文压缩（抽象模式）、多跳推理等依赖 LLM API。未配置时自动降级为规则模式，但效果大幅退化 |
| **向量嵌入** | 语义相似度分块（`similarity_threshold`）依赖 NVIDIA API 或本地 sentence-transformers 模型。无嵌入模型时退化为结构性分块 |
| **熔断器** | API 连续失败 5 次后触发熔断，冷却 30 秒后恢复。阈值与冷却时长可通过 `OpenAILikeClient(circuit_failure_threshold=..., circuit_cooldown_seconds=...)` 调整 |
| **缓存** | BM25 检索器内置 OrderedDict LRU 查询缓存（默认上限 128 条，TTL 默认 3600 秒，可经 `config` 的 `cache_max_size` / `cache_ttl_seconds` 调整；`cache_max_size=0` 关闭缓存）。`index_documents()` / `add_document()` 会**自动失效**缓存并重算 IDF；跨实例或外部改索引后可手动调用 `invalidate_cache()`。注意：TTL 随缓存条目生效，`cache_ttl_seconds=0` 表示永不过期 |

---

## 一、问题诊断

### 痛点自查表

| 症状 | 可能原因 | 诊断方法 |
|------|---------|---------|
| 检索不到内容 | 分块策略不当、向量模型不适配 | 检查召回率（Recall@K） |
| 检索到但答案不准 | 检索噪音、重排序缺失 | 检查精确率（Precision@K） |
| 答案不完整 | 上下文窗口不足、分块断裂 | 检查上下文完整性 |
| 答案有幻觉 | 检索内容不相关、模型过度推理 | 对比答案与检索内容 |
| 简单问题答不对 | 查询理解失败 | 检查查询转换效果 |
| 复杂问题答不出 | 缺乏多跳推理能力 | 评估是否需要Graph RAG |

### 基准测试

优化前建立基准指标：`recall@10`、`precision@5`、`MRR`、`answer_accuracy`

**评估工具**：调用 [scripts/evaluate.py](scripts/evaluate.py) 进行系统评估

---

## 二、策略全景图

### 策略分类

- **检索前优化**：语义分块、命题分块、上下文头增强、由小到大检索、文档预处理、查询转换、查询意图识别
- **检索中优化**：混合检索（向量+BM25）、HyDE、多跳检索、分层路由
- **检索后优化**：重排序、相关片段提取、上下文压缩、引用溯源、幻觉检测
- **生成控制**：Self-RAG/CRAG（自我纠错与质量评估）、反馈循环（持续优化）
- **架构级优化**：分层索引（多级索引结构）、Graph RAG（图结构知识）

### 策略选择决策树

```
你的问题是什么？
│
├─ 检索不到内容？
│   ├─ 文档很长？ → 由小到大检索
│   ├─ 查询模糊？ → HyDE + 查询扩展
│   ├─ 分块断裂？ → 语义分块
│   └─ 召回率低？ → 上下文头增强
│
├─ 检索到太多噪音？
│   ├─ 有精确术语？ → 混合检索（增加关键词权重）
│   ├─ 排序不准？ → 重排序
│   ├─ Token浪费？ → 相关片段提取
│   └─ 需要溯源？ → 引用溯源
│
├─ 复杂问题答不出？
│   ├─ 需要多步推理？ → 多跳检索 / Graph RAG
│   └─ 跨领域查询？ → 分层路由
│
├─ 答案有幻觉？
│   ├─ 检索内容太长？ → 上下文压缩
│   ├─ 检索质量差？ → Self-RAG/CRAG
│   └─ 无法验证？ → 引用溯源 + 幻觉检测
│
└─ 需要精确匹配事实？
    └─ 命题分块
```

---

## 三、核心策略详解

> 各策略的代码级实现均见 [高级技术指南](references/advanced-techniques.md)（下文不再逐条重复链接）。

### 策略1：语义分块

**问题**：固定大小分块会切断语义完整性

**方案**：基于语义边界动态分块（段落/句子边界聚合，`chunker_factory.py` 零依赖实现）；接入向量模型后可升级为真正的相似度切分（`similarity_threshold` 生效）

**效果**：准确率 0.30 → 0.85，性价比最高

### 策略2：由小到大检索

**问题**：小块检索精准但上下文不足，大块完整但检索不准

**方案**：检索小块（100-200字），返回大块（500-1000字）

**三步流程**：1. 文档切分为子块 + 父块；2. 用子块向量检索；3. 返回对应的父块

**参数建议**：技术文档(150/600字)、学术论文(200/800字)、法律条文(100/500字)

### 策略3：查询转换

**问题**：用户查询表述不清、过于复杂

**方案**：用LLM转换查询形式

**三种模式**：查询扩展（生成多个语义变体，适用于查询词少）、查询分解（拆解复杂问题，适用于多条件查询）、HyDE（生成假设答案用于检索，适用于短查询）

### 策略4：重排序（Reranking）

**问题**：向量检索的初步排序不够精准

**方案**：两阶段检索 - 粗筛(top 50) + 精排(top 5)

**流程**：查询 → 向量检索 → 重排序模型 → 最终结果

**模型推荐**：英文 ms-marco-MiniLM-L-6-v2（快速）或 L-12-v2（高精度）；中文 BAAI/bge-reranker-large

**效果**：准确率 0.50 → 0.70

### 策略5：混合检索

**问题**：纯向量检索无法精准匹配关键词

**方案**：向量检索 + BM25关键词检索

**融合公式**：`final_score = α × vector_score + (1-α) × bm25_score`

**自适应权重**：短查询/专有名词 → α=0.5，长查询 → α=0.7

**效果**：准确率 0.50 → 0.83

### 策略6：Self-RAG / Corrective RAG

**问题**：检索结果质量差时仍会生成错误答案

**方案**：在检索和生成环节增加质量评估，自动纠正错误

**两种模式**：Corrective RAG（检索后评估 + 纠正动作）、Self-RAG（全流程自检 + 来源标注）

**脚本调用**：`scripts/self_rag.py`，支持 `CorrectiveRAG` 和 `SelfRAG` 两种模式

**配置参数**：`max_retries`、`high_relevance_threshold`、`eval_mode` 等

**效果**：幻觉率降低 30-50%

### 策略7：相关片段提取

**问题**：检索到的文档块包含大量无关内容

**方案**：从文档块中提取与问题最相关的句子/段落

**三种粒度**：句子级（精确问答）、滑动窗口（通用）、语义边界（学术论文）

**脚本调用**：`scripts/segment_extractor.py`

**效果**：Token减少 60-80%

### 策略8：命题分块

**问题**：传统分块粒度粗，无法精准匹配具体事实

**方案**：将文档拆解为最小的事实单元（命题），每个命题独立可检索

**示例**：传统分块 `"RAG是一种技术。它能降低幻觉。"` → 命题分块 `"RAG是一种技术"` + `"RAG能降低幻觉"`

**脚本调用**：`scripts/proposition_chunker.py`

**最佳实践**：与Small-to-Big结合，命题作为子块，原段落作为父块

### 策略9：上下文头增强分块

**问题**：文档块脱离上下文后语义不完整

**方案**：为每个文档块添加元数据头部，补充全局背景信息

**头部内容**：文档标题、章节路径、主题标签、关键实体

**效果**：召回率提升 10-20%

**脚本调用**：`scripts/contextual_header.py`

### 策略10：上下文压缩

**问题**：检索到的上下文包含大量无关内容，浪费Token

**方案**：对检索结果压缩，保留核心信息

**三种模式**：提取式（选取关键句子，保真度高）、摘要式（LLM生成精炼摘要，信息密度高）、混合式（先提取再摘要，平衡方案）

**脚本调用**：`scripts/context_compression.py`

**效果**：Token减少 50-70%

### 策略11：引用溯源

**问题**：答案来源不明确，无法判断可信度

**方案**：为答案标注引用来源，提供可信度评分

**四种格式**：行内引用[1]、脚注引用¹、详细引用（来源+可信度）、JSON引用

**脚本调用**：`scripts/citation_tracker.py`

**效果**：答案可信度显著提升

### 策略12：查询意图识别

**问题**：用户查询表达模糊，检索策略一刀切

**方案**：识别查询意图类型，动态调整检索策略

**七种意图**：事实查询、对比分析、操作指导、概念解释、开放讨论、问题诊断、闲聊问候

**脚本调用**：`scripts/query_intent.py`

**效果**：答案质量提升 15-25%

### 策略13：多跳检索

**问题**：复杂问题需要综合多个信息源

**方案**：迭代检索，逐步收集信息直到答案完整

**适用场景**：`"A公司的CEO在哪所大学毕业？"`（先查CEO，再查毕业院校）

**脚本调用**：`scripts/multi_hop_retriever.py`

**效果**：复杂问题完整度提高 40%+

### 策略14：文档预处理

**问题**：多格式文档直接向量化效果差

**方案**：标准化预处理，提取结构化内容

**支持格式**：PDF、Word、Excel、HTML、Markdown、图片（OCR）

**脚本调用**：`scripts/document_preprocessor.py`

### 策略15：Graph RAG

**问题**：传统检索无法捕捉实体间关系，对"X和Y有什么关系"类问题效果差

**方案**：从文档中提取实体和关系构建知识图谱，支持图遍历检索

**支持能力**：实体提取（规则模式 + LLM 模式）、关系构建（located_in / is_capital_of / belongs_to 等）、图遍历检索（根据查询实体找到关联实体和关系）

**脚本调用**：`scripts/graph_rag.py`，用法：`GraphRAG().build_from_text(text)` 后调用 `.query(q)`，如输入 "北京是中国的首都，故宫位于北京。"，查询 "故宫在哪里" 返回关系 `故宫 --[located_in]--> 北京`

**限制**：规则模式仅支持预定义实体词表和关系模板；LLM 模式可识别更广泛的实体类型但依赖 API 可用性

### 策略16：查询路由

**问题**：所有查询走同一路径，不同查询类型应使用不同检索策略

**方案**：根据查询意图（FAQ / 开放域 / 代码 / 推理）自动路由到不同检索器

**脚本调用**：`scripts/query_router.py`，用法：`QueryRouter(retrievers={"faq": ..., "open_domain": ..., "default": ...}).route(q, top_k=5)`，短查询自动匹配 FAQ 检索器

### 基础设施：LLM 客户端

`scripts/llm_client.py` 提供统一 LLM 抽象，所有智能特性（Self-RAG、Reranking、HyDE、多跳推理）通过此接口调用：

| 方法 | 用途 |
|------|------|
| `score(prompt)` | 评分（安全解析数字，支持 `X/10`、`X%`、`X out of Y` 格式） |
| `generate(prompt)` | 文本生成 |
| `classify(prompt, options)` | 分类（多标签选择） |
| `extract_json(prompt)` | 提取 JSON 输出 |

**安全特性**：
- 重试 + 指数退避：次数与基础延迟可通过 `OpenAILikeClient(max_retries=N, retry_delay=S)` 配置（默认 3 次）
- **熔断器**：连续失败达到阈值（默认 5）后熔断，冷却（默认 30 秒）后进入 half-open 恢复
- 安全数字解析：优先匹配显式格式，避免错误截断
- LRU 缓存（128 条上限）

**统一包装入口**：各脚本接收的 `llm_client` 参数请经 `wrap_llm()` 归一——已是 `LLMClient` 的对象原样返回，裸客户端才包一层（`llm = wrap_llm(your_client)`，None / 裸客户端 / LLMClient 均安全）。直接 `LLMClient(llm_client=x)` 叠套会造成 3×3=9 次重试放大。

**向量嵌入**：`EmbeddingClient`（本地 sentence-transformers，缺依赖时哈希降级并明确告警）与 `NvidiaEmbeddingClient`（API 嵌入）维度统一由 `EMBEDDING_DIMS` / `resolve_embedding_dim(model_name)` 查表解析，返回 `EmbeddingResult`（可用 `.vectors` / `.list` 取裸向量）。未知模型回退默认 2048 维。

**零配置加载**：`from llm_client import load_from_env; llm = load_from_env()` —— 自动读取环境变量（含 `.env` 文件）中的 API 凭证，配置方法见 [全局操作说明](references/global-operations.md)。

---

## 四、核心技术对比

| 技术 | 解决的问题 | 效果提升 | 实现难度 | 推荐优先级 |
|------|-----------|---------|---------|-----------|
| Self-RAG/CRAG | 检索错误导致答案错误 | 幻觉率↓30-50% | 中高 | 1 |
| 相关片段提取 | Token浪费、噪声多 | Token↓60-80% | 中 | 2 |
| 命题分块 | 无法精准匹配事实 | 精确度↑ | 高 | 3 |
| 上下文头增强 | 召回率低 | 召回率↑10-20% | 低 | 4 |
| 上下文压缩 | Token浪费、噪声多 | Token↓50-70% | 中 | 5 |
| 引用溯源 | 答案来源不明确 | 可信度↑ | 低 | 6 |
| 查询意图识别 | 检索策略一刀切 | 质量↑15-25% | 低 | 7 |
| 多跳检索 | 复杂问题答不全 | 完整度↑40% | 中高 | 8 |
| 文档预处理 | 文档质量差 | 基础质量↑ | 中 | 9 |

---

## 五、操作步骤

### 步骤1：问题诊断

使用痛点自查表识别问题，调用 [scripts/evaluate.py](scripts/evaluate.py) 建立基准指标

### 步骤2：选择策略

根据策略选择决策树确定优化策略组合

### 步骤3：配置实现

两条路径任选：

**a. 一键装配管道（推荐）**：`scripts/config_loader.py` 读取 [assets/config-template.json](assets/config-template.json)，先经 `config_validator` 校验（strict 模式抛 `ConfigError`），再装配出分块器/检索器/LLM 客户端等组件：

```python
from config_loader import load_config, build_pipeline

cfg = load_config("assets/config-template.json")   # 校验 + 展开
parts = build_pipeline(cfg)                         # parts["chunker"] / parts["retriever"] / ...
```

**b. 手动读取**：仅需要参数时，直接 `json.load` 模板中对应节即可（配置项与代码的对应关系见模板内 `_status` 标注：`IMPLEMENTED` 表示已有消费者，`NOT YET IMPLEMENTED` 表示当前由其它组件间接覆盖或未实现）。

模板含 9 个场景预设（顶层 `presets` 键），详见 [全局操作说明](references/global-operations.md)。

### 步骤4：验证效果

使用评估脚本验证优化效果，对比基准指标，持续迭代

---

## 使用示例

- 示例1：评估现有 RAG 效果
  - 场景/输入：已有 RAG 实现（Python 类）与测试集（可参考 [assets/test-cases-example.json](assets/test-cases-example.json)）
  - 操作：`python scripts/evaluate.py --test-data test_cases.json --config config.json --rag-class my_rag.MyRAG --compare old_report.json`
  - 预期产出：评估报告 JSON（recall@K / precision@K / MRR / answer_accuracy）；`--compare` 时附新旧指标对比
  - 关键要点：`--test-data` 必填；未配置 LLM 凭证时自动降级为规则模式（结果准确性下降）
- 示例2：一键装配优化管道
  - 场景/输入：选定策略组合后需要快速搭建组件
  - 操作：`from config_loader import load_config, build_pipeline; parts = build_pipeline(load_config("assets/config-template.json"))`
  - 预期产出：装配好的分块器、检索器、LLM 客户端等组件字典
  - 关键要点：可基于 [assets/config-template.json](assets/config-template.json) 的 9 个场景预设修改；配置不合法会被 `config_validator` 拦截
- 示例3：检索性能基准测试
  - 场景/输入：需要了解 BM25 检索随文档规模的增长表现
  - 操作：`python scripts/benchmark_retrieval.py --docs 1000`
  - 预期产出：不同文档量级下的索引/检索耗时数据
  - 关键要点：用于容量规划，与效果评估（示例1）互为补充

---

## 六、资源索引

### 核心脚本
| 脚本 | 用途 |
|------|------|
| [evaluate.py](scripts/evaluate.py) | RAG系统评估（核心评估 CLI：`--config` 接装配管道、`--rag-class` 指定你的 RAG 类、`--compare` 新旧对比） |
| [config_loader.py](scripts/config_loader.py) | 配置校验 + 组件装配管道（步骤3 推荐入口） |
| [self_rag.py](scripts/self_rag.py) | Self-RAG/CRAG实现 |
| [bm25_retriever.py](scripts/bm25_retriever.py) | BM25/向量/混合检索（纯标准库，含 LRU+TTL 缓存、k1/b 变参重试） |
| [chunker_factory.py](scripts/chunker_factory.py) | 分块工厂（5种策略统一入口） |
| [query_transformer.py](scripts/query_transformer.py) | 查询转换（扩展/分解/HyDE） |
| [reranker.py](scripts/reranker.py) | 两阶段重排序（无模型时回退 BM25） |
| [segment_extractor.py](scripts/segment_extractor.py) | 相关片段提取 |
| [proposition_chunker.py](scripts/proposition_chunker.py) | 命题分块 |
| [contextual_header.py](scripts/contextual_header.py) | 上下文头增强 |
| [context_compression.py](scripts/context_compression.py) | 上下文压缩 |
| [citation_tracker.py](scripts/citation_tracker.py) | 引用溯源（规则匹配 + LLM 语义兜底） |
| [query_intent.py](scripts/query_intent.py) | 查询意图识别（主类 `QueryIntentRecognizer`） |
| [multi_hop_retriever.py](scripts/multi_hop_retriever.py) | 多跳检索 |
| [document_preprocessor.py](scripts/document_preprocessor.py) | 文档预处理 |
| [graph_rag.py](scripts/graph_rag.py) | Graph RAG（实体/关系/图遍历） |
| [query_router.py](scripts/query_router.py) | 查询路由 |
| [llm_client.py](scripts/llm_client.py) | 统一 LLM/嵌入客户端（score/generate/classify/extract_json + 熔断 + wrap_llm） |
| [retriever_base.py](scripts/retriever_base.py) | 检索器基类与公共协议（自定义检索器时继承） |
| [document_unit.py](scripts/document_unit.py) | 统一文档单元协议（分块/命题/片段/引用互操作的数据结构） |
| [benchmark_retrieval.py](scripts/benchmark_retrieval.py) | BM25 检索性能基准测试（CLI：`--docs N`） |
| [generate-api-docs.py](scripts/generate-api-docs.py) | 从源码自动生成 API 文档（`python scripts/generate-api-docs.py references`，输出 api_reference / api_class_reference / api_enums 三份，以代码为唯一真相源） |

> **导入约定**：`scripts/` 下脚本互相使用平铺导入（如 `from llm_client import ...`）。在你的代码中请先将 `scripts/` 加入 `sys.path` 再平铺导入各模块；`from scripts.xxx import ...` 的包式写法**不可用**。

### 参考文档
| 文档 | 说明 |
|------|------|
| [global-operations.md](references/global-operations.md) | 全局操作说明（环境准备、LLM 凭证配置、`.env` 格式、参数调优） |
| [quickstart.md](references/quickstart.md) | 5分钟快速上手 |
| [advanced-techniques.md](references/advanced-techniques.md) | 9项核心技术详细实现 |
| [implementation-guide.md](references/implementation-guide.md) | 全链路落地实践 |
| [golden-set-guide.md](references/golden-set-guide.md) | Golden Set（黄金测试集）建设指南 |
| [api-docs-auto-generation.md](references/api-docs-auto-generation.md) | API 文档自动生成方案说明（配套 `scripts/generate-api-docs.py`） |
| [api_reference.md](references/api_reference.md) | 完整 API 参考（自动生成，以代码为唯一真相源；查阅类/方法签名以本文件为准，配套 [api_class_reference.md](references/api_class_reference.md) 符号速查表与 [api_enums.md](references/api_enums.md) 枚举汇总） |

### 配置与数据
| 资源 | 说明 |
|------|------|
| [config-template.json](assets/config-template.json) | 完整配置模板（含预设） |
| [test-cases-example.json](assets/test-cases-example.json) | 测试用例示例（58 例） |

---

## 注意事项

- **环境准备**：参考 [全局操作说明](references/global-operations.md) 完成依赖安装和配置；LLM 凭证通过环境变量或项目根目录 `.env` 文件注入（格式模板见该文档 1.4 节），切勿将真实凭证写入任何被分发/提交的文件
- **参数调优**：根据文档类型和查询特征调整参数，详见 [参数调优指南](references/global-operations.md)
- **策略组合**：避免过度优化，根据问题诊断选择必要策略
- **评估迭代**：优化前建立基准指标，定期评估效果
