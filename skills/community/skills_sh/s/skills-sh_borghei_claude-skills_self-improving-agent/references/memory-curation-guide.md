# Memory Curation Guide

Read this for step-by-step memory review and promotion procedures, and for the continuous calibration (confidence scoring + belief revision) machinery.

## Memory Curation System

### The Memory Stack

```
┌─────────────────────────────────────────────────┐
│  CLAUDE.md / .claude/rules/                      │
│  Highest authority. Enforced every session.       │
│  Capacity: Unlimited. Load: Full file.           │
├─────────────────────────────────────────────────┤
│  MEMORY.md (auto-memory)                         │
│  Project learnings. Auto-captured by Claude.     │
│  Capacity: First 200 lines loaded. Overflow to   │
│  topic files.                                    │
├─────────────────────────────────────────────────┤
│  Session Context                                  │
│  Current conversation. Ephemeral.                │
│  Capacity: Context window.                       │
└─────────────────────────────────────────────────┘
```

### Memory Review Protocol

Run periodically (weekly or after every 10 sessions):

```
Step 1: Read MEMORY.md and all topic files
Step 2: Classify each entry

  Categories:
  - PROMOTE: Pattern proven 3+ times, should be a rule
  - CONSOLIDATE: Multiple entries saying the same thing
  - STALE: References deleted files, old patterns, resolved issues
  - KEEP: Still relevant, not yet proven enough to promote
  - EXTRACT: Recurring solution that should be a reusable skill

Step 3: Execute actions
  - PROMOTE entries → move to CLAUDE.md or .claude/rules/
  - CONSOLIDATE entries → merge into single clear entry
  - STALE entries → delete
  - EXTRACT entries → create skill package (see Skill Extraction)

Step 4: Verify MEMORY.md is under 200 lines
  - If over 200: move topic-specific entries to topic files
  - Topic files: ~/.claude/projects/<path>/memory/<topic>.md
```

### Promotion Criteria

An entry is ready for promotion when:

| Criterion | Threshold | Why |
|-----------|-----------|-----|
| Recurrence | Seen in 3+ sessions | Not a one-off |
| Consistency | Same solution every time | Not context-dependent |
| Impact | Prevented errors or saved significant time | Worth enforcing |
| Stability | Underlying code/system unchanged | Won't immediately become stale |
| Clarity | Can be stated in 1-2 sentences | Rules must be unambiguous |

### Promotion Targets

| Pattern Type | Promote To | Example |
|-------------|-----------|---------|
| Coding convention | `.claude/rules/<area>.md` | "Always use `type` not `interface` for object shapes" |
| Project architecture | `CLAUDE.md` | "All API routes go through middleware chain" |
| Tool preference | `CLAUDE.md` | "Use pnpm, not npm" |
| Debugging pattern | `.claude/rules/debugging.md` | "When tests fail, check env vars first" |
| File-scoped rule | `.claude/rules/<scope>.md` with `paths:` | "In migrations/, always add down migration" |

## Continuous Calibration

### Confidence Scoring

Every piece of learned knowledge carries a confidence score:

```
Confidence = base_score * recency_factor * consistency_factor

base_score:
  - User explicitly stated: 1.0
  - Observed from successful outcome: 0.8
  - Inferred from pattern: 0.6
  - Guessed from context: 0.3

recency_factor:
  - Last 7 days: 1.0
  - 7-30 days: 0.9
  - 30-90 days: 0.7
  - 90+ days: 0.5

consistency_factor:
  - Never contradicted: 1.0
  - Contradicted once, reaffirmed: 0.9
  - Contradicted, not reaffirmed: 0.5
  - Actively contradicted: 0.0 (delete)
```

### Belief Revision

When new information contradicts existing knowledge:

```
1. Compare confidence scores
2. If new info higher confidence → update knowledge
3. If roughly equal → flag for user confirmation
4. If new info lower confidence → keep existing, note conflict
5. Always log the conflict for review
```

## Workflows

### Workflow 1: Weekly Memory Health Check

```
1. Read all memory files (MEMORY.md + topic files)
2. Count total entries and lines
3. For each entry, classify: PROMOTE / CONSOLIDATE / STALE / KEEP / EXTRACT
4. Execute promotions (with user confirmation)
5. Execute consolidations
6. Delete stale entries
7. Verify under 200-line limit
8. Report: entries promoted, consolidated, deleted, remaining
```
