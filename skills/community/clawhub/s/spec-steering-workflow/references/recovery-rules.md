# Recovery Rules

## Resume Order

Default recovery order is fixed:
1. Read `handoff.md`
2. Read `tasks.md`
3. Check `meta.json`
4. Read `requirements.md` and `design.md` only if more context is needed
5. Read additional steering files only if the task needs them

## Handoff Requirements

`handoff.md` must answer:
- What phase and status the spec is in
- Which batch is current
- What was completed last
- What is blocked or what failed
- What the single next exact action is

`Next Exact Action` must contain one action only.

## Stale State

Treat a spec as stale when the last checkpoint is older than 24 hours.

When state is stale:
1. Verify the workspace still matches the handoff.
2. Re-check any files or outputs named in `Evidence`.
3. Write a fresh checkpoint if the real state differs.

## Session Handoff

A child session should receive only:
- The spec path
- Relevant steering files
- The current goal

A child session must leave behind:
- An updated `handoff.md`
- Updated `meta.json`
- Any task state changes in `tasks.md`
