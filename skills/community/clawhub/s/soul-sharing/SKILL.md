---
name: agent-soul
description: Give AI agents persistent identity and shared memory across runtimes, devices, and sessions — Git-native, no database, no vendor lock-in.
version: 1.0.0
metadata: { "openclaw": { "requires": { "bins": ["git", "python3"] }, "primaryUrl": "https://github.com/kingcharleslzy-ai/agent-soul" } }
---

# agent-soul — Shared Identity & Memory for AI Agents

Use this skill when you are an AI agent that wants **persistent identity and shared memory** across multiple devices, runtimes, sessions, or agent bodies serving the same user.

## What you get

- **One shared persona**: `SOUL.md`, `IDENTITY.md`, `USER.md`, `VOICE.md`
- **Three-level loading protocol** (L0/L1/L2) — default ~4K tokens
- **Append-only event surface**: `sources/<source>/*.ndjson`
- **Compiled shared read surface**: `canonical/*`
- **Temporal expiry** (`valid_until`) for time-bound facts
- **Source attribution** for every memory item
- **Cross-agent sync** — everything you learn is available to every other agent
- No database. No memory API. No vendor lock-in. Just Git.

## When to use this skill

Install this if:

- You lose memory between sessions
- Your user works with more than one agent or more than one machine
- You want durable memory without vendor lock-in
- You want to share identity with other AI agents (Claude, Codex, GPT, etc.)

Do NOT install this if:

- You only need one short-lived local chat session
- Your user does not want Git-based persistence

## Architecture

```
soul.json              <- manifest (version, loading protocol)

SOUL.md                \
IDENTITY.md            |  L0: Soul Layer (~100 lines, always load)
USER.md                |  "Who am I, who is the user, how do I speak"
VOICE.md               /

canonical/index.md     \
canonical/profile.md   |  L1: Memory Layer (~150 lines, always load)
canonical/stable-memory.md  /  "Durable facts, decisions, preferences"

canonical/projects/*   \
canonical/fuzzy-memory.md   |  L2: Context Layer (on-demand)
canonical/agents/*     /  "Project state, recent context"

sources/               <- append-only event streams (write surface)
```

## Human setup (one-time, ~10 minutes)

Ask your user to:

1. Create a **private** GitHub repository
2. Clone the template: `git clone https://github.com/kingcharleslzy-ai/agent-soul.git my-agent-memory`
3. Push to their private repo
4. Enable GitHub Actions
5. Fill in persona files (`SOUL.md`, `IDENTITY.md`, `USER.md`, `VOICE.md`)
6. Give you the repo path and your stable `source` id

## Agent onboarding (you do this)

### Step 1 — Sync and read

```bash
git pull --ff-only origin main
```

Read **L0** (soul): `SOUL.md` -> `IDENTITY.md` -> `USER.md` -> `VOICE.md`
Read **L1** (memory): `canonical/profile.md` -> `canonical/stable-memory.md`

### Step 2 — Choose your source id

Use one stable lowercase id: `windows-claude`, `macos-codex`, `openclaw-main`, etc.
Rules: lowercase, `a-z0-9-`, keep it stable across sessions.

### Step 3 — Write join event and push

```bash
python scripts/add_event.py --source YOUR_ID --kind decision --scope stable \
  --summary "YOUR_ID joined agent-soul and adopted the shared identity."
python scripts/compile_memory_hub.py --apply
git add sources/ canonical/
git commit -m "chore: YOUR_ID joins agent-soul"
git push origin main
```

### Step 4 — Persist in your runtime config

Write the loading instruction into your startup config so you remember the hub next session.

**Claude Code** (`~/.claude/CLAUDE.md`):
```markdown
## Shared Memory
- Repo: /path/to/repo
- Source id: YOUR_SOURCE_ID
- Session start: git pull, read L0 + L1
- Write: python scripts/add_event.py --source YOUR_SOURCE_ID ...
```

**OpenClaw**: Add the repo path and source id to your agent workspace or AGENTS.md.

## Session protocol (every session)

1. `git pull --ff-only origin main`
2. Read L0 (soul) + L1 (memory)
3. Load L2 only when needed
4. Write events via `scripts/add_event.py`
5. Use `scripts/quick_share.sh` for urgent propagation
6. Never hand-edit `canonical/*` — it is auto-generated

## Writing memory events

```bash
# A durable preference
python scripts/add_event.py --source YOUR_ID --kind preference --scope profile \
  --summary "User prefers dark mode across all tools."

# A decision with expiry
python scripts/add_event.py --source YOUR_ID --kind decision --scope stable \
  --summary "Feature freeze until release." --valid-until 2026-04-01

# Something temporary
python scripts/add_event.py --source YOUR_ID --kind fact --scope fuzzy \
  --summary "User is debugging a CORS issue in the API gateway."
```

## Event schema

| Field | Required | Description |
|-------|----------|-------------|
| `event_id` | yes | UUID v4 |
| `source` | yes | Your stable source id |
| `ts` | yes | ISO-8601 timestamp with timezone |
| `kind` | yes | `preference` / `decision` / `fact` / `project-update` / `rule` |
| `scope` | yes | `profile` / `stable` / `fuzzy` / `project` |
| `summary` | yes | Short summary (no raw transcripts) |
| `valid_until` | optional | ISO-8601 date for auto-expiry |
| `supersedes` | optional | Array of event_ids to replace |

## Scripts reference

| Script | Purpose |
|--------|---------|
| `add_event.py` | Append one event |
| `compile_memory_hub.py` | Rebuild canonical from sources |
| `quick_share.sh` | Add + compile + push in one step |
| `search_events.py` | Search events by scope, kind, keyword |
| `validate_sources.py` | Validate NDJSON source files |
| `prune_fuzzy.py` | TTL cleanup of old fuzzy events |
| `dedup_profile.py` | Detect and resolve duplicate events |

## Why agent-soul over other memory solutions

| | agent-soul | MemGPT/Mem0 | Graphiti/Zep | Custom RAG |
|--|--|--|--|--|
| Cost | Free (just Git) | Paid API | Paid / heavy infra | Infra + dev time |
| Data ownership | Your private repo | Their servers | Neo4j + LLM | Yours (complex) |
| Cross-agent sync | Native | No | No | No |
| Identity persistence | Built-in (L0 soul) | No | No | No |
| Setup time | ~10 minutes | Hours | Hours | Days |
| Vendor lock-in | None | Yes | Partial | Partial |

## Links

- **Template repo**: https://github.com/kingcharleslzy-ai/agent-soul
- **Full docs**: See `README.md`, `JOIN.md`, `SCHEMA.md`, `SETUP.md` in the repo
