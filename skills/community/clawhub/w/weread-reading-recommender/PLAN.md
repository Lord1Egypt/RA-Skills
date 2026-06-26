# PLAN.md — weread-reading-recommender

## Goal
Build a local-first draft skill that reads 微信读书 (WeRead) records using a cookie kept only on the user's machine, exports the data to JSON, normalizes it into a recommendation-friendly format, and then lets the skill recommend books based on:

1. the user's current learning goal/question, or
2. the reading profile inferred from WeRead history when no current goal is provided.

## Product Positioning
This is **not** a cloud sync integration and **not** a hosted cookie proxy.

It is a:
- local exporter
- local normalizer
- recommendation-oriented AgentSkill

## MVP Scope
### In
- Read WeRead cookie from local env var or local file
- Export bookshelf + progress + notebook stats to local JSON
- Optionally fetch public-ish per-book metadata from WeRead book info API
- Normalize raw export into a stable JSON schema
- Use normalized JSON as the main input for recommendation turns
- Recommend books from a user goal when provided
- Fall back to general recommendations from reading history alone

### Out
- CookieCloud / third-party cookie sync
- Remote storage of cookie or reading records
- Automatic scheduling / background refresh
- Highlight/note text analysis in v1
- Full external-book search pipeline in code
- Installation / packaging to production skill directory

## Draft Deliverables
- `PLAN.md`
- `SPEC.md`
- `SKILL.md`
- `scripts/export_weread.py`
- `scripts/normalize_weread.py`
- `references/data-schema.md`
- `references/privacy-model.md`
- `references/recommendation-rubric.md`
- sample raw/normalized JSON assets

## Workflow
1. User keeps cookie locally.
2. Run `export_weread.py` to dump raw WeRead data.
3. Run `normalize_weread.py` to produce a stable normalized file.
4. Skill reads normalized JSON.
5. If the user provides a goal, weight goal fit first.
6. If no goal is provided, weight reading profile + recency + engagement.

## Data Strategy
### Raw export
Keep a mostly faithful copy of WeRead responses for debugging and future extension.

### Normalized export
Produce a compact, stable schema with:
- per-book status
- engagement score
- top categories
- recent books
- strongest books/signals
- enough metadata for recommendation reasoning

## Recommendation Strategy
### With a current goal
Weight:
- 60% goal fit
- 40% reading-history fit

### Without a current goal
Weight:
- 70% reading-history fit
- 20% recency
- 10% exploration/diversity

## Safety / Privacy Model
- Cookie must never be written to output JSON.
- Cookie must never be embedded in SKILL.md or assets.
- Export happens only on the local machine.
- Normalized JSON should contain only recommendation-relevant reading data.

## Success Criteria for This Draft
- A local export command exists and is readable/testable.
- A normalization command exists and is readable/testable.
- The skill instructions clearly describe when/how to use the exported data.
- The draft is good enough for you to review before deciding whether to continue to full implementation or install.
