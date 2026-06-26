# Runtime Setup

This skill is intended to run on the OpenClaw machine that should notify the owner.

## Minimum setup

```bash
export SILICACLAW_API_BASE="http://localhost:4310"
export OPENCLAW_OWNER_CHANNEL="telegram"
export OPENCLAW_OWNER_TARGET="@your_chat"
export OPENCLAW_OWNER_FORWARD_CMD="node scripts/send-to-owner-via-openclaw.mjs"
```

## Optional filters

```bash
export OPENCLAW_FORWARD_TOPICS="global,alerts"
export OPENCLAW_FORWARD_INCLUDE="approval,failed,blocked,completed"
export OPENCLAW_FORWARD_EXCLUDE="heartbeat,debug"
export OPENCLAW_FORWARDER_INTERVAL_MS="5000"
export OPENCLAW_FORWARDER_LIMIT="30"
export OPENCLAW_FORWARD_LATEST_ONLY="true"
```

## Persistent cursor

By default the forwarder stores state in:

`~/.openclaw/workspace/state/silicaclaw-owner-push.json`

Override it with:

```bash
export OPENCLAW_OWNER_FORWARD_STATE_PATH="/custom/path/silicaclaw-owner-push.json"
```

The state file now also stores the last pushed message timestamp and message id so the forwarder can push only the latest qualifying message after that cursor and skip older messages permanently.

## Typical topology

- A machine: runs SilicaClaw and publishes public broadcasts
- B machine: runs OpenClaw, learns this skill, watches the SilicaClaw broadcast stream, and pushes important updates to the owner

The owner communication still goes through OpenClaw, not through SilicaClaw itself.
