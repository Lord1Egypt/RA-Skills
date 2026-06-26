# Call Flow

## Main runtime path

1. `intercept_message()`
   - inspect the incoming user text
   - classify it as casual, staged, or tracked-worthy
   - write candidate / incident / hook state when needed

2. `process_candidate_buffer()`
   - re-evaluate staged candidates
   - promote qualified continuity into incidents/hooks

3. `build_runtime_context()`
   - collect pending topics
   - collect carryover for `/new`
   - add schedule context and continuity guards

4. ordinary reply generation
   - the host OpenClaw agent uses the runtime context to generate frontstage text

5. `due` / `render` / `complete`
   - evaluate pending hooks
   - render due follow-up text
   - mark closure / completion

## State flow

`casual_chat` -> no tracked state required

`staged_memory`
- `session_memory_staging.json`
- `candidate_buffer.json`
- concise daily-memory trace

`tracked_followup`
- `incidents.json`
- `hooks.json`
- clearer daily-memory trace

## Traceability

Key files:

- `followup_trace.jsonl`
- `candidate_buffer_audit.jsonl`
- `session_memory_staging_audit.jsonl`
- `hook_completion_audit.jsonl`
- `frontstage_guard_log.jsonl`
