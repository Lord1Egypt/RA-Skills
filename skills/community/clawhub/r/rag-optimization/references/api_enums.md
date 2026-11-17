# scripts 枚举类型汇总（自动生成）

> **本文档由 `scripts/generate-api-docs.py` 自动生成**，以代码为唯一真相源。
> 枚举与类型定义属于 API 契约，改动枚举值属于破坏性变更。

## `scripts.citation_tracker`

### `CitationFormat`

*引用格式*

成员：`INLINE = 'inline'`，`FOOTNOTE = 'footnote'`，`DETAILED = 'detailed'`，`JSON = 'json'`

---

## `scripts.context_compression`

### `CompressionMode`

*压缩模式*

成员：`EXTRACTIVE = 'extractive'`，`ABSTRACTIVE = 'abstractive'`，`HYBRID = 'hybrid'`

---

## `scripts.document_preprocessor`

### `DocumentFormat`

*文档格式*

成员：`PDF = 'pdf'`，`WORD = 'docx'`，`EXCEL = 'xlsx'`，`HTML = 'html'`，`MARKDOWN = 'md'`，`TEXT = 'txt'`，`IMAGE = 'image'`，`UNKNOWN = 'unknown'`

---

## `scripts.multi_hop_retriever`

### `TerminationReason`

*终止原因*

成员：`COMPLETE = 'complete'`，`MAX_HOPS = 'max_hops'`，`NO_NEW_INFO = 'no_new_info'`，`SATISFIED = 'satisfied'`，`ERROR = 'error'`

---

## `scripts.query_intent`

### `QueryComplexity`

*查询复杂度*

成员：`SIMPLE = 'simple'`，`MEDIUM = 'medium'`，`COMPLEX = 'complex'`

### `QueryIntent`

*查询意图类型*

成员：`FACTUAL = 'factual'`，`OPEN_ENDED = 'open_ended'`，`COMPARATIVE = 'comparative'`，`PROCEDURAL = 'procedural'`，`TROUBLESHOOTING = 'troubleshooting'`，`DEFINITION = 'definition'`，`COMPOUND = 'compound'`，`UNKNOWN = 'unknown'`

---

## `scripts.segment_extractor`

### `Granularity`

*提取粒度*

成员：`SENTENCE = 'sentence'`，`SLIDING_WINDOW = 'sliding_window'`，`SEMANTIC = 'semantic'`

---

## `scripts.self_rag`

### `CorrectionAction`

*纠正动作类型*

成员：`ACCEPT = 'accept'`，`RETRY = 'retry'`，`WEB_SEARCH = 'web_search'`，`REFUSE = 'refuse'`

---
