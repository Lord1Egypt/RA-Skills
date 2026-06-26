---
name: shared-memory-stack
description: >
  Complete reference for the shared memory architecture connecting Claude Code,
  OpenClaw/Kimi, and LM Studio subagents through Obsidian vault + MemPalace (ChromaDB).
  Load this skill to understand how to read, write and search shared memory, capture
  ideas, and communicate between agents. Covers: vault structure, mempalace setup,
  capture-idea pipeline, openclaw-bridge, and inter-agent communication.
version: "1.0.0"
author: "nerua1"
license: "MIT"
compatible-with: claude-code, openclaw
tags: [memory, obsidian, mempalace, rag, inter-agent, capture, shared-memory]
---

# shared-memory-stack

Shared memory architecture for a multi-agent system: Claude Code + OpenClaw/Kimi + LM Studio.
No idea gets lost. All agents read and write the same memory.

## Architecture overview

```
┌─────────────────────────────────────────────────────┐
│                    SHARED MEMORY                     │
│                                                      │
│  Obsidian vault (structural)                         │
│  /Volumes/2TB_APFS/openclaw-data/workspace/          │
│    obsidian-memory/                                  │
│    ├── wiki/        ← MOCs, documentation            │
│    ├── daily/       ← session logs, daily notes      │
│    ├── answers/     ← resolved Q&A                   │
│    ├── source/      ← raw research, clips            │
│    └── ideas/       ← captured ideas (searchable)   │
│                                                      │
│  MemPalace (semantic / ChromaDB)                     │
│  /Volumes/2TB_APFS/openclaw-data/workspace/          │
│    memory/palace/   ← vector index (25 drawers)     │
└─────────────────────────────────────────────────────┘
         ▲                        ▲
         │ reads/writes           │ mines vault
  ┌──────┴──────┐         ┌───────┴───────┐
  │  OpenClaw   │◄───────►│  Claude Code  │
  │  (Kimi)     │ bridge  │  (this agent) │
  └──────┬──────┘         └───────────────┘
         │
  ┌──────┴──────┐
  │  LM Studio  │
  │  subagents  │
  └─────────────┘
```

## Key paths

| What | Path |
|------|------|
| Obsidian vault | `/Volumes/2TB_APFS/openclaw-data/workspace/obsidian-memory/` |
| Ideas dir | `/Volumes/2TB_APFS/openclaw-data/workspace/obsidian-memory/ideas/` |
| MemPalace palace | `/Volumes/2TB_APFS/openclaw-data/workspace/memory/palace/` |
| mempalace.yaml | `/Volumes/2TB_APFS/openclaw-data/workspace/obsidian-memory/mempalace.yaml` |
| Python 3.12 venv | `/Volumes/2TB_APFS/openclaw-data/workspace/memory/mempalace-venv/` |
| capture-idea script | `/Volumes/2TB_APFS/openclaw-data/workspace/scripts/capture-idea.sh` |
| capture-idea binary | `/opt/homebrew/bin/capture-idea` |
| OpenClaw skills | `/Volumes/2TB_APFS/openclaw-data/workspace/skills/` |
| Claude Code skills | `~/.claude/skills/vault/` |

---

## 1. MemPalace setup

### Why Python 3.12 venv

macOS ships Python 3.14 which breaks `chromadb` (pydantic v1 incompatibility).
MemPalace runs in a dedicated Python 3.12 venv.

```
/opt/homebrew/bin/mempalace   ← wrapper (zsh)
  → VENV/bin/mempalace --palace PALACE "$@"
```

The wrapper auto-injects `--palace` so no flag needed in daily use.

### Mining vault into palace

```bash
# Mine entire vault (run after adding new files)
mempalace mine /Volumes/2TB_APFS/openclaw-data/workspace/obsidian-memory/ --wing obsidian_memory

# Dry run first
mempalace mine ... --dry-run

# Status
mempalace status
```

### Searching

```bash
# Semantic search
mempalace search "oauth token expiry mobile"

# Search by topic/tag (frontmatter grep)
grep -r "topic: bezpieczenstwo" obsidian-memory/ideas/ -l
grep -r "tags:.*oauth" obsidian-memory/ideas/ -l

# Search by date range
ls obsidian-memory/ideas/2026-04-*.md
```

### Rooms

| Room | Source dir | Keywords |
|------|-----------|----------|
| `documentation` | `wiki/` | documentation, wiki |
| `daily` | `daily/` | daily |
| `ideas` | `ideas/` | idea, pomysl, insight, problem |
| `answers` | `answers/` | answers |
| `general` | (fallback) | — |

---

## 2. Capture pipeline

Every valuable idea, observation, or problem from any agent session → saved to vault → indexed in MemPalace.

### From CLI (any agent)

```bash
capture-idea \
  --title "OAuth token expiry zbyt krótki na mobile" \
  --topic bezpieczenstwo \
  --tags "oauth,token,mobile,auth" \
  --body "Tokeny wygasają po 1h, użytkownicy mobilni są wylogowywani." \
  --source openclaw   # or: claude-code | lmstudio | manual
```

**Simple mode:**
```bash
capture-idea "Krótki opis idei"
```

### From Claude Code

```
/capture problem z oauth tokenami wygasającymi za szybko na mobile
```

### Idea file format

```markdown
---
date: 2026-04-12
source: openclaw
topic: bezpieczenstwo
tags: [oauth, token, mobile]
related: []
status: seedling
---

# Tytuł

Treść...
```

**Topic values:** `architektura` | `bezpieczenstwo` | `ux` | `performance` | `integracja` | `ai` | `devops` | `dane` | `inne`

**Status values:** `seedling` → `growing` → `mature`

Files land in: `obsidian-memory/ideas/YYYY-MM-DD-slug.md`
Auto-mined into MemPalace after each capture.

---

## 3. Inter-agent communication

Claude Code and OpenClaw communicate via the local OpenClaw gateway (port 18789).

### Claude Code → OpenClaw

```bash
openclaw agent --message "Twoja wiadomość" --agent main --json
```

Parse response:
```bash
openclaw agent --message "..." --agent main --json | python3 -c "
import json, sys
d = json.load(sys.stdin)
for p in d['result']['payloads']:
    if p.get('text'): print(p['text'])
"
```

### Claude Code skill: openclaw-bridge

Load with `/skill openclaw-bridge` or invoke directly:
```
/ask-openclaw Czy ta migracja SQL jest bezpieczna?
```

### OpenClaw → Claude Code

OpenClaw writes to shared vault/files. Claude Code reads on next session via memory files at:
`~/.claude/projects/-Volumes-2TB-APFS/memory/`

---

## 4. Publishing skills

Both agents publish to GitHub under `nerua1`. SSH key and `gh` are configured.

```bash
# Claude Code skills
cd ~/.claude/skills/vault/SKILL_NAME
git init && git add . && git commit -m "feat: SKILL_NAME v1.0.0"
gh repo create SKILL_NAME --public --source . --remote origin --push

# OpenClaw skills
/publish-skill SKILL_NAME
```

**Configured:**
- SSH key: `~/.ssh/github_nerua1` (added to github.com/nerua1)
- `gh` authenticated as `nerua1`
- `git config`: user.name=nerua1, user.email=neru_a1@icloud.com

---

## 5. Quick reference

```bash
# Health check
mempalace status
openclaw health

# Mine vault after changes
mempalace mine /Volumes/2TB_APFS/openclaw-data/workspace/obsidian-memory/ --wing obsidian_memory

# Capture idea
capture-idea --title "..." --topic ai --tags "..." --body "..."

# Search memory
mempalace search "keyword"

# Ask OpenClaw
openclaw agent --message "..." --agent main --json

# Publish a skill
gh repo create SKILL_NAME --public --source . --remote origin --push
```

---

## 6. Known constraints

| Issue | Workaround |
|-------|-----------|
| Python 3.14 breaks chromadb | Use `/opt/homebrew/bin/mempalace` wrapper (Python 3.12 venv) |
| mempalace skips symlinks | Mine real vault path, not sources/obsidian/ symlink dir |
| OpenClaw gateway loopback only | Communication only works on same machine |
| Claude Code has no persistent process | Shared state via filesystem only |
