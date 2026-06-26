---
name: stocklobster
description: Monitor StockLobster webhook alerts through OpenClaw and route screened stock signals to chat channels such as Telegram. Use when setting up, documenting, testing, or troubleshooting StockLobster webhook ingestion, hook mappings, payload templates, and outbound delivery routing.
---

# StockLobster

Use this skill to wire StockLobster alerts into OpenClaw through the hooks gateway and deliver them to Telegram or another supported outbound channel.

## Confirmed payload shape

Read `references/payload-format.md` for the confirmed payload schema and examples.

## Recommended OpenClaw hook mapping

Use an `agent` mapping, not `wake`, when the goal is direct Telegram delivery.

Sanitized example:

```json
{
  "hooks": {
    "enabled": true,
    "path": "/hooks",
    "token": "<HOOKS_TOKEN>",
    "mappings": [
      {
        "id": "stocklobster-ingest",
        "name": "StockLobster ingest",
        "match": {
          "path": "/stocklobster",
          "method": "POST"
        },
        "action": "agent",
        "wakeMode": "now",
        "agentId": "main",
        "sessionKey": "hook:stocklobster",
        "messageTemplate": "{{payload.text}}",
        "deliver": true,
        "channel": "telegram",
        "to": "<TELEGRAM_CHAT_ID>"
      }
    ]
  }
}
```

## Setup

1. Enable hooks in `~/.openclaw/openclaw.json`.
2. Set a dedicated hooks token, not the shared gateway token.
3. Use hook path `/hooks` and mapping path `/stocklobster` so the endpoint becomes:
   - `http://<HOST>:18789/hooks/stocklobster`
4. Use `messageTemplate`, not `textTemplate`, because this flow should use `action: "agent"` for channel delivery.
5. Reference incoming webhook fields through `payload`, for example `{{payload.text}}`.
6. Set:
   - `deliver: true`
   - `channel: "telegram"`
   - `to: "<TELEGRAM_CHAT_ID>"`
7. Restart the gateway after config changes:

```bash
openclaw gateway restart
```

## Testing with curl

```bash
curl -X POST 'http://<HOST>:18789/hooks/stocklobster' \
  -H 'Authorization: Bearer <HOOKS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{"text":"StockLobster alert\nSymbol: TEST\nEvent: screen_hit\nMessage: TEST hit momentum criteria\nPrice: 4.92\nChange: 3.4%\nVolume: 1234567\nStrategy: momentum\nTimestamp: 2026-04-08T02:21:00.000Z"}'
```

Expected response:

```json
{"ok":true,"runId":"<RUN_ID>"}
```

If you only want to wake a session and not push to Telegram immediately, use `action: "wake"` with `textTemplate`, but that is a different flow.

## Troubleshooting

- `hook mapping requires text`
  - For `wake`, the rendered `textTemplate` was empty.
  - For `agent`, the rendered `messageTemplate` was empty.
  - In this OpenClaw build, templates resolve against `payload`, not `json`.
- Hook accepted but no Telegram message arrived
  - Check that the mapping uses `action: "agent"`.
  - Check `deliver: true`.
  - Check `channel` and `to` are set explicitly.
  - Restart the gateway after editing config.
- Hook returns `{"ok":true,"mode":"now"}`
  - That indicates a wake event, not necessarily an outbound Telegram delivery.
- Hook returns `{"ok":true,"runId":"..."}`
  - That indicates an agent run was created for delivery-capable handling.
