# Realtime Agent Reference

## Table of Contents

- Endpoint summary
- Lifecycle
- 1) List agents
- 2) Invoke agent session
- 3) Query status
- 4) Leave session
- Common error codes

## Endpoint Summary

- List agents: `GET https://api.senseaudio.cn/v1/realtime/agents`
- Invoke session: `POST https://api.senseaudio.cn/v1/realtime/invoke`
- Query status: `GET https://api.senseaudio.cn/v1/realtime/status`
- Leave session: `POST https://api.senseaudio.cn/v1/realtime/leave`

Headers:

- `Authorization: Bearer <API_KEY>`
- `Content-Type: application/json`

## Lifecycle

Recommended flow:

1. `GET /v1/realtime/agents` to get `agent_id`
2. `POST /v1/realtime/invoke` to create/continue dialogue
3. Use returned realtime credentials (`app_id`, `room_id`, `room_user_id`, `token`) in media channel
4. Optional status checks with `GET /v1/realtime/status?room_id=...`
5. End session with `POST /v1/realtime/leave`

## 1) List Agents

Query params:

- `page` default `1`
- `size` default `10`

Response:

- `total`
- `list[]` with `id`, `title`, `intro`, `avatar`

## 2) Invoke Agent Session

Request body:

- `agent_id` required
- `new_dialogue` required
- `conv_id` required only when `new_dialogue=false`

Response:

- `conv_id`
- `app_id`
- `room_id`
- `room_user_id`
- `token`

Usage rules:

- Persist `conv_id` if user needs conversational continuity.
- Treat `token` as short-lived credential; avoid logging full value.

## 3) Query Status

Query param:

- `room_id` required

Response:

- `status`: `RUNNING` or `STOPPED`

## 4) Leave Session

Request body:

- `room_id` required

Success response:

- `{}`

## Common Error Codes

List/invoke/status/leave docs include:

- `401000` unauthorized
- `500000` server internal error

Invoke-specific:

- `400000` invalid param
- `403000` forbidden
- `404002` conversation not exists
- `400087` insufficient quota

Status/leave specific:

- `404001` room not exists

Implementation checklist:

- Handle unauthorized by rotating/refreshing API key source.
- Handle `400087` with clear user guidance about quota.
- Reconcile `room_id` and `conv_id` separately; they are different identifiers.

