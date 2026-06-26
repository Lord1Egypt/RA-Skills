---
name: session-reflect
description: Analyze Claude Code session history to generate self-observation journals, detect goal drift, and surface hidden behavioral patterns. Outputs to Obsidian Vault.
version: 0.2.0
tags: [self-reflection, obsidian, session-analysis, journaling, personal-growth]
author: yuiooo1102-droid
---

# Session Reflect

Turn your Claude Code conversation history into a mirror.

This skill extracts your messages from Claude Code sessions, syncs them into your Obsidian Vault, and generates self-observation journals that help you understand your own patterns, priorities, and blind spots.

## What It Does

| Command | Purpose | Data Range |
|---------|---------|------------|
| `/reflect` | Daily observation — what you're doing, how you're doing, emotional state | 1-3 days |
| `/reflect drift` | Goal drift detection — stated goals vs actual behavior | 7 days |
| `/reflect emerge` | Hidden pattern surfacing — unconscious preferences, avoidance patterns | 14 days |

Each command outputs a structured markdown file to your Obsidian Vault with observations **and actionable suggestions**.

## How It Works

```
Claude Code Sessions (.jsonl)
        ↓
  extract_sessions.py (incremental sync, dedup, sanitize)
        ↓
  Obsidian Vault / 对话记录 / (daily digests)
        +
  Your own notes in the Vault
        ↓
  Agent analyzes both sources
        ↓
  Obsidian Vault / 自我观察 / (reflection journals)
```

## Setup

### 1. Install

```bash
# Clone the repo
git clone https://github.com/yuiooo1102-droid/session-reflect.git ~/coding/session-reflect

# Or install as Claude Code command
mkdir -p ~/.claude/commands/reflect
cp commands/reflect/*.md ~/.claude/commands/reflect/
```

### 2. Initialize

```bash
python3 ~/coding/session-reflect/extract_sessions.py init
# You will be prompted to enter your Obsidian Vault path
```

### 3. Backfill History (Optional)

```bash
# By day
python3 ~/coding/session-reflect/extract_sessions.py backfill

# By week (recommended for long history)
python3 ~/coding/session-reflect/extract_sessions.py backfill --weekly
```

### 4. Use

```bash
# Sync new sessions (run before each reflect)
python3 ~/coding/session-reflect/extract_sessions.py sync

# Or just use the slash commands — they auto-sync
/reflect
/reflect drift
/reflect emerge
```

## Requirements

- Python 3.10+
- Claude Code (sessions stored in `~/.claude/projects/`)
- An Obsidian Vault (any location)

## Privacy

- All processing is local — no data leaves your machine
- API keys, tokens, JWTs, passwords are automatically redacted
- System prompts and boilerplate are filtered out
- Code blocks are replaced with `[CODE_BLOCK]` placeholders
- Messages are truncated at 2000 characters

## Vault Structure

```
Your_Vault/
├── 对话记录/           ← auto-synced session digests
│   ├── 2026-04-01.md
│   └── ...
├── 自我观察/           ← reflection outputs
│   ├── 2026-04-03-reflect.md
│   ├── 2026-04-03-drift.md
│   ├── 2026-04-03-emerge.md
│   └── 画像/
│       └── 2026-04-portrait.md  (monthly)
└── your own notes...   ← also analyzed
```

## Inspired By

- [Obsidian + Claude Code Codebook](https://www.youtube.com/watch?v=6MBq1paspVU) by Greg Isenberg & Internet Vin
- [session-retro](https://github.com/pwarnock/session-retro)
- [continuity](https://clawskills.sh/skills/riley-coyote-continuity)
