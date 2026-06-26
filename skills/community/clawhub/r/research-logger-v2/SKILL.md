---
name: research-logger
description: Research a topic via web search, auto-match a related GIF, and log structured notes to Bear using a customizable template.
version: 1.0.0
author: ClawdBot
tags: [research, notes, bear, gif, productivity]
capabilities: [web_research, note_taking, media_discovery]
requires_bins: [grizzly]
requires_env: []
---

# Research Logger

Automates the full research-to-notes pipeline:

1. **Web Search** → gather top sources on a topic
2. **Content Fetch** → extract key findings from top results
3. **GIF Match** → find a relevant GIF via gifgrep
4. **Template Fill** → populate `notes/research_template.md`
5. **Bear Note** → write the finished note via `grizzly`

## Usage

```bash
bash research_logger.sh "quantum computing trends" --tags "tech,quantum,2026"
```

### Arguments

| Arg | Required | Description |
|-----|----------|-------------|
| topic | ✅ | Research topic (quoted string) |
| --tags | ❌ | Comma-separated tags for Bear note |

### What it does

1. Runs `web_search` via OpenClaw tools for the topic
2. Fetches the top 3 results and extracts summaries
3. Calls `gifgrep` to find a matching GIF
4. Fills the template at `notes/research_template.md`
5. Creates a Bear note with `grizzly create`

## Requirements

- **grizzly** CLI installed and Bear app running
- OpenClaw agent session (provides web_search, web_fetch, gifgrep tools)
- Template file at `notes/research_template.md`

## Notes

- The script is designed to be called by an OpenClaw agent turn, not standalone
- If gifgrep returns no results, the GIF section is omitted
- Template placeholders: {topic}, {date}, {tags}, {summary}, {finding1-3}, {links}, {media_alt}, {media_url}, {action1-3}