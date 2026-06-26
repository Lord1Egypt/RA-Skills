# Self-Improving Loop

## Goal
Make Shared Memory OS continuously maintain and refine itself instead of only waiting for manual edits.

## Loop
1. real work happens
2. lessons are harvested into `.learnings/`
3. learnings index is rebuilt
4. duplicate and stale signals are checked
5. promotion candidates are identified
6. stable repeated lessons are promoted into durable rules when appropriate

## Required automation targets
- health check on a schedule
- learnings index rebuild on a schedule
- weekly review for duplicates and promotion candidates

## Important boundary
This is guided self-improvement through memory governance.
It is not unrestricted self-modification.
Promotions into durable memory should still be conservative and reviewable.
