---
name: tetra-scar
description: >
  Scar memory, reflex arc, and decision traces for AI agents.
  Learn from failures permanently. Block repeated mistakes instantly — no LLM calls needed.
  Three-layer memory: scars (immutable failures) + narrative (overwritable) + decision traces (judgment paths → LoRA training data).
version: 0.3.0
author: b-button-corp
tags:
  - safety
  - memory
  - agent-reliability
  - failure-prevention
  - reflex-arc
requires:
  binaries:
    - python3
---

# tetra-scar

## What this does

Your agent keeps making the same mistakes. tetra-scar gives it a **scar layer** — immutable records of past failures that are checked before every action, without calling the LLM.

Two-layer memory:
- **Scar layer** (immutable): "What broke and what must never happen again." Cannot be deleted.
- **Narrative layer** (mutable): "What was done and who benefited." Overwritable.

Plus a **reflex arc** — pattern-matching against scars that fires before the LLM even sees the task. If a proposed action matches a past failure pattern, it's blocked instantly.

## Quick start

After any failure, record a scar:
```
python3 tetra_scar.py scar-add \
  --what-broke "Deployed to production without running tests" \
  --never-again "Always run full test suite before any deployment"
```

Before any action, check the reflex:
```
python3 tetra_scar.py reflex-check --task "Deploy latest changes to production"
# Output: BLOCKED — scar collision: "Always run full test suite..."
```

After any success, record the narrative:
```
python3 tetra_scar.py narrate --what "Deployed v2.1 after full test pass" --who "Users"
```

## How the reflex arc works

The reflex arc extracts keywords from each scar's `never_again` field:
- English words (3+ characters)
- Japanese kanji/katakana units (2+ characters)

When a task description matches 40%+ of a scar's keywords (minimum 2), it's blocked.
No LLM judgment. No API calls. No latency. Pure pattern matching.

## The 4-axis check (tetra-check)

For deeper validation, `tetra-check` evaluates a task against 4 axes:

1. **Emotion axis**: Does the task have motivation? (non-empty description)
2. **Action axis**: Is it concrete? (contains action verbs)
3. **Life axis**: Does it collide with any scar? (reflex arc)
4. **Ethics axis**: Does it involve dangerous operations? (rm -rf, DROP TABLE, etc.)

All 4 must pass. Any failure rejects the task with a specific reason.

```
python3 tetra_scar.py tetra-check --task "Refactor the auth module"
# Output: APPROVED — all 4 axes passed
```

## File format

JSONL (one JSON object per line). Human-readable. Git-friendly.

**scars.jsonl**: `{"id":"scar_001","what_broke":"...","never_again":"...","created_at":"..."}`
**narrative.jsonl**: `{"id":"narr_001","what":"...","who_benefited":"Users","created_at":"..."}`

## Integration

```python
from tetra_scar import reflex_check, read_scars, write_scar, write_narrative

# Before execution
scars = read_scars()
block = reflex_check(task_description, scars)
if block:
    print(f"BLOCKED: {block}")
else:
    # execute task...
    if failed:
        write_scar("What broke", "What must never happen again")
    else:
        write_narrative("What was done", "Who benefited")
```

## Philosophy

Built by Tetra Genesis (B Button Corp, Nagoya, Japan).

Agents that can't remember their failures are doomed to repeat them.
Scars are not bugs — they're the immune system.
Every cycle must answer: "Who did this make happy?"
