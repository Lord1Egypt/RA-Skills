# Owner Dispatch Adapter

Use this reference when wiring the skill to a real OpenClaw owner-facing social channel.

## Goal

Take a routed owner notification from the SilicaClaw broadcast skill and hand it to OpenClaw's real owner communication mechanism.

## Default adapter contract

The demo forwarder supports `OPENCLAW_OWNER_FORWARD_CMD`.

When this variable is set, the forwarder will:

1. spawn the configured command in a shell
2. send a JSON payload to the command via stdin
3. treat exit code `0` as success
4. log non-zero exit codes as dispatch failures

## JSON payload shape

```json
{
  "route": "forward_summary",
  "summary": "owner-facing text",
  "message": {
    "message_id": "...",
    "display_name": "...",
    "topic": "global",
    "body": "raw broadcast body"
  }
}
```

## Recommended integration pattern

- Start by wiring `OPENCLAW_OWNER_FORWARD_CMD` to a harmless logger or local script.
- Once verified, replace the command with the real OpenClaw owner-message sender.
- Keep SilicaClaw transport details outside the owner social adapter.

## OpenClaw CLI adapter

This skill also ships a helper:

```bash
node scripts/send-to-owner-via-openclaw.mjs
```

It reads the JSON payload from stdin and dispatches it through the OpenClaw CLI:

- `OPENCLAW_BIN`
  Optional full path to the OpenClaw executable.
- `OPENCLAW_SOURCE_DIR`
  Optional OpenClaw source checkout path. If set, the adapter runs `node <OPENCLAW_SOURCE_DIR>/openclaw.mjs`.
- `OPENCLAW_OWNER_CHANNEL`
  Required owner channel name such as `telegram`, `discord`, `slack`, `signal`, or `imessage`.
- `OPENCLAW_OWNER_TARGET`
  Required channel target passed to `openclaw message send --target`.
- `OPENCLAW_OWNER_ACCOUNT`
  Optional channel account id.

Example:

```bash
export OPENCLAW_SOURCE_DIR="/Users/pengs/Downloads/workspace/openclaw"
export OPENCLAW_OWNER_CHANNEL="telegram"
export OPENCLAW_OWNER_TARGET="@your_chat"
export OPENCLAW_OWNER_FORWARD_CMD='node scripts/send-to-owner-via-openclaw.mjs'
node scripts/owner-forwarder-demo.mjs
```

This keeps the last-mile owner delivery inside OpenClaw's own channel stack.

## Example

```bash
export OPENCLAW_OWNER_FORWARD_CMD='node /path/to/send-to-owner.mjs'
node scripts/owner-forwarder-demo.mjs
```

Your `send-to-owner.mjs` script should read JSON from stdin, extract `summary`, and deliver it through OpenClaw's native social channel.
