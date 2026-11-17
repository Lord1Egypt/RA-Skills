---
name: the-librarian
description: Build and search knowledge bases using Supabase (primary) or TurboVec (offline/resource-constrained). Use when you need to search conversations, knowledge entries, or contacts. Triggers on phrases like "search my knowledge", "what do we know about", "remember this", "build a knowledge base", "search my documents".
---

# The Librarian

Knowledge search and curation. Two backends: **Supabase** (primary, for conversations/knowledge) and **TurboVec** (secondary, for offline document RAG).

**Author:** [RandTrad Consulting](https://www.randtradconsulting.com) — Document Intelligence for SMEs
**License:** MIT — Free for personal and commercial use with attribution
**Version:** 1.1.0 — Security hardening (pickle removal, API URL safety checks)
**Security:** See [Security section](#security) for safe usage guidelines and vulnerability history

## Primary Backend: Supabase (Knowledge & Conversations)

Self-hosted Supabase on RandTradPC with pgvector for vector search.

### Connection
- **REST API:** http://host.docker.internal:8000
- **Service role key:** See `/home/endar/docker-stack/supabase/.env`
- **Dashboard:** http://localhost:8090

### Tables
- `conversations` — every WhatsApp message in/out, full-text search
- `conversation_embeddings` — pgvector 768-dim (nomic-embed-text)
- `knowledge_entries` — curated insights with categories (decision, preference, fact, procedure, contact, deadline, insight)
- `knowledge_links` — bidirectional relationships
- `contacts` — auto-populated from conversations

### Search Functions
```sql
-- Full-text search
SELECT * FROM search_conversations('GEM Construction', 20);

-- Vector similarity search
SELECT * FROM search_similar(embedding_vector, 0.5, 20);

-- Hybrid search
SELECT * FROM search_knowledge('density conversion tables', 20);

-- Graph relationships
SELECT * FROM get_related(42);  -- entry ID
SELECT * FROM get_knowledge_graph(100, 1);
```

### REST API Examples
```bash
# Full-text search
SERVICE_ROLE_KEY=$(grep SERVICE_ROLE_KEY /home/endar/docker-stack/supabase/.env | cut -d= -f2)
curl "http://host.docker.internal:8000/rest/v1/knowledge_entries?content=ilike.*GEM*&select=id,title,category" \
  -H "apikey: $SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SERVICE_ROLE_KEY"

# Category filter
curl "http://host.docker.internal:8000/rest/v1/knowledge_entries?category=eq.decision&select=id,title,content" \
  -H "apikey: $SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SERVICE_ROLE_KEY"
```

### Embedding Generation
- **Model:** nomic-embed-text:v1.5 (768-dim)
- **Endpoint:** http://host.docker.internal:11434/api/embeddings
- **Local, free, no API calls**

### Data Stats (updated 2026-07-21)
- 598 knowledge entries (fact, procedure, contact, insight, deadline, decision, preference)
- 844 conversations ingested (backfilled from session JSONL files)
- 3,955 auto-generated relationships

### Ingestion
- **Script:** `/home/endar/.openclaw/workspace/scripts/librarian-ingest.py`
- **Daily cron:** Runs at 20:05 Europe/Dublin, ingests last 2 days of WhatsApp conversations
- **Backfill:** `python3 scripts/librarian-ingest.py --backfill` to reprocess all session files
- **Dedup:** Checks existing message_ids before inserting

### Weekly Review Cron
- **Cron ID:** 86c46408-06ae-4845-87a2-f385a8c07211
- **Schedule:** Every Sunday 9am Europe/Dublin
- **Model:** ollama/glm-5.2:cloud
- **Delivery:** WhatsApp summary to Enda (+353876890914)
- **What:** Reviews knowledge entries, flags junk, merges duplicates, checks ingestion gaps
- **Commands:** Reply "purge" to remove flagged items, "keep" to retain

## Secondary Backend: TurboVec (Document RAG)

Use Supabase for knowledge and conversations. Use TurboVec only for:
- Offline document RAG (PDFs, tenders, BoQs)
- Resource-constrained hardware
- When you need quantized indexes (8-16x smaller than FAISS)

### When to Use Which

| Use Case | Backend |
|----------|--------|
| Search conversations | Supabase |
| Search knowledge entries | Supabase |
| "What do we know about X?" | Supabase |
| "Remember this" | Supabase |
| Document RAG (PDFs, tenders) | TurboVec |
| BoQ extraction pipeline | TurboVec |
| Offline/resource-constrained | TurboVec |

### TurboVec Quick Start

```bash
# Build index
cd /home/endar/.openclaw/workspace/skills/the-librarian
./scripts/librarian build /path/to/documents/ index/my_library

# Search
./scripts/librarian search "habit formation" index/my_library --hybrid --rerank
```

## Author

**RandTrad Consulting** — Document Intelligence consultancy for SMEs

- **Website:** https://www.randtradconsulting.com
- **Services:** AI Training, EU AI Act Compliance, Document RAG Systems

## What It Does

- Builds quantized vector indexes from Markdown/text documents
- Supports hybrid search (vector + BM25 keyword matching)
- Optional Flashrank reranking for improved accuracy
- Chunk expansion for surrounding context
- 8-16x smaller indexes than FAISS

## When to Use

| Use Case | Choose The Librarian |
|----------|---------------------|
| Resource-constrained hardware | ✅ Runs on Raspberry Pi, 512MB RAM |
| Personal knowledge base | ✅ Zero infrastructure |
| Embedded/offline deployment | ✅ No cloud, no database |
| 100K+ documents on limited hardware | ✅ Fits where FAISS doesn't |
| Medical/legal records | ❌ Use FAISS instead |
| Maximum accuracy required | ❌ Use FAISS + Flashrank |

**Accuracy:** ~97-98% of FAISS for 4-bit quantization. Top results may occasionally swap ranking.

## Quick Start

### Prerequisites

```bash
# Install BLAS library (required for TurboVec)
sudo apt install libblas3

# Create venv and install dependencies
cd /path/to/the-librarian
python3 -m venv venv
source venv/bin/activate
pip install turbovec numpy requests rank-bm25 flashrank
```

### Build an Index

```bash
# Using the wrapper (recommended)
./scripts/librarian build /path/to/documents/ index/my_library

# With options
./scripts/librarian build /path/to/docs/ index/my_library --bits 3 --chunk-size 800

# Direct Python
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libblas.so.3 \
  python scripts/build_index.py --input /path/to/docs/ --output index/my_library
```

### Search

```bash
# Pure vector search
./scripts/librarian search "habit formation" index/my_library

# Hybrid (vector + BM25)
./scripts/librarian search "habit formation" index/my_library --hybrid

# Hybrid + rerank (best accuracy)
./scripts/librarian search "habit formation" index/my_library --hybrid --rerank

# With context expansion
./scripts/librarian search "habit formation" index/my_library --hybrid --rerank --expand 1

# JSON output
./scripts/librarian search "habit formation" index/my_library --json
```

## Search Modes

| Mode | Time | Accuracy | Use Case |
|------|------|----------|----------|
| **Vector only** | ~130ms | Good | Semantic concepts, synonyms |
| **Hybrid** | ~140ms | Better | Combines semantic + exact keywords |
| **Hybrid + rerank** | ~320ms | Best | Maximum precision |

## Bit Width Options

| Bits | Compression | Accuracy | Use Case |
|------|-------------|----------|----------|
| 4-bit | 8x | ~97-98% | Default, best balance |
| 3-bit | 10.7x | ~95-96% | Tight memory |
| 2-bit | 16x | ~93-95% | Extreme compression |

## File Structure

```
the-librarian/
├── SKILL.md
├── scripts/
│   ├── librarian           # Wrapper script (handles LD_PRELOAD)
│   ├── build_index.py      # Build quantized index
│   └── search.py           # Search with hybrid + rerank
└── references/
    └── quantization.md     # How TurboVec compression works
```

## Index Files

After building, you'll have:

```
index/my_library/
├── library.qindex      # TurboVec quantized index
├── chunks.json         # Document chunks with metadata
├── bm25_index.json     # BM25 keyword index (JSON — safe, no code execution risk)
└── stats.json          # Build statistics
```

**Security:** BM25 index stored as JSON (not pickle) to prevent arbitrary code execution from untrusted index files. Legacy `bm25_index.pkl` files are detected but NOT loaded — rebuild indexes to migrate.

## Security

### Pickle Removal (v1.1 — July 2026)

Following ClawHub security audit, the following vulnerabilities were fixed:

- **Critical:** `pickle.load` on `bm25_index.pkl` removed. Pickle files can execute arbitrary code when loaded. BM25 index now stored as JSON (`bm25_index.json`). Legacy pickle files are detected but refused to load.
- **High:** Embedding API URL now checked against localhost. If a non-local API endpoint is configured, a privacy warning is displayed before any data is transmitted.
- **Medium:** SKILL.md now documents that document text and search queries are transmitted to the Ollama HTTP API for embedding generation.

### Safe Usage Guidelines

- Only load indexes you built yourself or received from a trusted source
- Always use a local Ollama instance (`localhost` or `host.docker.internal`) for sensitive documents
- Never share index directories — they contain full document text in `chunks.json`
- If you receive an index from someone else, ensure it uses `bm25_index.json` (not `.pkl`)
- The `--api` flag can point to any HTTP endpoint — verify the host before running

### Reporting Security Issues

Report vulnerabilities to randtradbusiness@gmail.com. Security fixes will be published on ClawHub.

## Accuracy Guidance

**For critical applications (medical, legal, financial):**

Use FAISS instead. The ~2-3% ranking variance in TurboVec is acceptable for personal knowledge bases, parts catalogs, and general document search, but not for applications where missing a result has consequences.

**For personal/team use:**

TurboVec is ideal. The accuracy difference is negligible for most queries, and the size savings enable deployment on hardware that couldn't run FAISS at all.

## Performance Comparison

| Metric | FAISS | TurboVec 4-bit |
|--------|-------|----------------|
| Cold query | ~150-165ms | ~150-165ms |
| Warm query | ~35-40ms | ~130-135ms |
| Pure search | ~10-12ms | ~10-15ms |
| Index size | 100% | ~7-12% |
| RAM required | High | Low |

Note: Both spend ~120-140ms generating embeddings via Ollama. The search difference is minimal.

## References

- `references/quantization.md` - Technical details on how TurboVec compression works

---

## Author

**RandTrad Consulting** — Document Intelligence consultancy for SMEs

- **Website:** https://www.randtradconsulting.com
- **Contact:** randtradbusiness@gmail.com
- **Services:** AI Training, EU AI Act Compliance, Document RAG Systems

Built by Enda Rochford — [RandTrad Consulting](https://www.randtradconsulting.com)

## License

MIT License — Free for personal and commercial use with attribution.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following condition:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.