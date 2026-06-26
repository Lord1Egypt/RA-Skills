---
name: rag-optimization
description: 当需要RAG检索内容时触发；完整的RAG系统优化方案，涵盖21+种策略（含Self-RAG、命题分块、片段提取、上下文压缩、引用溯源、查询意图、多跳检索、文档预处理）；提供诊断工具、实现代码、配置模板与评估框架；帮助构建高准确率生产级RAG应用；当用户需要优化知识库问答、提升检索准确率、评估RAG系统效果、解决检索噪音或降低幻觉问题时使用
author: kiwifruit
dependency:
  python:
    - anthropic>=0.18.0
    - sentence-transformers>=2.2.0
    - rank-bm25>=0.2.2
    - networkx>=3.0
---

# RAG检索优化技能

## 技能概述

本技能提供完整的RAG系统优化方案，涵盖21+种优化策略，帮助构建高准确率、生产级的RAG应用。

**核心价值**：
- 准确率可从 0.3 提升至 0.85+
- 提供可落地的实施代码与配置模板
- 包含完整的评估框架

**适用场景**：构建知识库问答、优化检索准确率、解决检索噪音、降低幻觉问题

**环境准备与配置**：详见 [全局操作说明](references/global-operations.md)

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

```
RAG优化策略
├── 检索前优化
│   ├── 语义分块 - 基于语义相似度动态分块
│   ├── 命题分块 - 拆解为最小事实单元
│   ├── 上下文头增强 - 添加元数据头部
│   ├── 由小到大检索 - 小块检索、大块返回
│   ├── 文档预处理 - 多格式标准化处理
│   └── 查询转换 - 扩展/分解/HyDE
│
├── 检索中优化
│   ├── 混合检索 - 向量 + BM25
│   ├── HyDE - 假设文档嵌入
│   ├── 多跳检索 - 迭代收集信息
│   ├── 查询意图识别 - 动态策略调整
│   └── 自适应检索 - 根据查询特征调整
│
├── 检索后优化
│   ├── 重排序 - 两阶段检索精排
│   ├── 相关片段提取 - 提取核心内容
│   ├── 上下文压缩 - 减少Token消耗
│   ├── 引用溯源 - 标注答案来源
│   └── 幻觉检测 - 验证答案可靠性
│
├── 生成控制
│   ├── Self-RAG/CRAG - 自我纠错与质量评估
│   └── 反馈循环 - 持续优化
│
└── 架构级优化
    ├── 分层索引 - 多级索引结构
    ├── Graph RAG - 图结构知识
    └── 分层路由 - 智能路由分发
```

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

### 策略1：语义分块

**问题**：固定大小分块会切断语义完整性

**方案**：基于语义相似度动态分块，相似度低于阈值时切分

**效果**：准确率 0.30 → 0.85，性价比最高

**详细实现**：见 [高级技术指南](references/advanced-techniques.md)

---

### 策略2：由小到大检索

**问题**：小块检索精准但上下文不足，大块完整但检索不准

**方案**：检索小块（100-200字），返回大块（500-1000字）

**三步流程**：
1. 文档切分为子块 + 父块
2. 用子块向量检索
3. 返回对应的父块

**参数建议**：技术文档(150/600字)、学术论文(200/800字)、法律条文(100/500字)

**详细实现**：见 [高级技术指南](references/advanced-techniques.md)

---

### 策略3：查询转换

**问题**：用户查询表述不清、过于复杂

**方案**：用LLM转换查询形式

**三种模式**：
- 查询扩展：生成多个语义变体（适用于查询词少）
- 查询分解：拆解复杂问题（适用于多条件查询）
- HyDE：生成假设答案用于检索（适用于短查询）

**详细实现**：见 [高级技术指南](references/advanced-techniques.md)

---

### 策略4：重排序（Reranking）

**问题**：向量检索的初步排序不够精准

**方案**：两阶段检索 - 粗筛(top 50) + 精排(top 5)

**流程**：查询 → 向量检索 → 重排序模型 → 最终结果

**模型推荐**：
- 英文：ms-marco-MiniLM-L-6-v2（快速）或 L-12-v2（高精度）
- 中文：BAAI/bge-reranker-large

**效果**：准确率 0.50 → 0.70

---

### 策略5：混合检索

**问题**：纯向量检索无法精准匹配关键词

**方案**：向量检索 + BM25关键词检索

**融合公式**：`final_score = α × vector_score + (1-α) × bm25_score`

**自适应权重**：短查询/专有名词 → α=0.5，长查询 → α=0.7

**效果**：准确率 0.50 → 0.83

---

### 策略6：Self-RAG / Corrective RAG

**问题**：检索结果质量差时仍会生成错误答案

**方案**：在检索和生成环节增加质量评估，自动纠正错误

**两种模式**：
- Corrective RAG：检索后评估 + 纠正动作
- Self-RAG：全流程自检 + 来源标注

**脚本调用**：`scripts/self_rag.py`，支持 `CorrectiveRAG` 和 `SelfRAG` 两种模式

**配置参数**：`max_retries`、`high_relevance_threshold`、`eval_mode` 等

**效果**：幻觉率降低 30-50%

**详细实现**：见 [高级技术指南](references/advanced-techniques.md#一self-rag--corrective-rag)

---

### 策略7：相关片段提取

**问题**：检索到的文档块包含大量无关内容

**方案**：从文档块中提取与问题最相关的句子/段落

**三种粒度**：句子级（精确问答）、滑动窗口（通用）、语义边界（学术论文）

**脚本调用**：`scripts/segment_extractor.py`

**效果**：Token减少 60-80%

**详细实现**：见 [高级技术指南](references/advanced-techniques.md#二相关片段提取)

---

### 策略8：命题分块

**问题**：传统分块粒度粗，无法精准匹配具体事实

**方案**：将文档拆解为最小的事实单元（命题），每个命题独立可检索

**示例**：
- 传统分块：`"RAG是一种技术。它能降低幻觉。"`
- 命题分块：`"RAG是一种技术"` + `"RAG能降低幻觉"`

**脚本调用**：`scripts/proposition_chunker.py`

**最佳实践**：与Small-to-Big结合，命题作为子块，原段落作为父块

**详细实现**：见 [高级技术指南](references/advanced-techniques.md#三命题分块)

---

### 策略9：上下文头增强分块

**问题**：文档块脱离上下文后语义不完整

**方案**：为每个文档块添加元数据头部，补充全局背景信息

**头部内容**：文档标题、章节路径、主题标签、关键实体

**效果**：召回率提升 10-20%

**脚本调用**：`scripts/contextual_header.py`

**详细实现**：见 [高级技术指南](references/advanced-techniques.md#四上下文头增强分块)

---

### 策略10：上下文压缩

**问题**：检索到的上下文包含大量无关内容，浪费Token

**方案**：对检索结果压缩，保留核心信息

**三种模式**：
- 提取式：选取关键句子（保真度高）
- 摘要式：LLM生成精炼摘要（信息密度高）
- 混合式：先提取再摘要（平衡方案）

**脚本调用**：`scripts/context_compression.py`

**效果**：Token减少 50-70%

**详细实现**：见 [高级技术指南](references/advanced-techniques.md#五上下文压缩)

---

### 策略11：引用溯源

**问题**：答案来源不明确，无法判断可信度

**方案**：为答案标注引用来源，提供可信度评分

**四种格式**：行内引用[1]、脚注引用¹、详细引用（来源+可信度）、JSON引用

**脚本调用**：`scripts/citation_tracker.py`

**效果**：答案可信度显著提升

**详细实现**：见 [高级技术指南](references/advanced-techniques.md#六引用溯源)

---

### 策略12：查询意图识别

**问题**：用户查询表达模糊，检索策略一刀切

**方案**：识别查询意图类型，动态调整检索策略

**七种意图**：事实查询、对比分析、操作指导、概念解释、开放讨论、问题诊断、闲聊问候

**脚本调用**：`scripts/query_intent.py`

**效果**：答案质量提升 15-25%

**详细实现**：见 [高级技术指南](references/advanced-techniques.md#七查询意图识别)

---

### 策略13：多跳检索

**问题**：复杂问题需要综合多个信息源

**方案**：迭代检索，逐步收集信息直到答案完整

**适用场景**：`"A公司的CEO在哪所大学毕业？"`（先查CEO，再查毕业院校）

**脚本调用**：`scripts/multi_hop_retriever.py`

**效果**：复杂问题完整度提高 40%+

**详细实现**：见 [高级技术指南](references/advanced-techniques.md#八多跳检索)

---

### 策略14：文档预处理

**问题**：多格式文档直接向量化效果差

**方案**：标准化预处理，提取结构化内容

**支持格式**：PDF、Word、Excel、HTML、Markdown、图片（OCR）

**脚本调用**：`scripts/document_preprocessor.py`

**详细实现**：见 [高级技术指南](references/advanced-techniques.md#九文档预处理)

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

使用 [assets/config-template.json](assets/config-template.json) 配置参数，参考 [全局操作说明](references/global-operations.md) 了解参数调优建议

### 步骤4：验证效果

使用评估脚本验证优化效果，对比基准指标，持续迭代

---

## 六、资源索引

### 核心脚本
| 脚本 | 用途 |
|------|------|
| [evaluate.py](scripts/evaluate.py) | RAG系统评估 |
| [self_rag.py](scripts/self_rag.py) | Self-RAG/CRAG实现 |
| [segment_extractor.py](scripts/segment_extractor.py) | 相关片段提取 |
| [proposition_chunker.py](scripts/proposition_chunker.py) | 命题分块 |
| [contextual_header.py](scripts/contextual_header.py) | 上下文头增强 |
| [context_compression.py](scripts/context_compression.py) | 上下文压缩 |
| [citation_tracker.py](scripts/citation_tracker.py) | 引用溯源 |
| [query_intent.py](scripts/query_intent.py) | 查询意图识别 |
| [multi_hop_retriever.py](scripts/multi_hop_retriever.py) | 多跳检索 |
| [document_preprocessor.py](scripts/document_preprocessor.py) | 文档预处理 |

### 参考文档
| 文档 | 说明 |
|------|------|
| [global-operations.md](references/global-operations.md) | 全局操作说明（环境准备、配置规范、参数调优） |
| [quickstart.md](references/quickstart.md) | 5分钟快速上手 |
| [advanced-techniques.md](references/advanced-techniques.md) | 9项核心技术详细实现 |
| [implementation-guide.md](references/implementation-guide.md) | 全链路落地实践 |

### 配置与数据
| 资源 | 说明 |
|------|------|
| [config-template.json](assets/config-template.json) | 完整配置模板（含预设） |
| [test-cases-example.json](assets/test-cases-example.json) | 测试用例示例 |

---

## 注意事项

- **环境准备**：参考 [全局操作说明](references/global-operations.md) 完成依赖安装和配置
- **参数调优**：根据文档类型和查询特征调整参数，详见 [参数调优指南](references/global-operations.md#五参数调优指南)
- **策略组合**：避免过度优化，根据问题诊断选择必要策略
- **评估迭代**：优化前建立基准指标，定期评估效果

---

## 版本信息

- **版本**: 2.0.0
- **更新日期**: 2024-12
- **本次更新**: 新增5项核心技术，策略总数21+，覆盖率80%+
