---
name: strategy-constitutional-memory
description: A living knowledge base of hard-earned strategy lessons and banned code patterns — prevents repeating past mistakes across strategy iterations by scanning code for violations and generating decision context.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "\U0001F4DC"
---

# Strategy Constitutional Memory

Stop making the same mistakes twice. This skill maintains a "constitutional memory" of lessons learned from past strategy iterations and a list of banned code patterns. Before generating new strategy code, the AI reads the constitution. After writing code, it scans for violations.

## When to use

- Starting a new strategy iteration: "What lessons should I remember?"
- After writing strategy code: "Scan this code for violations"
- After a failed backtest: "Add this lesson to the constitution"
- When reviewing strategy history: "Show me all critical lessons"

## Core Concepts

### Lessons
Structured records of what went wrong (or right) in past iterations:

```json
{
  "strategy": "v6",
  "category": "death_spiral",
  "description": "Periodic rebalance caused death spiral: sell anchor -> buy options -> expire worthless -> sell more",
  "evidence": "v6(-82%), v7(-71%), v8(-78.5%), v9(-71.8%)",
  "severity": "critical"
}
```

Severity levels: `critical` > `high` > `medium` > `low`

Categories: `drawdown`, `selection`, `position_sizing`, `timing`, `survival_structure`, `ml_failure`, `success`

### Bans
Code patterns that are absolutely prohibited because they've been proven catastrophic:

```json
["rebalance_qqq", "SetHoldings", "hard_stop_loss", "XGBClassifier"]
```

The scanner is case-insensitive and skips comments and string literals.

## API

### Initialize
```python
from memory_system import ConstitutionalMemory

memory = ConstitutionalMemory(memory_dir="./memory")
```

### Add a lesson
```python
memory.add_lesson(
    strategy_name="v6",
    category="death_spiral",
    description="Periodic equity rebalance caused -82% drawdown",
    evidence="DD: 82%, triggered at 20% progress",
    severity="critical",
    new_ban="rebalance_anchor"  # optionally add a new banned pattern
)
```

### Auto-extract lessons from diagnosis report
```python
memory.add_lesson_from_diagnosis("v30", diagnosis_report_text)
# Automatically detects: high drawdown, high zero rate, negative ROI
```

### Scan code for violations
```python
violations = memory.scan_code(strategy_code_string)
# Returns: [{"pattern": "rebalance_qqq", "line": 42, "content": "def rebalance_qqq():"}]
```

The scanner:
- Is case-insensitive
- Tracks multi-line strings (triple quotes) and skips them
- Skips comment lines (`#`)
- Strips inline strings and comments before matching

### Generate LLM context
```python
context = memory.get_context(max_lessons=30)
# Returns formatted text with lessons sorted by severity,
# banned patterns list, verified blueprints, and core rules
```

Feed this directly into your LLM system prompt before strategy generation.

## CLI Usage

```bash
# Get decision context (lessons + bans + blueprints)
python3 -m orchestrator briefing

# Scan a strategy file for violations
python3 -m orchestrator scan --code path/to/strategy.py

# Record an iteration result (auto-adds lessons for failures)
python3 -m orchestrator record \
  --name "my_strategy_v2" \
  --blueprint "baseline" \
  --dimension "position_sizing" \
  --hypothesis "Reduce Kelly from 3% to 2%" \
  --status "early_stop" \
  --drawdown 0.55
```

## Storage

- `memory/lessons.json` — Growing list of lessons (auto-persisted)
- `memory/bans.json` — Banned code patterns (auto-persisted)

Both files are JSON and human-readable. You can manually edit them.

## Seeding

For new projects, call `memory.seed_from_history()` to populate with your initial lessons. The method is idempotent — it won't overwrite existing data.

## Why This Matters

In iterative strategy development, the biggest risk isn't finding the right approach — it's **re-trying approaches that already failed**. With 20+ iterations, no human (or LLM) can remember every lesson. Constitutional memory makes failures permanent knowledge.

## Rules

- **Never bypass the code scanner.** Always run `scan_code()` on new strategy code before submission. The scanner exists to prevent known-fatal patterns from being re-tested.
- **Lessons are append-only by design.** Do not delete lessons from `lessons.json` unless you are certain the lesson was recorded in error. Deleting valid lessons re-opens the door to repeating past failures.
- **Severity levels are immutable once assigned.** A "critical" lesson should never be downgraded. If you disagree with a severity, add a new lesson with updated context rather than editing the original.
- **Bans are absolute prohibitions.** A banned pattern means "this has been proven catastrophic — do not use under any circumstances." If you believe a ban should be lifted, add a new lesson documenting why before removing the ban.
- **Always call `get_context()` before generating new strategy code.** The constitutional context must be in the LLM's prompt to prevent re-exploring failed approaches.
