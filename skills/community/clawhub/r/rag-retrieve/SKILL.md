---
name: rag-retrieve
version: 1.0.0
description: |
  Queries TiDB hybrid vector+BM25+metadata store for domain-relevant context.
  Supports version-aware filtering (critical for iOS — retrieving iOS 17 docs
  for iOS 26 questions is worse than no retrieval), multi-query expansion,
  and optional CoRAG (chain-of-retrieval) for multi-hop questions.
triggers:
  - always called by coding-orchestrator before generation
  - standalone for "find docs about X" queries
  - by decompose-plan when planning needs context
tools:
  - shell
  - file-system
  - llm
  - database
inputs:
  - query: task or question text
  - domain: "ios" | "web" | "python" | "trading" | "vc" | "general"
  - ios_version: target iOS version if ios domain (e.g. "26.0")
  - frameworks: list of frameworks to prioritize (e.g. ["SwiftData", "CloudKit"])
  - top_k: int, default 10 (more than 5 because M2.7 has generous context)
  - use_corag: bool, default false (enables chain-of-retrieval for multi-hop)
  - user_codebase: bool, default true (include user's own codebase chunks)
outputs:
  - chunks: list of retrieved passages with metadata
  - total_tokens: estimated token count of all chunks
  - query_expansions: the variant queries that were run
  - corag_trace: if use_corag, the retrieval steps taken
metadata:
  openclaw:
    category: coding
    tags:
      - coding
      - rag
      - retrieval
      - tidb
      - hybrid-search
    requires_openclaw: ">=2026.3.31"
    binaries:
      - python3
    python_packages:
      - pymysql
      - aiohttp
    env_vars:
      - OPENCLAW_LLM_ENDPOINT
      - TIDB_HOST
      - TIDB_PORT
      - EMBEDDING_ENDPOINT
      - RERANKER_ENDPOINT
---

# RAG Retrieve

## Architecture

```
Query
  ↓
Multi-query expansion (3-5 variants via Gemma 4)
  ↓
Parallel vector + BM25 + metadata search in TiDB
  ↓
Cross-encoder rerank (bge-reranker-v2-m3, local)
  ↓
Top-K chunks
  ↓ (if use_corag)
CoRAG controller: reason → retrieve again → accumulate
  ↓
Pack into context budget
```

## TiDB schema

```sql
CREATE TABLE knowledge_chunks (
    id BIGINT AUTO_RANDOM PRIMARY KEY,
    chunk_id VARCHAR(64) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    source TEXT NOT NULL,  -- 'apple_docs' | 'wwdc' | 'user_codebase' | 'blog' | etc.
    domain VARCHAR(32) NOT NULL,  -- 'ios' | 'web' | 'python' | 'trading' | 'vc'

    -- iOS-specific metadata
    ios_version_min VARCHAR(16),  -- '18.0', '26.0', NULL if not iOS
    ios_version_max VARCHAR(16),  -- null if current
    swift_version VARCHAR(16),
    framework_tags JSON,  -- ["SwiftData", "CloudKit"]
    deprecated BOOLEAN DEFAULT FALSE,
    deprecated_in VARCHAR(16),

    -- Chunking metadata
    chunk_type VARCHAR(32),  -- 'api_doc' | 'code_pattern' | 'user_code' | 'concept'
    parent_doc_id VARCHAR(64),
    chunk_index INT,

    -- Retrieval signals
    embedding VECTOR(1536),  -- voyage-code-3 or nomic-embed-text
    last_verified DATE,  -- for freshness filtering

    -- Full-text search
    FULLTEXT KEY content_fts (content) WITH PARSER NGRAM,
    VECTOR INDEX idx_embedding (embedding) USING HNSW,

    KEY idx_domain (domain),
    KEY idx_ios_version (ios_version_min, ios_version_max),
    KEY idx_framework (cast(framework_tags as char(128) array))
);
```

## Hybrid search query

```python
HYBRID_QUERY = """
SELECT
    chunk_id,
    content,
    source,
    domain,
    ios_version_min,
    ios_version_max,
    framework_tags,
    chunk_type,
    (
        0.55 * (1 - VEC_COSINE_DISTANCE(embedding, %(query_vec)s))
        + 0.30 * MATCH(content) AGAINST(%(query_text)s IN NATURAL LANGUAGE MODE) / 10
        + 0.15 * %(metadata_boost)s
    ) AS relevance
FROM knowledge_chunks
WHERE
    domain IN %(allowed_domains)s
    AND deprecated = FALSE
    AND (
        ios_version_min IS NULL
        OR ios_version_min <= %(target_ios)s
    )
    AND (
        ios_version_max IS NULL
        OR ios_version_max >= %(target_ios)s
    )
    AND (
        %(frameworks)s IS NULL
        OR JSON_OVERLAPS(framework_tags, %(frameworks)s)
    )
ORDER BY relevance DESC
LIMIT %(limit)s
"""
```

## Execution

```python
import asyncio
import json
from typing import List, Dict, Optional
import numpy as np
from pathlib import Path


async def rag_retrieve(
    query: str,
    domain: str = "general",
    ios_version: Optional[str] = None,
    frameworks: Optional[List[str]] = None,
    top_k: int = 10,
    use_corag: bool = False,
    user_codebase: bool = True,
):
    # 1. Multi-query expansion
    expansions = await _expand_query(query, domain, frameworks)

    # 2. Embed all variants
    query_vectors = await _embed_batch(expansions)

    # 3. Parallel hybrid search for each expansion
    allowed_domains = [domain, "general"]
    if user_codebase:
        allowed_domains.append("user_codebase")

    all_results = []
    for variant_text, variant_vec in zip(expansions, query_vectors):
        results = await _hybrid_search(
            query_text=variant_text,
            query_vec=variant_vec,
            allowed_domains=allowed_domains,
            target_ios=ios_version or "99.0",
            frameworks=frameworks,
            limit=top_k * 2,  # overfetch, dedup later
        )
        all_results.extend(results)

    # 4. Deduplicate by chunk_id
    unique = {}
    for r in all_results:
        cid = r["chunk_id"]
        if cid not in unique or r["relevance"] > unique[cid]["relevance"]:
            unique[cid] = r
    all_unique = list(unique.values())

    # 5. Cross-encoder rerank
    reranked = await _rerank(query, all_unique, top_k=top_k * 2)

    # 6. Optional CoRAG
    corag_trace = None
    if use_corag:
        final, corag_trace = await _corag_controller(
            query, reranked[:top_k], top_k, domain, ios_version, frameworks
        )
    else:
        final = reranked[:top_k]

    # 7. Estimate tokens
    total_tokens = sum(len(c["content"].split()) * 1.3 for c in final)

    return {
        "chunks": final,
        "total_tokens": int(total_tokens),
        "query_expansions": expansions,
        "corag_trace": corag_trace,
    }


# ── Multi-query expansion ────────────────────────────────────────────────────

async def _expand_query(query, domain, frameworks):
    """Generate 3-5 semantic variants of the query."""
    framework_hint = ", ".join(frameworks) if frameworks else "none specified"

    prompt = f"""Given this {domain} query, produce 4 semantic variants that
would retrieve complementary information.

Query: {query}
Frameworks: {framework_hint}

Variants should:
- Ask the same underlying question from different angles
- Use different vocabulary (if query says "how to do X", add "implementation
  of X", "example of X", "best practices for X")
- Include specific technical terms the original may have omitted

Output as JSON array of 4 strings. Include the original as the first entry.
Only the JSON, no explanation."""

    response = await llm.generate(
        prompt=prompt,
        model="gemma-4-26b-moe",  # fast router model handles this well
        temperature=0.3,
        max_tokens=400
    )

    try:
        variants = json.loads(response.strip().strip("`").strip("json").strip())
        return variants[:5]
    except Exception:
        # Fallback: just use the original query
        return [query]


# ── Embedding ────────────────────────────────────────────────────────────────

async def _embed_batch(texts):
    """Embed via local MLX nomic-embed-text or bge-m3."""
    import mlx.core as mx
    from mlx_lm import load

    # Assumes an embedding model is loaded globally
    # In practice, run a persistent MLX server and HTTP call it
    response = await shell.run(
        f"curl -X POST http://localhost:8888/embed "
        f"-H 'Content-Type: application/json' "
        f"-d '{json.dumps({\"texts\": texts})}'"
    )
    return json.loads(response.stdout)["embeddings"]


# ── TiDB hybrid search ───────────────────────────────────────────────────────

async def _hybrid_search(query_text, query_vec, allowed_domains,
                         target_ios, frameworks, limit):
    """Execute the hybrid query against TiDB."""
    from pymysql import connect

    conn = connect(
        host="127.0.0.1",
        port=4000,
        user="root",
        database="openclaw_rag",
    )

    cursor = conn.cursor(dictionary=True)

    # Convert embedding vector to TiDB VECTOR literal
    query_vec_str = "[" + ",".join(f"{v:.6f}" for v in query_vec) + "]"

    # Metadata boost calculation (domain match = 0.2, chunk_type match = 0.1)
    metadata_boost = 0.2 if len(allowed_domains) == 1 else 0.1

    params = {
        "query_vec": query_vec_str,
        "query_text": query_text,
        "metadata_boost": metadata_boost,
        "allowed_domains": tuple(allowed_domains),
        "target_ios": target_ios or "99.0",
        "frameworks": json.dumps(frameworks) if frameworks else None,
        "limit": limit,
    }

    cursor.execute(HYBRID_QUERY, params)
    results = cursor.fetchall()
    conn.close()

    return results


# ── Cross-encoder rerank ─────────────────────────────────────────────────────

async def _rerank(query, candidates, top_k):
    """Rerank candidates using bge-reranker-v2-m3 (local)."""
    if not candidates:
        return []

    pairs = [(query, c["content"][:512]) for c in candidates]

    # Call local reranker HTTP endpoint
    response = await shell.run(
        f"curl -X POST http://localhost:8889/rerank "
        f"-H 'Content-Type: application/json' "
        f"-d '{json.dumps({\"pairs\": pairs})}'"
    )
    scores = json.loads(response.stdout)["scores"]

    # Attach scores and sort
    scored = [
        {**c, "rerank_score": scores[i]}
        for i, c in enumerate(candidates)
    ]
    scored.sort(key=lambda x: x["rerank_score"], reverse=True)

    return scored[:top_k]


# ── CoRAG controller ─────────────────────────────────────────────────────────

async def _corag_controller(query, initial_chunks, top_k, domain,
                           ios_version, frameworks, max_hops=3):
    """
    Chain-of-retrieval for multi-hop questions.

    After first retrieval, ask the model: "do we have enough context to
    answer? if not, what follow-up would you retrieve?" Then retrieve that,
    accumulate, repeat.
    """
    trace = [{"hop": 0, "query": query, "retrieved_ids": [c["chunk_id"] for c in initial_chunks]}]
    accumulated = list(initial_chunks)

    for hop in range(1, max_hops + 1):
        # Ask the model if we need more
        ctx_summary = "\n\n".join(
            f"[{i+1}] {c['content'][:300]}"
            for i, c in enumerate(accumulated[:15])
        )

        decision_prompt = f"""Original question: {query}

Retrieved context so far:
{ctx_summary}

Question: Is the above context sufficient to answer the original question?

Respond with JSON:
- If sufficient: {{"sufficient": true}}
- If not: {{"sufficient": false, "follow_up_query": "specific follow-up question"}}

Only the JSON."""

        response = await llm.generate(
            prompt=decision_prompt,
            model="m27-jangtq-crack",
            temperature=0.1,
            max_tokens=200
        )

        try:
            decision = json.loads(response.strip().strip("`").strip("json").strip())
        except Exception:
            break  # Give up on CoRAG, use what we have

        if decision.get("sufficient"):
            break

        follow_up = decision.get("follow_up_query")
        if not follow_up:
            break

        # Retrieve for follow-up
        follow_up_vec = (await _embed_batch([follow_up]))[0]
        new_results = await _hybrid_search(
            query_text=follow_up,
            query_vec=follow_up_vec,
            allowed_domains=[domain, "general"],
            target_ios=ios_version or "99.0",
            frameworks=frameworks,
            limit=5,
        )

        # Dedup against what we already have
        existing_ids = {c["chunk_id"] for c in accumulated}
        new_unique = [r for r in new_results if r["chunk_id"] not in existing_ids]

        accumulated.extend(new_unique)
        trace.append({
            "hop": hop,
            "query": follow_up,
            "retrieved_ids": [c["chunk_id"] for c in new_unique]
        })

        if not new_unique:
            break  # No new info, stop

    # Final rerank against original query
    final = await _rerank(query, accumulated, top_k=top_k)
    return final, trace
```

## Ingestion (one-time setup)

You need to ingest your corpus into TiDB. Key sources:

```python
# From the training data collection script (collect_training_data.py):
# Use the same scraped docs but now embed and ingest

async def ingest_corpus(corpus_dir: Path):
    for jsonl_file in corpus_dir.rglob("*.jsonl"):
        with open(jsonl_file) as f:
            for line in f:
                doc = json.loads(line)
                # Chunk the document
                chunks = _chunk_document(doc)
                # Embed each chunk
                for chunk in chunks:
                    chunk["embedding"] = await _embed_batch([chunk["content"]])[0]
                    # Extract iOS version, frameworks from doc metadata
                    chunk["ios_version_min"] = doc.get("ios_version")
                    chunk["framework_tags"] = doc.get("frameworks", [])
                # Insert batch into TiDB
                await _insert_chunks(chunks)


def _chunk_document(doc):
    """Code-aware chunking via tree-sitter for Swift/Python, semantic for prose."""
    if doc.get("source") == "user_codebase" and doc.get("language") == "swift":
        return _chunk_swift_tree_sitter(doc["text"])
    if doc.get("source") == "user_codebase" and doc.get("language") == "python":
        return _chunk_python_ast(doc["text"])
    # Default: semantic chunking at heading/paragraph boundaries
    return _chunk_semantic(doc["text"], max_tokens=500)


def _chunk_swift_tree_sitter(source):
    """Use tree-sitter-swift to preserve function/struct/extension boundaries."""
    import tree_sitter_swift as tsswift
    import tree_sitter as ts

    parser = ts.Parser(ts.Language(tsswift.language()))
    tree = parser.parse(source.encode())

    chunks = []
    # Walk the tree, extract top-level declarations with their docs
    for node in tree.root_node.children:
        if node.type in ("function_declaration", "class_declaration",
                         "struct_declaration", "extension_declaration",
                         "enum_declaration", "actor_declaration"):
            # Include preceding comments
            start = node.start_byte
            prev = node.prev_sibling
            if prev and prev.type == "comment":
                start = prev.start_byte
            chunk_text = source[start:node.end_byte]
            chunks.append({"content": chunk_text, "chunk_type": "code_declaration"})

    return chunks
```

## Performance expectations

On M4 Max 128GB with TiDB running locally:
- Multi-query expansion: ~200ms (Gemma 4 26B on MBP M1)
- Embedding 4 query variants: ~100ms (nomic-embed-text local)
- TiDB hybrid search: ~50-200ms depending on corpus size
- Cross-encoder rerank of 40 candidates: ~400ms (bge-reranker-v2-m3 local)
- CoRAG 1 hop: +500ms (LLM decision + retrieval)

**Total**: ~1-2 seconds for non-CoRAG, 2-4 seconds with CoRAG.

## Context budgeting

Returns chunks with `total_tokens` so caller can make intelligent truncation
decisions. With M2.7 JANGTQ-CRACK at 180K context, you can easily fit 30K+
tokens of RAG context. But more isn't always better — the cross-encoder
rerank already picks the best chunks. Default top_k=10 is a reasonable
sweet spot.

For deep reasoning tasks where retrieval quality matters most: top_k=5,
use_corag=true.

For broad research where recall matters: top_k=20, use_corag=false.

## Integration

Called by:
- `coding-orchestrator` step 3
- `decompose-plan` to enrich planning context
- Standalone via "find docs about X"
