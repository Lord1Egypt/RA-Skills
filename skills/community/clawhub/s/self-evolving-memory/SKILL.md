---
name: self-evolving-memory
description: >
  Orchestrate the OpenClaw memory system so it actually runs reliably in practice.
  Use when the task involves capturing user preferences, current task state,
  corrections, decisions, recurring issues, memory cleanup, memory migration,
  or deciding where information should live across the workspace memory layers,
  including hot state, daily memory, structured long-term memory, root summary,
  and enforcement files such as SOUL.md, AGENTS.md, and TOOLS.md. Also use when
  the user asks to save memory, remember something, adapt old memories to the
  new system, or make the memory system actually stick and keep working over time.
---

# Memory Orchestrator

This skill is the workflow layer for the memory system. It does **not** replace
memory storage. It decides **what to capture, where to route it, when to
promote it, and when to harden it**.

## Source of truth

Use this order:
1. `MEMORY.md` + `memory/` = formal memory ledger
2. `SESSION-STATE.md` = current task state only
3. `.learnings/` = auxiliary scratch/noise layer only
4. vector recall = derived index, never source of truth

Never create a second formal ledger.

## Memory layers

### 1) Hot state
Use `SESSION-STATE.md` for:
- current task
- current blocker
- next actions
- recent decision needed for immediate continuity
- handoff / anti-compaction notes

Do **not** store durable history here.

### 2) Daily working memory
Use `memory/YYYY-MM-DD.md` for:
- user corrections
- task outcomes
- debugging notes
- temporary conclusions
- short self-reflection after non-trivial work
- observations that are not yet stable enough for long-term memory

### 3) Structured long-term memory
Route stable items to:
- `memory/preferences.md` — user preferences / communication style / stable likes-dislikes
- `memory/system.md` — stable environment facts / endpoints / toolchain constraints / paths
- `memory/projects.md` — long-running project context / decisions / status
- `memory/MEMORY.md` — cross-cutting long-term stable conclusions

### 4) Root summary
Use root `MEMORY.md` only for the few high-value facts worth automatic injection every session.
Keep it short.

### 5) Enforcement layer
If a recurring problem should change future behavior, also update one or more of:
- `SOUL.md`
- `AGENTS.md`
- `TOOLS.md`
- relevant `SKILL.md`
- relevant script/hook

## Embedding / vector recall setup

This skill supports semantic memory search via `memory_search`. Multiple embedding
backends are supported. See `references/embedding-setup.md` for full configuration:

- **Ollama** (local, recommended for privacy): `nomic-embed-text`, `mxbai-embed-large`, etc.
- **OpenAI Embeddings**: `text-embedding-3-small` / `text-embedding-3-large`
- **OpenAI-compatible APIs**: LocalAI, LM Studio, third-party providers
- **No embedding**: Rule-based routing still works without vector recall

Quick config example (Ollama, local):
```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "ollama",
    "model": "nomic-embed-text"
  }
}
```

Quick config example (OpenAI):
```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai",
    "model": "text-embedding-3-small",
    "remote": {
      "baseUrl": "https://api.openai.com/v1",
      "apiKey": "YOUR_OPENAI_API_KEY"
    }
  }
}
```

## First-run setup check

When this skill is triggered for the **first time**, or when the user asks to
"set up" / "initialize" / "check" the memory system, run this setup check:

### Auto-detect missing files

Check the current workspace for these files. If any are missing, create them
from templates OR tell the user exactly which command to run:

**Required files:**
```
SESSION-STATE.md          → templates/SESSION-STATE.md
MEMORY.md                 → templates/MEMORY.md
HEARTBEAT.md              → templates/HEARTBEAT.md
memory/preferences.md     → templates/memory/preferences.md
memory/system.md          → templates/memory/system.md
memory/projects.md        → templates/memory/projects.md
memory/MEMORY.md          → templates/memory/MEMORY.md
```

**Recommended agent files (prompt user to create if missing):**
```
SOUL.md      — add memory discipline section (see references/setup-checklist.md Step 3)
AGENTS.md    — add memory closeout protocol
TOOLS.md     — add memory-related tool discipline
```

**Action:**
- If files are missing: create them automatically, then confirm to the user what was created.
- If agent files (SOUL.md etc.) are missing: warn the user and point to `references/setup-checklist.md`.
- If embedding is not configured: remind user to check `references/embedding-setup.md`.

### One-command setup

Tell the user they can also run the setup script:
```bash
bash scripts/setup.sh [optional-workspace-path]
```

This will copy all templates and report what's missing.

## Runtime protocol

For the concrete operating protocol, read:
- `references/runtime-protocol.md`

Use that reference when the memory system needs to **operate reliably over time**, not just route one memory item.

For setup and initialization:
- `references/setup-checklist.md` — step-by-step first-time setup
- `scripts/setup.sh` — automated setup script

For embedding setup options, read:
- `references/embedding-setup.md`

## Routing rules

### A. User says "remember this" / gives a durable preference
- Write to `memory/YYYY-MM-DD.md`
- If clearly stable, also write to `memory/preferences.md` or other structured file
- If it must shape every session, also reflect it in root `MEMORY.md` or enforcement files

### B. Current task state changes
Before or during longer work, update `SESSION-STATE.md` with:
- current task
- key context
- pending actions
- blockers

Use hot state for continuity, not archiving.

### C. Error / correction / better approach discovered
- Log to `memory/YYYY-MM-DD.md`
- If it is noisy or needs raw staging, optionally also log to `.learnings/`
- If recurring or broadly applicable, promote to structured memory and/or enforcement layer

### D. Stable system fact discovered
- Daily first
- Then `memory/system.md`
- Only put in root `MEMORY.md` if it is worth automatic injection every session

### E. Project decision / project context
- Daily first
- Then `memory/projects.md`
- If very stable and cross-project, also `memory/MEMORY.md`

## Promotion / hardening state machine

Use this mental model:
- `observed` → captured in `SESSION-STATE.md` or daily
- `curated` → moved into structured long-term memory
- `hardened` → promoted into SOUL / AGENTS / TOOLS / skill / script
- `stable` → repeatedly validated, remains in long-term memory until marked stale

Rule:
- If the same issue appears **2+ times**, or the user is clearly annoyed, do not stop at memory. Harden it.

## Hygiene workflow

When asked to clean memory, adapt old memory, or audit the system:
1. Check whether old daily files contain content that already lives in structured memory
2. Add "converged/migrated/stale" style notes when appropriate
3. Ensure root `MEMORY.md` remains summary-only
4. Check `SESSION-STATE.md` is not stale or pretending to be long-term memory
5. Check `.learnings/` is not drifting into primary-ledger status
6. Check recall/reference docs still point to the new architecture

## When NOT to over-store
Do not promote every temporary detail.
Good memory systems are selective.
If uncertain, prefer:
- `SESSION-STATE.md` for immediate continuity
- `memory/YYYY-MM-DD.md` for tentative notes
- structured long-term only after stability is clear

## Trigger phrases / situations
Use this skill when the user asks or implies any of:
- remember / save memory / note this down
- adapt old memory / migrate memory / converge old memory
- memory cleanup / memory hygiene / memory system optimization
- current task state / handoff / anti-compaction continuity
- recurring issue / repeated annoyance / make it stick
- where should this memory go?
- should this be promoted to SOUL / AGENTS / TOOLS?

## Expected output style
Keep replies short.
Actually perform the routing/editing work.
Do not just say memory was saved — save it.
Do not ask for permission again when the memory action is already clear.

## Reliability requirements

For non-trivial memory operations, do not stop at classification.
Make sure the system actually advances:
- update `SESSION-STATE.md` when current continuity matters
- update `memory/YYYY-MM-DD.md` for daily capture
- promote stable items to structured long-term memory
- harden recurring issues into the enforcement layer
- use the closeout protocol from `references/runtime-protocol.md` when a task or phase ends

If any of these are skipped, the memory system is only partially operating.
