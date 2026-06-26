# Runtime Layout

Read this file when the user wants the skill to include runnable dependencies and a clearer implementation footprint.

## Goal

Separate the public skill from private data, while still making the runtime pieces explicit.

## Recommended generated layout

```text
retrieval/
  config/
    corpora.json
    agent_corpora.json
    agent_memory.json
    backend.json
  scripts/
    workspace_search.mjs
    build_index.py
    build_embeddings.mjs
    refresh_incremental.py
    retrieval_status.py
  indexes/
    workspace_retrieval.sqlite
```

## `backend.json` suggested shape

```json
{
  "version": 1,
  "embeddingProvider": "ollama",
  "embeddingModel": "nomic-embed-text",
  "embeddingEndpoint": "http://127.0.0.1:11434/api/embeddings",
  "sqlite": {
    "dbPath": "/ABSOLUTE/PATH/TO/WORKSPACE/retrieval/indexes/workspace_retrieval.sqlite",
    "requireFts5": true
  }
}
```

## Minimum runnable contract

A practical baseline implementation should provide:

- one keyword-capable SQLite database
- one configured embedding provider
- one wrapper command for agents
- one environment check step before indexing

## Cross-platform default

For portability, prefer:

- Python scripts for index build and maintenance
- Node wrapper for agent-facing query calls
- config-driven backend selection
- no shell-only dependency for the main workflow

## Important rule

When publishing publicly, include config templates and environment checks.
Do not include live indexes, real private paths, or machine-specific secrets.
