---
name: site-snapshot-review
description: Review one supported site's exported snapshot records without reopening live browser automation.
---

# Site Snapshot Review

Use this skill when you have an exported Campus Copilot workspace snapshot and want a read-only review of one site's current records.

## Steps

1. Load the snapshot through `@campus-copilot/sdk/snapshot`.
2. Build a workspace summary.
3. Filter to one site with `getSiteRecords`.
4. Report counts and the highest-signal assignments, messages, or events.

## Hard boundary

- Do not mutate site state.
- Do not claim live browser truth from a snapshot alone.
