# Promotion & Demotion Rules

## Promotion Ladder

### RAW → WARM (domain/project memory)

Promote when:
- Pattern appears 2x with evidence.
- Still context-specific (one domain or project).

Target: `.self-improving/domains/<domain>.md` or `.self-improving/projects/<project>.md`.

### RAW/WARM → HOT

Promote when:
- Pattern appears 3x within 7-30 days.
- Applies across multiple tasks or contexts.
- Can be expressed as a single actionable line.

Target: `.self-improving/HOT.md`.

### HOT → Workspace files

Promote when:
- Pattern is stable and repeatedly useful.
- Applies long-term, not just a phase.
- Worth embedding in the agent's permanent behavior.

Targets:
- `SOUL.md` — behavioral patterns, communication style.
- `AGENTS.md` — workflow rules, operational patterns.
- `TOOLS.md` — tool gotchas, integration notes.
- `MEMORY.md` — user preferences, decisions, long-term context.

## Demotion Ladder

### HOT → WARM

Demote when:
- Entry unused for 30+ days.
- Context has changed (project ended, tool replaced).

Move to the most relevant `domains/` or `projects/` file.

### WARM → COLD (archive)

Demote when:
- Entry unused for 90+ days.
- No longer relevant to active work.

Move to `.self-improving/archive/YYYY-MM.md`.

### COLD → Delete

Only with explicit user confirmation. Default: keep archived forever.

## Compaction Rules

When a file exceeds its size limit:

1. Merge similar entries into a single consolidated rule.
2. Summarize verbose entries into one-liners.
3. Archive the least-recently-used entries.
4. Never lose confirmed user preferences.

## Conflict Resolution

When two patterns contradict:

1. **Most specific wins**: project > domain > HOT/global.
2. **Same specificity**: most recent wins.
3. **Ambiguous**: ask the user, then log the decision.
