# scripts 类名速查表（自动生成）

> **本文档由 `scripts/generate-api-docs.py` 自动生成**，以代码为唯一真相源。
> 列出全部可导入类、枚举与函数及其真实所在模块。

## 导出符号总表

| 符号 | 类型 | 真实模块 | 职责/说明 |
|------|------|----------|-----------|
| `generate_corpus` | 函数 | `scripts.benchmark_retrieval` | 生成合成语料 |
| `main` | 函数 | `scripts.benchmark_retrieval` | - |
| `RetrievalResult` | 类 | `scripts.bm25_retriever` | 检索结果（兼容 RetrievalHit 接口，增加 content 属性） |
| `BM25Retriever` | 类 | `scripts.bm25_retriever` | Okapi BM25 检索器，支持 bm25 / vector / hybrid 三种策略。 |
| `Chunk` | 类 | `scripts.chunker_factory` | 统一分块数据结构 |
| `get_chunker` | 函数 | `scripts.chunker_factory` | 按策略名返回 chunker 函数。 |
| `chunk_document` | 函数 | `scripts.chunker_factory` | 便捷入口：切分单篇文档 |
| `CitationFormat` | 枚举 | `scripts.citation_tracker` | 引用格式 |
| `Source` | 类 | `scripts.citation_tracker` | 来源文档 |
| `Citation` | 类 | `scripts.citation_tracker` | 引用信息 |
| `CitedSegment` | 类 | `scripts.citation_tracker` | 带引用的答案片段 |
| `CredibilityScore` | 类 | `scripts.citation_tracker` | 可信度评分 |
| `CitationMatcher` | 类 | `scripts.citation_tracker` | 引用匹配器 - 将答案片段与源文档匹配 |
| `CitationFormatter` | 类 | `scripts.citation_tracker` | 引用格式化器 - 生成各种格式的引用 |
| `CredibilityScorer` | 类 | `scripts.citation_tracker` | 可信度评分器 |
| `CitationTracker` | 类 | `scripts.citation_tracker` | 引用溯源器 - 主入口类 |
| `ConfigError` | 类 | `scripts.config_loader` | 配置严重错误（strict 模式下抛出） |
| `load_config` | 函数 | `scripts.config_loader` | 加载配置文件并做入口校验。 |
| `strip_meta` | 函数 | `scripts.config_loader` | 去掉配置块里的描述性键（comment / _status），只保留真正的参数。 |
| `build_pipeline` | 函数 | `scripts.config_loader` | 按配置装配 RAG 组件。 |
| `DEFAULT_CONFIG_PATH` | 常量 | `unknown` | str(object='') -> str |
| `ValidationError` | 类 | `scripts.config_validator` | 配置错误 |
| `validate_config` | 函数 | `scripts.config_validator` | 校验配置字典，返回所有错误列表。 |
| `format_errors` | 函数 | `scripts.config_validator` | 格式化错误报告 |
| `CompressionMode` | 枚举 | `scripts.context_compression` | 压缩模式 |
| `CompressionResult` | 类 | `scripts.context_compression` | 压缩结果 |
| `Entity` | 类 | `scripts.context_compression` | 实体数据结构 |
| `EntityProtector` | 类 | `scripts.context_compression` | 实体保护器 - 确保关键信息不被压缩丢失 |
| `SentenceExtractor` | 类 | `scripts.context_compression` | 句子提取器 - 用于提取式压缩 |
| `AbstractiveCompressor` | 类 | `scripts.context_compression` | 摘要式压缩器 - 使用LLM生成精简摘要 |
| `ContextCompressor` | 类 | `scripts.context_compression` | 上下文压缩器 - 主入口类 |
| `ChunkHeader` | 类 | `scripts.contextual_header` | 上下文头结构 |
| `HeaderGenerator` | 类 | `scripts.contextual_header` | 上下文头生成器 |
| `ContextualHeaderEnhancer` | 类 | `scripts.contextual_header` | 上下文头增强器 |
| `HierarchicalHeaderBuilder` | 类 | `scripts.contextual_header` | 分层头部构建器 |
| `DocumentFormat` | 枚举 | `scripts.document_preprocessor` | 文档格式 |
| `DocumentSection` | 类 | `scripts.document_preprocessor` | 文档章节 |
| `StructuredTable` | 类 | `scripts.document_preprocessor` | 结构化表格 |
| `DocumentImage` | 类 | `scripts.document_preprocessor` | 文档图片 |
| `DocumentMetadata` | 类 | `scripts.document_preprocessor` | 文档元数据 |
| `ProcessedDocument` | 类 | `scripts.document_preprocessor` | 处理后的文档 |
| `FormatDetector` | 类 | `scripts.document_preprocessor` | 格式检测器 |
| `DataCleaner` | 类 | `scripts.document_preprocessor` | 数据清洗器 |
| `TextExtractor` | 类 | `scripts.document_preprocessor` | 文本提取器 |
| `SectionParser` | 类 | `scripts.document_preprocessor` | 章节解析器 |
| `DocumentPreprocessor` | 类 | `scripts.document_preprocessor` | 文档预处理器 - 主入口类 |
| `DocumentUnit` | 类 | `scripts.document_unit` | 统一文档单元：所有 RAG 处理流程中产生的文本块的基础数据结构。 |
| `UnitConverter` | 类 | `scripts.document_unit` | 各类数据结构与 DocumentUnit 之间的转换工具。 |
| `TestCase` | 类 | `scripts.evaluate` | 测试用例 |
| `EvaluationResult` | 类 | `scripts.evaluate` | 评估结果 |
| `RAGEvaluator` | 类 | `scripts.evaluate` | RAG系统评估器 |
| `load_test_cases` | 函数 | `scripts.evaluate` | 加载测试用例 |
| `save_report` | 函数 | `scripts.evaluate` | 保存评估报告 |
| `print_summary` | 函数 | `scripts.evaluate` | 打印摘要 |
| `print_comparison` | 函数 | `scripts.evaluate` | 打印新旧评估报告的指标对比（Ablation 前后 diff） |
| `load_rag_system` | 函数 | `scripts.evaluate` | H3：按 `--rag-class` 加载真实 RAG 系统；未指定时**显式**回退到 MockRAG。 |
| `main` | 函数 | `scripts.evaluate` | - |
| `main` | 函数 | `scripts.generate-api-docs` | - |
| `Entity` | 类 | `scripts.graph_rag` | 知识图谱实体 |
| `Relation` | 类 | `scripts.graph_rag` | 知识图谱关系 |
| `GraphQueryResult` | 类 | `scripts.graph_rag` | 图检索结果 |
| `EntityExtractor` | 类 | `scripts.graph_rag` | 实体提取器：从文本中提取实体。 |
| `RelationExtractor` | 类 | `scripts.graph_rag` | 关系提取器：从文本中识别实体之间的关系。 |
| `KnowledgeGraph` | 类 | `scripts.graph_rag` | 知识图谱：存储实体和关系，支持遍历查询 |
| `GraphRAG` | 类 | `scripts.graph_rag` | 图检索增强生成（Graph RAG） |
| `load_dotenv_if_available` | 函数 | `scripts.llm_client` | 尝试加载 .env 文件；python-dotenv 未安装时静默跳过。 |
| `LLMClient` | 类 | `scripts.llm_client` | 统一 LLM 客户端基类。 |
| `OpenAILikeClient` | 类 | `scripts.llm_client` | 兼容 OpenAI 协议的 LLM 客户端。 |
| `resolve_embedding_dim` | 函数 | `scripts.llm_client` | 按模型名解析向量维度（全项目唯一入口）。未知模型回退到默认值。 |
| `EmbeddingResult` | 类 | `scripts.llm_client` | encode() 的返回协议（H9）。 |
| `EmbeddingClient` | 类 | `scripts.llm_client` | 向量嵌入客户端。 |
| `NvidiaEmbeddingClient` | 类 | `scripts.llm_client` | 通过 NVIDIA API 调用向量嵌入模型。 |
| `wrap_llm` | 函数 | `scripts.llm_client` | 把外部传入的 LLM 对象统一成 LLMClient 接口。 |
| `load_from_env` | 函数 | `scripts.llm_client` | 从环境变量自动加载 LLM 配置，返回 OpenAILikeClient 实例。 |
| `load_embedding_from_env` | 函数 | `scripts.llm_client` | 从环境变量自动加载嵌入模型配置。 |
| `TerminationReason` | 枚举 | `scripts.multi_hop_retriever` | 终止原因 |
| `QueryHop` | 类 | `scripts.multi_hop_retriever` | 单跳查询信息 |
| `QueryChain` | 类 | `scripts.multi_hop_retriever` | 查询链 - 记录多跳检索全过程 |
| `SubQueryGenerator` | 类 | `scripts.multi_hop_retriever` | 子查询生成器 - 根据当前结果生成下一步查询 |
| `TerminationChecker` | 类 | `scripts.multi_hop_retriever` | 终止条件检查器 |
| `InformationExtractor` | 类 | `scripts.multi_hop_retriever` | 信息提取器 - 从检索结果中提取关键信息 |
| `AnswerAggregator` | 类 | `scripts.multi_hop_retriever` | 答案聚合器 - 合并多跳信息生成最终答案 |
| `MultiHopRetriever` | 类 | `scripts.multi_hop_retriever` | 多跳检索器 - 主入口类 |
| `Proposition` | 类 | `scripts.proposition_chunker` | 命题数据结构 |
| `PropositionExtractor` | 类 | `scripts.proposition_chunker` | 命题提取器 |
| `ReferenceResolver` | 类 | `scripts.proposition_chunker` | 指代消解器 |
| `PropositionDeduplicator` | 类 | `scripts.proposition_chunker` | 命题去重器 |
| `PropositionChunker` | 类 | `scripts.proposition_chunker` | 命题分块器 |
| `QueryIntent` | 枚举 | `scripts.query_intent` | 查询意图类型 |
| `QueryComplexity` | 枚举 | `scripts.query_intent` | 查询复杂度 |
| `IntentResult` | 类 | `scripts.query_intent` | 意图识别结果 |
| `QueryNormalizer` | 类 | `scripts.query_intent` | 查询标准化器 - 处理口语化表达 |
| `ComplexityEvaluator` | 类 | `scripts.query_intent` | 复杂度评估器 |
| `IntentClassifier` | 类 | `scripts.query_intent` | 意图分类器 |
| `EntityExtractor` | 类 | `scripts.query_intent` | 实体提取器 |
| `StrategyRouter` | 类 | `scripts.query_intent` | 策略路由器 - 根据意图推荐处理策略 |
| `QueryIntentRecognizer` | 类 | `scripts.query_intent` | 查询意图识别器 - 主入口类 |
| `QueryRouter` | 类 | `scripts.query_router` | 查询路由器：根据查询意图选择不同的检索器。 |
| `HyDETransformer` | 类 | `scripts.query_transformer` | 用 LLM 生成一个假设性答案文档，再用该文档的向量进行检索。 |
| `QueryExpander` | 类 | `scripts.query_transformer` | 生成多个语义变体的查询，提高召回率。 |
| `QueryDecomposer` | 类 | `scripts.query_transformer` | 将复杂查询拆解为多个子查询，分别检索后汇总。 |
| `QueryTransformer` | 类 | `scripts.query_transformer` | 统一查询转换器：根据查询特征自动选择最合适的转换策略。 |
| `RerankResult` | 类 | `scripts.reranker` | 重排序结果 |
| `Reranker` | 类 | `scripts.reranker` | 重排序器：对粗筛结果进行二次精排。 |
| `RetrievalHit` | 类 | `scripts.retriever_base` | 检索结果条目 |
| `BaseRetriever` | 类 | `scripts.retriever_base` | 检索器基类。 |
| `BM25Retriever` | 类 | `scripts.retriever_base` | Okapi BM25 检索器 —— 指向真实现的兼容适配层。 |
| `VectorRetriever` | 类 | `scripts.retriever_base` | 向量检索器：使用嵌入模型计算余弦相似度。 |
| `HybridRetriever` | 类 | `scripts.retriever_base` | 混合检索器：组合两个检索器，加权融合分数。 |
| `Granularity` | 枚举 | `scripts.segment_extractor` | 提取粒度 |
| `Segment` | 类 | `scripts.segment_extractor` | 片段数据结构 |
| `SegmentSplitter` | 类 | `scripts.segment_extractor` | 片段切分器 |
| `RelevanceScorer` | 类 | `scripts.segment_extractor` | 相关性评分器 |
| `ReferenceResolver` | 类 | `scripts.segment_extractor` | 指代消解器 |
| `RelevantSegmentExtractor` | 类 | `scripts.segment_extractor` | 相关片段提取器 |
| `CorrectionAction` | 枚举 | `scripts.self_rag` | 纠正动作类型 |
| `RetrievalAssessment` | 类 | `scripts.self_rag` | 检索质量评估结果 |
| `GenerationAssessment` | 类 | `scripts.self_rag` | 生成质量评估结果 |
| `RetrievalEvaluator` | 类 | `scripts.self_rag` | 检索质量评估器 |
| `GenerationEvaluator` | 类 | `scripts.self_rag` | 生成质量评估器 |
| `CorrectiveRAG` | 类 | `scripts.self_rag` | 纠正性RAG系统 |
| `SelfRAG` | 类 | `scripts.self_rag` | Self-RAG系统（更完整的自我反思RAG） |