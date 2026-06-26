---
name: senseaudio-realtime-agent
description: Implement and debug SenseAudio realtime Agent lifecycle APIs: list agents, invoke session, query status, and leave session (`/v1/realtime/agents`, `/invoke`, `/status`, `/leave`). Use this whenever user asks to start or manage SenseAudio conversational agents, continue dialogues, or handle room/conv/token lifecycle errors.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio Realtime Agent

Use this skill for SenseAudio Agent session lifecycle integration.

## Read First

- `references/agent.md`

## Workflow

1. Discover agent:
- List available agents and pick `agent_id`.

2. Start or continue dialogue:
- `new_dialogue=true` for new session.
- `new_dialogue=false` with `conv_id` for continuity.

3. Persist runtime credentials:
- Store `conv_id` and `room_id` in your application state (database or session store), never in client-side code or logs.
- Tokens returned by `/invoke` are short-lived — treat them like passwords: do not log, do not embed in URLs, and discard after the session ends via `/leave`.
- Rotate by calling `/invoke` again with the same `conv_id`; do not reuse expired tokens.

4. Operate session:
- Query room status when needed.
- Leave session explicitly when finished.

5. Handle failures:
- Distinguish quota/auth/not-found vs parameter errors.

