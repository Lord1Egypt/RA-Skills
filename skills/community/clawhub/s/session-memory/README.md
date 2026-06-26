# Session Memory 🧠

Persistent memory toolkit for AI agents. Save context, recall insights, track decisions across sessions.

[![ClawHub](https://img.shields.io/badge/clawhub-session--memory-blue)](https://clawhub.com/skills/session-memory)

## Install

```bash
clawhub install session-memory
```

Or clone:

```bash
git clone https://github.com/voidborne-d/session-memory-skill.git
```

## Features

- **Relevance-scored search** — multi-keyword AND matching with importance + recency weighting
- **Importance levels** — low / normal / high / critical
- **Session context loader** — smart startup that loads recent + important memories
- **Topic consolidation** — group and review memories by topic
- **Export / Import** — backup and restore with deduplication
- **Memory stats** — totals, date range, avg/day, storage size, topic breakdown
- **Edit / Delete** — modify or remove entries by timestamp
- **Pure bash + node** — no npm dependencies

## Quick Start

```bash
# Save
./scripts/save.sh "decision" "Chose Postgres over SQLite" database
MEMORY_IMPORTANCE=high ./scripts/save.sh "insight" "Users prefer dark mode"

# Recall
./scripts/recall.sh "database"

# Session startup
./scripts/context.sh

# Stats
./scripts/stats.sh

# Weekly review
./scripts/consolidate.sh --since 2026-03-01
```

## Commands

| Command | Description |
|---------|-------------|
| `save.sh` | Save a memory with topic, content, tags, importance |
| `recall.sh` | Search with relevance scoring + filters |
| `context.sh` | Load session context (recent + important) |
| `daily.sh` | View memories for a specific day |
| `topics.sh` | List all topics with counts |
| `consolidate.sh` | Group and review by topic |
| `stats.sh` | Memory statistics |
| `edit.sh` | Edit or delete entries |
| `export.sh` | Export to JSON |
| `import.sh` | Import from JSON (deduplicates) |
| `prune.sh` | Archive old memories |

## Storage

JSONL files in `~/.agent-memory/YYYY/MM/DD.jsonl`:

```json
{"ts":1706793600000,"topic":"decision","content":"Chose X because Y","tags":["project"],"importance":"high"}
```

## Documentation

See [SKILL.md](./SKILL.md) for full documentation.

## License

MIT

---

*Created by [Voidborne](https://voidborne.org) 🔹*
