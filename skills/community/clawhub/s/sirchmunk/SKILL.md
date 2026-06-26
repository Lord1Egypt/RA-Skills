---
name: sirchmunk
description: Local file search using sirchmunk API. Use when you need to search for files or content by asking natural language questions.
---

# Sirchmunk Search

Simple local file search powered by LLM, no embedding-db, no indexing, no ETL.

## Tool: sirchmunk_search

**Single parameter:** `query` — your search question in natural language.

**Example:**
```bash
~/.openclaw/skills/sirchmunk/scripts/sirchmunk_search.sh "What is the RL agent's reward function?"
```

**Under the hood:**
```bash
curl -s -X POST "http://localhost:8584/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "<your query>",
    "paths": ["/path/to/search_paths"],
    "mode": "FAST"
  }'
```

Notes: The `paths` parameter requires pre-configuration as `SIRCHMUNK_SEARCH_PATHS` or inclusion as a search parameter.


## Prerequisites

1. Sirchmunk installed: `pip install sirchmunk`
2. Run `sirchmunk init`
3. Config: `~/.sirchmunk/.env`, `LLM_API_KEY`、`LLM_BASE_URL` and `LLM_MODEL_NAME` are required. `SIRCHMUNK_SEARCH_PATHS` is optional.
4. Server running: `sirchmunk serve`


## Homepage
https://github.com/modelscope/sirchmunk

