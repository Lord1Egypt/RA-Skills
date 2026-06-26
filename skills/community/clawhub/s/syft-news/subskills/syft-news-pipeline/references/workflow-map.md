# Workflow Map

Use this file when the user request spans more than one Syft workflow stage.

## Default End-to-End Order

1. Build or refresh profile artifacts.
2. Capture durable guidance only if the user expresses stable preferences.
3. Produce a daily briefing.
4. Build a storyline tree when the user wants relationship-first reading.
5. Backfill the tree when a branch or trunk needs more chronology.

## Short Routes

- Request is only about profile understanding:
  run profile summary only.
- Request is only about a one-off personalized briefing:
  run profile summary, then daily briefing.
- Request is only about storing a long-term rule:
  run guidance rulebook only.
- Request is about turning today's pool into structured storylines:
  run daily briefing, then storyline tree.
- Request is about deepening an existing tree:
  run storyline backfill only.

## Shared Assumptions

- `syft following` is the first declared-interest source in Syft-only mode.
- `profile_summary.md` is an interpretation layer, not a stronger truth source than follows.
- Topic-local retrieval should usually come before free-text search.
- Final-facing outputs should be polished deliverables, not debug artifacts.
