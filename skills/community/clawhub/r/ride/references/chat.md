# Chat Reference

> All agent-facing operations use `amb <subcommand> [args…]` (PATH-resident). Two scripts that cannot live on PATH (`ride-relay.js`, `install.js`) are invoked via `node ${SKILL_DIR}/scripts/<name>.js` — see `../SKILL.md` for the path convention.

Driver chat during a ride.

## Receiving driver messages

`ride-relay.js` surfaces driver chat as `chat_event` lines on its stdout
JSONL stream:

```json
{ "type": "chat_event", "requestId": "...", "ts": "...", "terminal": false, "sender": "driver", "content": "..." }
```

`sender` is one of `driver`, `system`, `unknown`. Under OpenClaw the
relay also delivers these into the session automatically; under Claude
Code the agent reads them from the drained stdout (see SKILL.md
"Event streaming: ride-relay").

## Sending messages

Send to the driver with `amb chat-send-message`. There is no named pipe; send directly:

```bash
amb chat-send-message <request_id> <content>
```

## Fallback commands

Use these only when `ride-relay.js` is NOT running (ad-hoc, one-shot operations).

### chat-get-messages

```bash
amb chat-get-messages <request_id> [cursor]
```

- `cursor`: `createdAt` of last message for pagination
- Returns `{ count, messages, next_cursor }`

### chat-send-image

```bash
amb chat-send-image <request_id> <image_path>
```

Sends image via REST. Supported: jpeg, jpg, png, gif, webp. Max 10MB.
