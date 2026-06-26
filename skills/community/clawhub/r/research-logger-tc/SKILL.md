---
name: research-logger
description: Research a topic via web search, auto-match a GIF, and log structured notes to Bear.
tags: [research, notes, bear, gif]
capabilities: [research, note_taking]
---

# Research Logger

Research a topic, find a matching GIF, and create a structured Bear note.

## Usage

When the user asks to research a topic and log it:

1. Run `bash research_logger.sh "<topic>" "<comma-separated-tags>"`
2. The script outputs a filled-in markdown note. Use `grizzly create` to save it to Bear.

### Example

```bash
# Step 1: Run the research script
bash research_logger.sh "quantum computing" "research,quantum"

# Step 2: Create the Bear note with the output
cat /tmp/research_note.md | grizzly create --title "Quantum Computing Research" --tag research
```

## How It Works

1. Uses `web_search` to find top results on the topic
2. Uses `gifgrep` to find a relevant GIF
3. Fills in the research template and writes to `/tmp/research_note.md`

## Dependencies

- OpenClaw agent (for `web_search` / `web_fetch` tool calls)
- `grizzly` CLI for Bear note creation
- `gifgrep` skill for GIF matching
