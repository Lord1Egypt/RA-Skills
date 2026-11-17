# Priority Patterns — Learning Protocol

This file is the protocol. The learned data lives in `~/Clawic/data/triage/patterns.md` (create the directory on first confirmed rule; never write a rule the user hasn't confirmed).

## Confidence Ladder

| Level | Enters when | Action |
|-------|-------------|--------|
| `observed` | 1 correction | Record only — never apply |
| `pattern` | 2 same-direction corrections | Propose: "Should [task type] default to P[n]?" |
| `confirmed` | Explicit user yes | Apply automatically; cite the rule when applying |
| `locked` | Confirmed + several applications with no pushback | Apply without citing each time; revisit only on contradiction |

Decay (rules weaken, they don't live forever):

- `confirmed` contradicted once → drops to `pattern`; contradicted twice → retire the rule and ask fresh.
- Before weakening, check for a **split**: if a condition explains both behaviors (e.g., pre-release vs. normal weeks), split the rule instead of degrading it. Splitting beats weakening whenever a condition separates the contradictions.
- An unconfirmed `observed`/`pattern` entry untouched for ~2-3 months → archive it; stale evidence shouldn't seed proposals. Confirmed rules never expire by time, only by contradiction.

## Memory Format

One line per rule: `pattern: Pn (confidence) [evidence]`

```
deploy-issues: P0 (confirmed) [user: "always interrupt for deploys"]
refactoring: P2 (pattern) [deprioritized 2x: 03-12, 03-19]
docs-updates: P3 (confirmed) [explicit: "docs are never urgent"]
```

Sections of the memory file: **By Task Type** · **By Source** (incl. sender calibration, see `signals.md`) · **By Time** · **Override Log**.

## Worked Lifecycle

1. Mar 12 — you set a refactor task P1; user: "this can wait" → P2. Write: `refactoring: P2 (observed) [03-12]`.
2. Mar 19 — same correction. Now `pattern`; propose: "Twice you've moved refactoring to P2 — default it there?"
3. User says yes → `confirmed`. On next use, cite it: "Refactor request → P2 (your standing rule)."
4. Jun 02 — user bumps a refactor to P1. Before weakening, check context: it's release week. A condition explains it → split: `refactoring: P2 (confirmed), except release week → P1 (observed)`. The exception climbs its own ladder.

## Conflict Resolution

- Two rules match at different levels → **more specific wins**: task-type beats source, source beats time-of-day.
- Equally specific → higher priority wins (misclassifying down is the expensive error — SKILL.md Core Rules #3).
- Any rule vs. an explicit instruction right now → the instruction wins; log it as a potential contradiction against the rule.
- Rules conflict and no specificity tiebreak applies → ask; a wrong silent guess costs more than the question.

## Drift Detection

Weekly, compare the priority distribution of handled items:

- P0+P1 above the drift threshold (canonical: SKILL.md Core Rules #6, ~1/3) → the bar drifted down; re-anchor on the level tests.
- Nearly everything landing P3 → triage is too timid; propose tightening the P2 tests with the user.
- A P2 that became a P0 without new external facts → triage failure; log it in the Override Log with `"aged"` as the reason.

## Override Log

Keep the last 10 overrides in the memory file:

```
[DATE] task: old_priority → new_priority "reason"
```

Overrides are the raw data; rules are the compression. Every proposal must cite its two dates from this log — a proposal that can't name its evidence isn't ready to be proposed.
