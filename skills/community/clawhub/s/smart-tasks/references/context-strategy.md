# Context Window Management Strategy

The core challenge: task data grows, but context windows don't.
This strategy keeps token usage minimal while maintaining full awareness.

## Layered Reading Pattern

```
Layer 1 — Always read
  └── tasks/INDEX.md (~1-2KB)
        Full task awareness in one file.

Layer 2 — On demand
  └── tasks/active/{file}.md (~0.5-1KB each)
        Read only when detail is needed.
        Max 2-3 files per interaction.

Layer 3 — Rarely
  └── tasks/done/, tasks/archive/
        Only for weekly review or explicit search.
```

### When to Read What

| Scenario | Read INDEX | Read Active Files | Read Done/Archive |
|----------|-----------|-------------------|-------------------|
| Session startup | ✅ | ❌ | ❌ |
| "What's my status?" | ✅ | ❌ | ❌ |
| "Tell me about task T-005" | ✅ (find it) | ✅ (that one) | ❌ |
| "What should I do today?" | ✅ | ✅ (top 2-3) | ❌ |
| Creating a new task | ✅ + .meta.json | ❌ | ❌ |
| Completing a task | ✅ | ✅ (that one) | ❌ |
| Weekly review (cron) | ✅ | ✅ (all active) | ✅ (done/ scan) |
| "What did I finish last month?" | ❌ | ❌ | ✅ (done/ + archive/) |

### Decision Rule

> If INDEX.md alone can answer the question, do NOT read individual files.

This single rule saves the most tokens across all interactions.

## INDEX.md Size Management

INDEX.md must stay small. It is read at every session start.

| Active Tasks | Estimated Size | Strategy |
|-------------|---------------|----------|
| 1–20 | ~1KB | Full table with all columns |
| 20–50 | ~2.5KB | Abbreviate Later section (ID + Title + Due only) |
| 50+ | ~5KB+ | Split into per-category indexes |

### Splitting Strategy (50+ tasks)

When active tasks exceed 50, create category-specific indexes:

```
tasks/
├── INDEX.md              # Summary only: counts per category + overdue list
├── INDEX-research.md     # Full table for Research category
├── INDEX-teaching.md     # Full table for Teaching category
└── ...
```

Main INDEX.md becomes a routing file:

```markdown
# Tasks Index

> Active: 62 | Overdue: 3

## 🔴 Overdue (all categories)
| ID | Title | Due | Priority | Category |
...

## Category Summary
| Category | Active | Due This Week |
|----------|--------|---------------|
| Research | 25 | 4 |
| Teaching | 18 | 2 |
| Admin | 12 | 1 |
| Personal | 7 | 0 |

See: INDEX-research.md, INDEX-teaching.md, etc.
```

Read category index only when that category is relevant.

## Subagent & Cron Cost Optimization

Cron jobs run on Sonnet-class models. Optimize their token usage:

### Early Exit Pattern

```
1. Read INDEX.md
2. Check if any tasks match alert criteria
3. If NO match → HEARTBEAT_OK (exit, ~200 tokens total)
4. If match → read relevant detail files → compose message
```

The deadline-check cron should exit early on most runs (no alerts needed).

### Token Budget Estimates (per cron run)

| Job | No Alert | With Alert |
|-----|----------|------------|
| Morning briefing | ~500 tokens | ~1500 tokens |
| Deadline check | ~200 tokens | ~800 tokens |
| Weekly review | N/A (always runs) | ~3000 tokens |

### Batching Reads

When multiple task files need reading (e.g., weekly review):
- Read all active files in one batch rather than one-by-one
- Use `cat tasks/active/*.md` or sequential reads
- This avoids repeated tool-call overhead

## Cost-Saving Tips

1. **Don't read done/archive/ during normal conversation.** Only weekly review.
2. **Prefer INDEX answers.** "How many tasks?" → INDEX. Don't read files.
3. **Limit detail reads to 3 files per interaction** unless explicitly asked.
4. **Cron: Sonnet always.** Never use Opus for scheduled task checks.
5. **Silent when empty.** Deadline check with no alerts = no message = minimal cost.
