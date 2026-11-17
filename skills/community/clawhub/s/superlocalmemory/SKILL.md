---
name: superlocalmemory
description: Long-term memory for OpenClaw that stays on your computer. Recall past decisions and save new ones with SuperLocalMemory.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - slm
    homepage: https://superlocalmemory.com
---

# SuperLocalMemory

SuperLocalMemory (SLM) gives OpenClaw a memory that lasts across sessions and apps. Memories live in a SQLite database under `~/.superlocalmemory` on this computer. Nothing is sent anywhere unless the user turns on an optional cloud feature themselves.

The SLM engine is a separate open-source project (AGPL-3.0-or-later): https://github.com/qualixar/superlocalmemory. This skill only explains how to use it.

## Setup (once per computer)

1. Install the engine: `npm install -g superlocalmemory` (or `pipx install superlocalmemory`). This provides the `slm` command.
2. Connect OpenClaw: `slm connect openclaw`. This adds the `superlocalmemory` MCP server (command `slm`, argument `mcp`) under `mcp.servers` in `~/.openclaw/openclaw.json`. If that file uses JSON5 syntax, run instead: `openclaw mcp add superlocalmemory --command slm --arg mcp`.
3. Restart OpenClaw. Check the setup with `slm doctor`.

## When to recall

Before answering a question about the user's projects, preferences or earlier decisions, look it up first:
- MCP tool `recall` with a short natural-language query, or
- shell: `slm recall "what did we decide about the database"`

Use what comes back as context, and say so when an answer rests on a recalled memory.

## When to remember

Save things that will matter in a later session: a decision and its reason, a user preference, a fixed bug and its cause, a fact about the project.
- MCP tool `remember` with the content and optional `tags`, or
- shell: `slm remember "Chose Postgres over SQLite for multi-user writes" --tags decision,db`

Write each memory as one self-contained statement. Do not save secrets, passwords or API keys.

## Other useful commands

- `slm list` shows recent memories.
- `slm forget "<query>"` removes memories the user no longer wants.
- `slm dashboard` opens the local dashboard.
