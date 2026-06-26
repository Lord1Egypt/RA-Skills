# openclaw-self-evolving-memory

> Your AI agent finally has a memory system that actually works — and gets better over time.

A layered memory skill for [OpenClaw](https://github.com/openclaw/openclaw) that transforms agent memory from fragile session notes into a **structured, self-maintaining, behavior-changing long-term memory system**.

---

## Core Advantages

Most AI agent memory systems fail in the same ways. This one doesn't.

**❌ The problem with every other approach:**
- The agent "remembers" in a session, then forgets everything the next day
- Vector search finds the right fragment, but the agent still makes the same mistake
- Preferences, errors, decisions, and random notes pile into one giant undifferentiated file
- You've said the same correction five times and it still doesn't stick
- Nobody knows which memory file is the real source of truth anymore

**✅ What self-evolving-memory does differently:**

| Problem | How this solves it |
|--------|-------------------|
| Cross-session amnesia | Hot state layer captures task continuity across context windows |
| "Finds but doesn't change" | Enforcement layer promotes patterns into hard rules (SOUL/AGENTS/TOOLS) |
| Memory soup | Six-layer architecture routes every piece of information to the right place |
| Recurring mistakes | 2-strike rule: if it happens twice, it gets hardened into a behavioral rule |
| Bloated context | Root `MEMORY.md` stays short; detail lives in structured sub-files |

**The key insight:** Memory isn't a storage problem. It's an information routing problem. This system routes correctly — and then enforces.

---

## Architecture Overview

Six layers, one formal ledger. No fragmentation.

```
Layer 0  Enforcement     SOUL.md / AGENTS.md / TOOLS.md / hooks
         ↑ harden recurring issues into permanent behavioral rules

Layer 1  Hot State       SESSION-STATE.md
         ↑ current task, blockers, handoff — cleared after each task

Layer 2  Daily Memory    memory/YYYY-MM-DD.md
         ↑ corrections, outcomes, debugging notes, short reflections

Layer 3  Long-term       memory/preferences.md  system.md  projects.md
         ↑ stable facts, promoted from daily when confirmed

Layer 4  Root Summary    MEMORY.md
         ↑ auto-injected every session — kept ruthlessly short

Layer 5  Semantic Recall memory_search + embedding index
         ↑ retrieval layer only — never the source of truth
```

**Promotion flows upward. Truth lives at Layer 3–4. Behavior changes happen at Layer 0.**

---

## How It Works

### Memory routing

Every piece of information gets routed to the right layer automatically:

| Signal | Destination |
|--------|------------|
| "Remember this" / new preference stated | Daily → `preferences.md` if stable |
| Task starts or context changes | `SESSION-STATE.md` |
| Error found / correction made | Daily → enforcement layer if recurring |
| Stable environment fact discovered | Daily → `memory/system.md` |
| Project decision made | Daily → `memory/projects.md` |
| Recurring annoyance (2+ times) | Hardened into SOUL / AGENTS / TOOLS |

### Promotion state machine

Information moves through states as it stabilizes:

```
observed  →  logged in SESSION-STATE.md or daily
curated   →  promoted into structured long-term memory
hardened  →  encoded into enforcement layer (permanent behavior change)
stable    →  validated, remains until explicitly marked stale
```

**The 2-strike rule:** If the same problem appears twice — or the user is clearly frustrated — stop logging it. Harden it.

### Task closeout protocol

A discipline that prevents memory debt from accumulating:

1. Reset `SESSION-STATE.md` — clear the hot state
2. Write daily recap — what happened, what was learned
3. Promote anything stable — to preferences, system, or projects
4. Enforce anything recurring — update SOUL/AGENTS/TOOLS
5. Mark converged entries — annotate old daily files if content has been promoted

---

## Regular Maintenance & Self-Checks

Memory systems degrade without hygiene. Run these checks periodically (or configure a heartbeat):

- **Hot state stale?** — Is `SESSION-STATE.md` describing a task that ended days ago?
- **Root bloat?** — Is `MEMORY.md` growing into a journal? It should be ≤ 15 lines.
- **Promotion backlog?** — Are there daily entries from last week that should be in `preferences.md` or `system.md`?
- **Stale facts?** — Is `memory/system.md` referencing endpoints or paths that no longer exist?
- **Hardening gap?** — Are there recurring issues that only exist in daily logs but haven't reached the enforcement layer?

Configure `HEARTBEAT.md` in your workspace to make the agent self-audit on a schedule. See `templates/HEARTBEAT.md`.

---

## Compatibility

- **OpenClaw**: 2026.3.x and later
- **Models**: Any model (Claude, GPT, Gemini, local models, etc.)
- **Embedding**: Optional but recommended; supports Ollama, OpenAI, and any OpenAI-compatible API
- **OS**: Linux, macOS, any environment running OpenClaw

---

## Installation

```bash
# Copy skill to your OpenClaw skills directory
cp -r openclaw-self-evolving-memory ~/.openclaw/skills/self-evolving-memory
```

---

## Quick Setup

Run the setup script — it handles everything automatically:

```bash
cd ~/.openclaw/skills/self-evolving-memory
bash scripts/setup.sh
```

What it does:
- Detects or prompts for your workspace path
- Copies all memory file templates (never overwrites existing files)
- Checks whether SOUL.md / AGENTS.md / TOOLS.md exist and warns if missing
- Checks embedding configuration and points to the right setup guide

### Embedding setup

Semantic recall is optional but significantly improves memory retrieval quality. Supported backends:

- **Ollama** (local, free, private) — `ollama pull nomic-embed-text`
- **OpenAI Embeddings** — `text-embedding-3-small` or `text-embedding-3-large`
- **Any OpenAI-compatible API** — LocalAI, LM Studio, third-party providers

See `references/embedding-setup.md` for full configuration examples.

### Manual setup

Prefer doing it step-by-step? See `references/setup-checklist.md`.

### Verify your setup

Ask your agent after installation:

> "Check my memory system setup and tell me if anything is missing."

The skill will scan your workspace and report exactly what's configured and what needs attention.

---

## File Reference

```
SKILL.md
scripts/
  setup.sh                        — Automated setup script
templates/
  SESSION-STATE.md                — Hot state template
  MEMORY.md                       — Root summary template
  HEARTBEAT.md                    — Self-check instructions template
  memory/
    preferences.md
    system.md
    projects.md
    MEMORY.md
references/
  runtime-protocol.md             — Full operating protocol
  embedding-setup.md              — Vector recall configuration
  setup-checklist.md              — Step-by-step manual setup
```

---

## Credits

Inspired by:
- [Anthropic's agent best practices](https://docs.anthropic.com/en/docs/build-with-claude/agentic) on context engineering and progress files
- Real-world operational experience running multi-agent OpenClaw deployments

## License

MIT
