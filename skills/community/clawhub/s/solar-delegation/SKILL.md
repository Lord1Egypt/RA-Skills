---
name: solar-delegation
description: Delegate longer user-facing text generation to Upstage Solar Pro3 while keeping the primary model for planning and tool calls. Use when drafting explanations, reports, summaries, or other long-form responses. Delegation is controlled by session enablement and a token threshold.
---

# Solar Delegation

Route long user-facing text generation to Upstage Solar Pro3 (via OpenRouter), while the primary model handles planning/reasoning/tool use.

Model reference: https://openrouter.ai/upstage/solar-pro-3

## Enabled Sessions

Check runtime/session settings to see where delegation is enabled.

Typical values:
- `main`: direct/main session
- `slack`: Slack messages
- `telegram`: Telegram messages

If the current session is not enabled, skip delegation and respond directly.

## Delegation Threshold

Use a minimum output-token threshold:
- estimated output tokens **>= threshold** → delegate to Solar
- estimated output tokens **< threshold** → respond directly

Common examples:
- `0`: delegate all responses
- `200`: delegate medium/long responses only

If no threshold is configured, use `200` as default.

## How to Delegate

1. Estimate output token length.
2. Check whether current session is enabled.
3. If enabled and estimate >= threshold, run `sessions_spawn` with Solar Pro3.

Example spawn task pattern:

```text
<context + writing instruction>

중요: 도구(tool)를 사용하지 말고 텍스트만 바로 출력해줘. 파일 읽기/쓰기 등 도구 호출 금지.
```

Set model to:
- `openrouter/upstage/solar-pro-3`

### Main Session

Use `sessions_spawn` and wait for auto-announced result.

### Messenger Sessions (Slack/Telegram/etc.)

Use `sessions_spawn`, then fetch the final assistant text and forward it through the appropriate message channel/thread.

If no final text arrives within a reasonable timeout, fall back to direct response.

## Rules

- Pass through Solar output as-is (no extra summary/footer/metadata).
- Keep non-user-facing orchestration text minimal.
- Do not output intermediate narration between tool calls.
- Always include the “no tool call” instruction in spawn tasks.

## Decision Guide

Delegate when above threshold and user expects substantial writing:
- explanations
- summaries
- reports
- long-form answers

Keep direct response for:
- short operational confirmations
- urgent low-latency replies
- responses that must include immediate tool-call outputs

## Configuration Changes

Users may request:
- threshold changes (e.g., “set threshold to 300”)
- session enable/disable (e.g., enable delegation in Slack)

Apply updates to persistent memory/config used by your environment.

## First-Time Setup

If Solar Pro3 is not configured:
1. Confirm user wants setup.
2. Confirm OpenRouter API key is available.
3. Add OpenRouter provider + Solar model via gateway config update.
4. Restart/reload gateway as required.
5. Confirm delegation is active and report current threshold.

For manual setup details, see [references/setup-guide.md](references/setup-guide.md).
