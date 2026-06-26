---
name: segundo
description: |
  CLI tool for capturing and retrieving thoughts as a second brain. Stores memories as daily markdown journals with optional semantic search.

  USE FOR:
  - Capturing thoughts, notes, ideas, recommendations
  - Searching memories by text or semantic similarity
  - Listing and filtering memories by date range or tags
  - Importing/exporting notes, viewing brain statistics

  Requires: bun or npm. Semantic search requires an embedding provider (Ollama or OpenAI).
---

# segundo CLI

A zero-friction second brain CLI. Captures thoughts as daily markdown journals with tags and semantic search. Built with TypeScript, runs on Bun.

Run `segundo --help` for usage details.

## Workflow

1. **Init** - Create a brain first with `segundo init`
2. **Capture** - Add thoughts with `segundo add "thought"`
3. **Retrieve** - Search or list memories

| Need | Command | When |
|---|---|---|
| Create brain | `segundo init` | First time setup |
| Capture thought | `segundo add "thought" [--tag foo]` | Have something to remember |
| Search | `segundo search "query"` | Find a specific memory |
| List recent | `segundo list [--limit N]` | Browse recent memories |
| Stats | `segundo stats` | See brain overview |

## Commands

### init

```bash
segundo init
segundo init --reindex   # Rebuild embedding index
```

### add

```bash
segundo add "read Designing Data-Intensive Applications" --tag book
segundo add "line one\nline two"
segundo add "thought one" "thought two" "thought three"   # batch
echo "thought from pipe" | segundo add                     # stdin
cat notes.txt | segundo add --batch                        # split on blank lines
```

### search

```bash
segundo search "restaurant"
segundo search "data" --limit 5 --from 2026-01-01
```

Uses semantic search when an embedding provider is configured, falls back to text search otherwise.

### list

```bash
segundo list
segundo list --limit 5
segundo list --tag book
segundo list --from 2026-03-01 --to 2026-03-10
```

### edit

```bash
segundo edit <id> "new content"
segundo edit id1 "content1" id2 "content2"   # batch
```

### delete

```bash
segundo delete <id>
segundo delete id1 id2 id3
```

### import

```bash
segundo import notes.md
segundo import ./notes-dir/ --tag imported
segundo import file.txt --dry-run
```

### export

```bash
segundo export
segundo export --format json
segundo export --from 2026-03-01 --to 2026-03-10 --tag book
```

### stats

```bash
segundo stats
```

Shows total memory count, date range, top tags, embedding index size, and brain path.

## Tags

Tags go on the last line of an entry. Add via `--tag` flag or inline:

```bash
segundo add "great chapter on consistency\n#book #engineering"
segundo add "lunch spot" --tag food
```

## Filtering

All list/search/export commands support:
- `--tag <name>` - filter by tag
- `--from <DATE>` - start date (inclusive)
- `--to <DATE>` - end date (inclusive)
- `--limit <N>` - max results

## Profiles

```bash
segundo --profile work add "quarterly review notes"
segundo --profile personal list
segundo --brain /custom/path list
```

## JSON Output

All commands support `--json` for structured output:

```bash
segundo list --json
segundo add "thought" --json
segundo search "query" --json
```

## Storage

Memories live in `~/.segundo/memories/` as daily markdown files:

```
~/.segundo/
  config.json
  memories/
    2026-03-10.md
  embeddings/
    index.bin
    meta.json
```

## Semantic Search Setup

Configure in `~/.segundo/config.json`:

```json
{
  "embeddings": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "ollamaUrl": "http://localhost:11434"
  }
}
```

Supports **Ollama** (local, free) and **OpenAI** (cloud, requires `openaiApiKey` or `$OPENAI_API_KEY`).
