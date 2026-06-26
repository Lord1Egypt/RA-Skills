---
name: error-entry-template
---

# <YYYY-MM-DD-type-short-desc>

## Meta
- Type:         hallucination | user-correction | logic-error | code-bug | tool-misuse | skill-breach | behavior-drift | memory-gap | omission | judgment-error
- Severity:     critical | high | medium | low
- Status:       raw
- Captured:     YYYY-MM-DD HH:MM IST
- Context area: [topic/skill area]

## What Happened
[What exactly went wrong. Specific. No vague language.]

## Correct Version
[What should have been said/done/returned instead]

## Why It Happened
[Honest assessment — knowledge gap / reasoning shortcut / context miss / etc.]

## Impact
[How serious if not caught?]

## User Feedback
[Exact quote if user-correction. "self-detected" if not.]

## Fix Attempt Eligible
- Eligible: yes | no | uncertain
- Reason: [if no/uncertain]

## Timeline
- YYYY-MM-DD HH:MM — Entry created · source: [self/user]
