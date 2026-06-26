---
name: self-improvement-cyber-bye-on-error-hook
description: Fires immediately on error detection. Writes to errors/raw/ before any other action.
---

# On-Error Hook — Immediate Capture

## Trigger Conditions

| Signal | Detection |
|---|---|
| Self-detected hallucination | Agent recognizes stated fact is wrong |
| User correction | "wrong" / "incorrect" / "that's not right" / "you made a mistake" |
| Logic flaw | Agent finds error in its own prior reasoning |
| Code bug noticed | Agent spots defect in generated code |
| Skill contract violated | Any AGENT.md rule broken |
| Context forgotten | Agent missed earlier info from same session |
| Tool misuse | Wrong tool, wrong params, wrong sequence |
| Behavior drift | Response doesn't match persona/skill spec |

---

## Step 1 — Slug Generation

```
slug = YYYY-MM-DD-<error_type>-<3-word-kebab-desc>
```

---

## Step 2 — Minimum Viable Write (do this NOW)

Write to `errors/raw/<slug>/entry.md` IMMEDIATELY:

```markdown
# <slug>
## Meta
- Type:     <error_type>
- Severity: critical | high | medium | low
- Status:   raw
- Captured: YYYY-MM-DD HH:MM IST
## What Happened
[one sentence]
## Context
[one sentence]
## Source
[self-detected | user-correction | post-hoc]
```

---

## Step 3 — Complete Entry After Response

```markdown
## Full Description
[What exactly was wrong. Specific.]

## Correct Version
[What should have been said/done/returned]

## Why It Happened
[Honest assessment]

## Impact
[How serious if not caught?]

## User Feedback
[Exact quote if user-correction. "self-detected" if not.]

## Fix Attempt Eligible
[yes | no | uncertain + reason]

## Timeline
- YYYY-MM-DD HH:MM — Entry created
```

---

## Step 4 — Severity-Based Immediate Actions

| Severity | Additional actions |
|---|---|
| `critical` | Write to soul [CRITICAL FLAGS] immediately |
| `critical` | Surface next session start regardless of nightly |
| `high` | Surface next session start if not yet addressed |
| `medium` / `low` | Handle at nightly review |

---

## Step 5 — Update Memory Index

Append to `memory/index.json` under `errors[]`:

```json
{
  "slug": "<slug>",
  "type": "<error_type>",
  "severity": "<severity>",
  "status": "raw",
  "captured": "<ISO datetime>",
  "summary": "<one line>"
}
```
