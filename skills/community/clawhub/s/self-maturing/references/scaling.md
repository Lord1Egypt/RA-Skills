# Scaling Rules

## Volume Thresholds

| Scale | Entries | Strategy |
|-------|---------|----------|
| Small | <100 | Single memory.md, no namespacing |
| Medium | 100-500 | Split into domains/, basic indexing |
| Large | 500-2000 | Full namespace hierarchy, aggressive compaction |
| Massive | >2000 | Archive yearly, summary-only HOT tier |

## When to Split

Create new namespace file when:
- Single file exceeds 200 lines
- Topic has 10+ distinct corrections
- User explicitly separates contexts ("for work...", "in this project...")

## Compaction Rules

### Merge Similar
```
BEFORE (3 entries):
- [02-01] Use tabs not spaces
- [02-03] Indent with tabs
- [02-05] Tab indentation please

AFTER (1 entry):
- Indentation: tabs (confirmed 3x, 02-01 to 02-05)
```

### Summarize Verbose
```
BEFORE:
- When writing emails to Marcus, use bullet points, keep under 5 items,
  no jargon, bottom-line first, he prefers morning sends

AFTER:
- Marcus emails: bullets ≤5, no jargon, BLUF, AM preferred
```

### Archive with Context
```
## Archived 2026-02

### Project: old-app (inactive since 2025-08)
- Used Vue 2 patterns
- CI on Jenkins (deprecated)

Reason: Project completed, patterns unlikely to apply
```

## Index Maintenance

Update index.md line counts during heartbeat maintenance. Format:

```markdown
# Memory Index

## HOT (always loaded)
- memory.md: 87 lines, updated 2026-02-15

## WARM (load on match)
- projects/current-app.md: 45 lines
- domains/code.md: 112 lines

## COLD (archive)
- archive/2025.md: 234 lines

Last compaction: 2026-02-01
```

## Multi-Project Patterns

### Inheritance
```
global (memory.md)
  └── domain (domains/code.md)
       └── project (projects/app.md)
```

Most specific wins. Project overrides domain overrides global.

### Override Syntax
In project file:
```markdown
## Overrides
- indentation: spaces (overrides global tabs)
- Reason: Project eslint config requires spaces
```

## Recovery

### Context Lost
1. Run `agent_memory.py boot` → prints recovery state
2. Read SESSION-STATE.md → current task
3. Read ~/self-improving/memory.md → learned patterns
4. Check index.md → find relevant namespace files
5. Search memory/ → find recent daily logs

### Corruption
1. Check archive/ for backup
2. Rebuild from corrections.md
3. Ask user to re-confirm critical items
