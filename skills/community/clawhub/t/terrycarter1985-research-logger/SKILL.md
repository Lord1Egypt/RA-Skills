---
name: research-logger
version: 1.0.0
description: Research a topic via web search, auto-match a GIF with gifgrep, and log structured notes to Bear using a customizable template.
author: openclaw
tags: [research, notes, bear, gif, productivity]
metadata:
  openclaw:
    requires:
      bins: [grizzly, gifgrep]
    install:
      - id: go
        kind: go
        module: github.com/tylerwince/grizzly/cmd/grizzly@latest
        bins: [grizzly]
        label: Install grizzly (go)
capabilities: [web_search, note_taking, media_search]
---

# Research Logger

Automate the full research workflow: web search → extract findings → match a GIF → write a Bear note from a template.

## Quick Start

```bash
./research_logger.sh "Quantum Computing" "research,tech,qc"
```

## How It Works

1. **Web Search** — Searches the web for the given topic and extracts the top 3 results (URLs + snippets).
2. **Content Fetch** — Fetches the top result for a deeper summary.
3. **GIF Match** — Calls `gifgrep` with the topic to find a relevant animated GIF.
4. **Template Fill** — Reads `notes/research_template.md` (or uses an inline default) and replaces all `{placeholder}` tokens with the gathered data.
5. **Bear Note** — Creates a structured Bear note with tags via `grizzly create`.

## Requirements

| Tool      | Purpose              | Install                                         |
|-----------|----------------------|-------------------------------------------------|
| grizzly   | Bear note CLI        | `go install github.com/tylerwince/grizzly/...`  |
| gifgrep   | GIF search           | Via gifgrep skill                               |
| web_search| Web search (OpenClaw)| Built-in                                        |
| web_fetch | Page content fetch   | Built-in                                        |

## Template

Place your template at `notes/research_template.md` in the workspace root. Supported placeholders:

| Placeholder   | Filled With                     |
|---------------|---------------------------------|
| `{topic}`     | Research topic                  |
| `{date}`      | Current date/time               |
| `{tags}`      | Comma-separated tags            |
| `{summary}`   | Summary from top search result  |
| `{finding1-3}`| Snippets from top 3 results     |
| `{links}`     | Bulleted source links           |
| `{media_alt}` | GIF description                 |
| `{media_url}` | GIF URL                         |
| `{action1-3}` | Suggested action items          |

## Environment

- `WORKSPACE` — Workspace root (default: `$HOME/.openclaw/workspace`)
- `TEMPLATE_PATH` — Relative path to template (default: `notes/research_template.md`)