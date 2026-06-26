# Review Comment Templates

Use these templates for clear, actionable communication.

## Blocking Finding Template

`[P1][High] <file:line> - <issue title>`

- **What fails:**
- **Impact:**
- **Why this is likely:**
- **Minimal fix:**
- **How to verify:**

## Advisory Finding Template

`[P2][Medium] <file:line> - <improvement title>`

- **Current risk:**
- **Suggested improvement:**
- **Expected payoff:**

## Low-Confidence Question Template

`[Question][Low] <file:line> - <hypothesis>`

- Observed signal:
- Missing context:
- Clarification requested:

## No-Findings Summary Template

`No blocking defects found in reviewed scope.`

- Residual risks:
- Testing gaps:
- Suggested monitoring after release:

## Merge Recommendation Template

- **Recommend merge:** yes/no
- **Blocking count:**
- **Advisory count:**
- **Conditions before merge:**

## Tone Guardrails

- critique code, never author
- avoid sarcasm or absolute language
- keep each finding concise and evidence-based
