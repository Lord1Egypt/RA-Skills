# Backfill Merge Template

Use this structure when presenting backfill work.
This template is for the backfill memo, not for the final user-facing tree render.

## Target

- trunk / branch id
- branch meaning restatement
- time window

## Queries used

- query 1
- query 2
- query 3

## Primary evidence kept

- `YYYY-MM-DD | 事件标题`
- why it belongs

## Secondary evidence kept

- `YYYY-MM-DD | 事件标题`
- why it is only secondary

## Discarded patterns

- what kinds of results were dropped and why

## Merged timeline

Show one combined timeline with:

- known_pool events
- syft_search_primary events
- syft_search_secondary events

in strict chronological order.

## Important separation

Keep these two layers separate:

- working memo:
  can mention queries, triage decisions, dropped patterns, and retrieval reasoning
- final tree:
  should inherit only the cleaned timeline results and polished prose

Do not paste memo labels such as:

- `thin`
- `discard_note`
- `topic top 路`
- `targeted search 路`

into the final tree outputs.
