---
name: redline
description: Review and redline DOCX contracts paragraph by paragraph with tracked changes, clause-level risk analysis, and draft comment responses. Use when a user wants contract revisions that are specific to each paragraph or bullet, especially for privacy, security, data-processing, liability, AI, or other negotiated legal terms.
---

# Redline

## Overview

Use this skill to review contract `.docx` files at paragraph level and generate:
- a tracked-changes amended `.docx`
- a risk-report `.docx`
- a `.review.json` review dataset

Do not collapse multiple operative paragraphs into one generic comment. Each non-empty paragraph or bullet must be reviewed on its own merits, with distinct risk analysis and replacement language where needed.

## Workflow

1. Confirm the supported party and the priority risk areas.
2. Run `scripts/contract_review_pipeline.py init-review` for each source `.docx`.
3. Review the generated `.review.json` paragraph by paragraph.
4. For each `clauses[]` entry, write a specific assessment tied to that paragraph only:
   - `favorability`
   - `risk_level`
   - `risk_summary`
   - `why_it_matters`
   - `proposed_replacement`
5. Draft specific responses for any opponent comments in `opponent_comments[]`.
6. Run `materialize` to create the amended `.docx` and risk report `.docx`.
7. Verify the outputs exist and the tracked changes are readable.

## Required Review Standard

- Treat each review unit as one paragraph-level issue, not a whole section summary.
- Do not reuse the same replacement text across unrelated paragraphs.
- If several bullets in the same section have different obligations, analyze and redraft them separately.
- Keep replacement language narrow and operational. Match the exact risk in the source paragraph.
- When reviewing privacy and security language, check for:
  - uncapped or super-capped liability exposure
  - audit overreach
  - subprocessor approval friction
  - cross-border transfer restrictions
  - incident notification deadlines
  - certifications, penetration testing, and customer testing rights
  - unilateral policy updates
  - AI/security terms that exceed the actual service model

## Commands

Initialize a review file:

```bash
python scripts/contract_review_pipeline.py init-review \
  --input <contract.docx> \
  --output <contract.review.json> \
  --supported-party "<party>" \
  --focus-area "<area-1>" \
  --focus-area "<area-2>" \
  --opponent-comment-author "<author-1>"
```

Materialize the outputs:

```bash
python scripts/contract_review_pipeline.py materialize \
  --input <contract.docx> \
  --review-json <contract.review.json> \
  --amended-output <contract.amended.docx> \
  --report-output <contract.risk-report.docx> \
  --author "Codex Redline Reviewer"
```

## Resources

- JSON field details: `references/review-json-schema.md`
- Main tool: `scripts/contract_review_pipeline.py`

