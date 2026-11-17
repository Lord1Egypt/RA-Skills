# 数据格式与 ragas 0.4.3 注意点

## evalset.jsonl（build_evalset.py 产出）

每行一个 JSON 对象：

```json
{
  "query_id": "q0001",
  "query": "…",
  "reference_answer": "…",
  "gold_chunk_ids": ["guide-0007", "faq-0002"],
  "gold_sources": ["faq.md", "guide.md"],
  "reference_contexts": ["逐字的块原文…"],
  "synthesizer": "single_hop_specific_query_synthesizer",
  "needs_review": false,
  "unmatched_reference_contexts": []
}
```

- `gold_chunk_ids` 是 IR 层标注：先按归一化全文精确匹配回填，失败再降级到包含匹配（概括式 reference 跨多个块时返回全部被包含的块 ID）。为空且 `needs_review: true` 的样本需人工补标。
- `reference_answer` 是 ragas 层的 ground truth（对应 `SingleTurnSample.reference`）。

## manifest.json（评估报告引用的溯源文件）

`{generated_at, entry_mode (internal|external), params（全部 CLI 参数）, corpus_stats {num_chunks, num_sources}, ragas_version, results {num_queries, gold_matched, needs_review, by_synthesizer}, stage_seconds {"1_corpus":…, "2_load_client":…, "3_knowledge_graph":…, "4_generate_queries":…, "5_backfill":…, "6_write":…}}`。每个基线留档一份，指标数字才能归因到具体语料+参数组合；`stage_seconds` 直接告诉你时间花在哪一段。

## perq.jsonl（ir_metrics.py --out-perq）

`{"query_id":"q0001","MRR":1.0,"Recall@5":0.5,...}` —— 逐条 IR 指标，combine_report 的联合输入之一。

## answers.jsonl（make_runs.py --answers 输入）

`{"query_id":"q0001","response":"被测系统给出的答案"}` —— 回填 responses.jsonl 的 response 字段。

## personas.json（build_evalset.py --personas 输入）

JSON 数组：`[{"name":"王工","role_description":"企业RAG后端工程师，关注检索链路…"}]`——用目标语言撰写即可控制问题 persona 前缀的语言与视角；提供后跳过 LLM persona 生成（省调用且消除英文污染）。

## chunks.jsonl

`{"chunk_id": "guide-0007", "source": "guide.md", "text": "…"}` —— 让被测索引器直接摄入这批块，保证索引里的 chunk_id 与评估集对齐。

## runs.jsonl（ir_metrics.py 的输入）——由被测检索系统产出

```json
{"query_id": "q0001", "chunk_ids": ["faq-0002", "guide-0007", "…"]}
```

按相关性从好到差排序，长度应 ≥ 最大评估 K。每行一个查询；允许缺 query（按"缺失"计数，不算 0 分）。

## responses.jsonl（ragas_eval.py 的输入）

```json
{"query_id": "q0001", "response": "…", "retrieved_contexts": ["文本1", "文本2"]}
```

`retrieved_contexts` 是块原文（用 chunks.jsonl 按 chunk_id 反查文本）。

## 指标可用性

IR 层（ir_metrics.py）：Recall@K、Precision@K、HitRate@K、MRR、NDCG@K（二值相关性）。

ragas 层（ragas_eval.py，走 `ragas.metrics.collections`）：
- `faithfulness` —— user_input、response、retrieved_contexts
- `answer_relevancy` —— user_input、response（构造还需 embeddings）
- `context_precision` —— user_input、reference、retrieved_contexts（需要 reference_answer）
- `context_recall` —— user_input、reference、retrieved_contexts（需要 reference_answer）
- `answer_correctness` —— user_input、response、reference（构造还需 embeddings）

## ragas 0.4.3 源码级注意点（已验证）

- `SingleTurnSample` 有 `reference_context_ids`/`retrieved_context_ids` 字段，但 TestsetGenerator 从不回填——build_evalset.py 靠"精确匹配 → 包含匹配"两级策略回填（合成器逐字复制 `node.properties["page_content"]`，所以该策略可靠）。
- `TestsetGenerator.generate_with_chunks(...)` 保留你自己的块边界；用 `run_config=RunConfig(max_workers=N)` 控制 transform 并发。
- `llm_factory(model, client=AsyncOpenAI(...), cache=DiskCacheBackend(cache_dir=...), **model_kwargs)`——kwargs 直达 chat 调用（temperature 等）；cache 让结构化调用跨进程复用（需 `pip install diskcache`）。`OpenAIEmbeddings` 有同样的 `cache=` 参数。
- 语料太小时多跳合成器会静默跳过（图谱无关系簇）——看 manifest 的 `results.by_synthesizer`，别信请求的 size。
- 指标类在 `ragas.metrics.collections`，`__init__` 收 `llm=`/`embeddings=`，调用方式 `await metric.ascore(**fields)`；0.4.x 已没有旧版小写实例（如 `ragas.metrics.faithfulness`）。通过 `base_url` 兼容任何 OpenAI 风格端点（含 Dashscope/Qwen compatible-mode）。
- 查询分布可通过 generate 调用的 `query_distribution=` 参数定制（默认混合单跳、多跳、推理）。
