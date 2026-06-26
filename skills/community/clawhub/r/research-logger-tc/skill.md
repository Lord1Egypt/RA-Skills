---
name: research-logger
version: 1.0.0
description: Research a topic via web search, auto-match a GIF, and log structured notes to Bear.
author: ClawdBot
tags: [research, notes, bear, gif]
requires_bins: [grizzly, clawhub]
---

# Research Logger

Research a topic, find a matching GIF, and create a structured Bear note from a template.

## Quick Start

```bash
bash research_logger.sh "quantum computing" "research,quantum"
```

## How It Works

1. **Web Search** — Uses `web_search` (via OpenClaw tool) to gather top results on the given topic.
2. **GIF Match** — Calls `gifgrep` to find a relevant GIF for visual flair.
3. **Bear Note** — Fills in `notes/research_template.md` and creates a note in Bear via `grizzly`.

## Files

- `research_logger.sh` — Main script (called by the agent)
- `references/research_template.md` — Note template (mirrors workspace `notes/research_template.md`)

## Dependencies

- OpenClaw agent (for `web_search` / `web_fetch` tool calls)
- `grizzly` CLI (Bear notes)
- `gifgrep` skill (GIF search)
