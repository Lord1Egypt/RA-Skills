---
name: xhs-knowledge-retriever
description: Retrieve semantically relevant Xiaohongshu competitor-note chunks from a local RAG index built by xhs-knowledge-indexer.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: XHS_KNOWLEDGE_ROOT
        required: false
        description: Optional path to the canonical local XHS knowledge directory; when unset, the script infers the standard workspace path.
    homepage: https://github.com/catherinewu/xhs-knowledge-retriever
---

# XHS Knowledge Retriever

Query the competitor-note RAG index and get back the most relevant chunks.

## Run

From `workspace-xhs-agent/products/xhs-note-learning-cycle`:

```bash
python3 skills/xhs-knowledge-retriever/scripts/retrieve.py --query "有娃家庭怎么选沙发"
```

With options:

```bash
python3 skills/xhs-knowledge-retriever/scripts/retrieve.py \
  --query "有娃家庭怎么选沙发" \
  --top-k 5 \
  --output /tmp/retrieved.json
```

Check local readiness without running retrieval:

```bash
python3 skills/xhs-knowledge-retriever/scripts/retrieve.py --check-only
```

Runtime Python packages:

- `numpy`
- `sentence-transformers`

The script does not require API credentials. If the standard workspace layout is
not available, set `XHS_KNOWLEDGE_ROOT` to the local `knowledge/xhs` directory.

## What it consumes

- [Canonical Competitor RAG Storage](docs/KNOWLEDGE_CONTRACT.md) (`index.json`)
- [Canonical Competitor RAG Storage](docs/KNOWLEDGE_CONTRACT.md) (`embeddings.npy`)
- [Canonical Competitor RAG Storage](docs/KNOWLEDGE_CONTRACT.md) (`metadata.jsonl`)

## What it produces

- JSON with the query, model, and top-k results including:
  - `score` (cosine similarity)
  - `chunk` (the retrieved text)
  - `metadata` (competitor name, note title, note URL, title pattern, content signals, etc.)

## Rules

1. Read only. It only queries the local index.
2. Planner/Writer should call this before making creative decisions.
3. Retrieved chunks are inspiration, not copy sources.
4. Do not publish competitor text verbatim.
