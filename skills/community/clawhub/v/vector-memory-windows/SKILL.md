---
name: vector-memory-windows
description: Full memory stack for OpenClaw on Windows. Includes LanceDB semantic memory, git-notes decision memory, and memory hygiene workflow.
---

# Vector Memory (Windows)

Complete memory engineering bundle for OpenClaw.

## Included Modules

- `bundle/lancedb-memory`: semantic storage and retrieval backend
- `bundle/git-notes-memory`: branch-aware git-notes long-term memory
- `bundle/memory-hygiene`: cleanup and maintenance playbook

## Why use this bundle

- Works on Windows out of the box.
- Keeps compatibility with existing memory APIs.
- Provides both retrieval and governance, not only storage.

## Quick Start

1. Install LanceDB dependencies:

```bash
pip install -r bundle/lancedb-memory/requirements.txt
```

2. For semantic memory backend, import from:

- `bundle/lancedb-memory/final_memory.py`
- `bundle/lancedb-memory/clawdbot_memory.py`

3. For branch-aware memory:

```bash
python bundle/git-notes-memory/memory.py -p . sync --start
```

4. Apply hygiene recommendations from:

- `bundle/memory-hygiene/SKILL.md`

## Storage Defaults

- Windows: `D:\clawtest\memory\lancedb`
- Unix-like: `~/.clawdbot/memory/lancedb`

You can override with:

- `OPENCLAW_LANCEDB_PATH`
- `CLAWTEST_ROOT` (Windows)
