# Storyline Backfill Route

Use this route after a storyline tree already exists and the user wants one branch, one trunk, or the full tree extended with older or missing events.

## Preferred Inputs

- an existing storyline tree markdown file
- optional html or notes for the same tree
- `profiles/following_topics.md`
- `profiles/profile_summary.md`
- optional confirmed guidance rules

## Outputs

Create:

- `storylines/storyline_backfill_<date>.md`
- optionally updated storyline tree files
- optionally `storylines/backfill_keyword_strategy_<date>.md`

Treat `storyline_backfill_<date>.md` as a working memo.
Treat updated tree files as final-facing outputs.

## Workflow

1. Choose the target branch, trunk, or full tree scope.
2. Restate the branch logic in one sentence before searching.
3. Use the retrieval ladder:
   1. existing known events
   2. topic top
   3. targeted search
4. Generate 3 to 6 query angles only when search is still necessary.
5. Triage results into primary evidence, secondary evidence, and discard.
6. Merge accepted events into the same branch timeline as known events.
7. Sort the merged timeline chronologically.
8. Preserve the existing tree identity unless the user explicitly asks for a reframe.

## Evidence Rules

Primary evidence:

- advances the branch storyline
- fills a missing step
- sharpens causality or escalation
- for hobby lines, marks a meaningful official release, collab, event, merch step, or destination update

Secondary evidence:

- adds surrounding context without advancing the core chain directly

Discard:

- wrong storyline
- generic commentary
- noisy duplicates

## Failure Modes

- drowning the branch in weak search hits
- separating known and backfilled events into different panes
- forgetting chronological ordering
- rewriting the whole taxonomy during a normal backfill run
- leaking working-note tone into final-facing markdown or HTML
