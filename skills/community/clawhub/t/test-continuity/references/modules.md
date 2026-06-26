# V2 module map

## Core

- continuity routing
- staged memory promotion
- tracked follow-up
- carryover
- closure consistency
- frontstage safety

## State layer

- `profile.json`
- `user_model.json`
- `emotion_state.json`
- `persona_state.json`
- `memory_rank.json`
- `autonomy_state.json`
- `settings.json`

## Event layer

- `candidate_buffer.json`
- `incidents.json`
- `hooks.json`
- `session_memory_staging.json`

## Trace layer

- `followup_trace.jsonl`
- `candidate_buffer_audit.jsonl`
- `session_memory_staging_audit.jsonl`
- `hook_completion_audit.jsonl`
- `frontstage_guard_log.jsonl`

## Public V2 tracked event types

- `parked_topic`
- `watchful_state`
- `delegated_task`
- `sensitive_event`

## Optional and host-boundary items

- host delivery concerns
- provider/network transport concerns
- optional rhythm or nudge layers
