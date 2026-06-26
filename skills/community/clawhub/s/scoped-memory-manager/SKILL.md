---
name: scoped-memory-manager
description: Installs and manages Scope-Based Memory and Automated REM Sleep (memory consolidation) for OpenClaw agents. Use this skill when an agent's MEMORY.md is bloated, when the user asks to implement "REM Sleep", "memory decay", or "scoped memory", or to organize an agent's memory into domain-specific topics to save context window tokens.
---

# Scoped Memory Manager

This skill upgrades an OpenClaw agent's memory architecture from a single, bloated `MEMORY.md` to a **Scope-Based Memory** system with automated **REM Sleep** (memory consolidation and decay).

## Architecture

1. **Global Router (`MEMORY.md`)**: Kept extremely lean. Only contains core identity, active focus, and an index of domain-specific memory files.
2. **Domain-Specific Memory (`memory/topics/*.md`)**: Stores hyper-specific rules, constraints, and knowledge (e.g., `shopify.md`, `rails.md`). Retrieved dynamically via `memory_search` and `memory_get` only when relevant.
3. **Automated REM Sleep**: A scheduled background job (cron) that wakes up an isolated agent to compress daily logs, extract new patterns, prune outdated "trauma" constraints, and file the distilled knowledge into the correct topic files.

## Installation & Setup

When the user asks to install or configure scoped memory / REM sleep, follow these steps:

### 1. Scaffold the Directory Structure
Run the setup script to create the necessary directories:
```bash
sh scripts/setup.sh
```

### 2. Schedule the REM Sleep Cron Job
Use the `cron` tool to schedule the weekly consolidation job.
Call the `cron` tool with `action: "add"` and the following payload:

- **name**: "Memory REM Sleep (Consolidation)"
- **schedule**: `{ "kind": "cron", "expr": "0 3 * * 0" }` (Sundays at 3:00 AM)
- **sessionTarget**: "isolated"
- **delivery**: `{ "mode": "announce" }`
- **payload**:
  ```json
  {
    "kind": "agentTurn",
    "message": "It is time for your weekly REM sleep cycle. Please read the current `MEMORY.md` and the daily log files (`memory/YYYY-MM-DD.md`) from the past 7 days. Your task is to perform memory consolidation: \n1. Extract new patterns and important context from the logs.\n2. Review `MEMORY.md` and prune obsolete rules or constraints.\n3. Move domain-specific knowledge into the appropriate `memory/topics/*.md` files.\n4. Rewrite `MEMORY.md` to be a concise global router.\n5. Summarize what was added, moved, and forgotten."
  }
  ```

### 3. Migrate Existing Memory
If the agent already has a bloated `MEMORY.md`, proactively offer to read it and partition the content into `memory/topics/*.md` files right now.

## Usage Guidelines
- Remind users that `MEMORY.md` is NOT for storing everything.
- When learning a new specific framework, proactively create a new topic file in `memory/topics/` instead of polluting the global `MEMORY.md`.
