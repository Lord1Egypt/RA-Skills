---
name: qmd-search
description: Query the local knowledge base (OpenClaw docs, skills, internal wikis) using the QMD hybrid search engine (BM25 + Vector + LLM Re-ranking). Use this for technical questions about the agent's own capabilities, available skills, or documentation.
---

# QMD Search

Access the local knowledge base at `/root/clawd/knowledge`.

## Usage

### Search (Hybrid)
Best for general queries. Combines keyword and semantic search with re-ranking.
```bash
qmd query "your query here"
```

### Search (Fast)
Keyword-only search. Use for exact phrases.
```bash
qmd search "exact phrase"
```

### Get Document
Read a specific document by path or docid (from search results).
```bash
qmd get "path/to/doc.md" --full
```

### Tips
- Use `--json` if you need structured output for processing.
- Use `--min-score 0.5` to filter noise.
- The knowledge base includes:
  - OpenClaw Documentation (`openclaw-docs/`)
  - Skill Definitions (`skills/`)
  - QMD Documentation (`qmd.md`)
