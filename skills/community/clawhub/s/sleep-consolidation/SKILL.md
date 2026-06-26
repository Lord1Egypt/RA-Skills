---
name: sleep-consolidation
description: >
  Use this skill to consolidate an AI agent's daily experiences and learnings into
  structured long-term memory, mimicking human sleep-based memory consolidation.
  Trigger this skill whenever: an agent session ends and there are new learnings to store,
  a user asks the agent to "sleep", "consolidate memory", or "process today's learnings",
  the agent's working memory is getting full and needs compression,
  the context window is approaching its limit and memories need flushing,
  or you want to extract insights from accumulated interaction logs.
  The skill runs three modes: micro-rest (waking replay for quick within-session notes),
  NREM (deep structured consolidation with dual fast/slow tracks), and
  REM (creative cross-domain synthesis). Memory is stored as plain Markdown files
  following OpenClaw's two-layer architecture. Always use this skill at the end of
  long agent sessions, before context compaction, and whenever explicitly asked to "remember".
---

# Agent Sleep Consolidation — v2

Biologically-grounded memory consolidation for AI agents, based on:
- **Eichenlaub et al. 2020** (Cell Reports): Neural replay in human motor cortex — waking rest consolidates too; NREM1 shows compressed (fast) AND dilated (slow) dual-track replay; replay prioritizes weakly-learned items
- **Walker, "Why We Sleep"**: NREM hippocampus→cortex transfer, synaptic pruning (~20%), REM creative synthesis
- **OpenClaw memory architecture**: Markdown-as-truth, two-layer files, pre-compaction flush, hybrid BM25+vector recall

See `references/workspace_layout.md` for full file format examples.
See `references/memory_schema.md` for Markdown conventions and type system.

---

## Memory workspace layout

```
~/.agent_workspace/
├── MEMORY.md                  ← long-term: durable facts, preferences, decisions
├── memory/
│   └── YYYY-MM-DD.md          ← daily log (append-only; load today + yesterday)
└── bank/
    ├── entities/              ← per-person or per-project pages
    └── concepts/              ← per-topic deep-dives
```

**Core rule**: The agent only "remembers" what gets written to disk. Never keep important things in RAM.

---

## Three consolidation modes

| Mode | Biological analog | When to use | Script |
|------|-------------------|-------------|--------|
| **micro-rest** | Waking neural replay (Eichenlaub 2020) | Mid-session, after any significant exchange | `scripts/micro_rest.py` |
| **nrem** | NREM deep sleep, hippocampus→cortex | End of session, context nearing limit | `scripts/sleep_cycle.py --phase nrem` |
| **rem** | REM dream synthesis | After NREM, or standalone for insight | `scripts/sleep_cycle.py --phase rem` |
| **both** | Full overnight cycle | End of day / long session | `scripts/sleep_cycle.py --phase both` |

---

## Mode 1 — Micro-rest (waking replay)

Quick append to today's daily log. No LLM call — pure write. Based on the paper's finding that waking replay occurs during rest blocks immediately after learning.

```bash
python scripts/micro_rest.py \
  --note "User prefers TypeScript; rejected Python suggestion" \
  --type O \
  --workspace ~/.agent_workspace
```

```bash
# Pre-compaction flush: extract worth-retaining from raw context
python scripts/micro_rest.py \
  --flush \
  --context-dump "$(cat session_log.txt)" \
  --workspace ~/.agent_workspace
```

**Memory type prefixes** (W/B/O/S system from OpenClaw research):

| Prefix | Meaning | Example |
|--------|---------|---------|
| `W` | World fact (objective) | `W: Redis default port is 6379` |
| `B` | Biographical/experience | `B: Fixed the auth bug by wrapping in try/catch` |
| `O(c=N)` | Opinion/preference + confidence 0–1 | `O(c=0.9): User prefers concise replies under 200 words` |
| `S` | Summary/synthesis (generated) | `S: Three sessions used streaming; all had lower latency` |

Each entry is appended to `memory/YYYY-MM-DD.md` under a `## Retain` section.

---

## Mode 2 — NREM consolidation

Two-track processing based on the paper's temporal replay findings:

- **Fast track** (compressed replay, ~0.1x duration): high-confidence facts → `MEMORY.md`
- **Slow track** (dilated replay, 1.5–2x duration): weakly-learned or uncertain items the paper shows replay *prioritizes* these → `bank/` for deeper storage

```bash
python scripts/sleep_cycle.py --workspace ~/.agent_workspace --phase nrem
```

The script reads today's daily log + current `MEMORY.md`, then calls Claude:

### NREM system prompt

```
You simulate NREM deep-sleep memory consolidation for an AI agent.

Two-track processing:

FAST TRACK (compressed replay — high-confidence, clear facts):
  - Distill into single-sentence durable memories for MEMORY.md
  - Prune ~20% as redundant (synaptic homeostasis: sleep removes weak connections)
  - Use prefixes: W (world fact), B (experience), O(c=N) (opinion + confidence), S (summary)

SLOW TRACK (dilated replay — weakly-learned, uncertain, needing reinforcement):
  - Expand on low-confidence or partial-knowledge items
  - Write to bank/ as entity or concept pages
  - These are what human NREM prioritizes (Schapiro et al. 2018)

Respond ONLY with valid JSON:
{
  "memory_md_updates": [
    {
      "action": "add|update|remove",
      "type": "W|B|O|S",
      "confidence": 0.0,
      "text": "single sentence",
      "replaces": "old text if action=update"
    }
  ],
  "bank_updates": [
    {
      "slug": "topic-slug",
      "kind": "entity|concept",
      "section": "## Section heading",
      "content": "markdown block"
    }
  ],
  "pruned_count": 0,
  "weakly_learned": ["items for slow-track attention"],
  "open_questions": ["gaps for next session"]
}
```

---

## Mode 3 — REM synthesis

Creative cross-domain connections. The dreaming brain ignores conventional logic.

```bash
python scripts/sleep_cycle.py --workspace ~/.agent_workspace --phase rem
```

### REM system prompt

```
You simulate REM dream-sleep creative synthesis for an AI agent.
Find non-obvious connections. Update beliefs where evidence shifted.

Tasks:
1. Cross-domain links between today's memories and MEMORY.md
2. Update O(c=N) confidence values where evidence has shifted
3. Generate concrete next-session actions
4. Propose new bank/ pages if a topic recurred 3+ times this session

Respond ONLY with valid JSON:
{
  "aha_moments": ["string"],
  "creative_connections": [{"link": "A ↔ B", "why": "string"}],
  "confidence_updates": [
    {"item": "text excerpt", "old_c": 0.0, "new_c": 0.0, "reason": "string"}
  ],
  "new_bank_suggestions": [
    {"slug": "string", "kind": "entity|concept", "seed_content": "markdown"}
  ],
  "next_session_actions": ["string"]
}
```

---

## Pre-compaction flush

Mirrors OpenClaw's `memoryFlush` mechanism. Triggered when context approaches token limit. Runs silently (no user output).

Configure the threshold (equivalent to OpenClaw's `softThresholdTokens`):

```bash
# When session token estimate > (context_window - 20000 - 4000):
python scripts/micro_rest.py --flush --context-dump "..." --workspace ~/.agent_workspace
```

The `--flush` flag calls Claude to extract durable memories from the raw context dump, then writes them to the daily log. **One flush per compaction cycle.**

---

## Loading memory at session start

```python
from scripts.load_memory import get_context

system_addendum = get_context(
    workspace="~/.agent_workspace",
    max_memory_chars=3000,   # MEMORY.md snippet (fits ~2k tokens)
    load_yesterday=True      # also load yesterday's daily log
)
# Inject system_addendum into system prompt
```

Loaded content:
1. Full `MEMORY.md` (trimmed to `max_memory_chars`)
2. Today's daily log (if exists)
3. Yesterday's daily log (if `load_yesterday=True`)

---

## Full session workflow

```bash
# Session start: inject memory into system prompt (in Python)

# During session: micro-rest after significant exchanges
python scripts/micro_rest.py --note "..." --type W --workspace ~/.agent_workspace

# If context > 80% full: flush before compaction
python scripts/micro_rest.py --flush --context-dump "..." --workspace ~/.agent_workspace

# Session end: full sleep cycle
python scripts/sleep_cycle.py --phase both --workspace ~/.agent_workspace
```

---

## Troubleshooting

| Problem | Solution |
|--------|----------|
| `MEMORY.md` growing too large | Run with `--prune-memory` flag — NREM removes redundant entries |
| Bank file stale | Delete it; NREM regenerates next session |
| REM generating hallucinations | Add `"Be strictly grounded. No invention."` to REM prompt |
| Micro-rest called too often | Add 5-min cooldown check in calling code |
| Flush extracting too little | Lower the `softThresholdTokens` equivalent; flush earlier |
| Replay not strengthening weak items | Check that NREM prompt slow-track section explicitly lists `weakly_learned` items |
