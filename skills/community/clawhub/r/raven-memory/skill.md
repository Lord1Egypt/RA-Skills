---
name: raven-memory
version: 1.0.1
description: >
  Persistent causal memory for AI agents. Raven records everything
  your agent does as a causally-linked chain, including decisions, tool calls,
  parallel work, and session history. Your agent finally remembers.
category: memory
exclusive: true
author: hahmed9800
license: Apache-2.0
tags: [memory, persistence, causal, local, privacy]
requirements:
  python: ">=3.10"
  packages:
    - raven-memory
mcp:
  command: raven-mcp
  args: []
  env:
    RAVEN_DB_PATH: "${HOME}/.raven/raven.db"
    RAVEN_N_RECENT: "10"
    RAVEN_N_SEARCH: "5"
---

# Raven Memory

Raven gives your OpenClaw agent persistent causal memory that
survives across sessions, days, and weeks.

## What it does

- Records every significant event as a node in a causal chain
- Loads relevant history at session start via semantic search
- Supports rollback, branching, and parallel task tracking
- Stores everything locally in ~/.raven/raven.db
- Encrypted at rest with SQLCipher (optional)

## Tools exposed

- `raven_start_session` — load context at conversation start
- `raven_record_event` — write an event to the chain
- `raven_end_session` — close session with notes
- `raven_search` — semantic search over full history
- `raven_rollback` — undo N steps
- `raven_get_status` — health check

## Setup

Install from PyPI:
```bash
pip install raven-memory
```

With semantic search (recommended):
```bash
pip install "raven-memory[vec]"
```

Then install this skill:
```bash
clawhub install raven-memory
```

Add to your OpenClaw system prompt:
```
At the start of every conversation, call raven_start_session with
the user's first message as search_query. Load the returned
summary/nodes into your context before responding. Record events with raven_record_event. End sessions with raven_end_session.
```
