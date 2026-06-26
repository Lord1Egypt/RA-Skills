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

本技能使用Anthropic API进行LLM调用，需要配置API密钥：

```python
import os
os.environ["ANTHROPIC_API_KEY"] = "your-api-key"
```

或在脚本初始化时传入：

```python
client = anthropic.Anthropic(api_key="your-api-key")
```

---

## 二、依赖管理

### 2.1 核心依赖

| 依赖包 | 版本要求 | 用途 |
|--------|---------|------|
| anthropic | >=0.18.0 | LLM调用（Self-RAG、查询转换等） |
| sentence-transformers | >=2.2.0 | 向量嵌入、重排序模型 |
| rank-bm25 | >=0.2.2 | BM25关键词检索 |
| networkx | >=3.0 | 图结构处理（Graph RAG） |

### 2.2 安装命令

```bash
pip install anthropic>=0.18.0
pip install sentence-transformers>=2.2.0
pip install rank-bm25>=0.2.2
pip install networkx>=3.0
```

### 2.3 版本兼容性

- Python 3.8-3.11：完全支持
- Python 3.12：核心功能支持，部分可选依赖可能需要从源码安装
- Python < 3.8：不支持

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

### 3.2 配置加载示例

```python
import json

def load_config(config_path: str = "config.json") -> dict:
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

config = load_config("assets/config-template.json")
```

### 3.3 预设配置

配置模板提供两种预设：

| 预设名称 | 适用场景 | 特点 |
|---------|---------|------|
| `complex_reasoning` | 复杂推理场景 | 多跳检索、Self-RAG、深度分块 |
| `customer_service` | 客服问答场景 | 快速响应、引用溯源、意图识别 |

使用预设：

```python
# 加载预设配置
preset = config["presets"]["complex_reasoning"]
```

---

## 四、脚本调用约定

### 4.1 统一初始化模式

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
| evaluate.py | RAGEvaluator | 系统评估 | queries, documents, answers |
| self_rag.py | CorrectiveRAG / SelfRAG | 自我纠错 | retriever, generator, llm_client |
| segment_extractor.py | RelevantSegmentExtractor | 片段提取 | query, documents |
| proposition_chunker.py | PropositionChunker | 命题分块 | document |
| contextual_header.py | ContextualHeaderEnhancer | 头部增强 | chunk, metadata |
| context_compression.py | ContextCompressor | 上下文压缩 | query, contexts |
| citation_tracker.py | CitationTracker | 引用溯源 | answer, sources |
| query_intent.py | QueryIntentAnalyzer | 意图识别 | query |
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

### 5.2 检索参数

| 参数 | 默认值 | 调优建议 |
|------|--------|---------|
| top_k | 5 | 简单问题3-5，复杂问题8-10 |
| alpha（混合检索权重） | 0.7 | 关键词多时降至0.5 |
| docs_per_hop（多跳） | 3 | 复杂问题可提高到5 |

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
