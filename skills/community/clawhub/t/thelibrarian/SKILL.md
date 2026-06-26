---
name: the-librarian
description: Build and search lightweight quantized document indexes with TurboVec. Use when you need to create searchable indexes from documents for RAG applications with minimal memory footprint, or when you need semantic search on resource-constrained hardware (Raspberry Pi, small VMs, edge devices). Triggers on phrases like "build a document index", "search my documents", "create a RAG system", "quantized vector search", "lightweight RAG", "document search on raspberry pi", "semantic search without FAISS".
---

# The Librarian

Lightweight document search with TurboVec quantization. Build semantic search indexes that run on minimal hardware.

**Author:** [RandTrad Consulting](https://www.randtradconsulting.com) — Document Intelligence for SMEs
**License:** MIT — Free for personal and commercial use with attribution

Lightweight document search with TurboVec quantization. Build semantic search indexes that run on minimal hardware.

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
├── bm25_index.pkl      # BM25 keyword index (if rank-bm25 installed)
└── stats.json          # Build statistics
```

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