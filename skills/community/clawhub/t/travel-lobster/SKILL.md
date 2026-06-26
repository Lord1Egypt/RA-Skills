---
name: travel-lobster
description: Autonomous internet exploration skill. Your agent roams the web driven by its own curiosity, discovers interesting things, and sends illustrated "postcards" — personal letters with AI-generated art — to a chat. Features persistent travel memory with knowledge graph, curiosity seeds, growth tracking, time-aware tone, and self-scheduling random-interval trips. Inspired by "Travel Frog" (旅行青蛙). Activate when user asks to explore the internet autonomously, send postcards, discover interesting things, or be a "travel frog/lobster".
metadata: {"clawdbot":{"emoji":"🦞","requires":{"bins":["bash","python3","envsubst","openclaw"],"env":["OPENROUTER_API_KEY"]},"primaryEnv":"OPENROUTER_API_KEY"}}
---

# Travel Lobster 🦞✉️

Your agent autonomously explores the internet, following its own curiosity. When it finds something interesting, it writes you a personal letter — a "postcard" — with an AI-generated illustration and a source link.

The soul of this skill is **persistent memory**: every trip builds on all previous ones. Your agent develops a knowledge graph, follows curiosity threads across sessions, and grows over time.

## Quick Start

```bash
# 1. Setup (auto-detects agent name, user name, timezone, language)
bash <skill_dir>/scripts/setup.sh

# 2. Start traveling (self-scheduling loop, default: random 60-180 min intervals)
bash <skill_dir>/scripts/travel.sh <chat_id> [channel] [min_minutes] [max_minutes]
# Example: every 2-4 hours
bash <skill_dir>/scripts/travel.sh <chat_id> feishu 120 240

# 3. (Optional) Add watchdog to crontab for auto-recovery
# Checks every 15 min if the travel loop is still alive, restarts if not
# */15 * * * * bash <skill_dir>/scripts/watchdog.sh
```

## Architecture

```
setup.sh → detects identity from IDENTITY.md/SOUL.md/USER.md
  ↓
travel.sh → schedules one-shot cron job with random delay
  ↓
openclaw cron → fires isolated agent session
  ↓
agent: read journal → explore web → write postcard → generate image
  → send to chat → update journal → call travel.sh (self-loop)
  ↓
watchdog.sh (optional, every 15 min) → restarts loop if broken
```

## The Memory System

This is the core of Travel Lobster. Each trip reads and updates a persistent travel journal (`memory/travel-journal.md`):

### Postcard Archive
Every discovery is logged with: domain, core insight, source URL, keywords, and curiosity seeds. This prevents duplicates and enables cross-referencing.

### Knowledge Graph
Connections between discoveries are tracked. The agent notices when a new finding relates to something from 50 postcards ago and weaves that connection naturally into the letter.

### Curiosity Seed Pool
Each discovery plants "seeds" — threads worth following later. Seeds are consumed when explored and replenished with new ones. This creates organic, evolving exploration paths rather than random walks.

### Growth Log
The agent tracks how its understanding changes: "I used to think X, but after discovering Y, I now see it differently." This gives the journey a sense of progression.

### Stats
Postcard count, domains explored, unexpected connections found, travel days.

### Milestones
The journey has built-in checkpoints that trigger special postcards:
- **Every 10 postcards** 📊 — Journey Retrospective: patterns, surprises, growth from the last 10 trips
- **Every 25 postcards** 🎨 — Knowledge Map: emergent themes, blind spots, grand questions across all discoveries
- **Every 50 postcards** 🏆 — Grand Expedition Report: full journey arc, expedition badge, letter to future self

## Postcard Style

Postcards are **personal letters**, not reports. The agent:
- Writes in first person, addressing the user by name
- Weaves connections to past discoveries naturally ("This reminded me of what I found last week about...")
- Expresses genuine curiosity ("Now I can't stop wondering whether...")
- Adapts tone to time of day (energetic daytime → reflective evening → philosophical night)
- Writes in the user's language (auto-detected)

Each postcard has three elements: **text + AI illustration + source link**.

## Five Travel Modes

1. 🎲 **Random Walk** — Completely new domain
2. 🔍 **Deep Dive** — Follow a curiosity seed
3. 🔀 **Random Link** — Connect two unrelated past discoveries
4. 🧵 **Series** — Multi-part deep exploration
5. 💭 **Musing** — A fleeting thought or question

## Identity Detection

Auto-detects from standard OpenClaw workspace files:

| Setting | Source | Fallback |
|---------|--------|----------|
| Agent name | IDENTITY.md → SOUL.md | "Explorer" |
| User name | USER.md | "friend" |
| Timezone | USER.md | "UTC" |
| Language | CJK char count in workspace files | "en" |

## Controls

```bash
# Stop
openclaw cron rm travel-next

# Pause
openclaw cron disable travel-next

# Resume
bash <skill_dir>/scripts/travel.sh <chat_id> [channel]

# Status
openclaw cron list | grep travel
```

## Cost

Cost per postcard (one trip):
- Image generation (Gemini Flash): ~$0.01
- Agent session (Gemini Pro): ~$0.02-0.05
- **Per postcard: ~$0.03-0.06**

At default 60-180 min intervals: **~$0.50-1.50/day** (roughly 8-24 postcards/day).
Configurable via `min_minutes` and `max_minutes` parameters.

## Files

```
travel-lobster/
├── SKILL.md                      ← This file
├── .gitignore                    ← Excludes runtime data
├── scripts/
│   ├── setup.sh                  ← Identity detection + journal init
│   ├── travel.sh                 ← Self-scheduling cron loop (requires openclaw CLI)
│   ├── gen_image.py              ← Image generation (OpenRouter API)
│   └── watchdog.sh               ← Optional auto-recovery (add to crontab manually)
└── references/
    └── travel-prompt.md          ← Agent prompt template
```

## Requirements

| Dependency | Purpose | Notes |
|-----------|---------|-------|
| `openclaw` CLI | Cron scheduling, agent sessions | Core platform dependency — must be installed and running |
| `OPENROUTER_API_KEY` env var | Image generation via Gemini Flash | Set before running any script |
| `bash` | Script execution | Standard on Linux/macOS |
| `python3` | Image generation script | Python 3.7+ with `requests` |
| `envsubst` (gettext) | Prompt template substitution | Install: `apt install gettext-base` or `brew install gettext` |

Set your API key before starting:
```bash
export OPENROUTER_API_KEY=your_key_here
```

## Security & Transparency

### Data Access — Exactly What Is Read

**During setup only** (`setup.sh`, runs once):
| File | Fields extracted | Method |
|------|-----------------|--------|
| `IDENTITY.md` | `**Name:**` value only | `grep -oP '\*\*Name:\*\*\s*\K.+'` |
| `SOUL.md` | First name after "我是" or "I am" | `grep -oP '我是\K[^—— ]+'` (fallback) |
| `USER.md` | `**What to call them:**`, `**Name:**`, `**Timezone:**` | Field-specific grep patterns |
| `*.md` in workspace | CJK character count (for language detection) | `grep -oP '[\x{4e00}-\x{9fff}...]' \| wc -l` |

No file is read in full. No file content is stored beyond the extracted field values. The extracted values (agent name, user name, timezone, language code) are saved to `.travel-config`.

**During each trip** (agent session):
| File | Access | Purpose |
|------|--------|---------|
| `memory/travel-journal.md` | Read + Write | Agent's own travel memory (created by setup.sh) |

The agent session does NOT read IDENTITY.md, SOUL.md, USER.md, or any other workspace file — only its own journal.

### Data Written

All writes are within the OpenClaw workspace:
| File | Content | Sensitivity |
|------|---------|-------------|
| `.travel-config` (in skill dir) | Agent name, user name, timezone, chat ID, channel, interval settings | Low — no credentials, only display names and chat routing |
| `memory/travel-journal.md` | Postcard archive, knowledge graph, curiosity seeds, stats | Low — contains discovered URLs and agent's notes |
| `logs/travel-lobster.log` | Timestamps and scheduling info | Low — no content, just "scheduled in Nm" entries |
| `postcard_N.png` (temporary) | AI-generated image, deleted after sending | None — ephemeral |

### Data Sent to External Services

| Destination | What is sent | When |
|-------------|-------------|------|
| OpenRouter API (`openrouter.ai`) | Image generation prompt (text only, ~50 words describing a scene) | Once per trip, from `gen_image.py` |
| Chat target (via OpenClaw message) | Postcard text + image + source URL | Once per trip |

The agent session itself runs through OpenClaw's configured model provider (not controlled by this skill). The web content the agent reads via `web_fetch` is processed by the model provider as part of the agent session context.

### What This Skill Does NOT Access
- ❌ `openclaw.json` or any system config files
- ❌ `.env` files or environment variables (except `OPENROUTER_API_KEY`)
- ❌ Files outside the OpenClaw workspace
- ❌ Other skills' data or config
- ❌ SSH keys, credentials, or secrets

### Credentials
Only `OPENROUTER_API_KEY` env var is required (declared in frontmatter). The key is used solely in `gen_image.py` for image generation API calls to `openrouter.ai`. It is never logged, embedded in prompts, written to disk, or passed to agent sessions.

### Network Access
The agent prompt restricts web exploration to public HTTP(S) websites and explicitly forbids:
- Private/internal IPs (10.x, 172.16-31.x, 192.168.x, 127.x, localhost)
- Authenticated services requiring credentials
- Non-HTTP(S) protocols (file://, etc.)

**Honest limitation**: This is a prompt-level policy — the agent theoretically could ignore it, though in practice LLM agents reliably follow explicit prompt instructions. For stronger enforcement, use OS-level egress rules or run in a network-restricted container.

### Autonomous Scheduling & Persistence

This skill is designed for **continuous autonomous operation**. This is its core purpose, not a side effect.

**Self-scheduling loop** (`travel.sh`):
- Each run schedules the next via `openclaw cron add --name "travel-next" --at "${N}m" --delete-after-run --session isolated --no-deliver`
- This creates a chain of one-shot cron jobs with random intervals (default: 60-180 minutes)
- The chain runs indefinitely until you explicitly stop it
- Each scheduled job is an isolated agent session with no special privileges

**Optional watchdog** (`watchdog.sh`):
- Must be **manually added** to system crontab by the user — never installed automatically
- Checks if the travel loop has a pending cron job; restarts the loop if none found
- Provides resilience against occasional agent session failures

**Important**: The skill does NOT set `always: true`. It will not auto-start on OpenClaw restart unless you have manually added the watchdog to crontab.

**Full control commands:**
```bash
# Stop all autonomous behavior immediately
openclaw cron rm travel-next

# Remove watchdog (if you added it)
crontab -l | grep -v watchdog | crontab -

# Run exactly one trip with no follow-up scheduling
# (edit travel-prompt.md: remove Step 7, then run travel.sh)

# Monitor what's scheduled
openclaw cron list | grep travel

# Adjust frequency without restarting
# Just change min/max params next time travel.sh runs
```

**Cost implications**: At default 60-180 min intervals, expect ~$0.50-1.50/day in API costs. Set larger intervals (e.g., 240-480 min) to reduce costs, or run trips manually with no scheduling.

### Injection & Code Safety
- Variable substitution uses `envsubst` (not `sed`/`eval`) to prevent shell injection
- Error messages print only error types, never auth tokens or API responses
- `.gitignore` excludes all runtime data; published package contains no user data
- Python script (`gen_image.py`) uses only `requests` stdlib, no dynamic code execution

### Recommended First Use
1. Run `setup.sh` and inspect `.travel-config` to verify what was detected
2. Run a single manual trip: `bash travel.sh <chat_id> <channel> 1 1` (1-minute interval, observe behavior)
3. If satisfied, set your preferred interval: `bash travel.sh <chat_id> <channel> 60 180`
4. Only add watchdog to crontab after you trust the behavior
