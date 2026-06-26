---
name: research-logger
description: Research a topic via web search, auto-match a relevant GIF, and log results as a Bear note using a configurable template.
version: 1.0.0
author: openclaw
tags: [research, notes, bear, gif, productivity]
requires_bins: [grizzly, clawhub]
---

# Research Logger

Automates the research-logging workflow:
1. **Search** — Uses `web_search` / `web_fetch` to gather content on a topic.
2. **GIF Match** — Uses `gifgrep` to find a relevant GIF for visual context.
3. **Note Creation** — Fills the `notes/research_template.md` template and writes a Bear note via `grizzly`.

## Quick Start

```bash
bash scripts/research_logger.sh "quantum computing" "research,quantum"
```

## Script: `scripts/research_logger.sh`

| Argument | Required | Description |
|----------|----------|-------------|
| `$1` — topic | ✅ | Research topic (quoted) |
| `$2` — tags | ❌ | Comma-separated Bear tags (default: `research`) |

### What it does

1. Calls `web_search` for the topic, fetches top results.
2. Searches `gifgrep` for a matching GIF.
3. Reads `notes/research_template.md`, substitutes placeholders with gathered data.
4. Creates a Bear note with the rendered content and tags.

## Template

The template lives at `notes/research_template.md` (workspace root) and uses `{placeholder}` syntax:

| Placeholder | Source |
|-------------|--------|
| `{topic}` | CLI argument |
| `{date}` | Current date (YYYY-MM-DD) |
| `{tags}` | CLI argument |
| `{summary}` | LLM-generated summary of search results |
| `{finding1}` … `{finding3}` | Top 3 key findings |
| `{links}` | Source URLs from search |
| `{media_alt}` / `{media_url}` | GIF from gifgrep |
| `{action1}` … `{action3}` | Suggested action items |

## Requirements

- **grizzly** — Bear CLI (`go install github.com/tylerwince/grizzly/cmd/grizzly@latest`)
- **Bear** app running on macOS
- Internet access for search and GIF lookup
