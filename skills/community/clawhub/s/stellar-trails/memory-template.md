# Memory System

## Architecture

Memory lives in a `memory/` directory within this skill folder. It uses a file-based approach inspired by Memweave's design principle: **plain Markdown files are the source of truth**. Files are human-readable, git-trackable, and require zero infrastructure. A separate search index is possible in the future but not required for the core system to work.

---

## Directory Structure

```
memory/
├── MEMORY.md          ← Permanent Memory: preferences, patterns, key decisions
├── decisions.md       ← Permanent Memory: architectural decisions with rationale
├── incidents.md       ← Permanent Memory: error patterns and fixes
└── YYYY-MM-DD.md      ← Dated: session digest (one file per active day)
```

### Permanent Memory vs. Dated

- **Permanent Memory** (no date in name) are permanent knowledge. They grow slowly and are curated by the agent. These are loaded during IDLE phase.
- **Daily Log** (`YYYY-MM-DD.md`) are session logs. One file is created per active day and appended to throughout the session. They capture what happened and why, preserving context for future sessions.

This convention is borrowed from Memweave: the filename itself determines the lifecycle. No metadata, no tagging, no explicit expiration logic. A file without a date is permanent. A file with a date is a log entry.

---

## Memory Budget (inspired by Hermes)

MEMORY.md has a **soft budget of ~3,000 characters** (~1,000 tokens). This keeps evergreen memory lean enough to load in IDLE without consuming disproportionate context, while providing enough room for meaningful preference and pattern entries.

This is not a hard limit enforced by code — it is a guideline. When the DELIVER phase detects that MEMORY.md exceeds the budget, it flags it to the agent. The agent then decides what to consolidate, archive, or rephrase. This follows Hermes's philosophy: let the LLM perform its own importance assessment rather than relying on mechanical eviction algorithms.

Consolidation options when budget is exceeded:
- Merge duplicate or closely related entries
- Move resolved items (e.g., a fixed "never" rule) to dated files as context
- Archive project-specific knowledge to dated files
- Rephrase verbose entries concisely

## Phase-Transition Memory Reminders

Memory is not only loaded in IDLE. At each phase transition, a one-line check ensures continuity:

| Transition | Memory Action |
|-----------|--------------|
| IDLE → SPECIFY | Read `memory/MEMORY.md` for preferences and constraints |
| SPECIFY → PLAN | Check `memory/decisions.md` for relevant prior decisions |
| PLAN → IMPLEMENT | Check `memory/MEMORY.md` for workflow patterns |
| IMPLEMENT → VERIFY | No memory check needed |
| VERIFY → DELIVER | Check `memory/MEMORY.md` before writing session digest |
| Recovery | Read `memory/incidents.md` for similar past errors |

These reminders are lightweight — a single line of context that keeps memory active throughout the entire workflow, not just at the start.

---

## File Templates

### MEMORY.md (Permanent Memory)

```markdown
# Memory

## Preferences
<!-- User's coding workflow preferences -->
<!-- Added only when user explicitly asks: "Remember I prefer X" -->

## Never
<!-- Things that don't work for this user -->

## Patterns
<!-- Approaches that work well for this user/project -->

---
budget: ~X/3000 chars
```

### decisions.md (Permanent Memory)

```markdown
# Decisions

<!-- Log significant architectural or design decisions with rationale. -->
<!-- Format: -->
<!-- [YYYY-MM-DD] decision: <what was decided> | rationale: <why> | context: <what informed it> -->

## Decisions Log

```

### incidents.md (Permanent Memory)

```markdown
# Incidents

<!-- Error patterns and fixes. Two entry types: -->

<!-- Auto-logged (Error Handling step 5, no judgment): -->
<!-- [YYYY-MM-DD] error: <type> | cause: <root cause> | fix: <fix applied> -->

## Incident Log

```

### Dated Session File (YYYY-MM-DD.md)

```markdown
# YYYY-MM-DD

<!-- Session digests are appended here throughout the day. -->

<!-- Simple tasks use compact format: -->
<!-- [HH:MM] task: <desc> | outcome: PASS/FAIL | files: <n> | incidents: <n> -->

<!-- Standard/Complex tasks use rich format: -->
<!-- [HH:MM] task: <desc> | outcome: PASS/FAIL | files: <n> | incidents: <n> -->
<!--   decisions: <key decision made and why> -->
<!--   context: <what informed the approach> -->
<!--   caveats: <things to watch for> -->

```

---

## Storage Rules

- **Only save** user preferences when the user explicitly asks ("Remember I prefer X", "Always do Y")
- **Don't save** one-off requests, project-specific requirements, or temporary preferences
- **Ask before saving** a user preference: "Should I remember this preference?"
- **Session digests are written automatically** by the DELIVER phase — no approval needed
- **Incident log entries are written automatically** by Error Handling — no approval needed
- **Only modify files under `memory/`** — never modify other skill files
- **Create `memory/` directory and files on first write** if they do not exist

---

## Phase Integration

| Phase | Memory Action |
|-------|--------------|
| IDLE (action 4) | Read `memory/MEMORY.md` for preferences and patterns |
| Every phase transition | One-line check of relevant memory file |
| DELIVER (action 1) | Append session digest to `memory/YYYY-MM-DD.md` |
| DELIVER (action 2) | Check MEMORY.md budget (~3000 chars), flag if exceeded |
| Error Handling (step 5) | Append incident to `memory/incidents.md` |
