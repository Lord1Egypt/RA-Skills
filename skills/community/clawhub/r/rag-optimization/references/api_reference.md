# scripts API 参考文档（自动生成）

> **本文档由 `scripts/generate-api-docs.py` 自动生成，以代码为唯一真相源**，人工修改会被下次生成覆盖。
> 若需更新 API 描述，请修改代码 docstring 后重新生成。

---

## `scripts.benchmark_retrieval`

### `generate_corpus`

*生成合成语料*

- 签名: `generate_corpus(doc_count: <class 'int'>) -> <class 'list'>`

### `main`

- 签名: `main()`

---

## `scripts.bm25_retriever`

### `BM25Retriever`

*Okapi BM25 检索器，支持 bm25 / vector / hybrid 三种策略。
纯标准库实现，中英文兼容分词。
继承 retriever_base.BaseRetriever，与 VectorRetriever/HybridRetriever 可组合。*

- 构造: `BM25Retriever(config: typing.Dict = None, embedding_model = None)`
- 方法:
  - `add_document(doc: <class 'dict'>) -> None`
  - `index(documents: typing.List[typing.Dict]) -> <class 'int'>`
  - `index_documents(documents: typing.List[dict]) -> <class 'int'>`
  - `invalidate_cache() -> None`
  - `retrieve(query: <class 'str'>, top_k: <class 'int'> = 10, strategy: <class 'str'> = 'hybrid', kwargs) -> typing.List[scripts.bm25_retriever.RetrievalResult]`

### `RetrievalResult`

*检索结果（兼容 RetrievalHit 接口，增加 content 属性）*

- 构造: `RetrievalResult(id: <class 'str'>, text: <class 'str'>, score: <class 'float'> = 0.0, metadata: typing.Dict = <factory>) -> None`

---

## `scripts.chunker_factory`

### `Chunk`

*统一分块数据结构*

- 构造: `Chunk(id: <class 'str'>, content: <class 'str'>, parent_paragraph: <class 'str'> = '', metadata: typing.Dict = <factory>) -> None`
- 方法:
  - `to_document_unit() -> DocumentUnit`

### `chunk_document`

*便捷入口：切分单篇文档*

- 签名: `chunk_document(document: <class 'str'>, strategy: <class 'str'> = 'small_to_big', config: Dict = None) -> List[scripts.chunker_factory.Chunk]`

### `get_chunker`

*按策略名返回 chunker 函数。

Args:
    strategy: fixed / semantic / small_to_big / proposition / contextual_header
    config: 分块配置（chunk_size、overlap、child_chunk_size 等）

Returns:
    chunker(document: str) -> List[Chunk]*

- 签名: `get_chunker(strategy: <class 'str'> = 'small_to_big', config: Dict = None) -> Callable[[str], List[scripts.chunker_factory.Chunk]]`

---

## `scripts.citation_tracker`

### `Citation`

*引用信息*

- 构造: `Citation(id: <class 'str'>, source: <class 'scripts.citation_tracker.Source'>, matched_text: <class 'str'>, match_type: <class 'str'>, confidence: <class 'float'>, answer_segment: <class 'str'>, start_pos: <class 'int'> = 0, end_pos: <class 'int'> = 0) -> None`
- 方法:
  - `to_document_unit() -> DocumentUnit`

### `CitationFormat`

*引用格式*

成员：`INLINE = 'inline'`，`FOOTNOTE = 'footnote'`，`DETAILED = 'detailed'`，`JSON = 'json'`

### `CitationFormatter`

*引用格式化器 - 生成各种格式的引用*

- 构造: `CitationFormatter(config: typing.Dict = None)`
- 方法:
  - `format_citations(answer: <class 'str'>, citations: typing.List[scripts.citation_tracker.Citation], format: <class 'str'> = None) -> <class 'str'>`

### `CitationMatcher`

*引用匹配器 - 将答案片段与源文档匹配*

- 构造: `CitationMatcher(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `match(answer_segment: <class 'str'>, sources: typing.List[scripts.citation_tracker.Source]) -> typing.List[scripts.citation_tracker.Citation]`

### `CitationTracker`

*引用溯源器 - 主入口类*

- 构造: `CitationTracker(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `get_credibility_report(answer: <class 'str'>, sources: typing.List[scripts.citation_tracker.Source]) -> <class 'str'>`
  - `track(answer: <class 'str'>, sources: typing.List[scripts.citation_tracker.Source], format: <class 'str'> = None, min_confidence: <class 'float'> = None) -> typing.Dict[str, typing.Any]`
  - `track_and_format(answer: <class 'str'>, sources: typing.List[scripts.citation_tracker.Source], format: <class 'str'> = 'footnote') -> <class 'str'>`

### `CitedSegment`

*带引用的答案片段*

- 构造: `CitedSegment(args, kwargs)`

### `CredibilityScore`

*可信度评分*

- 构造: `CredibilityScore(source_coverage: <class 'float'>, citation_density: <class 'float'>, source_authority: <class 'float'>, overall_credibility: <class 'float'>, details: typing.Dict[str, typing.Any] = <factory>) -> None`

### `CredibilityScorer`

*可信度评分器*

- 构造: `CredibilityScorer(config: typing.Dict = None)`
- 方法:
  - `score(answer: <class 'str'>, citations: typing.List[scripts.citation_tracker.Citation]) -> <class 'scripts.citation_tracker.CredibilityScore'>`

### `Source`

*来源文档*

- 构造: `Source(id: <class 'str'>, title: <class 'str'>, content: <class 'str'>, location: <class 'str'> = '', authority_level: <class 'int'> = 1, publish_date: <class 'str'> = '', url: <class 'str'> = '') -> None`

---

## `scripts.config_loader`

### `ConfigError`

*配置严重错误（strict 模式下抛出）*

- 构造: `ConfigError(errors: typing.List[typing.Any])`
- 方法:
  - `add_note(object)`
  - `with_traceback(object)`

### `build_pipeline`

*按配置装配 RAG 组件。

只装配配置中 `enabled: true`（或未提供该开关）的模块，
但**所有被装配的组件都会真正收到配置参数**——这是 H2 的核心：
此前配置只是文档，现在它决定组件行为。

Args:
    cfg: `load_config()` 的返回值
    llm_client: 外部注入的 LLM（任意形态，内部统一用 wrap_llm 归一）
    embedding_model: 外部注入的嵌入模型
    retriever: 外部注入的检索器（不传则按 retrieval.strategy 装配 BM25Retriever）
    generator: 外部注入的答案生成器（供 Self-RAG 使用）

Returns:
    {组件名: 实例} 字典，至少含 "chunker" 与 "retriever"*

- 签名: `build_pipeline(cfg: Dict[str, Any], llm_client = None, embedding_model = None, retriever = None, generator = None) -> Dict[str, Any]`

### `load_config`

*加载配置文件并做入口校验。

Args:
    path: 配置文件路径；缺省使用 `assets/config-template.json`
    strict: True 时，severity=error 的校验失败直接抛 ConfigError；
            False 时仅告警（warning 级别无论 strict 与否都只告警）

Returns:
    解包后的 `rag_optimization_config` 字典（已是组件可直接消费的形状）

Raises:
    FileNotFoundError: 配置文件不存在
    ConfigError: strict 模式下存在 error 级校验失败*

- 签名: `load_config(path: <class 'str'> = None, strict: <class 'bool'> = False) -> Dict[str, Any]`

### `strip_meta`

*去掉配置块里的描述性键（comment / _status），只保留真正的参数。*

- 签名: `strip_meta(cfg: Dict[str, Any]) -> Dict[str, Any]`

---

## `scripts.config_validator`

### `ValidationError`

*配置错误*

- 构造: `ValidationError(field: <class 'str'>, message: <class 'str'>, severity: <class 'str'> = 'error')`

### `format_errors`

*格式化错误报告*

- 签名: `format_errors(errors: List[scripts.config_validator.ValidationError]) -> <class 'str'>`

### `validate_config`

*校验配置字典，返回所有错误列表。

校验规则：
    - 所有数值参数 >= 0
    - chunk_size > overlap
    - vector_weight + bm25_weight == 1.0
    - cache_max_size >= 0
    - top_k >= 1*

- 签名: `validate_config(config: Dict[str, Any]) -> List[scripts.config_validator.ValidationError]`

---

## `scripts.context_compression`

### `AbstractiveCompressor`

*摘要式压缩器 - 使用LLM生成精简摘要*

- 构造: `AbstractiveCompressor(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `compress(text: <class 'str'>, query: <class 'str'>, target_length: <class 'int'> = None, preserved_entities: typing.List[str] = None) -> <class 'str'>`

### `CompressionMode`

*压缩模式*

成员：`EXTRACTIVE = 'extractive'`，`ABSTRACTIVE = 'abstractive'`，`HYBRID = 'hybrid'`

### `CompressionResult`

*压缩结果*

- 构造: `CompressionResult(compressed_text: <class 'str'>, original_length: <class 'int'>, compressed_length: <class 'int'>, compression_ratio: <class 'float'>, preserved_entities: typing.List[str], key_sentences: typing.List[str], mode: <class 'str'>, quality_score: <class 'float'> = 1.0) -> None`

### `ContextCompressor`

*上下文压缩器 - 主入口类*

- 构造: `ContextCompressor(llm_client = None, embedding_model = None, config: typing.Dict = None)`
- 方法:
  - `compress(documents: typing.List[str], query: <class 'str'>, mode: <class 'str'> = None, target_length: <class 'int'> = None, preserve_entities: <class 'bool'> = True) -> <class 'scripts.context_compression.CompressionResult'>`
  - `compress_for_llm(documents: typing.List[str], query: <class 'str'>, max_tokens: <class 'int'> = 4000, mode: <class 'str'> = 'hybrid') -> <class 'str'>`

### `Entity`

*实体数据结构*

- 构造: `Entity(text: <class 'str'>, type: <class 'str'>, start: <class 'int'>, end: <class 'int'>, must_preserve: <class 'bool'> = True) -> None`

### `EntityProtector`

*实体保护器 - 确保关键信息不被压缩丢失*

- 构造: `EntityProtector(config: typing.Dict = None)`
- 方法:
  - `check_preservation(original: <class 'str'>, compressed: <class 'str'>) -> typing.Tuple[bool, typing.List[str]]`
  - `extract_entities(text: <class 'str'>) -> typing.List[scripts.context_compression.Entity]`

### `SentenceExtractor`

*句子提取器 - 用于提取式压缩*

- 构造: `SentenceExtractor(llm_client = None, embedding_model = None, config: typing.Dict = None)`
- 方法:
  - `extract_key_sentences(text: <class 'str'>, query: <class 'str'>, target_count: <class 'int'> = None, min_score: <class 'float'> = 0.3) -> typing.List[typing.Tuple[str, float]]`
  - `score_sentence(sentence: <class 'str'>, query: <class 'str'>, context: <class 'str'> = '') -> <class 'float'>`
  - `split_sentences(text: <class 'str'>) -> typing.List[str]`

---

## `scripts.contextual_header`

### `ChunkHeader`

*上下文头结构*

- 构造: `ChunkHeader(document_title: <class 'str'> = '', document_type: <class 'str'> = '', document_source: <class 'str'> = '', publish_date: <class 'str'> = '', section_path: <class 'str'> = '', topic_tags: typing.List[str] = <factory>, key_entities: typing.List[str] = <factory>, summary: <class 'str'> = '', chunk_index: <class 'int'> = 0, total_chunks: <class 'int'> = 0, created_at: <class 'str'> = '') -> None`
- 方法:
  - `to_json() -> <class 'str'>`
  - `to_natural_language(max_length: <class 'int'> = 100) -> <class 'str'>`
  - `to_tags() -> <class 'str'>`

### `ContextualHeaderEnhancer`

*上下文头增强器*

- 构造: `ContextualHeaderEnhancer(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `enhance(chunk: <class 'str'>, document_metadata: typing.Dict = None) -> <class 'str'>`
  - `enhance_document(document: <class 'str'>, metadata: typing.Dict = None) -> typing.List[typing.Dict]`

### `HeaderGenerator`

*上下文头生成器*

- 构造: `HeaderGenerator(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `generate(chunk: <class 'str'>, document_metadata: typing.Dict = None) -> <class 'scripts.contextual_header.ChunkHeader'>`

### `HierarchicalHeaderBuilder`

*分层头部构建器*

- 构造: `HierarchicalHeaderBuilder(config: typing.Dict = None)`
- 方法:
  - `build_chunk_header(chunk: <class 'str'>, topics: typing.List[str] = None, entities: typing.List[str] = None) -> <class 'str'>`
  - `build_document_header(document: <class 'str'>, metadata: typing.Dict = None) -> <class 'str'>`
  - `build_full_header(document: <class 'str'>, chunk: <class 'str'>, document_metadata: typing.Dict = None, section_info: typing.Dict = None, chunk_info: typing.Dict = None) -> <class 'str'>`
  - `build_section_header(section_title: <class 'str'>, section_path: <class 'str'>) -> <class 'str'>`

---

## `scripts.document_preprocessor`

### `DataCleaner`

*数据清洗器*

- 构造: `DataCleaner(config: typing.Dict = None)`
- 方法:
  - `clean(text: <class 'str'>) -> <class 'str'>`

### `DocumentFormat`

*文档格式*

成员：`PDF = 'pdf'`，`WORD = 'docx'`，`EXCEL = 'xlsx'`，`HTML = 'html'`，`MARKDOWN = 'md'`，`TEXT = 'txt'`，`IMAGE = 'image'`，`UNKNOWN = 'unknown'`

### `DocumentImage`

*文档图片*

- 构造: `DocumentImage(id: <class 'str'>, path: <class 'str'>, caption: <class 'str'>, ocr_text: <class 'str'> = '', location: <class 'str'> = '') -> None`

### `DocumentMetadata`

*文档元数据*

- 构造: `DocumentMetadata(source: <class 'str'> = '', author: <class 'str'> = '', publish_date: <class 'str'> = '', doc_type: <class 'str'> = '', language: <class 'str'> = 'zh', page_count: <class 'int'> = 0, word_count: <class 'int'> = 0, encoding: <class 'str'> = 'utf-8', file_size: <class 'int'> = 0, created_at: <class 'str'> = '', modified_at: <class 'str'> = '') -> None`

### `DocumentPreprocessor`

*文档预处理器 - 主入口类*

- 构造: `DocumentPreprocessor(config: typing.Dict = None)`
- 方法:
  - `process(file_path: <class 'str'>) -> <class 'scripts.document_preprocessor.ProcessedDocument'>`
  - `process_batch(file_paths: typing.List[str]) -> typing.List[scripts.document_preprocessor.ProcessedDocument]`
  - `to_indexable_format(doc: <class 'scripts.document_preprocessor.ProcessedDocument'>) -> typing.List[typing.Dict]`

### `DocumentSection`

*文档章节*

- 构造: `DocumentSection(level: <class 'int'>, title: <class 'str'>, content: <class 'str'>, path: <class 'str'>, start_pos: <class 'int'> = 0, end_pos: <class 'int'> = 0) -> None`

### `FormatDetector`

*格式检测器*

- 构造: `FormatDetector(args, kwargs)`
- 方法:
  - `detect(file_path: <class 'str'>) -> <enum 'DocumentFormat'>`

### `ProcessedDocument`

*处理后的文档*

- 构造: `ProcessedDocument(id: <class 'str'>, title: <class 'str'>, content: <class 'str'>, sections: typing.List[scripts.document_preprocessor.DocumentSection], tables: typing.List[scripts.document_preprocessor.StructuredTable], images: typing.List[scripts.document_preprocessor.DocumentImage], metadata: <class 'scripts.document_preprocessor.DocumentMetadata'>, raw_text: <class 'str'> = '', status: <class 'str'> = 'success', error: <class 'str'> = '') -> None`

### `SectionParser`

*章节解析器*

- 构造: `SectionParser(config: typing.Dict = None)`
- 方法:
  - `parse(text: <class 'str'>) -> typing.List[scripts.document_preprocessor.DocumentSection]`

### `StructuredTable`

*结构化表格*

- 构造: `StructuredTable(id: <class 'str'>, headers: typing.List[str], rows: typing.List[typing.List[str]], markdown: <class 'str'>, json_data: typing.List[typing.Dict], description: <class 'str'>, location: <class 'str'> = '') -> None`

### `TextExtractor`

*文本提取器*

- 构造: `TextExtractor(config: typing.Dict = None)`
- 方法:
  - `extract_from_html(file_path: <class 'str'>) -> typing.Tuple[str, scripts.document_preprocessor.DocumentMetadata]`
  - `extract_from_image(file_path: <class 'str'>) -> typing.Tuple[str, scripts.document_preprocessor.DocumentMetadata]`
  - `extract_from_markdown(file_path: <class 'str'>) -> typing.Tuple[str, scripts.document_preprocessor.DocumentMetadata]`
  - `extract_from_pdf(file_path: <class 'str'>) -> typing.Tuple[str, scripts.document_preprocessor.DocumentMetadata, typing.List[scripts.document_preprocessor.StructuredTable]]`
  - `extract_from_text(file_path: <class 'str'>) -> typing.Tuple[str, scripts.document_preprocessor.DocumentMetadata]`
  - `extract_from_word(file_path: <class 'str'>) -> typing.Tuple[str, scripts.document_preprocessor.DocumentMetadata]`

---

## `scripts.document_unit`

### `DocumentUnit`

*统一文档单元：所有 RAG 处理流程中产生的文本块的基础数据结构。

属性约定：
    - id: 全局唯一标识符
    - content: 用于向量化索引/检索的内容
    - parent_paragraph: 父块（用于返回给 LLM 的完整上下文）
    - metadata: 附加元数据（标题/章节/主题/实体等）*

- 构造: `DocumentUnit(id: <class 'str'>, content: <class 'str'>, parent_paragraph: <class 'str'> = '', metadata: typing.Dict[str, typing.Any] = <factory>) -> None`
- 方法:
  - `from_dict(data: typing.Dict[str, typing.Any]) -> DocumentUnit`
  - `to_dict() -> typing.Dict[str, typing.Any]`

### `UnitConverter`

*各类数据结构与 DocumentUnit 之间的转换工具。

支持：
    - from_proposition: 从 PropositionChunker 的 Proposition 转换
    - from_segment: 从 RelevantSegmentExtractor 的 Segment 转换
    - from_retrieval: 从 BM25Retriever 的 RetrievalResult 转换
    - from_dict: 从任意字典转换
    - to_list: 批量转换*

- 构造: `UnitConverter(args, kwargs)`
- 方法:
  - `from_chunk(chunk) -> <class 'scripts.document_unit.DocumentUnit'>`
  - `from_dict(data: typing.Dict[str, typing.Any]) -> <class 'scripts.document_unit.DocumentUnit'>`
  - `from_proposition(prop) -> <class 'scripts.document_unit.DocumentUnit'>`
  - `from_retrieval(result) -> <class 'scripts.document_unit.DocumentUnit'>`
  - `from_segment(seg) -> <class 'scripts.document_unit.DocumentUnit'>`
  - `from_source(source) -> <class 'scripts.document_unit.DocumentUnit'>`
  - `to_list(units, factory_fn) -> typing.List[scripts.document_unit.DocumentUnit]`

---

## `scripts.evaluate`

### `EvaluationResult`

*评估结果*

- 构造: `EvaluationResult(query: <class 'str'>, retrieved_docs: typing.List[str], generated_answer: <class 'str'>, retrieval_metrics: typing.Dict[str, float], generation_metrics: typing.Dict[str, float], latency_ms: <class 'float'>) -> None`

### `RAGEvaluator`

*RAG系统评估器*

- 构造: `RAGEvaluator(rag_system, config: typing.Dict = None)`
- 方法:
  - `evaluate(test_cases: typing.List[scripts.evaluate.TestCase]) -> typing.Dict[str, typing.Any]`

### `TestCase`

*测试用例*

- 构造: `TestCase(query: <class 'str'>, expected_answer: <class 'str'>, expected_doc_ids: typing.List[str], category: typing.Optional[str] = None, difficulty: typing.Optional[str] = None) -> None`

### `load_rag_system`

*H3：按 `--rag-class` 加载真实 RAG 系统；未指定时**显式**回退到 MockRAG。

此前 main() 里 `args.config` 从未被使用，评估永远跑硬编码 MockRAG，
用户以为拿到了真实系统的评估报告。这里把选择权交回给用户，
并在回退时给出醒目警告（H3 配套环节①）。

Args:
    rag_class_spec: "module:ClassName" 格式，如 `myrag.MyRAG:MyRAG`
    config: 已加载的配置字典（供接受 config= 的类使用）
    config_path: 配置文件路径（供接受 config_path= 的类使用）

Returns:
    (rag_system, system_label)*

- 签名: `load_rag_system(rag_class_spec: <class 'str'> = None, config: Dict = None, config_path: <class 'str'> = None)`

### `load_test_cases`

*加载测试用例*

- 签名: `load_test_cases(file_path: <class 'str'>) -> List[scripts.evaluate.TestCase]`

### `main`

- 签名: `main()`

### `print_comparison`

*打印新旧评估报告的指标对比（Ablation 前后 diff）*

- 签名: `print_comparison(old_report: Dict, new_report: Dict)`

### `print_summary`

*打印摘要*

- 签名: `print_summary(report: Dict)`

### `save_report`

*保存评估报告*

- 签名: `save_report(report: Dict, output_path: <class 'str'>)`

---

## `scripts.generate-api-docs`

### `main`

- 签名: `main()`

---

## `scripts.graph_rag`

### `Entity`

*知识图谱实体*

- 构造: `Entity(id: <class 'str'>, label: <class 'str'>, type: <class 'str'>, mentions: <class 'int'> = 0, aliases: typing.Set[str] = <factory>) -> None`
- 方法:
  - `to_dict() -> typing.Dict`

### `EntityExtractor`

*实体提取器：从文本中提取实体。

规则模式：基于中文/英文常见实体模式匹配。
LLM 模式：传入 llm_client 后使用 LLM 识别实体。*

- 构造: `EntityExtractor(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `extract(text: <class 'str'>) -> typing.List[scripts.graph_rag.Entity]`

### `GraphQueryResult`

*图检索结果*

- 构造: `GraphQueryResult(query: <class 'str'>, matched_entities: typing.List[scripts.graph_rag.Entity], related_entities: typing.List[scripts.graph_rag.Entity], relations: typing.List[scripts.graph_rag.Relation], answer: <class 'str'>, confidence: <class 'float'>) -> None`
- 方法:
  - `to_dict() -> typing.Dict`

### `GraphRAG`

*图检索增强生成（Graph RAG）

将文档转换为知识图谱，支持：
1. 实体提取：从文本中识别命名实体
2. 关系构建：识别实体之间的关系
3. 图遍历检索：根据查询找到相关实体和关系
4. 答案生成：基于图谱信息生成答案*

- 构造: `GraphRAG(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `build_from_text(text: <class 'str'>, source: <class 'str'> = 'default') -> typing.Dict`
  - `build_from_texts(texts: typing.List[str], sources: typing.List[str] = None) -> typing.Dict`
  - `export_graph(output_path: <class 'str'> = None) -> typing.Dict`
  - `get_graph_stats() -> typing.Dict`
  - `query(query_text: <class 'str'>, top_k: <class 'int'> = 5, depth: <class 'int'> = 2) -> <class 'scripts.graph_rag.GraphQueryResult'>`

### `KnowledgeGraph`

*知识图谱：存储实体和关系，支持遍历查询*

- 构造: `KnowledgeGraph()`
- 方法:
  - `add_entity(entity: <class 'scripts.graph_rag.Entity'>)`
  - `add_relation(relation: <class 'scripts.graph_rag.Relation'>)`
  - `find_entity_by_label(label: <class 'str'>) -> typing.Optional[scripts.graph_rag.Entity]`
  - `get_neighbors(entity_id: <class 'str'>, depth: <class 'int'> = 1) -> typing.List[scripts.graph_rag.Entity]`
  - `to_dict() -> typing.Dict`

### `Relation`

*知识图谱关系*

- 构造: `Relation(id: <class 'str'>, source: <class 'str'>, target: <class 'str'>, relation_type: <class 'str'>, confidence: <class 'float'> = 1.0, evidence: <class 'str'> = '') -> None`
- 方法:
  - `to_dict() -> typing.Dict`

### `RelationExtractor`

*关系提取器：从文本中识别实体之间的关系。

规则模式：基于预定义的关系模板匹配。*

- 构造: `RelationExtractor(config: typing.Dict = None)`
- 方法:
  - `extract(text: <class 'str'>, entities: typing.List[scripts.graph_rag.Entity]) -> typing.List[scripts.graph_rag.Relation]`

---

## `scripts.llm_client`

### `EmbeddingClient`

*向量嵌入客户端。

支持：
- sentence-transformers 模型（需安装）
- 零依赖的哈希向量（降级方案）*

- 构造: `EmbeddingClient(model_name: <class 'str'> = 'all-MiniLM-L6-v2')`
- 方法:
  - `encode(texts: typing.List[str]) -> <class 'scripts.llm_client.EmbeddingResult'>`

### `EmbeddingResult`

*encode() 的返回协议（H9）。

降级为哈希向量时必须可被识别——否则调用方拿到一份"看起来正常"的向量，
语义检索静默失效却无任何迹象。

为保持向后兼容，本对象支持像 List[List[float]] 一样被
len() / 索引 / 迭代（`encode([q])[0]` 这种既有写法继续可用）。*

- 构造: `EmbeddingResult(vectors: typing.List[typing.List[float]], is_degraded: <class 'bool'> = False, degraded_indices: typing.List[int] = <factory>, reason: <class 'str'> = '') -> None`

### `LLMClient`

*统一 LLM 客户端基类。

所有 LLM 交互统一通过以下 4 个方法，内部封装：
- 安全的数字解析（解决各脚本中重复的脆弱拼接）
- 安全的 JSON 解析（处理 LLM 返回的多余文本）
- 3 次自动重试 + 指数退避
- LRU 缓存（可配置开关）
- 无 LLM 时的安全降级*

- 构造: `LLMClient(cache_enabled: <class 'bool'> = True, cache_size: <class 'int'> = 128, max_retries: <class 'int'> = 3, retry_delay: <class 'float'> = 1.0, llm_client = None)`
- 方法:
  - `classify(prompt: <class 'str'>, options: typing.List[str]) -> <class 'str'>`
  - `extract_json(prompt: <class 'str'>) -> typing.Dict`
  - `generate(prompt: <class 'str'>, system_prompt: <class 'str'> = None, kwargs) -> <class 'str'>`
  - `score(prompt: <class 'str'>, default: <class 'float'> = 0.5) -> <class 'float'>`

### `NvidiaEmbeddingClient`

*通过 NVIDIA API 调用向量嵌入模型。

支持模型（截至 2026-07）：
    - nvidia/nemotron-3-embed-1b（推荐，2048 维，快速）
    - nvidia/nv-embed-v1（4096 维）
    - snowflake/arctic-embed-l

零依赖：不安装任何模型文件，纯 HTTP 调用。*

- 构造: `NvidiaEmbeddingClient(model_name: <class 'str'> = 'nvidia/nemotron-3-embed-1b', api_key: <class 'str'> = None, api_url: <class 'str'> = None)`
- 方法:
  - `encode(texts: typing.List[str]) -> <class 'scripts.llm_client.EmbeddingResult'>`

### `OpenAILikeClient`

*兼容 OpenAI 协议的 LLM 客户端。

支持豆包、NVIDIA、OpenAI 等所有使用 chat/completions 端点的服务商。

使用环境变量注入（通过 .env 加载）：
    OPENAI_API_KEY / DOUBAO_API_KEY / NVIDIA_API_KEY
    OPENAI_API_URL / DOUBAO_API_URL / NVIDIA_API_URL
    OPENAI_MODEL / DOUBAO_MODEL*

- 构造: `OpenAILikeClient(api_key: <class 'str'> = None, api_url: <class 'str'> = None, model: <class 'str'> = None, max_retries: <class 'int'> = None, retry_delay: <class 'float'> = None, cache_enabled: <class 'bool'> = True, circuit_failure_threshold: <class 'int'> = None, circuit_cooldown_seconds: <class 'float'> = None)`
- 方法:
  - `classify(prompt: <class 'str'>, options: typing.List[str]) -> <class 'str'>`
  - `extract_json(prompt: <class 'str'>) -> typing.Dict`
  - `generate(prompt: <class 'str'>, system_prompt: <class 'str'> = None, kwargs) -> <class 'str'>`
  - `invoke(prompt: <class 'str'>, kwargs) -> <class 'str'>`
  - `score(prompt: <class 'str'>, default: <class 'float'> = 0.5) -> <class 'float'>`

### `load_dotenv_if_available`

*尝试加载 .env 文件；python-dotenv 未安装时静默跳过。

全局唯一的 dotenv 入口——其它模块应调用本函数，不要各自 try/import，
否则会出现"有的入口加载了、有的没加载"的不一致。

注意：load_dotenv() 默认不覆盖已存在的环境变量，
因此真实环境注入的凭证优先级高于 .env（符合直觉）。

Returns:
    是否成功加载了 .env*

- 签名: `load_dotenv_if_available() -> <class 'bool'>`

### `load_embedding_from_env`

*从环境变量自动加载嵌入模型配置。

搜索顺序：
    1. EMBEDDING_MODEL / DOUBAO_API_KEY（环境变量）
    2. NVIDIA_API_KEY（.env 桥接）

返回 NvidiaEmbeddingClient 实例；无凭证时返回 None。*

- 签名: `load_embedding_from_env(api_key_env: <class 'str'> = 'DOUBAO_API_KEY', model_env: <class 'str'> = 'EMBEDDING_MODEL', fallback_model: <class 'str'> = 'nvidia/nemotron-3-embed-1b') -> Optional[scripts.llm_client.NvidiaEmbeddingClient]`

### `load_from_env`

*从环境变量自动加载 LLM 配置，返回 OpenAILikeClient 实例。

搜索顺序：
    1. DOUBAO_API_URL / DOUBAO_API_KEY / DOUBAO_MODEL（环境变量）
    2. NVIDIA_API_URL / NVIDIA_API_KEY（.env 桥接）
    3. 内置 NVIDIA 默认值（零配置）

所有凭证缺失时返回 None（降级模式）。*

- 签名: `load_from_env(api_url_env: <class 'str'> = 'DOUBAO_API_URL', api_key_env: <class 'str'> = 'DOUBAO_API_KEY', model_env: <class 'str'> = 'DOUBAO_MODEL', fallback_url: <class 'str'> = 'https://integrate.api.nvidia.com/v1/chat/completions', fallback_model: <class 'str'> = 'nvidia/nemotron-3-super-120b-a12b') -> Optional[scripts.llm_client.OpenAILikeClient]`

### `resolve_embedding_dim`

*按模型名解析向量维度（全项目唯一入口）。未知模型回退到默认值。*

- 签名: `resolve_embedding_dim(model_name: <class 'str'>) -> <class 'int'>`

### `wrap_llm`

*把外部传入的 LLM 对象统一成 LLMClient 接口。

关键（H23）：若传入对象**已经是 LLMClient 实例**（OpenAILikeClient 也是其子类），
直接返回、不再套一层。否则会造成重试放大：

    外层 LLMClient._retry_with_backoff 重试 3 次
      × 内层 OpenAILikeClient.generate 重试 3 次 = 最多 9 次调用、
        退避 sleep 累计可达 21 秒

各脚本的 `self.llm_client = LLMClient(llm_client=llm_client)` 一律改为调用本函数。

Args:
    llm_client: LLMClient 实例 / 有 invoke() 的对象 / 可调用对象
    **kwargs: 透传给 LLMClient 构造（cache_enabled、max_retries 等）

Returns:
    LLMClient；入参为 None 时返回 None*

- 签名: `wrap_llm(llm_client, kwargs) -> Optional[scripts.llm_client.LLMClient]`

---

## `scripts.multi_hop_retriever`

### `AnswerAggregator`

*答案聚合器 - 合并多跳信息生成最终答案*

- 构造: `AnswerAggregator(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `aggregate(chain: <class 'scripts.multi_hop_retriever.QueryChain'>) -> typing.Tuple[str, float]`

### `InformationExtractor`

*信息提取器 - 从检索结果中提取关键信息*

- 构造: `InformationExtractor(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `extract(query: <class 'str'>, documents: typing.List[str]) -> typing.Tuple[str, typing.List[str]]`

### `MultiHopRetriever`

*多跳检索器 - 主入口类*

- 构造: `MultiHopRetriever(retriever: typing.Callable = None, llm_client = None, config: typing.Dict = None)`
- 方法:
  - `get_hop_summary(chain: <class 'scripts.multi_hop_retriever.QueryChain'>) -> <class 'str'>`
  - `retrieve(query: <class 'str'>) -> <class 'scripts.multi_hop_retriever.QueryChain'>`

### `QueryChain`

*查询链 - 记录多跳检索全过程*

- 构造: `QueryChain(original_query: <class 'str'>, hops: typing.List[scripts.multi_hop_retriever.QueryHop], final_answer: <class 'str'>, total_hops: <class 'int'>, termination_reason: <enum 'TerminationReason'>, confidence: <class 'float'>, metadata: typing.Dict[str, typing.Any] = <factory>) -> None`

### `QueryHop`

*单跳查询信息*

- 构造: `QueryHop(hop_index: <class 'int'>, query: <class 'str'>, retrieved_docs: typing.List[str], extracted_info: <class 'str'>, relevance_score: <class 'float'>, next_query: typing.Optional[str], entities_found: typing.List[str]) -> None`

### `SubQueryGenerator`

*子查询生成器 - 根据当前结果生成下一步查询*

- 构造: `SubQueryGenerator(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `generate(original_query: <class 'str'>, current_info: <class 'str'>, hop_history: typing.List[scripts.multi_hop_retriever.QueryHop]) -> typing.Tuple[typing.Optional[str], str]`

### `TerminationChecker`

*终止条件检查器*

- 构造: `TerminationChecker(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `should_stop(chain: <class 'scripts.multi_hop_retriever.QueryChain'>) -> typing.Tuple[bool, scripts.multi_hop_retriever.TerminationReason, str]`

### `TerminationReason`

*终止原因*

成员：`COMPLETE = 'complete'`，`MAX_HOPS = 'max_hops'`，`NO_NEW_INFO = 'no_new_info'`，`SATISFIED = 'satisfied'`，`ERROR = 'error'`

---

## `scripts.proposition_chunker`

### `Proposition`

*命题数据结构*

- 构造: `Proposition(id: <class 'str'>, content: <class 'str'>, original_text: <class 'str'>, parent_paragraph: <class 'str'>, metadata: typing.Dict[str, typing.Any] = <factory>, is_atomic: <class 'bool'> = True, is_self_contained: <class 'bool'> = True, entities: typing.List[str] = <factory>, confidence: <class 'float'> = 1.0) -> None`
- 方法:
  - `to_document_unit() -> DocumentUnit`

### `PropositionChunker`

*命题分块器*

- 构造: `PropositionChunker(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `chunk(document: <class 'str'>) -> typing.List[scripts.proposition_chunker.Proposition]`
  - `chunk_batch(documents: typing.List[str]) -> typing.Dict[str, typing.List[scripts.proposition_chunker.Proposition]]`
  - `get_child_propositions(paragraph: <class 'str'>) -> typing.List[str]`
  - `get_parent_context(proposition_id: <class 'str'>) -> typing.Optional[str]`
  - `to_indexable_format(propositions: typing.List[scripts.proposition_chunker.Proposition]) -> typing.List[typing.Dict]`

### `PropositionDeduplicator`

*命题去重器*

- 构造: `PropositionDeduplicator(config: typing.Dict = None)`
- 方法:
  - `deduplicate(propositions: typing.List[scripts.proposition_chunker.Proposition]) -> typing.List[scripts.proposition_chunker.Proposition]`

### `PropositionExtractor`

*命题提取器*

- 构造: `PropositionExtractor(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `extract(text: <class 'str'>) -> typing.List[scripts.proposition_chunker.Proposition]`

### `ReferenceResolver`

*指代消解器*

- 构造: `ReferenceResolver(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `resolve(proposition: <class 'scripts.proposition_chunker.Proposition'>, context: <class 'str'>) -> <class 'scripts.proposition_chunker.Proposition'>`

---

## `scripts.query_intent`

### `ComplexityEvaluator`

*复杂度评估器*

- 构造: `ComplexityEvaluator(config: typing.Dict = None)`
- 方法:
  - `evaluate(query: <class 'str'>, entities: typing.List[str] = None) -> <enum 'QueryComplexity'>`

### `EntityExtractor`

*实体提取器*

- 构造: `EntityExtractor(config: typing.Dict = None)`
- 方法:
  - `extract(query: <class 'str'>) -> typing.List[str]`

### `IntentClassifier`

*意图分类器*

- 构造: `IntentClassifier(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `classify(query: <class 'str'>) -> typing.Tuple[scripts.query_intent.QueryIntent, float, typing.List[scripts.query_intent.QueryIntent]]`

### `IntentResult`

*意图识别结果*

- 构造: `IntentResult(primary_intent: <enum 'QueryIntent'>, secondary_intents: typing.List[scripts.query_intent.QueryIntent], confidence: <class 'float'>, complexity: <enum 'QueryComplexity'>, normalized_query: <class 'str'>, entities: typing.List[str], sub_queries: typing.List[str], suggested_strategy: typing.Dict[str, typing.Any], reasoning: <class 'str'>) -> None`

### `QueryComplexity`

*查询复杂度*

成员：`SIMPLE = 'simple'`，`MEDIUM = 'medium'`，`COMPLEX = 'complex'`

### `QueryIntent`

*查询意图类型*

成员：`FACTUAL = 'factual'`，`OPEN_ENDED = 'open_ended'`，`COMPARATIVE = 'comparative'`，`PROCEDURAL = 'procedural'`，`TROUBLESHOOTING = 'troubleshooting'`，`DEFINITION = 'definition'`，`COMPOUND = 'compound'`，`UNKNOWN = 'unknown'`

### `QueryIntentRecognizer`

*查询意图识别器 - 主入口类*

- 构造: `QueryIntentRecognizer(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `get_strategy(query: <class 'str'>) -> typing.Dict[str, typing.Any]`
  - `is_multi_hop_needed(query: <class 'str'>) -> <class 'bool'>`
  - `recognize(query: <class 'str'>) -> <class 'scripts.query_intent.IntentResult'>`

### `QueryNormalizer`

*查询标准化器 - 处理口语化表达*

- 构造: `QueryNormalizer(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `normalize(query: <class 'str'>) -> <class 'str'>`

### `StrategyRouter`

*策略路由器 - 根据意图推荐处理策略*

- 构造: `StrategyRouter(config: typing.Dict = None)`
- 方法:
  - `route(intent_result: <class 'scripts.query_intent.IntentResult'>) -> typing.Dict[str, typing.Any]`

---

## `scripts.query_router`

### `QueryRouter`

*查询路由器：根据查询意图选择不同的检索器。

典型场景：
    - FAQ / 精确问答 -> BM25 检索
    - 开放域问题 -> Hybrid 检索
    - 代码相关 -> 专门的代码检索器
    - 默认 -> 通用检索器*

- 构造: `QueryRouter(intent_classifier = None, retrievers: typing.Dict[str, typing.Any] = None, config: typing.Dict = None)`
- 方法:
  - `route(query: <class 'str'>, top_k: <class 'int'> = 10) -> typing.Dict[str, typing.Any]`

---

## `scripts.query_transformer`

### `HyDETransformer`

*用 LLM 生成一个假设性答案文档，再用该文档的向量进行检索。

原理：用户查询（如 "RAG优化策略"）过于简短，直接编码后难以匹配
完整的知识条目。先生成一个假设的完整回答，再编码，语义更丰富。

适用场景：短查询（< 10 字）、模糊查询、概念性查询。
不适用：精确匹配查询（如产品型号、版本号）。*

- 构造: `HyDETransformer(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `transform(query: <class 'str'>) -> <class 'str'>`

### `QueryDecomposer`

*将复杂查询拆解为多个子查询，分别检索后汇总。

适用场景：复合问题（"A和B的区别是什么，各有什么优缺点"）、
需要多步推理的问题。*

- 构造: `QueryDecomposer(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `decompose(query: <class 'str'>) -> typing.List[str]`

### `QueryExpander`

*生成多个语义变体的查询，提高召回率。

适用场景：查询词太少导致召回不足、需要多角度检索。*

- 构造: `QueryExpander(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `expand(query: <class 'str'>, n: <class 'int'> = 3) -> typing.List[str]`

### `QueryTransformer`

*统一查询转换器：根据查询特征自动选择最合适的转换策略。

决策逻辑：
- 短查询（< 5 字）→ HyDE
- 模糊查询 → 查询扩展
- 复杂查询 → 查询分解
- 普通查询 → 原样输出*

- 构造: `QueryTransformer(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `transform(query: <class 'str'>) -> typing.Dict[str, str]`

---

## `scripts.reranker`

### `RerankResult`

*重排序结果*

- 构造: `RerankResult(rank: <class 'int'>, original_rank: <class 'int'>, document_id: <class 'str'>, content: <class 'str'>, score: <class 'float'>, delta: <class 'float'> = 0.0) -> None`

### `Reranker`

*重排序器：对粗筛结果进行二次精排。

支持两种模式：
- bge-reranker（推荐）：使用 BAAI 的交叉编码器模型
- cross-encoder（备选）：使用 ms-marco 系列模型
- fallback（降级）：使用 BM25 关键词匹配分数

模型推荐：
- 英文：cross-encoder/ms-marco-MiniLM-L-6-v2（快速）
        cross-encoder/ms-marco-MiniLM-L-12-v2（高精度）
- 中文：BAAI/bge-reranker-base（基础）
        BAAI/bge-reranker-large（高精度）*

- 构造: `Reranker(model_name: <class 'str'> = 'BAAI/bge-reranker-base', batch_size: <class 'int'> = 32, config: typing.Dict = None)`
- 方法:
  - `get_stats(query: <class 'str'>, candidates: typing.List[typing.Dict]) -> typing.Dict[str, typing.Any]`
  - `rerank(query: <class 'str'>, candidates: typing.List[typing.Dict], top_k: <class 'int'> = 5) -> typing.List[scripts.reranker.RerankResult]`

---

## `scripts.retriever_base`

### `BM25Retriever`

*Okapi BM25 检索器 —— 指向真实现的兼容适配层。

H21：此前这里是第二份平行实现。两份副本各自演化，所有加固
（IDF 缓存失效 H6/H7、查询缓存 TTL H18、k1/b 变参 H5、零分文档
过滤 H24）都只落在 scripts/bm25_retriever.py 的真实现上，这份副本
静默落后——谁 import 到它，谁就拿到带旧缺陷的检索器。

现改为延迟导入的适配层：
  - 保持 BaseRetriever 的接口契约（index()/retrieve() → RetrievalHit），
    老调用方零改动；
  - 构造签名 (k1, b) 映射到真实现的 config；
  - 延迟导入（在方法内 import）规避循环依赖：
    bm25_retriever.py 顶部 from retriever_base import BaseRetriever。*

- 构造: `BM25Retriever(k1: <class 'float'> = 1.5, b: <class 'float'> = 0.75)`
- 方法:
  - `index(documents: typing.List[typing.Dict]) -> <class 'int'>`
  - `invalidate_cache()`
  - `retrieve(query: <class 'str'>, top_k: <class 'int'> = 10) -> typing.List[scripts.retriever_base.RetrievalHit]`

### `BaseRetriever`

*检索器基类。

所有检索器必须实现：
    - index(): 建立索引
    - retrieve(): 执行检索

支持组合：HybridRetriever 组合两个检索器并加权融合。*

- 构造: `BaseRetriever(args, kwargs)`
- 方法:
  - `index(documents: typing.List[typing.Dict]) -> <class 'int'>`
  - `retrieve(query: <class 'str'>, top_k: <class 'int'> = 10) -> typing.List[scripts.retriever_base.RetrievalHit]`

### `HybridRetriever`

*混合检索器：组合两个检索器，加权融合分数。

使用方式：
    hybrid = HybridRetriever(
        left=BM25Retriever(),
        right=VectorRetriever(model),
        weight=0.7  # left 的权重
    )
    results = hybrid.retrieve("RAG 优化", top_k=10)

权重说明：
    weight=0.7 → 左侧检索器占 70%，右侧占 30%
    weight=0.5 → 各占 50%（等权）*

- 构造: `HybridRetriever(left: <class 'scripts.retriever_base.BaseRetriever'>, right: <class 'scripts.retriever_base.BaseRetriever'>, weight: <class 'float'> = 0.7)`
- 方法:
  - `index(documents: typing.List[typing.Dict]) -> <class 'int'>`
  - `retrieve(query: <class 'str'>, top_k: <class 'int'> = 10) -> typing.List[scripts.retriever_base.RetrievalHit]`

### `RetrievalHit`

*检索结果条目*

- 构造: `RetrievalHit(id: <class 'str'>, content: <class 'str'>, score: <class 'float'> = 0.0, metadata: typing.Dict = <factory>) -> None`

### `VectorRetriever`

*向量检索器：使用嵌入模型计算余弦相似度。

需要 embedding_model（提供 encode(texts) -> List[List[float]]）。
无模型时回退为 BM25。*

- 构造: `VectorRetriever(embedding_model = None, fallback: <class 'scripts.retriever_base.BaseRetriever'> = None)`
- 方法:
  - `index(documents: typing.List[typing.Dict]) -> <class 'int'>`
  - `retrieve(query: <class 'str'>, top_k: <class 'int'> = 10) -> typing.List[scripts.retriever_base.RetrievalHit]`

---

## `scripts.segment_extractor`

### `Granularity`

*提取粒度*

成员：`SENTENCE = 'sentence'`，`SLIDING_WINDOW = 'sliding_window'`，`SEMANTIC = 'semantic'`

### `ReferenceResolver`

*指代消解器*

- 构造: `ReferenceResolver(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `resolve(segment: <class 'str'>, context: <class 'str'>) -> <class 'str'>`

### `RelevanceScorer`

*相关性评分器*

- 构造: `RelevanceScorer(llm_client = None, embedding_model = None, config: typing.Dict = None)`
- 方法:
  - `score(query: <class 'str'>, segment: <class 'str'>) -> <class 'float'>`

### `RelevantSegmentExtractor`

*相关片段提取器*

- 构造: `RelevantSegmentExtractor(llm_client = None, embedding_model = None, config: typing.Dict = None)`
- 方法:
  - `extract(query: <class 'str'>, documents: typing.List[str]) -> typing.List[scripts.segment_extractor.Segment]`
  - `extract_and_compose(query: <class 'str'>, documents: typing.List[str]) -> <class 'str'>`
  - `get_context_for_llm(query: <class 'str'>, documents: typing.List[str], max_length: <class 'int'> = 2000) -> <class 'str'>`

### `Segment`

*片段数据结构*

- 构造: `Segment(text: <class 'str'>, source_doc: <class 'str'>, relevance_score: <class 'float'>, start_pos: <class 'int'>, end_pos: <class 'int'>, resolved_text: typing.Optional[str]) -> None`
- 方法:
  - `to_document_unit() -> DocumentUnit`

### `SegmentSplitter`

*片段切分器*

- 构造: `SegmentSplitter(config: typing.Dict = None)`
- 方法:
  - `split(text: <class 'str'>) -> typing.List[typing.Tuple[str, int, int]]`

---

## `scripts.self_rag`

### `CorrectionAction`

*纠正动作类型*

成员：`ACCEPT = 'accept'`，`RETRY = 'retry'`，`WEB_SEARCH = 'web_search'`，`REFUSE = 'refuse'`

### `CorrectiveRAG`

*纠正性RAG系统*

- 构造: `CorrectiveRAG(retriever, generator, llm_client = None, config: typing.Dict = None, retrievers: typing.List = None)`
- 方法:
  - `query(question: <class 'str'>, top_k: <class 'int'> = 5) -> typing.Dict[str, typing.Any]`

### `GenerationAssessment`

*生成质量评估结果*

- 构造: `GenerationAssessment(faithfulness_score: <class 'float'>, relevance_score: <class 'float'>, has_hallucination: <class 'bool'>, action: <class 'str'>, reason: <class 'str'>) -> None`

### `GenerationEvaluator`

*生成质量评估器*

- 构造: `GenerationEvaluator(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `assess(query: <class 'str'>, answer: <class 'str'>, sources: typing.List[str]) -> <class 'scripts.self_rag.GenerationAssessment'>`

### `RetrievalAssessment`

*检索质量评估结果*

- 构造: `RetrievalAssessment(relevance_score: <class 'float'>, coverage_score: <class 'float'>, action: <enum 'CorrectionAction'>, reason: <class 'str'>) -> None`

### `RetrievalEvaluator`

*检索质量评估器*

- 构造: `RetrievalEvaluator(llm_client = None, config: typing.Dict = None)`
- 方法:
  - `assess(query: <class 'str'>, documents: typing.List[str]) -> <class 'scripts.self_rag.RetrievalAssessment'>`

### `SelfRAG`

*Self-RAG系统（更完整的自我反思RAG）*

- 构造: `SelfRAG(retriever, generator, llm_client = None, config: typing.Dict = None, retrievers: typing.List = None)`
- 方法:
  - `query(question: <class 'str'>) -> typing.Dict[str, typing.Any]`

---
