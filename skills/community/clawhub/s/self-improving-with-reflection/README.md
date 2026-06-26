# Self-Improving with Reflection

A self-improving agent skill that enables AI assistants to learn from corrections, reflect on their work, and compound execution quality over time.

## Overview

**Self-Improving with Reflection** transforms AI agents into learning systems that:

- **Learn from corrections** — Captures explicit user feedback and converts it into reusable patterns
- **Self-reflect** — Evaluates completed work to identify improvements
- **Organize memory** — Uses a tiered storage system (HOT/WARM/COLD) for efficient context management
- **Compound knowledge** — Patterns that work well are promoted; unused ones decay gracefully

## Architecture

```
self-improving/
├── memory.md          # HOT: ≤100 lines, always loaded
├── index.md           # Topic index with line counts
├── corrections.md     # Last 50 corrections log
├── reflections.md     # Self-reflection entries
├── projects/          # Per-project learnings
├── domains/           # Domain-specific (code, writing, comms)
└── archive/           # COLD: decayed patterns
```

### Memory Tiers

| Tier | Location | Size Limit | Behavior |
|------|----------|------------|----------|
| HOT | `memory.md` | ≤100 lines | Always loaded in context |
| WARM | `projects/`, `domains/` | ≤200 lines each | Load on context match |
| COLD | `archive/` | Unlimited | Load on explicit query |

## Features

### Learning from Corrections

Automatically detects and logs corrections when users say things like:

- "No, that's not right..."
- "Actually, it should be..."
- "Always do X for me"
- "I prefer Y over Z"

### Self-Reflection

After completing significant work, the agent evaluates:

1. Did the outcome meet expectations?
2. What could be improved?
3. Is this a reusable pattern?

### Automatic Promotion/Demotion

- Pattern used 3x in 7 days → promoted to HOT
- Pattern unused 30 days → demoted to WARM
- Pattern unused 90 days → archived to COLD

### Namespace Isolation

```
global (memory.md)
  └── domain (domains/code.md)
       └── project (projects/app.md)
```

Most specific namespace wins on conflicts.

## Quick Start

### 1. Create Memory Structure

```bash
mkdir -p self-improving/{projects,domains,archive}
```

### 2. Initialize Core Files

Create `self-improving/memory.md`:

```markdown
# Memory (HOT Tier)

## Preferences

## Patterns

## Rules
```

Create `self-improving/corrections.md`:

```markdown
# Corrections Log

| Date | What I Got Wrong | Correct Answer | Status |
|------|-----------------|----------------|--------|
```

Create `self-improving/index.md`:

```markdown
# Memory Index

| File | Lines | Last Updated |
|------|-------|--------------|
| memory.md | 0 | — |
| corrections.md | 0 | — |
```

### 3. Verify Setup

Run "memory stats" to confirm:

```
📊 Self-Improving Memory

🔥 HOT (always loaded):
   memory.md: 0 entries

🌡️ WARM (load on demand):
   projects/: 0 files
   domains/: 0 files

❄️ COLD (archived):
   archive/: 0 files
```

## User Commands

| Command | Action |
|---------|--------|
| "What do you know about X?" | Search all tiers for X |
| "Show my memory" | Display memory.md contents |
| "Show [project] patterns" | Load specific namespace |
| "Forget X" | Remove from all tiers |
| "Export memory" | Generate downloadable archive |
| "Memory stats" | Show tier sizes and health |

## Security Boundaries

### Never Store

- Credentials (passwords, API keys, tokens)
- Financial data (card numbers, bank accounts)
- Medical information
- Third-party personal information
- Location patterns

### Store with Caution

- Work context (decay after project ends)
- Emotional states (only if explicitly shared)
- Relationships (roles only, no personal details)

## File Reference

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition and rules |
| `setup.md` | First-time setup instructions |
| `memory-template.md` | Template for HOT memory |
| `learning.md` | Learning mechanics and triggers |
| `operations.md` | Memory operations guide |
| `boundaries.md` | Security and privacy rules |
| `scaling.md` | Scaling patterns for large memory |
| `reflections.md` | Self-reflection log |
| `corrections.md` | Corrections log template |

## License

MIT
