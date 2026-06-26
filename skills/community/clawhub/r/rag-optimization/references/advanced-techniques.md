# RAG高级技术实现指南

> 本文档详细介绍九项核心RAG优化技术的实现细节、配置参数与最佳实践

## 目录

1. [Self-RAG / Corrective RAG](#一self-rag--corrective-rag)
2. [相关片段提取](#二相关片段提取)
3. [命题分块](#三命题分块)
4. [上下文头增强分块](#四上下文头增强分块)
5. [上下文压缩](#五上下文压缩)
6. [引用溯源](#六引用溯源)
7. [查询意图识别](#七查询意图识别)
8. [多跳检索](#八多跳检索)
9. [文档预处理](#九文档预处理)

---

## 一、Self-RAG / Corrective RAG

### 1.1 技术概述

**核心思想**：在RAG流程中增加质量评估和自我纠错机制，避免"检索错误导致答案错误"的问题。

**两种模式对比**：

| 特性 | Corrective RAG | Self-RAG |
|------|---------------|----------|
| 检索前评估 | ✗ | ✓ 判断是否需要检索 |
| 检索后评估 | ✓ 相关性评估 | ✓ 相关性评估 |
| 生成后评估 | ✗ | ✓ 忠实度/幻觉检测 |
| 来源标注 | ✗ | ✓ 每个片段标注来源 |
| 实现复杂度 | 中等 | 较高 |

### 1.2 核心流程

```
Corrective RAG 流程：
┌─────────────────────────────────────────────────────┐
│  用户查询 → 检索 → 质量评估 → [不合格] → 纠正动作   │
│                         ↓ [合格]                     │
│                      生成答案                         │
└─────────────────────────────────────────────────────┘

Self-RAG 流程：
┌─────────────────────────────────────────────────────┐
│  用户查询 → [需要检索?] → 检索 → [相关?] → 生成     │
│      ↓否           ↓是              ↓否             │
│   直接生成      重试/搜索        重新检索            │
│                                                      │
│  生成 → [基于检索?] → [有幻觉?] → 输出(带来源标注)  │
└─────────────────────────────────────────────────────┘
```

### 1.3 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `max_retries` | int | 3 | 最大重试次数 |
| `high_relevance_threshold` | float | 0.7 | 高相关性阈值（>=此值直接生成） |
| `low_relevance_threshold` | float | 0.3 | 低相关性阈值（<此值转网络搜索） |
| `eval_mode` | str | 'hybrid' | 评估模式：vector/llm/hybrid |
| `hallucination_threshold` | float | 0.5 | 幻觉检测阈值 |
| `enable_retrieval_decision` | bool | True | 是否启用检索决策（Self-RAG） |
| `enable_segment_labeling` | bool | True | 是否启用来源标注（Self-RAG） |

### 1.4 使用示例

```python
from scripts.self_rag import CorrectiveRAG, SelfRAG

# Corrective RAG
crag = CorrectiveRAG(
    retriever=your_retriever,
    generator=your_generator,
    llm_client=your_llm,
    config={
        'max_retries': 3,
        'high_relevance_threshold': 0.7,
        'low_relevance_threshold': 0.3
    }
)

result = crag.query("RAG系统如何优化？")

# Self-RAG（更完整）
self_rag = SelfRAG(
    retriever=your_retriever,
    generator=your_generator,
    llm_client=your_llm
)

result = self_rag.query("RAG系统如何优化？")
# result['retrieval_needed'] - 是否需要检索
# result['segments'] - 带来源标注的答案片段
```

### 1.5 最佳实践

1. **评估器选择**：
   - 对延迟敏感 → 使用 `eval_mode='vector'`
   - 对精度要求高 → 使用 `eval_mode='llm'`
   - 平衡方案 → 使用 `eval_mode='hybrid'`（推荐）

2. **阈值调优**：
   - 基于测试数据调优阈值
   - 不同领域可能需要不同阈值

3. **纠正策略**：
   - 设置合理的 `max_retries`，避免无限循环
   - 对于简单问题，可以关闭 `enable_retrieval_decision`

---

## 二、相关片段提取

### 2.1 技术概述

**核心思想**：从检索到的文档块中提取与问题最相关的句子/段落，减少噪声、节省Token。

**效果对比**：

```
传统方式：
检索到5个文档块（共3000字）→ 全部输入LLM → 生成答案

片段提取：
检索到5个文档块 → 提取相关片段（共800字）→ 输入LLM → 生成答案

收益：Token减少73%，噪声减少，答案质量提升
```

### 2.2 核心流程

```
┌─────────────────────────────────────────────────────┐
│  检索到的文档                                        │
│       ↓                                              │
│  【片段切分】句子级/滑动窗口/语义边界               │
│       ↓                                              │
│  【相关性评分】向量相似度 + LLM精评                 │
│       ↓                                              │
│  【筛选过滤】低于阈值的片段丢弃                     │
│       ↓                                              │
│  【指代消解】补全缺失的主语/宾语                    │
│       ↓                                              │
│  【片段重组】按相关性排序，保持语义连贯             │
│       ↓                                              │
│  输出相关片段                                        │
└─────────────────────────────────────────────────────┘
```

### 2.3 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `granularity` | str | 'sentence' | 切分粒度：sentence/sliding_window/semantic |
| `window_size` | int | 100 | 滑动窗口大小（字符） |
| `stride` | int | 50 | 滑动窗口步长 |
| `score_mode` | str | 'hybrid' | 评分模式：vector/llm/hybrid |
| `max_segments` | int | 10 | 最大返回片段数 |
| `min_relevance` | float | 0.4 | 最小相关性阈值 |
| `enable_resolution` | bool | True | 是否启用指代消解 |

### 2.4 使用示例

```python
from scripts.segment_extractor import RelevantSegmentExtractor

extractor = RelevantSegmentExtractor(
    llm_client=your_llm,
    embedding_model=your_embedding_model,
    config={
        'granularity': 'sentence',
        'score_mode': 'hybrid',
        'max_segments': 10,
        'min_relevance': 0.4
    }
)

# 提取相关片段
segments = extractor.extract(query, documents)

# 获取LLM输入上下文（自动控制长度）
context = extractor.get_context_for_llm(query, documents, max_length=2000)
```

### 2.5 最佳实践

1. **粒度选择**：
   - 精确问答场景 → `granularity='sentence'`
   - 需要上下文连贯 → `granularity='sliding_window'`
   - 学术论文/长文档 → `granularity='semantic'`

2. **评分模式**：
   - 快速场景 → `score_mode='vector'`
   - 高精度场景 → `score_mode='hybrid'`（推荐）

3. **片段数量**：
   - 简单问题：3-5个片段
   - 复杂问题：8-10个片段

---

## 三、命题分块

### 3.1 技术概述

**核心思想**：将文档拆解为最小的事实单元（命题），每个命题独立可检索。

**与传统分块对比**：

```
传统语义分块：
"RAG是一种技术。它能降低幻觉。成本低于微调。"
→ 整体作为一个块

命题分块：
→ "RAG是一种技术"
→ "RAG能降低幻觉"
→ "RAG成本低于微调"
→ 每个独立命题可精准匹配用户问题
```

### 3.2 核心流程

```
┌─────────────────────────────────────────────────────┐
│  原始文档                                            │
│       ↓                                              │
│  【段落切分】按空行/章节边界切分                    │
│       ↓                                              │
│  【命题提取】LLM识别独立事实/观点                   │
│       ↓                                              │
│  【指代消解】将代词替换为实际实体                   │
│       ↓                                              │
│  【验证过滤】检查原子性、自包含性                   │
│       ↓                                              │
│  【去重聚合】移除重复或高度相似的命题               │
│       ↓                                              │
│  命题列表（建立父子映射）                           │
└─────────────────────────────────────────────────────┘
```

### 3.3 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `min_proposition_length` | int | 15 | 命题最小长度（字符） |
| `max_proposition_length` | int | 150 | 命题最大长度（字符） |
| `mode` | str | 'strict' | 提取模式：strict/relaxed |
| `enable_resolution` | bool | True | 是否启用指代消解 |
| `enable_deduplication` | bool | True | 是否启用去重 |
| `similarity_threshold` | float | 0.9 | 去重相似度阈值 |

### 3.4 使用示例

```python
from scripts.proposition_chunker import PropositionChunker

chunker = PropositionChunker(
    llm_client=your_llm,
    config={
        'min_proposition_length': 15,
        'max_proposition_length': 150,
        'enable_resolution': True
    }
)

# 分块
propositions = chunker.chunk(document)

# 获取父段落
parent = chunker.get_parent_context(proposition_id)

# 转换为索引格式
indexable = chunker.to_indexable_format(propositions)
# 存入向量数据库
```

### 3.5 最佳实践

1. **与Small-to-Big结合**：
   - 命题作为子块，原段落作为父块
   - 检索到命题后返回完整段落

2. **适用场景**：
   - 精确问答（如FAQ系统）
   - 事实型检索
   - 知识库问答

3. **注意事项**：
   - 命题数量可能比传统分块多3-5倍
   - 需要更多存储空间
   - 检索时需要聚合去重

---

## 四、上下文头增强分块

### 4.1 技术概述

**核心思想**：为每个文档块添加元数据头部，补充全局背景信息，提升向量语义准确性。

**效果对比**：

```
传统分块：
"充电时间为2小时，支持快充。"

上下文头增强分块：
"【来源：产品手册-第3章-充电参数】【主题：充电时间, 快充】
充电时间为2小时，支持快充。"
```

### 4.2 头部内容设计

| 信息类型 | 说明 | 来源 |
|---------|------|------|
| 文档标题 | 文档名称 | 文档元数据 |
| 章节路径 | 文档层级结构 | 文档结构解析 |
| 主题标签 | 段落主题关键词 | LLM提取/规则提取 |
| 关键实体 | 涉及的人/事/物 | LLM提取/规则提取 |
| 时间戳 | 文档发布日期 | 文档元数据 |

### 4.3 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `header_format` | str | 'natural' | 头部格式：natural/json/tags |
| `max_header_length` | int | 100 | 头部最大长度（字符） |
| `enable_llm_extraction` | bool | True | 是否使用LLM提取语义信息 |
| `chunk_size` | int | 500 | 分块大小 |
| `overlap` | int | 50 | 分块重叠 |

### 4.4 使用示例

```python
from scripts.contextual_header import ContextualHeaderEnhancer

enhancer = ContextualHeaderEnhancer(
    llm_client=your_llm,
    config={
        'header_format': 'natural',
        'max_header_length': 100,
        'enable_llm_extraction': True
    }
)

# 增强单个块
enhanced = enhancer.enhance(chunk, document_metadata)

# 处理整个文档
enhanced_chunks = enhancer.enhance_document(document, metadata)

# 分层头部构建
from scripts.contextual_header import HierarchicalHeaderBuilder

builder = HierarchicalHeaderBuilder()
full_header = builder.build_full_header(
    document=document,
    chunk=chunk,
    document_metadata=metadata,
    section_info={'title': '充电参数', 'path': '第三章'},
    chunk_info={'topics': ['快充'], 'entities': ['Type-C']}
)
```

### 4.5 最佳实践

1. **头部格式选择**：
   - 向量化场景 → `header_format='natural'`（推荐）
   - 结构化检索 → `header_format='json'`
   - 标签检索 → `header_format='tags'`

2. **头部长度控制**：
   - 建议50-100字符
   - 太短信息不足，太长引入噪声

3. **与分块策略配合**：
   - 可与语义分块、命题分块组合使用
   - 优先提取文档结构信息作为头部

---

## 五、上下文压缩

### 5.1 技术概述

**核心思想**：对检索到的文档片段进行压缩，去除无关内容，保留核心信息，减少Token消耗并降低噪声干扰。

**三种压缩模式**：

| 模式 | 原理 | 优点 | 缺点 | 适用场景 |
|------|------|------|------|---------|
| 提取式 | 选取关键句子，原样输出 | 保真度高、速度快 | 可能丢失关联信息 | 事实型问答 |
| 摘要式 | LLM生成精炼摘要 | 信息密度高、连贯性好 | 可能引入幻觉 | 长文档理解 |
| 混合式 | 先提取再摘要 | 平衡保真与密度 | 计算开销较大 | 高质量要求场景 |

### 5.2 核心流程

```
┌─────────────────────────────────────────────────────┐
│  检索到的文档片段                                    │
│       ↓                                              │
│  【句子分割】按标点/段落边界分割                    │
│       ↓                                              │
│  【相关性评分】计算每个句子与查询的相关性           │
│       ↓                                              │
│  【关键句提取】选择高相关性句子                     │
│       ↓                                              │
│  【实体保护】识别并保护关键实体不被截断             │
│       ↓                                              │
│  【摘要压缩】（可选）对提取结果进一步精简           │
│       ↓                                              │
│  压缩后的上下文                                      │
└─────────────────────────────────────────────────────┘
```

### 5.3 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `mode` | str | 'extractive' | 压缩模式：extractive/abstractive/hybrid |
| `target_ratio` | float | 0.5 | 目标压缩比（压缩后长度/原长度） |
| `min_length` | int | 50 | 最小保留长度（字符） |
| `max_length` | int | 1000 | 最大输出长度（字符） |
| `protect_entities` | bool | True | 是否保护关键实体 |
| `sentence_selection` | str | 'relevance' | 句子选择策略：relevance/position/hybrid |
| `preserve_structure` | bool | False | 是否保留原文结构（段落/标题） |

### 5.4 使用示例

```python
from scripts.context_compression import ContextCompressor

# 初始化压缩器
compressor = ContextCompressor(
    llm_client=your_llm,
    embed_model=your_embed_model,
    config={
        'mode': 'hybrid',
        'target_ratio': 0.5,
        'protect_entities': True
    }
)

# 压缩上下文
result = compressor.compress(
    query="RAG系统如何优化？",
    contexts=retrieved_chunks,
    target_length=500
)

print(f"原始长度: {result['original_length']}")
print(f"压缩后长度: {result['compressed_length']}")
print(f"压缩比: {result['compression_ratio']:.2%}")
print(f"压缩内容: {result['compressed_text']}")
```

### 5.5 最佳实践

1. **模式选择**：
   - 对事实准确性要求高 → 提取式
   - 对连贯性要求高 → 摘要式
   - 综合要求 → 混合式（推荐）

2. **压缩比控制**：
   - 建议0.3-0.6，过低可能丢失关键信息
   - 根据查询复杂度动态调整

3. **实体保护**：
   - 启用后可避免关键实体（如人名、地名、数据）被截断
   - 对精确问答场景尤其重要

4. **与重排序配合**：
   - 先重排序筛选相关文档，再压缩
   - 避免压缩无关文档浪费计算资源

---

## 六、引用溯源

### 6.1 技术概述

**核心思想**：为生成的答案标注引用来源，提供可追溯性和可信度验证，帮助用户判断答案可靠性。

**四种引用格式**：

| 格式 | 示例 | 适用场景 |
|------|------|---------|
| 行内引用 | RAG是一种检索增强技术[1]。 | 学术论文、研究报告 |
| 脚注引用 | RAG是一种检索增强技术¹。 | 博客文章、文档 |
| 详细引用 | RAG是一种技术。（来源：文档A-第3段） | 客服系统、知识问答 |
| JSON引用 | `{"text": "...", "source_id": "doc1"}` | API调用、结构化输出 |

### 6.2 核心流程

```
┌─────────────────────────────────────────────────────┐
│  生成的答案 + 检索到的文档片段                       │
│       ↓                                              │
│  【答案分割】按句子/段落切分答案                    │
│       ↓                                              │
│  【来源匹配】为每个答案片段匹配最相关的文档         │
│       ↓                                              │
│  【相似度计算】计算答案与文档的语义相似度           │
│       ↓                                              │
│  【可信度评分】评估每个引用的可信度                 │
│       ↓                                              │
│  【格式化输出】按指定格式生成带引用的答案           │
│       ↓                                              │
│  带引用的答案                                        │
└─────────────────────────────────────────────────────┘
```

### 6.3 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `citation_format` | str | 'inline' | 引用格式：inline/footnote/detailed/json |
| `min_confidence` | float | 0.5 | 最小引用可信度阈值 |
| `max_citations_per_sentence` | int | 3 | 每句最多引用数 |
| `include_source_text` | bool | False | 是否包含来源文本片段 |
| `include_confidence_score` | bool | True | 是否包含可信度评分 |
| `sort_by_confidence` | bool | True | 是否按可信度排序引用 |

### 6.4 使用示例

```python
from scripts.citation_tracker import CitationTracker

# 初始化引用追踪器
tracker = CitationTracker(
    llm_client=your_llm,
    embed_model=your_embed_model,
    config={
        'citation_format': 'detailed',
        'min_confidence': 0.6,
        'include_confidence_score': True
    }
)

# 生成带引用的答案
result = tracker.add_citations(
    answer="RAG是一种检索增强生成技术。它通过检索相关文档来增强生成质量。",
    sources=[
        {"id": "doc1", "content": "RAG全称Retrieval-Augmented Generation...", "metadata": {...}},
        {"id": "doc2", "content": "检索增强技术能降低幻觉...", "metadata": {...}}
    ]
)

print(result['cited_answer'])
# 输出：RAG是一种检索增强生成技术。（来源：doc1-可信度0.92）

# 获取引用详情
for citation in result['citations']:
    print(f"来源ID: {citation['source_id']}")
    print(f"可信度: {citation['confidence']:.2f}")
    print(f"原文片段: {citation['source_text']}")
```

### 6.5 最佳实践

1. **格式选择**：
   - 学术/研究场景 → 行内引用
   - 用户友好的展示 → 详细引用
   - API/程序调用 → JSON引用

2. **可信度阈值**：
   - 建议0.5-0.7，过低可能引入不相关引用
   - 高风险场景（如医疗、法律）建议提高到0.7+

3. **来源展示**：
   - 启用 `include_source_text` 可让用户验证引用
   - 对于长文档，展示来源片段比完整文档更实用

4. **引用数量控制**：
   - 每句引用不宜过多，建议1-3个
   - 过多引用会降低答案可读性

---

## 七、查询意图识别

### 7.1 技术概述

**核心思想**：分析用户查询的意图类型和复杂度，动态调整检索策略和生成方式，提升响应质量。

**七种意图类型**：

| 意图类型 | 特征 | 示例查询 | 推荐策略 |
|---------|------|---------|---------|
| 事实查询 | 寻找具体事实 | "RAG是什么？" | 精确检索+命题分块 |
| 对比分析 | 比较多个对象 | "RAG和微调的区别？" | 多对象检索+对比提示 |
| 操作指导 | 需要步骤说明 | "如何部署RAG系统？" | 流程检索+步骤生成 |
| 概念解释 | 需要详细阐述 | "RAG的工作原理是什么？" | 深度检索+详细回答 |
| 开放讨论 | 无固定答案 | "RAG的未来发展趋势？" | 广泛检索+观点整合 |
| 问题诊断 | 需要分析原因 | "为什么RAG召回率低？" | 诊断检索+原因分析 |
| 闲聊问候 | 非信息需求 | "你好"、"谢谢" | 无需检索 |

**三级复杂度**：
- 简单：单一问题、单一答案
- 中等：多角度问题、需要整合信息
- 复杂：多跳推理、需要综合分析

### 7.2 核心流程

```
┌─────────────────────────────────────────────────────┐
│  用户查询                                            │
│       ↓                                              │
│  【预处理】去除噪声、标准化表达                     │
│       ↓                                              │
│  【意图分类】LLM识别意图类型                        │
│       ↓                                              │
│  【复杂度评估】判断问题复杂程度                     │
│       ↓                                              │
│  【查询改写】根据意图优化查询表达                   │
│       ↓                                              │
│  【策略选择】选择匹配的检索策略                     │
│       ↓                                              │
│  意图分析结果 + 优化后的查询                        │
└─────────────────────────────────────────────────────┘
```

### 7.3 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enable_complexity` | bool | True | 是否评估复杂度 |
| `enable_query_rewrite` | bool | True | 是否改写查询 |
| `enable_colloquial_fix` | bool | True | 是否标准化口语表达 |
| `intent_types` | list | 七种标准类型 | 自定义意图类型列表 |
| `complexity_levels` | int | 3 | 复杂度级别数 |
| `rewrite_rules` | dict | {} | 自定义改写规则 |

### 7.4 使用示例

```python
from scripts.query_intent import QueryIntentAnalyzer

# 初始化意图分析器
analyzer = QueryIntentAnalyzer(
    llm_client=your_llm,
    config={
        'enable_complexity': True,
        'enable_query_rewrite': True,
        'enable_colloquial_fix': True
    }
)

# 分析查询
result = analyzer.analyze("RAG和微调有什么区别，哪个更适合企业？")

print(f"意图类型: {result['intent_type']}")  # 对比分析
print(f"复杂度: {result['complexity']}")      # 中等
print(f"改写查询: {result['rewritten_query']}")  # "RAG与微调的对比分析..."
print(f"推荐策略: {result['recommended_strategy']}")  # 多对象检索+对比

# 获取检索参数建议
params = analyzer.get_retrieval_params(result)
print(f"建议检索数量: {params['top_k']}")
print(f"建议检索模式: {params['retrieval_mode']}")
```

### 7.5 最佳实践

1. **意图分类应用**：
   - 事实查询 → 命题分块+精确匹配
   - 对比分析 → 检索多个对象+对比提示词
   - 操作指导 → 流程文档+步骤化输出

2. **复杂度自适应**：
   - 简单问题：top_k=3，快速响应
   - 中等问题：top_k=5，标准处理
   - 复杂问题：top_k=10，多跳检索

3. **查询改写**：
   - 口语化表达（"咋回事"→"怎么回事"）
   - 模糊查询补充上下文
   - 多意图拆分（"A和B的区别以及C的用法"）

4. **与检索优化配合**：
   - 意图识别结果可用于路由到不同的检索器
   - 复杂度高的问题启用多跳检索

---

## 八、多跳检索

### 8.1 技术概述

**核心思想**：对于需要综合多个信息源的复杂问题，通过迭代检索逐步收集信息，直到获得完整答案。

**适用场景**：
- "A公司的CEO在哪所大学毕业？"（需要先查A公司CEO是谁，再查其毕业院校）
- "RAG技术在医疗领域的应用案例有哪些挑战？"（需要查应用案例+挑战分析）
- "Python 3.11相比3.10有哪些新特性影响异步编程？"（需要查新特性+异步相关特性）

### 8.2 核心流程

```
┌─────────────────────────────────────────────────────┐
│  原始查询                                            │
│       ↓                                              │
│  【查询分解】将复杂问题拆解为子问题                 │
│       ↓                                              │
│  【第1跳检索】检索第一个子问题的答案                │
│       ↓                                              │
│  【信息整合】将检索结果加入上下文                   │
│       ↓                                              │
│  【生成下一跳查询】基于已知信息生成新的查询        │
│       ↓                                              │
│  【第2跳检索】检索新的查询                          │
│       ↓                                              │
│  【循环迭代】直到信息完整或达到最大跳数            │
│       ↓                                              │
│  【答案合成】整合所有检索结果生成最终答案          │
└─────────────────────────────────────────────────────┘
```

### 8.3 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `max_hops` | int | 3 | 最大检索跳数 |
| `docs_per_hop` | int | 3 | 每跳检索文档数 |
| `enable_decomposition` | bool | True | 是否启用查询分解 |
| `enable_early_stop` | bool | True | 是否启用早停机制 |
| `stop_threshold` | float | 0.85 | 早停阈值（信息完整度） |
| `merge_strategy` | str | 'cumulative' | 结果合并策略：cumulative/weighted |
| `show_reasoning` | bool | False | 是否展示推理过程 |

### 8.4 使用示例

```python
from scripts.multi_hop_retriever import MultiHopRetriever

# 初始化多跳检索器
retriever = MultiHopRetriever(
    base_retriever=your_retriever,
    llm_client=your_llm,
    config={
        'max_hops': 3,
        'docs_per_hop': 3,
        'enable_early_stop': True
    }
)

# 执行多跳检索
result = retriever.retrieve(
    query="A公司的CEO在哪所大学毕业？"
)

print(f"总跳数: {result['total_hops']}")
print(f"检索到的文档: {len(result['documents'])}")
print(f"最终答案: {result['answer']}")

# 查看检索链路
for hop in result['hop_details']:
    print(f"第{hop['hop_num']}跳查询: {hop['query']}")
    print(f"检索文档: {[doc['id'] for doc in hop['docs']]}")
```

### 8.5 最佳实践

1. **跳数控制**：
   - 建议2-4跳，过多跳数会显著增加延迟
   - 启用早停机制避免不必要的检索

2. **查询分解策略**：
   - 明确依赖关系的问题优先分解
   - 独立子问题可并行检索

3. **结果合并**：
   - 简单场景使用累加合并（`cumulative`）
   - 对质量要求高使用加权合并（`weighted`）

4. **与意图识别配合**：
   - 意图识别判断复杂度为"复杂"时启用多跳检索
   - 简单问题直接单跳检索避免过度处理

---

## 九、文档预处理

### 9.1 技术概述

**核心思想**：对不同格式的源文档进行标准化预处理，提取结构化内容，为后续分块和索引提供高质量输入。

**支持的文档格式**：

| 格式 | 处理工具 | 特殊处理 |
|------|---------|---------|
| PDF | pdfplumber | 表格识别、版面分析 |
| Word | python-docx | 样式提取、目录解析 |
| Excel | openpyxl | 多Sheet处理、公式提取 |
| HTML | BeautifulSoup | 标签清理、正文提取 |
| Markdown | 正则解析 | 标题层级、代码块识别 |
| 图片 | pytesseract | OCR识别、图片描述 |

### 9.2 核心流程

```
┌─────────────────────────────────────────────────────┐
│  输入文档（PDF/Word/Excel/HTML/Markdown/图片）      │
│       ↓                                              │
│  【格式识别】识别文件类型                           │
│       ↓                                              │
│  【内容提取】根据格式选择对应提取器                 │
│       ↓                                              │
│  【结构解析】提取标题、段落、表格、列表等           │
│       ↓                                              │
│  【噪声清理】移除页眉页脚、广告、无关内容           │
│       ↓                                              │
│  【元数据提取】提取作者、日期、标题等元数据         │
│       ↓                                              │
│  【质量校验】检查提取完整性                         │
│       ↓                                              │
│  标准化输出（JSON格式）                             │
└─────────────────────────────────────────────────────┘
```

### 9.3 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `extract_tables` | bool | True | 是否提取表格 |
| `extract_images` | bool | False | 是否提取并处理图片 |
| `clean_noise` | bool | True | 是否清理噪声内容 |
| `preserve_structure` | bool | True | 是否保留文档结构 |
| `ocr_language` | str | 'chi_sim+eng' | OCR语言（中文+英文） |
| `output_format` | str | 'json' | 输出格式：json/markdown/text |
| `max_file_size` | int | 50 | 最大文件大小（MB） |

### 9.4 使用示例

```python
from scripts.document_preprocessor import DocumentPreprocessor

# 初始化预处理器
preprocessor = DocumentPreprocessor(
    config={
        'extract_tables': True,
        'clean_noise': True,
        'preserve_structure': True,
        'output_format': 'json'
    }
)

# 处理单个文档
result = preprocessor.process('document.pdf')

print(f"提取文本长度: {len(result['text'])}")
print(f"表格数量: {len(result.get('tables', []))}")
print(f"元数据: {result['metadata']}")

# 批量处理
results = preprocessor.batch_process(
    file_paths=['doc1.pdf', 'doc2.docx', 'doc3.html'],
    output_dir='./processed/'
)

# 获取结构化内容
for section in result['sections']:
    print(f"标题: {section['title']}")
    print(f"层级: {section['level']}")
    print(f"内容: {section['content'][:100]}...")
```

### 9.5 最佳实践

1. **格式选择**：
   - 有文档源文件优先使用源格式（Word > PDF）
   - PDF使用 `pdfplumber` 而非 `PyPDF2`，表格提取更准确

2. **结构保留**：
   - 启用 `preserve_structure` 保留标题层级
   - 为后续分块提供结构信息

3. **噪声清理**：
   - 页眉页脚、页码等对RAG无用的内容应清理
   - HTML文档重点清理广告、导航栏

4. **表格处理**：
   - 表格建议转为Markdown格式或结构化JSON
   - 纯文本会丢失表格语义

5. **图片处理**：
   - 需要OCR时启用 `extract_images`
   - 考虑使用多模态模型直接理解图片内容

---

## 十、技术选型决策矩阵

| 问题场景 | 推荐技术 | 组合建议 |
|---------|---------|---------|
| 检索结果质量不稳定 | Self-RAG/CRAG | + 重排序 |
| 上下文噪声多、Token浪费 | 相关片段提取 | + 上下文压缩 |
| 需要精确匹配事实 | 命题分块 | + 由小到大检索 |
| 检索召回率低 | 上下文头增强 | + 混合检索 |
| 复杂问题多步推理 | 多跳检索 | + Self-RAG |
| 长文档处理 | 上下文头增强 | + 分层索引 |
| 答案可信度要求高 | 引用溯源 | + 上下文压缩 |
| 查询表达模糊 | 查询意图识别 | + 查询改写 |
| 多格式文档处理 | 文档预处理 | + 结构化分块 |

---

## 十一、性能对比

| 技术 | 实现复杂度 | LLM依赖 | 效果提升 | 延迟影响 |
|------|-----------|---------|---------|---------|
| Self-RAG | 中高 | 高 | ⭐⭐⭐⭐⭐ | +20-50% |
| 相关片段提取 | 中 | 中 | ⭐⭐⭐⭐ | +10-20% |
| 命题分块 | 高 | 高 | ⭐⭐⭐⭐ | 索引时开销 |
| 上下文头增强 | 低 | 中 | ⭐⭐⭐ | 索引时开销 |
| 上下文压缩 | 中 | 中 | ⭐⭐⭐⭐ | +5-15% |
| 引用溯源 | 低 | 低 | ⭐⭐⭐ | +5-10% |
| 查询意图识别 | 低 | 低 | ⭐⭐⭐⭐ | +5% |
| 多跳检索 | 中高 | 高 | ⭐⭐⭐⭐⭐ | +50-200% |
| 文档预处理 | 中 | 低 | ⭐⭐⭐ | 索引时开销 |

---

## 十二、常见问题

### Q1: Self-RAG会增加多少延迟？
A: 取决于评估模式。使用 `eval_mode='vector'` 延迟增加约10%，使用 `eval_mode='llm'` 延迟增加约30-50%。推荐使用 `hybrid` 模式平衡精度和速度。

### Q2: 命题分块适合什么场景？
A: 适合需要精确匹配事实的场景，如FAQ问答、知识库检索。不适合需要完整上下文的场景，如小说阅读、文档摘要。

### Q3: 上下文头会干扰向量检索吗？
A: 如果头部过长或包含无关信息，可能会干扰。建议控制头部长度在100字符以内，只保留关键信息。

### Q4: 九种技术可以组合使用吗？
A: 可以。推荐组合：
- 上下文头增强 + 命题分块（分块阶段）
- 相关片段提取 + 上下文压缩（后处理阶段）
- Self-RAG + 引用溯源（生成控制阶段）
- 查询意图识别 + 多跳检索（查询优化阶段）

### Q5: 多跳检索什么时候启用？
A: 当查询意图识别判断问题复杂度为"复杂"，或问题明确需要多步推理时启用。简单问题不建议使用，会增加延迟。

### Q6: 上下文压缩会损失信息吗？
A: 提取式压缩保真度高但可能丢失关联信息，摘要式压缩连贯性好但可能引入幻觉。对准确性要求高的场景建议使用提取式或混合式，并启用实体保护。

### Q7: 如何选择引用格式？
A: 根据应用场景选择：
- 学术/研究 → 行内引用
- 用户展示 → 详细引用
- API调用 → JSON引用
- 文档/博客 → 脚注引用

### Q8: 文档预处理需要注意什么？
A: 重点注意：
1. PDF优先使用 `pdfplumber` 而非 `PyPDF2`，表格提取更准确
2. 表格建议转为Markdown或JSON格式保留语义
3. 启用噪声清理移除页眉页脚、广告等无关内容
4. 保留文档结构信息为后续分块提供支持
