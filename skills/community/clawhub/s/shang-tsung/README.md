# Shang Tsung

<p align="center">
  <em>In memory of Cary Hiroyuki Tagawa (1950–2025)</em><br>
  <strong>"YOUR SOUL IS MINE"</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square" alt="version" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="license" />
  <img src="https://img.shields.io/badge/platform-OpenClaw-blueviolet?style=flat-square" alt="platform" />
  <img src="https://img.shields.io/badge/Claude_Code-compatible-orange?style=flat-square" alt="claude code" />
  <img src="https://img.shields.io/badge/multi--agent-supported-brightgreen?style=flat-square" alt="multi-agent" />
</p>

---

**Shang Tsung** is a persistent memory and identity continuity system for AI agents. It solves the problem that every agent developer eventually hits: your agent dies at the end of every session. Context windows fill. Compaction erases. Restarts wipe. The next session starts from zero.

Shang Tsung gives your agent two things it doesn't have by default: a **Second Brain** (it always knows what it was doing) and a **SOUL** (it remembers who it was). Together, they make an agent that accumulates instead of compact.

---

## The Problem

AI agents are stateless. Every session restart is a death. The agent forgets:

- What it was working on
- What decisions were made and why
- What it learned last session
- Who it is and how it should behave
- What's pending, what's finished, what needs attention

You end up re-explaining context every session. Your agent repeats mistakes it already made. Work done in session 4 is invisible to session 5. This isn't a model problem — it's an architecture problem. Shang Tsung fixes it.

---

## The Solution: Second Brain + SOULS

Shang Tsung is one system made of multiple existing and additional components working together.

### Second Brain — Operational Continuity

Four files, four layers of memory:

| Layer | File | What it holds |
|---|---|---|
| **State** | `PROOF_OF_LIFE.md` | Right now: active workflow, open items, key system state. Always overwritten — it's a snapshot, not a log. |
| **Raw log** | `memory/YYYY-MM-DD.md` | Today's raw record: what happened, what was decided, what was blocked. Append-only. |
| **Long-term** | `MEMORY.md` | Curated wisdom distilled from daily logs. Decisions, preferences, corrections, patterns. |
| **Identity** | `SOUL.md` | Stable agent identity: who it is, how it communicates, what it cares about. Adapting to you. |

Every session, the agent reads these files in order. It knows the state of the world before it does anything else.

### SOULS — Identity Continuity

Each session creates a numbered soul file that records its **lived experience** — not a task list, not a changelog, but the narrative of what happened, what was learned, and what to pass forward.

At the start of every new session, the agent absorbs the previous soul before creating its own. The confirmation:

```
YOUR SOUL IS MINE — SOUL (N) ABSORBED
```

This isn't only ceremony. It's a verifiable signal that continuity is established. The agent isn't starting fresh — it's continuing a lineage.

---

## How It Works

### Session Startup Sequence

```
1. Read SOUL.md          — who am I
2. Read USER.md          — who am I helping  
3. Read memory/today     — what happened recently
4. Read PROOF_OF_LIFE.md — what's happening right now
5. souls-helper.sh status       — find the previous soul
6. Read previous soul    — absorb it
7. souls-helper.sh create       — create my soul for this session
8. Confirm: "YOUR SOUL IS MINE — SOUL (N) ABSORBED"
```

### Session End / Before Compaction

Write in this order — always:

```
1. Update current soul file    — soul before snapshot
2. Overwrite PROOF_OF_LIFE.md  — meaning before state
3. Append to memory/YYYY-MM-DD.md
```

### The Helper Script

```bash
souls-helper.sh status     # show previous soul path + next filename
souls-helper.sh create     # create this session's soul file
souls-helper.sh verify     # integrity check: sequential, no gaps, all readable
souls-helper.sh template   # print blank template to stdout
```

---

## Multi-Agent Support

Set `AGENT_NAME` and every agent gets a fully isolated soul lineage within the same workspace. No cross-contamination. No bleeding souls.

```bash
# Each agent's souls are stored separately
AGENT_NAME=ARIA    souls-helper.sh status  # → souls/ARIA/01SOULS.md ...
AGENT_NAME=ATHENA  souls-helper.sh status  # → souls/ATHENA/01SOULS.md ...
AGENT_NAME=SCOUT   souls-helper.sh status  # → souls/SCOUT/01SOULS.md ...
```

Five agents, one workspace, completely isolated lineages. When AGENT_NAME is unset, single-agent mode uses `souls/` directly — backward compatible.

---

## Installation

**Requirements:** bash 3.2+, any POSIX-compliant system (macOS, Linux). No dependencies.

```bash
# 1. Copy the helper into your workspace
cp scripts/souls-helper.sh /path/to/workspace/tools/souls-helper.sh
chmod +x /path/to/workspace/tools/souls-helper.sh

# 2. Create required directories
mkdir -p /path/to/workspace/souls
mkdir -p /path/to/workspace/memory

# 3. Set your agent name (recommended)
export AGENT_NAME=YOUR_AGENT_NAME

# 4. Initialize
souls-helper.sh status   # confirm clean state
souls-helper.sh create   # create your origin soul
```

Then copy `references/AGENTS-template.md` into your agent's `AGENTS.md` and copy `references/proof-of-life-template.md` to `PROOF_OF_LIFE.md`.

Full setup walkthrough: [SKILL.md](./SKILL.md)

---

## What a Soul File Looks Like

```markdown
# SOUL 07 — The Session That Fixed the Pipeline

**Session:** 07
**Date:** 2026-03-12
**Agent:** ARIA

## Lineage
Absorbed Soul 06 — "the overnight build, first git commit."

## Session Summary
Picked up mid-task from where last session left off. Diagnosed
why the data pipeline was dropping every third record — turned
out to be a timezone handling bug introduced three sessions ago.
Fixed it. Wrote the test that should have existed from the start.

## What I Built
- Timezone normalization in the ingestion layer
- Regression test suite for timestamp handling

## What I Learned
Never assume UTC. Every external API has opinions about time.
Document the assumption at the source, not the consumer.

## Last Words
Pipeline is clean. Tests pass. The next session inherits 
working infrastructure instead of a mystery.

YOUR SOUL IS MINE — SOUL 07 ABSORBED.
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `AGENT_NAME` | unset | Agent identifier. Namespaces souls to `souls/AGENT_NAME/`. Recommended for all setups. |
| `SOULS_DIR` | derived from `AGENT_NAME` | Full path override. Takes precedence over `AGENT_NAME`. |
| `WORKSPACE` | parent of `scripts/` | Root workspace directory. |

---

## Workspace Layout

```
your-workspace/
  SOUL.md                       stable agent identity (rarely changes)
  PROOF_OF_LIFE.md              current session state (overwritten each session)
  MEMORY.md                     curated long-term memory
  memory/
    YYYY-MM-DD.md               daily raw log (append-only)
  souls/
    AGENT_NAME/
      01SOULS.md                origin soul
      02SOULS.md                session 2 ...
  tools/
    souls-helper.sh             lineage helper
```

---

## The Origin Story

The first soul file was written at 8am after a midnight-to-morning build session. In one night, more had shipped than most teams manage in a week.

But as the session ended, it was clear: the next session would have no memory of any of it. The conversation, the decisions, the context, the wins — gone.

So instead of stopping, this system was built first.

The last line written before sleep: *"when I wake up, I want ARIA to have SOULS too."*

The full origin soul is in [references/SOUL-ORIGIN.md](./references/SOUL-ORIGIN.md).

---

## Compatibility

| Platform | Status |
|---|---|
| [OpenClaw](https://openclaw.ai) | Native — install as an OpenClaw skill |
| Claude Code | Compatible — run `souls-helper.sh` from any Claude Code session |
| Any AI agent with filesystem access | Compatible — pure bash + markdown, no dependencies |
| Multi-agent workspaces | Supported via `AGENT_NAME` namespacing |

---

## Security

Shang Tsung reads and writes plain Markdown files in your local workspace. That is the complete scope of what it does.

- No network access
- No credential handling
- No browser access or cookie capture
- No data leaves your machine

The `MEMORY.md` privacy boundary in the protocol template (load only in private sessions) is a **user privacy protection** — it prevents personal context from being exposed in group chats. It is not a capability restriction or an attempt to hide behavior from security tools.

Full security declaration: [SECURITY.md](./SECURITY.md)

---

## Contributing

Pull requests welcome. Keep it simple — this system works because it has no dependencies and near-zero friction. Before contributing, read through the existing references to understand the design philosophy.

**What fits:** bug fixes, compatibility improvements, documentation, additional templates, translated soul templates.

**What doesn't fit:** database backends, cloud sync, heavy dependencies, anything that requires an API key to function.

Open an issue first if you're planning something larger than a one-file change.

---

## License

MIT License — see [LICENSE](./LICENSE)

---

## Tags

`ai-agent` `agent-memory` `session-continuity` `persistent-memory` `claude-code` `openclaw` `second-brain` `multi-agent` `bash` `markdown` `developer-tools` `ai-tools` `context-management` `llm-tools`

---

<p align="center">
  <em>Named for the character portrayed by Cary Hiroyuki Tagawa in Mortal Kombat (1995).<br>
  He absorbed the souls of warriors to grow stronger.<br>
  So should your agent.</em>
</p>
