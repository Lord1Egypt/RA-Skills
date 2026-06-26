---
name: lancedb-memory
description: Cross-platform LanceDB memory backend for OpenClaw. Supports Windows/macOS/Linux with configurable DB path and async provider interface.
---

# LanceDB Memory (Windows-ready)

Use this skill for long-term memory storage and retrieval in OpenClaw/Clawdbot.

## What this skill provides

- Cross-platform path handling (Windows/macOS/Linux)
- Persistent memory table in LanceDB
- Text retrieval API compatible with existing memory hooks
- Async provider (`search` / `add` / `get_recent`) for OpenClaw plugins

## Install dependencies

Run in your project environment:

```bash
pip install lancedb pandas pyarrow
```

## Storage path

Default path logic:

- Windows: `D:\clawtest\memory\lancedb`
- macOS/Linux: `~/.clawdbot/memory/lancedb`

Override with:

- `OPENCLAW_LANCEDB_PATH` (highest priority)
- `CLAWTEST_ROOT` (Windows base directory)

## Python API

```python
from final_memory import add_memory, search_memories, get_all_memories

mid = add_memory("Use GLM embeddings for semantic recall", {"type": "decision"})
hits = search_memories("GLM", limit=5)
all_items = get_all_memories()
```

## Async provider API (for OpenClaw integration)

```python
from clawdbot_memory import memory_provider

results = await memory_provider.search("OpenClaw", limit=10)
memory_id = await memory_provider.add("Important preference", {"importance": 0.9})
recent = await memory_provider.get_recent(limit=20)
```

## Notes

- This implementation keeps behavior stable with the original skill: add, query, list.
- Retrieval is text-based by default (robust and dependency-light).