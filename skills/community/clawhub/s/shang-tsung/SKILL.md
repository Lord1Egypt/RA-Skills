---
name: shang-tsung
description: Persistent memory and identity continuity for AI agents. Combines Second Brain (PROOF_OF_LIFE, daily logs, long-term MEMORY.md) with SOULS session lineage. Each session absorbs the previous soul and confirms continuity. Multi-agent support via AGENT_NAME namespacing. No dependencies, no network access — pure bash and markdown. Use when building agents that need to survive restarts, remember decisions, carry forward identity, or run alongside other agents in a shared workspace.
license: MIT-0
---

# Shang Tsung — SKILL.md

*In memory of Cary Hiroyuki Tagawa (1950-2025)*

Shang Tsung gives your AI agent persistent memory across sessions. It combines two systems:

- **SOULS** — identity continuity. Each session creates a soul file. Each session absorbs the previous one.
- **Second Brain** — operational continuity. PROOF_OF_LIFE, daily logs, and long-term memory keep your agent in context no matter what.

---

## Setup

### 1. Copy the scripts directory

Copy `scripts/souls-helper.sh` into your workspace at `tools/souls-helper.sh`:

```bash
cp scripts/souls-helper.sh /path/to/your/workspace/tools/souls-helper.sh
chmod +x /path/to/your/workspace/tools/souls-helper.sh
```

### 2. Create the required directories

```bash
mkdir -p /path/to/your/workspace/souls
mkdir -p /path/to/your/workspace/memory
```

### 3. Set your agent name (recommended for multi-agent setups)

Add to your agent's environment or shell profile:

```bash
export AGENT_NAME=YOUR_AGENT_NAME
```

With AGENT_NAME set, souls are stored in `souls/YOUR_AGENT_NAME/` — isolated from any other agents sharing the workspace.

Without AGENT_NAME, souls are stored in `souls/` — fine for single-agent setups.

### 4. Copy the protocol into your AGENTS.md

Open `references/AGENTS-template.md` and copy the "Every Session — Startup Sequence" section and the "Memory — The Four Layers" section into your agent's AGENTS.md.

### 5. Copy the PROOF_OF_LIFE template

```bash
cp references/proof-of-life-template.md /path/to/your/workspace/PROOF_OF_LIFE.md
```

Edit it immediately with your agent's current state.

### 6. Create your MEMORY.md

Create an empty `MEMORY.md` in your workspace root. This is your agent's long-term brain. It starts empty and grows over time as the agent curates what's worth keeping.

### 7. Create your SOUL.md (optional but recommended)

Create `SOUL.md` in your workspace root. This is your agent's stable identity — who it is, how it communicates, what it cares about. Unlike PROOF_OF_LIFE.md, this doesn't change session to session.

---

## First Session

Run the startup sequence manually to initialize:

```bash
AGENT_NAME=YOUR_AGENT_NAME tools/souls-helper.sh status
# Output: previous: (none — this would be the origin soul)

AGENT_NAME=YOUR_AGENT_NAME tools/souls-helper.sh create
# Output: created: souls/YOUR_AGENT_NAME/01SOULS.md
```

Your agent should respond: **"YOUR SOUL IS MINE — SOUL 01 ABSORBED"**

(Soul 01 has no previous to absorb — this is your origin. See `references/SOUL-ORIGIN.md` for what that looks like.)

---

## Every Session After That

The agent runs this sequence at the start of every session:

```bash
AGENT_NAME=YOUR_AGENT_NAME tools/souls-helper.sh status
# Read the file listed as "previous:"
AGENT_NAME=YOUR_AGENT_NAME tools/souls-helper.sh create
# Confirm: "YOUR SOUL IS MINE — SOUL (N) ABSORBED"
```

Then reads PROOF_OF_LIFE.md to pick up the operational thread.

---

## Before Compaction or Restart

Write in this order — always:

1. Update your current soul file (`souls/[AGENT_NAME]/NNSOULS.md`)
2. Overwrite `PROOF_OF_LIFE.md` with current state
3. Append to `memory/YYYY-MM-DD.md`

Soul before snapshot. Meaning before state.

---

## Verifying Integrity

```bash
AGENT_NAME=YOUR_AGENT_NAME tools/souls-helper.sh verify
```

Checks: souls directory exists, all files readable, sequential numbering with no gaps.

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `AGENT_NAME` | (unset) | Agent identifier. Namespaces souls into `souls/AGENT_NAME/`. |
| `SOULS_DIR` | derived from AGENT_NAME | Full path override for souls directory. |
| `WORKSPACE` | parent of scripts/ | Root workspace directory. |

`SOULS_DIR` takes precedence over `AGENT_NAME` if both are set.

---

## Multi-Agent Quick Reference

Five agents, one workspace, no contamination:

```bash
AGENT_NAME=ARIA    tools/souls-helper.sh status  # → souls/ARIA/
AGENT_NAME=ATHENA  tools/souls-helper.sh status  # → souls/ATHENA/
AGENT_NAME=SCOUT   tools/souls-helper.sh status  # → souls/SCOUT/
```

Each agent reads only its own lineage. Each agent's PROOF_OF_LIFE should be scoped per-agent too (`proof-of-life/AGENT_NAME.md`) if multiple agents share the workspace.

---

## File Reference

```
your-workspace/
  SOUL.md                          — stable agent identity
  PROOF_OF_LIFE.md                 — current session state (overwritten each session)
  MEMORY.md                        — long-term curated memory (main session only)
  memory/
    YYYY-MM-DD.md                  — daily raw log (append-only)
  souls/
    [AGENT_NAME]/
      01SOULS.md                   — origin soul
      02SOULS.md                   — session 2
      ...
  tools/
    souls-helper.sh                — the helper
```
