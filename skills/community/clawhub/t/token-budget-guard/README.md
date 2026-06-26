# Token Budget Guard 💰

> Your context window is a budget, not unlimited storage. This skill makes every token count — 99% savings proven possible.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-green.svg)]()
[![Skill](https://img.shields.io/badge/type-agent--skill-blue.svg)]()

## The Numbers

| Source | Finding |
|--------|---------|
| AAI Gateway | **99% token savings** via progressive disclosure |
| Typical session | **40-60%** of context wasted on redundant info |
| Multi-MCP workflows | 7,500 → **75 tokens** for tool schemas |

## The Problem

AI agents burn their context window on things they don't need:

| Waste Source | What Happens | Tokens Lost |
|-------------|-------------|-------------|
| Full tool schemas | Loading complete schemas for tools not used | 50-200 each |
| Raw conversation history | Every message preserved when summaries work | 500-5000 |
| Whole file reads | `cat file` when `grep` or `jq` would do | 1000s |
| Uncompressed outputs | Tool responses accumulate without pruning | Variable |
| Redundant context | Same info in multiple places | Duplicated |

**Result:** Agent hits context limit mid-task, loses earlier context, or can't complete complex workflows.

## The Solution

```
Context Window = Budget
Every token = $1
Spend wisely.
```

### 4 Core Strategies

#### 1. Progressive Disclosure (99% savings on tool schemas)

```
┌─────────────────────────────────────────────────────────┐
│  Level 0: Name only        → 1-5 tokens (listing)      │
│  Level 1: Summary          → 10-30 tokens (default)    │
│  Level 2: Full schema      → 50-200 tokens (when used) │
│  Level 3: With examples    → 200-500 tokens (learning) │
└─────────────────────────────────────────────────────────┘

Default: Level 1 (summary)
Escalate to Level 2 only when actively using the tool
```

**Before:** 150 tokens × 50 tools = 7,500 tokens
**After:** 25 tokens × 50 tools = 1,250 tokens + 150 when actually using one

#### 2. Conversation Compression

```
Turn 1-5:   Full context preserved
Turn 6-10:  Summarize turns 1-5, keep summary + recent
Turn 11+:   Aggressive summarization
80% full:   Drop everything except current task + compressed summary
```

#### 3. Selective File Operations

| Instead of | Use | Savings |
|-----------|-----|---------|
| `cat package.json` | `jq '.dependencies'` | ~80% |
| `cat file.js` | `grep -n "function" file.js` | ~90% |
| Full file | `head -50` + `tail -50` | ~70% |
| `cat *.log` | `grep "ERROR" *.log` | ~95% |

#### 4. Budget Monitoring

```
┌────────────────────────────────────────┐
│  Context Usage                         │
│  ████████████░░░░░░░░░░░░  52%         │
│                                        │
│  ⚠️ Alert at 60%: Consider compression │
│  🔴 Alert at 80%: Aggressive pruning   │
│  🚨 Alert at 90%: Emergency summarize  │
└────────────────────────────────────────┘
```

## Quick Start

```bash
# Claude Code
cp SKILL.md .claude/skills/token-budget-guard/

# OpenClaw
cp SKILL.md ~/.openclaw/workspace/skills/token-budget-guard/

# Cursor
cp SKILL.md .cursor/rules/token-budget-guard.mdc
```

Then tell your agent:
```
"Be token-efficient"
"Reduce my context usage"
"Am I running out of context?"
"Summarize earlier conversation"
```

## Real Impact Examples

### Multi-MCP Workflow
```
Before: 7,500 tokens (full schemas for all tools)
After:  75 tokens (stubs only, full schema on demand)
Saved:  99%
```

### Long Conversation
```
Before: 5,000 tokens (raw history)
After:  1,000 tokens (compressed summary + recent)
Saved:  80%
```

### File Analysis
```
Before: 2,000 tokens (cat large-file.js)
After:  600 tokens (grep + head/tail)
Saved:  70%
```

## Token Budget Guard vs Monitoring Tools

| | Monitoring Tools | Token Budget Guard |
|---|---|---|
| **Approach** | Retroactive analysis | Proactive prevention |
| **When** | After the session | During the session |
| **Output** | Cost dashboards | Context management rules |
| **Dependencies** | Python, JSONL parsing | None (pure markdown) |
| **Best for** | Understanding spend | Reducing spend |

**Use both!** Monitor with [codeburn](https://github.com/getagentseal/codeburn) or [token-dashboard](https://github.com/nateherkai/token-dashboard), prevent with this skill.

## What's Included

- **SKILL.md** — Complete token management framework
- **COST_TRACKING_TEMPLATE.md** — Template for tracking token costs over time

## Works With

- [OpenClaw](https://openclaw.ai)
- Claude Code
- Cursor
- Codex
- Any agent framework

## Related Skills

| Skill | Purpose |
|-------|---------|
| [Context Optimizer](https://github.com/aptratcn/openclaw-context-optimizer) | OpenClaw-specific context management |
| [Error Recovery](https://github.com/aptratcn/skill-error-recovery) | Handle context overflow errors |

## License

MIT — Spend wisely.
