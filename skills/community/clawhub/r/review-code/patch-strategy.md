# Patch Strategy for Review Findings

Use this when proposing concrete fixes after a finding.

## Principles

- prefer minimal diffs over large rewrites
- protect behavior with tests before refactoring
- include rollback-safe steps for risky changes
- keep patch scope aligned with the identified defect

## Fix Planning Sequence

1. Reproduce the failure or risk condition.
2. Add or update test that captures the issue.
3. Apply minimal code change to pass the test.
4. Re-run nearby tests and static checks.
5. Document any follow-up refactor separately.

## High-Risk Change Guardrails

For auth, billing, migration, or data integrity fixes:
- require explicit rollback path
- require monitoring signal after deploy
- avoid bundled unrelated cleanups

## Suggested Output Format

- `Patch goal:` one sentence
- `Files touched:` list
- `Test added/updated:` exact scenario
- `Risk after patch:` low/medium/high with reason
- `Rollback note:` one concrete step

## Example Short Plan

- Patch goal: prevent stale cache writes during concurrent updates.
- Files touched: cache service write path and retry helper.
- Test added: concurrent writer test with conflict retries.
- Risk after patch: medium due to deployment ordering.
- Rollback note: disable retry path via feature flag.
