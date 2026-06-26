---
name: semantic-code-search
description: Semantic search engine for codebases that understands intent and finds functionally similar code. Use when searching code by meaning rather than text, finding similar implementations, discovering duplicate logic, or navigating unfamiliar codebases. Covers AST parsing, embedding generation, similarity search, and intent-based queries.
---

# Semantic Code Search

Find code by meaning, not just text. Search across codebases using natural language intent.

## Quick Start

```python
from code_search import CodeIndex, SemanticSearch

index = CodeIndex("/path/to/codebase")
index.build()  # Parse AST, generate embeddings

search = SemanticSearch(index)
results = search.query("how is authentication handled?")
results = search.similar_to("src/auth/login.py:validate_token")
```

## How It Works

1. **Parse** — Walk codebase, extract functions/classes with AST
2. **Embed** — Generate vector embeddings from code + docstrings
3. **Index** — Store in vector index with metadata (file, line, type)
4. **Search** — Query by intent or find similar code

## Search Types

- **Intent search**: "find error handling patterns" → returns matching code
- **Similarity search**: Given a function, find others doing the same thing
- **Structural search**: Find all functions matching a call pattern
- **Duplicate detection**: Find code doing the same thing differently

## CLI

```bash
python3 scripts/search.py index /path/to/codebase
python3 scripts/search.py query "database connection setup"
python3 scripts/search.py similar src/db/connect.py:10
python3 scripts/search.py duplicates
```
