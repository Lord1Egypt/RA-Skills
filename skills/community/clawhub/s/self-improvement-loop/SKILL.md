---
name: self-improvement-loop
version: 4.6.13
description: |
  Per-agent feedback loop for OpenClaw — captures corrections/errors/features, detects patterns per agent workspace, notifies via per-agent channel bot, and executes A/B/C/D decisions in the correct agent session.
  Auto-detects agents from openclaw.json, auto-maps agent ID → channel account → bindings.
  A/B/C/D handling logic lives in scripts/agents-append.md (shared); install.sh injects a reference into each agent's AGENTS.md and memory.md.
---

# self-improvement-loop v4.6.13

## Overview

**Core Capability**: Each agent has its own self-improvement feedback loop — isolated learnings directory, independent cron scan, notifications bound to their own channel bot, and A/B/C/D execution in the correct agent session.

```
User corrects code-dev agent
    ↓
code-dev hook captures → writes to code-dev/.learnings/
    ↓
self-improvement-code-dev cron (hourly) → scans only code-dev/.learnings/
    ↓
Pattern detected (count≥2) → notifies user via code bot
    ↓
User replies A → code-dev agent session executes → writes back to code-dev workspace
```

---

## Data Flow (Per-Agent Isolation)

```
openclaw.json (agents.list + bindings)
    │
    ├─→ install.sh reads agents
    │         ↓
    │    Creates per-agent directories (e.g., agents/workspace/.learnings/)
    │
    ├─→ install.sh reads channel accounts
    │         ↓
    │    Writes bindings (agentId → accountId)
    │    { "agentId": "code-dev", "match": { "channel": "telegram", "accountId": "code" } }
    │
    └─→ setup_crons.py creates per-agent cron
              ↓
         Each cron carries --agent flag
         LEARNINGS_DIR points to that agent's workspace
         delivery uses that agent's account

┌─────────────────────────────────────────────────────────────┐
│  Hook (handler.js) - Global shared, dynamic routing         │
│  sessionKey: "agent:code-dev:telegram:..."                 │
│  → extractAgentId("code-dev")                              │
│  → getAgentWorkspace("code-dev") → agent workspace path     │
│  → learningsDir = workspace + "/.learnings/"               │
│  Pushes reminders to context.messages                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Cron (per-agent) - Independent execution                   │
│  Name: self-improvement-code-dev                           │
│  --agent code-dev → bound to code-dev agent session        │
│  LEARNINGS_DIR=".../agents/code-dev/.learnings"             │
│  delivery: channel=telegram, accountId=code                │
│  Scans only its own LEARNINGS_DIR                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Notification - Sent via respective channel bot           │
│  code bot → user conversation with code-dev                 │
│  moling bot → user conversation with moling                 │
│  User replies A/B/C/D → OpenClaw routes to correct agent   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  A/B/C/D Execution - Runs in correct agent session        │
│  Reads pending JSON → executes skill-creator/skill-improvement
│  Writes back to that agent's learnings directory            │
└─────────────────────────────────────────────────────────────┘
```

---

## Permissions Required

| Permission    | Scope                        | Purpose                                            |
|---------------|------------------------------|----------------------------------------------------|
| `exec`        | `scripts/`                  | Run distill.sh, archive.sh (mechanical scan/archive) |
| `read`        | `<agent>/workspace/.learnings/` | Read LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md |
| `write`       | `<agent>/workspace/.learnings/` | Update notified status; create `.pending_notifications/*.json` |
| `cron`        | Global                      | Create and manage self-improvement-{agent} cron jobs |
| `gateway_api` | Gateway :18789              | setup_crons.py calls API to create crons           |
| `openclaw.json` | `HOME/.openclaw/`         | install.sh reads agent config; writes bindings     |

**Security Boundaries**:

- File operations strictly scoped to per-agent learnings directories under `~/.openclaw/workspace/`
- All paths dynamically generated, no hardcoding
- Cron runs in isolated session with minimal toolset
- install.sh prompts for confirmation before writing bindings, can be skipped

---

## Core Components

| Component           | Type          | Routing Basis                        |
|---------------------|---------------|--------------------------------------|
| `handler.js`        | Global Hook   | sessionKey → agent ID → workspace    |
| `distill.sh`        | Shared Script | `LEARNINGS_DIR` environment variable |
| `setup_crons.py`    | Shared Script | agent config → cron --agent flag     |
| `install.sh`        | Install Script| agents.list + accounts → bindings     |
| `agents-append.md`   | A/B/C/D Logic | Shared across agents; install.sh injects index reference |

---

## Installation

```bash
bash ~/.openclaw/workspace/skills/self-improvement-loop/install.sh
openclaw gateway restart
```

Installation automatically:

1. Creates `.learnings/` directories for each agent
2. Installs hook and scripts
3. Creates per-agent cron jobs
4. Updates `openclaw.json` bindings (enables message routing)
5. Injects self-improvement index instructions into each agent workspace's `AGENTS.md` and `memory.md`

**A/B/C/D handling logic** is stored in `skills/self-improvement-loop/scripts/agents-append.md` (shared). During install, index references are injected into each agent's `AGENTS.md` and `memory.md`:

```markdown
## Self-Improvement (A/B/C/D)

Before handling A/B/C/D, must consult:
skills/self-improvement-loop/scripts/agents-append.md
```

No manual appending needed after install; skill updates automatically use the latest version for all agents.

---

## Verification

```bash
# Check bindings
python3 -c "import json; print(json.dumps(json.load(open('$HOME/.openclaw/openclaw.json')).get('bindings',[]), indent=2))"

# Check per-agent crons
openclaw cron list | grep self-improvement

# Test distill (specific agent)
LEARNINGS_DIR="$HOME/.openclaw/workspace/agents/code-dev/.learnings" \
  bash ~/.openclaw/workspace/skills/self-improvement-loop/scripts/distill.sh --check-only
```

---

## Dependencies

| Dependency        | Version   | Purpose                                |
|-------------------|-----------|----------------------------------------|
| OpenClaw          | ≥2026.4   | Platform foundation                    |
| Python3           | ≥3.8      | distill_json.py, write_notified.py     |
| Node.js           | any       | handler.js                             |
| skill-creator     | any       | Path A - create skills                 |
| skill-improvement | any       | Path B - improve skills                |

---

## Limitations & Known Issues

- **ACP runtime agent (claude)**: No independent channel, falls back to `defaultAccount`
- **API (Gateway)**: API unreachable (404), falls back to CLI for cron creation, sessionTarget downgraded to isolated
- **Concurrent notifications**: When multiple agents trigger simultaneously, user replies may route to wrong agent session
- **sessionTarget=current**: Requires Gateway API support, currently unavailable

---

## See Also

- `references/setup-guide.md` — Full installation and configuration guide
