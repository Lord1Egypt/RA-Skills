---
name: scar-code-review
description: >
  Code review that learns from failures.
  Reflex arc blocks repeat mistakes without LLM calls.
  Combines systematic checklist review (security, performance, correctness, maintainability)
  with scar memory — when a review misses a bug, record a scar, and the reflex arc
  automatically flags similar patterns next time.
version: 0.1.0
author: b-button-corp
tags:
  - code-review
  - safety
  - memory
  - learning
  - scar
requires:
  binaries:
    - python3
---

# scar-code-review

## What this does

A code review system that **learns from its own misses**. Two layers work together:

1. **Checklist review** — Regex/heuristic checks across 4 dimensions:
   - **Security**: SQL injection, hardcoded secrets, XSS, eval/exec
   - **Performance**: N+1 queries, missing pagination, unbounded SELECTs
   - **Correctness**: Unchecked nulls, off-by-one patterns, unhandled promises
   - **Maintainability**: Long functions, deep nesting, magic numbers

2. **Scar reflex arc** — Pattern-matching against past review misses. When a review
   fails to catch a bug that later causes an incident, record a scar. Next time,
   the reflex fires before the LLM even looks at the diff.

No external dependencies. stdlib only. Python 3.9+.

## Quick start

Review a file:
```
python3 scar_code_review.py review path/to/file.py
```

Check a diff against past scars:
```
python3 scar_code_review.py check-diff path/to/changes.diff
```

Record a missed review finding:
```
python3 scar_code_review.py record-miss \
  --what-missed "Missed SQL injection in user input handler" \
  --pattern "execute.*format.*user" \
  --severity critical
```

## File format

JSONL, compatible with tetra-scar:

```json
{"id":"rscar_1234","what_missed":"...","pattern":"...","severity":"critical","created_at":"..."}
```

## Integration

```python
from scar_code_review import review, reflex_check, record_miss, load_review_scars

# Review a file
findings = review("app/views.py")
for f in findings:
    print(f"{f['severity']} [{f['dimension']}] {f['message']} (line {f['line']})")

# Check diff against past scars
scars = load_review_scars()
blocks = reflex_check(diff_text, scars)
for b in blocks:
    print(f"BLOCKED: {b}")

# Record a miss after an incident
record_miss(
    what_missed="Missed unvalidated redirect",
    pattern="redirect.*request\\.GET",
    severity="high",
)
```
