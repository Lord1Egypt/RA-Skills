# Persistent Worker Session Rollout (Historical / Advanced)

This reference is **not the published V1 default path**.
Keep it only as a historical and advanced note for future exploration.

## Current published recommendation

For the published Workhorse Duo V1 route, prefer:
- real local agents `xiaoma` and `xiaoniu`
- CLI agent routing via `openclaw agent --agent xiaoma ...` / `openclaw agent --agent xiaoniu ...`
- asynchronous main-session orchestration

Do not use this file to describe the default day-one user path.

## What this file is for

Use this file only when:
- exploring a future V2 persistent worker design
- documenting historical assumptions from earlier drafts
- evaluating whether a later environment now supports stable persistent worker routing that is clearly better than the published V1 route

## What this file must not do

Do not claim that published V1 currently depends on:
- visible dedicated WebChat worker sessions
- persistent local worker bootstrap
- thread-bound worker cards
- `sessions_spawn(runtime="subagent")` as the default production route
- session-id-only temporary dispatch as the canonical published route

## Future re-evaluation checklist

Only promote persistent worker rollout back to the main path if all of the following become true:
1. persistent worker creation succeeds reliably in the local environment
2. execution routing is stable across multiple tasks
3. QA routing is stable across multiple tasks
4. failure recovery is simpler than or clearly more valuable than the published CLI agent routing path
5. the extra ceremony is justified by real long-context value

## Current product recommendation

For now:
- published V1 default = real-agent CLI orchestration
- V2 optional exploration = persistent worker architecture

That keeps the skill aligned with the clearest and most reproducible route for new users.
