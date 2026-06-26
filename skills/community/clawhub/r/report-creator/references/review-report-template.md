# Review Report Template

Use this template when presenting a report-review result to the user after `--review`, a silent final review pass audit, or a demo comparison.

```markdown
# Report Review Report

**Target file:** `[path/to/report.html]`
**Review mode:** `--review` | `--generate (silent final review)` | `manual demo`
**Language:** `zh` | `en`
**Review scope:** `13-checkpoint review system`

## Summary

- Overall assessment: `[one-sentence judgment]`
- Primary improvement area: `[opening | heading stack | prose density | data interpretation | skimmability]`
- Biggest remaining limitation: `[brief note or "none in this pass"]`

## Triggered Checkpoints

### 1. BLUF Opening
- Status: `fixed | unchanged | skipped`
- Before: `[short quote or paraphrase]`
- After: `[short quote or paraphrase]`
- Why it mattered: `[one sentence]`

### 2. Heading Stack Logic
- Status: `fixed | unchanged | skipped`
- Before:
  - `[old h2/h3]`
- After:
  - `[new h2/h3]`
- Why it mattered: `[one sentence]`

### 3. Anti-Template Section Headings
- Status: `fixed | unchanged | skipped`
- Notes: `[brief note]`

### 4. Prose Wall Detection
- Status: `fixed | unchanged | skipped`
- Notes: `[brief note]`

### 5. Takeaway After Data
- Status: `fixed | unchanged | skipped`
- Notes: `[brief note]`

### 6. Insight Over Data
- Status: `fixed | unchanged | skipped`
- Notes: `[brief note]`

### 7. Scan-Anchor Coverage
- Status: `fixed | unchanged | skipped`
- Notes: `[brief note]`

### 8. Conditional Reader Guidance
- Status: `fixed | unchanged | skipped`
- Notes: `[brief note]`

## Not Applied

- `[checkpoint or rejected candidate]` — `[why it was not appropriate in this document]`

## Files

- Before: `[path/to/before.html]`
- After: `[path/to/after.html]`
- Screenshot before: `[path/to/before.png]`
- Screenshot after: `[path/to/after.png]`

## Reviewer Notes

- Keep this section short and factual.
- Distinguish between issues the system fixed and issues intentionally left alone.
- Do not claim factual corrections unless the source actually supported them.
```
