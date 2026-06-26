---
name: upstage-solar-delegation
description: Delegate longer user-facing text generation to Upstage Solar Pro3 while keeping the primary model for planning and tool calls. Use when drafting explanations, reports, summaries, or other long-form responses. Delegation is controlled by session enablement and a token threshold.
---

# Upstage Solar Delegation

Delegate long text generation to Upstage Solar Pro3 while the primary model focuses on planning, reasoning, and tool calls.

## Call Routes

| Route | Model | Env Variable | Description |
|-------|-------|-------------|-------------|
| **Upstage Direct** | `solar-pro3` | `UPSTAGE_API_KEY` | Direct Upstage API call (recommended) |
| **Via OpenRouter** | `openrouter/upstage/solar-pro-3` | `OPENROUTER_API_KEY` | Call through OpenRouter |

### Upstage Direct (Recommended)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["UPSTAGE_API_KEY"],
    base_url="https://api.upstage.ai/v1"
)

response = client.chat.completions.create(
    model="solar-pro3",
    messages=[{"role": "user", "content": "Write a detailed report..."}]
)
print(response.choices[0].message.content)
```

Get your key at [console.upstage.ai](https://console.upstage.ai).

### Via OpenRouter

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

Important: Do not use any tools. Output text only. No file read/write or tool calls allowed.
```

Set model to:
- `solar-pro3` (Upstage direct — recommended)
- `openrouter/upstage/solar-pro-3` (via OpenRouter)

### Main Session

Use `sessions_spawn` and wait for auto-announced result.

### Messenger Sessions (Slack/Telegram/etc.)

Use `sessions_spawn`, then fetch the final assistant text and forward it through the appropriate message channel/thread.

If no final text arrives within a reasonable timeout, fall back to direct response.

## Output Files

- **Inline default**: when the user expects the response in chat, do NOT write a file — return the text directly.
- **When saving to disk**: write to `<system-temp>/<timestamp>-solar.<ext>` (e.g., `/tmp/20260504-153022-solar.md`). Pick `.md` for markdown content, `.txt` for plain prose.
- **Override**: if the user specifies an output path, use it.
- **Always print the resolved absolute path** when writing to disk.

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

### Option A: Upstage Direct (Recommended)

1. Confirm user wants setup.
2. Verify `UPSTAGE_API_KEY` environment variable is configured. Get key at [console.upstage.ai](https://console.upstage.ai).
3. Set base_url to `https://api.upstage.ai/v1`, model to `solar-pro3`.
4. Confirm delegation is active and report current threshold.

### Option B: Via OpenRouter

1. Confirm user wants setup.
2. Confirm OpenRouter API key is available (`OPENROUTER_API_KEY`).
3. Add OpenRouter provider + Solar model via gateway config update.
4. Restart/reload gateway as required.
5. Confirm delegation is active and report current threshold.

For manual setup details, see [references/setup-guide.md](references/setup-guide.md).
