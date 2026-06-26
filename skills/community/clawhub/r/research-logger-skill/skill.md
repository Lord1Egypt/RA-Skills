---
name: research-logger
description: Research a topic via web search, auto-match a relevant GIF, and log structured notes to Bear using a configurable template.
version: 1.0.0
author: clawd
tags: [research, notes, bear, gif, productivity]
requires_bins: [grizzly]
requires_env: []
requires_config: []
---

# Research Logger

Automate the research-to-notes pipeline: search the web, fill in a structured template, find a relevant GIF, and save it all as a Bear note.

## Usage

```bash
bash research_logger.sh "quantum computing" "tech,science"
```

## What It Does

1. **Web Search** — Uses `web_search` to find top results for the topic
2. **Content Fetch** — Pulls key content from the top result
3. **GIF Match** — Searches for a relevant GIF via gifgrep
4. **Template Fill** — Fills `notes/research_template.md` with gathered data
5. **Bear Note** — Creates a Bear note with the filled template via `grizzly`

## Requirements

- `grizzly` CLI (Bear notes)
- OpenClaw agent with `web_search`, `web_fetch`, and `gifgrep` access
