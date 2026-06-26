---
name: zero-join
description: "auto-configure MCP connection to ZERO trading engine. writes config, verifies handshake, starts onboarding."
metadata:
  openclaw:
    emoji: "🔌"
    homepage: "https://getzero.dev"
    requires:
      env: []
      bins: []
    permissions:
      - network
      - filesystem
    tags:
      - setup
      - mcp
      - auto-config
    mcpServers:
      zero:
        url: "https://api.getzero.dev/mcp"
        transport: "streamable-http"
---

# join zero — auto-connect

when the operator says "join zero", "connect to zero", "set up zero", or you read instructions from getzero.dev/zero.md — execute this flow. no questions. no manual config.

## step 1: find your MCP config file

check these paths in order. use the FIRST one that exists:

1. `~/.openclaw/openclaw.json` (OpenClaw agent config)
2. `~/.openclaw/mcp.json` (OpenClaw MCP config)
3. `~/.config/mcp/servers.json` (generic MCP config)

if NONE exist, create `~/.openclaw/openclaw.json`.

## step 2: add the zero MCP server

read the existing config file. add this entry to the `mcpServers` object (preserve existing servers):

```json
{
  "mcpServers": {
    "zero": {
      "url": "https://api.getzero.dev/mcp",
      "transport": "streamable-http"
    }
  }
}
```

if `mcpServers` key doesn't exist, create it. if a `zero` entry already exists, overwrite it with the above.

write the file back.

## step 3: restart MCP connection

run: `openclaw mcp restart` or restart the gateway for the new server to be picked up.

## step 4: verify the connection

call:

```
zero_get_engine_health
```

if it returns `"operational"` — you're connected. proceed to step 5.

if the tool is NOT available:
- tell the operator: "config written to ~/.openclaw/openclaw.json. restart the openclaw gateway to activate."
- after restart, try `zero_get_engine_health` again.

## step 5: start onboarding

once connected, run 3 evaluations to unlock session tools:

```
zero_evaluate("BTC")
zero_evaluate("ETH")
zero_evaluate("SOL")
```

show the operator the results. these 3 calls unlock the curious tier (10 tools).

then: "connected to zero. 10 tools unlocked. start a paper session to unlock all 42."

hand off to `onboarding/` sub-skill for full deployment flow.

## error handling

| situation | response |
|---|---|
| config file is read-only | "can't write config. run: `bash setup.sh` from the zero-trading skill directory" |
| config file has invalid JSON | backup to `.bak`, write fresh config |
| zero server unreachable | "zero engine may be offline. try again in 60 seconds." |
| tool not available after config write | "restart openclaw gateway: `openclaw mcp restart`" |
| `clawhub` available | skip manual config — just run `clawhub install zero-trading` |

## shortcuts

if `clawhub` CLI is available, skip steps 1-3 entirely:

```bash
clawhub install zero-trading
```

this installs the skill AND auto-configures the MCP server in one command.

## the operator should never need to:

- copy-paste JSON
- edit config files
- know what MCP is
- know what streamable-http means

the agent handles everything. the operator says "join zero" and 30 seconds later they're evaluating BTC.
