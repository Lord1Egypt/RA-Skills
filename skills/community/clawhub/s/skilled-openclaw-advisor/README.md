# skilled-openclaw-advisor

> Local FTS5 docs index for instant OpenClaw answers. No external API calls. Sub-10ms queries.

[![ClawHub](https://img.shields.io/badge/clawhub-skilled--openclaw--advisor-blue)](https://clawhub.com/seanford/skilled-openclaw-advisor)

An OpenClaw skill that builds a local full-text search index of all OpenClaw
documentation and queries it before answering any OpenClaw-related question.
No network calls, no token burn — just fast, accurate, authoritative answers
straight from the source.

## Install

```bash
clawhub install skilled-openclaw-advisor
```

## Setup (one-time)

```bash
python3 $SKILL_DIR/scripts/build_index.py
```

This builds the FTS5 SQLite index from your local OpenClaw docs. Data is stored in:

```
~/.openclaw/skills-data/skilled-openclaw-advisor/
```

See [SKILLS_DATA_CONVENTION.md](https://github.com/seanford/skilled-openclaw-advisor/blob/main/SKILLS_DATA_CONVENTION.md)
for rationale.

## Usage

Use this skill for any OpenClaw question — configuration, CLI, channels, providers, sessions, and troubleshooting.
You can also query it directly:

```bash
# Quick agent lookup
python3 $SKILL_DIR/scripts/query_index.py \
  --query "how do I configure cron jobs" --mode agent

# Human-readable
python3 $SKILL_DIR/scripts/query_index.py \
  --query "telegram channel setup"

# Chinese results
python3 $SKILL_DIR/scripts/query_index.py \
  --query "配置频道" --lang zh-CN

# Index status
python3 $SKILL_DIR/scripts/query_index.py --status

# What changed in last update
python3 $SKILL_DIR/scripts/query_index.py --diff
```

## Index Management

```bash
# Incremental update (checks for doc changes)
python3 $SKILL_DIR/scripts/update_index.py

# Force full re-index
python3 $SKILL_DIR/scripts/build_index.py --force
```

The `update_index.py` script is designed to run nightly (default: 5:30am via cron).

## Data Directory Convention

This skill follows the `skills-data/` convention — runtime data is stored separately
from skill code, keeping the package clean and publishable.

```
skills-data/skilled-openclaw-advisor/
├── index.db       # FTS5 SQLite index
├── state.json     # Last-indexed state
├── diffs/         # Change history per update run
└── versions/      # Previous doc snapshots
```

See [SKILLS_DATA_CONVENTION.md](SKILLS_DATA_CONVENTION.md) for the full standard.

## Languages

| Flag | Language |
|------|----------|
| `--lang en` | English (default) |
| `--lang zh-CN` | Simplified Chinese |

## License

MIT
