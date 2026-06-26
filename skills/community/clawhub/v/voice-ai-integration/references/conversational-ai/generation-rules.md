# ConvoAI Generation Rules

Stable constraints that do NOT change with API updates. Always apply when generating code.

## Field Types

- `agent_rtc_uid`: STRING `"0"`, not int `0`
- `remote_rtc_uids`: array `["*"]`, not `"*"`
- `name`: unique per project — use `agent_{uuid[:8]}`
- `agent_rtc_uid` must not collide with any human participant's UID

## Create Agent (`POST /join`)

- `token`: `""` if no App Certificate; otherwise RTC token
- `agent_rtc_uid`: `"0"` for auto-assign
- `remote_rtc_uids`: `["*"]` unless the user specifies UIDs

## Update Agent (`POST /update`)

- `llm.params` is FULLY REPLACED — always send the complete object
- Only `token` and `llm` are updatable; everything else is immutable

## Terminology

- `agentId` in URL paths = `agent_id` in JSON bodies
- `/join` returns `agent_id` (snake_case); use it as the path parameter

## Error Handling

- `409`: extract the existing `agent_id` or generate a new name and retry
- `503/504`: exponential backoff, max 3 retries
- Always parse `detail` and `reason` from error responses
- Full diagnosis → [common-errors.md](common-errors.md)
