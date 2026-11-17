# 全局操作说明

> 本文档定义了RAG优化技能的全局操作规范、环境准备、配置约定与最佳实践

## 目录

1. [环境准备](#一环境准备)
2. [依赖管理](#二依赖管理)
3. [配置规范](#三配置规范)
4. [脚本调用约定](#四脚本调用约定)
5. [参数调优指南](#五参数调优指南)
6. [最佳实践](#六最佳实践)
7. [故障排查](#七故障排查)

---

## 一、环境准备

### 1.1 系统要求

| 项目 | 要求 |
|------|------|
| Python版本 | 3.8+ |
| 内存 | 建议8GB+ |
| 存储 | 视文档规模，建议10GB+ |

### 1.2 可选依赖

根据使用场景选择安装：

```bash
# PDF处理
pip install pdfplumber

# Word文档处理
pip install python-docx

# HTML解析
pip install beautifulsoup4 lxml

# OCR图片识别
pip install pytesseract Pillow

# Excel处理
pip install openpyxl
```

### 1.3 API密钥配置

本技能的 LLM 评估（evaluate.py）通过 HTTP 调用**豆包（Doubao）API**（OpenAI 兼容协议），按需配置以下环境变量；未配置时自动降级为简单指标（无 LLM 评估）：

```python
import os
os.environ["DOUBAO_API_KEY"] = "your-api-key"                    # 必填：豆包 API Key
os.environ["DOUBAO_API_URL"] = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"  # 可选：覆盖默认端点
os.environ["DOUBAO_MODEL"] = "ep-your-endpoint-id"               # 可选：覆盖默认模型端点 ID
```

> 说明：`evaluate.py` 支持 Workload Identity 自动获取凭证（`coze_workload_identity` 可用时），否则读取 `DOUBAO_API_KEY` / `COZE_DOUBAO_API_KEY_{skill_id}` 环境变量。接入其它 LLM 服务商时，按 OpenAI 兼容协议替换端点与模型即可。

### 1.4 .env 文件配置

除了手动 `export` 环境变量，本技能支持通过项目根目录的 `.env` 文件自动加载环境变量。

**安装依赖**：

```bash
pip install python-dotenv>=1.0
# 或
pip install -e ".[env]"
```

**`.env` 文件格式**：

```
# KEY=VALUE 格式，支持 # 注释
NVIDIA_API_URL=https://integrate.api.nvidia.com/v1
NVIDIA_API_KEY=your-nvidia-api-key-here
```

**变量映射表**：

`evaluate.py` 启动时自动加载 `.env` 并完成以下桥接：

| .env 中的变量 | 映射到 | 说明 |
|--------------|--------|------|
| `NVIDIA_API_KEY` | `DOUBAO_API_KEY` | 桥接 NVIDIA API Key 到豆包协议 |
| `NVIDIA_API_URL` | `DOUBAO_API_URL` | 桥接 NVIDIA API 端点（仅当 `DOUBAO_API_URL` 未设置时） |

**优先级**（从高到低）：

```
Workload Identity → 环境变量 COZE_DOUBAO_API_KEY_xxx → 环境变量 DOUBAO_API_KEY → 环境变量 NVIDIA_API_KEY（.env 桥接）→ None（降级）
```

**安全提醒**：

- `.env` 文件**已加入 .gitignore**，请勿手动提交到版本控制
- 若需分享配置模板，请使用 `assets/env.example`（不含真实凭证）

> **降级行为**：未安装 `python-dotenv` 时，`.env` 文件不被自动加载，用户仍需通过 `export` 或系统环境变量注入凭证，其他功能不受影响。

---

## 二、依赖管理

> **核心口径**：技能内所有核心脚本均为**纯标准库实现**，无需安装第三方依赖即可运行（分块、BM25检索、片段提取、评估等）。
> 以下依赖仅在接入 LLM / 向量模型 / 特定文档格式时才按需安装。

### 2.1 可选依赖（按需安装）

| 依赖包 | 版本要求 | 用途 |
|--------|---------|------|
| requests | >=2.0 | LLM评估调用（evaluate.py 通过 HTTP 调豆包 API，无需 SDK） |
| sentence-transformers | >=2.2.0 | 向量嵌入、重排序模型（接入语义检索时） |
| pdfplumber / pypdf | - | PDF 文档预处理 |
| python-docx | - | Word 文档预处理 |
| beautifulsoup4 / lxml | - | HTML 解析 |
| openpyxl | - | Excel 处理 |
| pytesseract / Pillow | - | OCR 图片识别 |
| networkx | >=3.0 | 图结构处理（Graph RAG 场景，可选） |

> 注：技能内置 `bm25_retriever.py` 为纯标准库 Okapi BM25 实现，**无需**安装 rank-bm25；LLM 评估走豆包 API（环境变量 `DOUBAO_API_KEY` / `DOUBAO_API_URL` / `DOUBAO_MODEL`），**无需** anthropic SDK。

### 2.2 安装命令（按需安装）

```bash
# LLM评估（豆包API，通常已随环境自带，如需显式安装）
pip install requests>=2.0

# 向量嵌入 / 重排序模型（接入语义检索与精排时）
pip install sentence-transformers>=2.2.0

# 文档预处理（按文档格式选装）
pip install pdfplumber pypdf python-docx beautifulsoup4 lxml openpyxl pytesseract Pillow

# Graph RAG 场景（可选）
pip install networkx>=3.0
```

### 2.3 版本兼容性

- Python 3.8-3.11：完全支持
- Python 3.12：核心功能支持，部分可选依赖可能需要从源码安装
- Python < 3.8：不支持


### 2.3 新增模块（进阶优化）

以下模块为进阶优化新增，补全了 config-template.json 中声明但未实现的核心功能。

| 模块 | 文件 | 功能 | 可选依赖 |
|------|------|------|---------|
| LLM 客户端 | scripts/llm_client.py | 统一 LLM 调用接口（score/generate/classify/extract_json），内置安全数字解析、可配置重试（`max_retries`/`retry_delay`）、熔断器、`wrap_llm()` 统一包装；另含向量嵌入客户端（`EmbeddingClient`/`NvidiaEmbeddingClient`，维度统一由 `EMBEDDING_DIMS`/`resolve_embedding_dim` 解析） | python-dotenv |
| 查询转换器 | scripts/query_transformer.py | HyDE 假设文档生成、查询扩展、查询分解（自动选择策略） | 无（LLM 可选） |
| 重排序器 | scripts/reranker.py | 两阶段检索精排，支持 bge-reranker / cross-encoder 模型，无模型时回退 BM25 | sentence-transformers |
| 文档单元 | scripts/document_unit.py | 统一数据协议 DocumentUnit，各脚本的数据类型可互操作 | 无 |
| 检索器基类 | scripts/retriever_base.py | BM25/Vector/Hybrid 可组合的检索器策略；其中 `BM25Retriever` 为**适配层**，延迟导入并委托功能完整的 `scripts/bm25_retriever.py`（含 LRU+TTL 缓存、缓存自动失效、k1/b 变参重试） | 无 |
| 配置装配 | scripts/config_loader.py | 配置校验（`ConfigError`）+ 组件一键装配（`load_config` / `build_pipeline`），config-template.json 的官方消费入口 | 无 |

**安装进阶依赖**：

```
pip install python-dotenv>=1.0
pip install sentence-transformers>=2.2.0
pip install -e ".[env,vector]"
```

---

## 三、配置规范

### 3.1 配置文件结构

使用JSON格式配置文件，标准结构：

```json
{
  "chunking": { ... },
  "retrieval": { ... },
  "reranking": { ... },
  "generation": { ... },
  "self_rag": { ... },
  "context_compression": { ... },
  "citation_tracking": { ... },
  "query_intent": { ... },
  "multi_hop_retrieval": { ... },
  "document_preprocessing": { ... }
}
```

### 3.2 配置加载（推荐走装配管道）

配置的**官方消费入口**是 `scripts/config_loader.py`——它先经 `config_validator` 校验，再装配出可直接使用的组件：

```python
import sys; sys.path.insert(0, "scripts")   # 导入约定见 4.1
from config_loader import load_config, build_pipeline, ConfigError

cfg = load_config("assets/config-template.json")          # 校验 + 展开模板
parts = build_pipeline(cfg)                                # 一键装配
# parts 中可取：chunker / retriever / llm 等已初始化组件
```

- `load_config(path=None, strict=False)`：path 缺省时自动定位 `assets/config-template.json`；`strict=True` 时校验失败抛 `ConfigError`，默认仅告警
- `build_pipeline(cfg, ...)`：按配置节（chunking / retrieval / performance 等）实例化组件，并注入 `performance.cache` 的开关与 TTL

仅需要读取个别参数时，才直接 `json.load`（此时注意区分模板中 `IMPLEMENTED` 与 `NOT YET IMPLEMENTED` 的 `_status` 标注，后者没有代码消费者）：

```python
import json
with open("assets/config-template.json", "r", encoding="utf-8") as f:
    raw = json.load(f)
config = raw["rag_optimization_config"]
```

### 3.3 预设配置

配置模板顶层 `presets` 键提供 **9 个场景预设**：

| 预设名称 | 适用场景 |
|---------|---------|
| `quick_start` | 快速体验最小可用组合 |
| `production` | 生产环境稳健配置 |
| `high_accuracy` | 精度优先（重排 + Self-RAG 全开） |
| `fact_qa` | 事实型问答（命题分块） |
| `long_document` | 长文档（由小到大检索） |
| `legal_documents` | 法律条文（细粒度 + 引用溯源） |
| `research_papers` | 学术论文（语义分块 + 头部增强） |
| `complex_reasoning` | 复杂推理（多跳 + Self-RAG） |
| `customer_service` | 客服问答（快速响应 + 意图识别） |

使用预设：

```python
preset = raw["presets"]["complex_reasoning"]   # 注意：presets 在模板顶层
cfg = load_config("assets/config-template.json")
cfg.update(preset)                              # 合并后再 build_pipeline
```

---

## 四、脚本调用约定

### 4.1 导入约定（重要）

`scripts/` 下的模块互相使用**平铺导入**（如 `from llm_client import ...`）。使用任一脚本前，先把 `scripts/` 目录加入 `sys.path`：

```python
import sys; sys.path.insert(0, "scripts")

from self_rag import SelfRAG
from bm25_retriever import BM25Retriever
from llm_client import load_from_env, wrap_llm
```

> 注意：`from scripts.xxx import ...` 的**包式写法不可用**：脚本内部是平铺导入，包式导入会触发 `ModuleNotFoundError`（实测：`from scripts.self_rag import SelfRAG` 报 `No module named 'llm_client'`）。

所有脚本遵循统一的初始化模式：

```python
from scripts.<module_name> import <ClassName>

# 初始化
instance = <ClassName>(
    llm_client=your_llm_client,        # LLM客户端（必需）
    embed_model=your_embedding_model,   # 嵌入模型（部分脚本需要）
    config={                            # 配置字典（可选）
        'param1': value1,
        'param2': value2
    }
)

# 调用
result = instance.method(required_param, **options)
```

### 4.2 脚本列表与用途

| 脚本 | 类名 | 用途 | 必需参数 |
|------|------|------|---------|
| evaluate.py | RAGEvaluator | 系统评估（CLI 另支持 `--config`/`--rag-class`/`--compare`） | queries, documents, answers |
| self_rag.py | CorrectiveRAG / SelfRAG | 自我纠错 | retriever, generator, llm_client |
| segment_extractor.py | RelevantSegmentExtractor | 片段提取 | query, documents |
| proposition_chunker.py | PropositionChunker | 命题分块 | document |
| contextual_header.py | ContextualHeaderEnhancer | 头部增强 | chunk, metadata |
| context_compression.py | ContextCompressor | 上下文压缩 | query, contexts |
| citation_tracker.py | CitationTracker（内部 CitationMatcher 支持 LLM 语义兜底） | 引用溯源 | answer, sources |
| query_intent.py | QueryIntentRecognizer（方法 `recognize(q)` 返回 `IntentResult`） | 意图识别 | query |
| multi_hop_retriever.py | MultiHopRetriever | 多跳检索 | query, base_retriever |
| document_preprocessor.py | DocumentPreprocessor | 文档预处理 | file_path |

### 4.3 返回值约定

所有脚本返回字典格式，包含：

```python
{
    'success': bool,           # 操作是否成功
    'result': Any,             # 主要结果
    'metrics': dict,           # 性能指标（可选）
    'error': str               # 错误信息（失败时）
}
```

---

## 五、参数调优指南

### 5.1 分块参数

| 参数 | 默认值 | 调优建议 |
|------|--------|---------|
| chunk_size | 500 | 技术文档500-800，学术论文800-1200 |
| overlap | 50 | 重要内容可提高到100-150 |
| min_proposition_length | 15 | 短问答场景可降至10 |
| max_proposition_length | 150 | 复杂场景可提高到200 |
| child_chunk_size（由小到大子块） | 150 | 技术文档150，学术论文200，法律条文100 |
| parent_chunk_size（由小到大父块） | 600 | 技术文档600，学术论文800，法律条文500 |

### 5.2 检索参数

| 参数 | 默认值 | 调优建议 |
|------|--------|---------|
| top_k | 5 | 简单问题3-5，复杂问题8-10 |
| alpha（混合检索权重） | 0.7 | 关键词多时降至0.5 |
| docs_per_hop（多跳） | 3 | 复杂问题可提高到5 |
| embedding_model | BAAI/bge-m3 | 中文/多语言文档推荐 bge-m3；纯英文可换 text-embedding-3-small |

### 5.3 重排序参数

| 参数 | 默认值 | 调优建议 |
|------|--------|---------|
| first_stage_k | 50 | 大型知识库可提高到100 |
| final_k | 5 | 根据上下文窗口调整 |

### 5.4 Self-RAG参数

| 参数 | 默认值 | 调优建议 |
|------|--------|---------|
| high_relevance_threshold | 0.7 | 高精度场景提高到0.8 |
| low_relevance_threshold | 0.3 | 可根据召回率调整 |
| max_retries | 3 | 延迟敏感可降至2 |

### 5.5 压缩参数

| 参数 | 默认值 | 调优建议 |
|------|--------|---------|
| target_ratio | 0.5 | Token预算紧张可降至0.3 |
| min_length | 50 | 根据最小信息需求调整 |
| protect_entities | True | 精确问答场景必须开启 |

---

## 六、最佳实践

### 6.1 策略组合推荐

**分块阶段**：
- 上下文头增强 + 命题分块
- 适用于：需要精确匹配事实的场景

**检索阶段**：
- 混合检索 + 查询意图识别
- 适用于：查询类型多样的场景

**后处理阶段**：
- 相关片段提取 + 上下文压缩
- 适用于：Token预算紧张的场景

**生成控制阶段**：
- Self-RAG + 引用溯源
- 适用于：高可信度要求的场景

### 6.2 性能优化建议

1. **延迟优化**：
   - 使用 `eval_mode='vector'` 而非 `llm`
   - 减少重试次数
   - 启用早停机制

2. **Token优化**：
   - 启用上下文压缩
   - 使用相关片段提取
   - 控制检索数量（top_k）

3. **准确率优化**：
   - 启用重排序
   - 使用Self-RAG质量评估
   - 根据查询意图动态调整策略

### 6.3 避免的常见错误

| 错误 | 影响 | 解决方案 |
|------|------|---------|
| 过度优化 | 延迟增加、成本上升 | 根据问题诊断选择必要策略 |
| 忽略基准测试 | 无法评估效果 | 优化前建立baseline指标 |
| 参数一刀切 | 效果不稳定 | 根据文档类型和查询特征调整 |
| 不评估迭代 | 效果不可知 | 定期使用evaluate.py评估 |

---

## 七、故障排查

### 7.1 常见错误与解决方案

| 错误现象 | 可能原因 | 解决方案 |
|---------|---------|---------|
| 检索结果为空 | 向量库未初始化 | 检查index_documents是否执行 |
| API调用失败 | 密钥无效/网络问题 | 检查API密钥配置和网络连接 |
| 内存溢出 | 文档过大/分块过多 | 减小chunk_size或分批处理 |
| 延迟过高 | LLM调用过多 | 使用vector模式或减少重试 |
| 答案有幻觉 | 检索质量差 | 启用Self-RAG和重排序 |

### 7.2 调试建议

1. **启用详细日志**：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **单步验证**：
   - 先测试单个小文档
   - 逐步增加数据规模
   - 每个策略单独测试再组合

3. **性能监控**：
```python
import time

start = time.time()
result = instance.method(params)
print(f"耗时: {time.time() - start:.2f}s")
```

### 7.3 获取帮助

- 查看详细实现：[advanced-techniques.md](advanced-techniques.md)
- 快速入门：[quickstart.md](quickstart.md)
- 完整说明：[README.md](README.md)

---

## 附录：配置模板说明

完整配置模板见 [assets/config-template.json](../assets/config-template.json)，包含：

- 分块配置（chunking）
- 检索配置（retrieval）
- 重排序配置（reranking）
- Self-RAG配置（self_rag）
- 上下文压缩配置（context_compression）
- 引用溯源配置（citation_tracking）
- 查询意图配置（query_intent）
- 多跳检索配置（multi_hop_retrieval）
- 文档预处理配置（document_preprocessing）
- 预设配置（presets）
