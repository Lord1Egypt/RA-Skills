---
name: smartgate
description: >
  Connect OpenClaw to the hosted SmartGate MCP (search, fetch, compress,
  dedup, budget, memory, pipelines). Not an LLM proxy. Requires SMARTGATE_API_KEY.
metadata:
  openclaw:
    emoji: "🚪"
    homepage: https://smartgate.network
    primaryEnv: SMARTGATE_API_KEY
    requires:
      env:
        - SMARTGATE_API_KEY
    envVars:
      - name: SMARTGATE_API_KEY
        required: true
        description: Bearer sk_live_ key from https://smartgate.network Dashboard → API Keys
---

# SmartGate

Hosted Streamable HTTP MCP. Do not clone this repo to run a local server.

- Endpoint: `https://smartgate.network/api/mcp`
- Official Registry name: `network.smartgate/smartgate`
- Key: mint at https://smartgate.network Dashboard → API Keys (`sk_live_…`)
- A request without `Authorization` returns **401**. That is expected.
- Hosted service has a free tier and paid plans; the key is billed on the SmartGate account, not ClawHub.
- Contact: support@smartgate.network

## Connect

1. Export `SMARTGATE_API_KEY` (never paste a live key into chat or commit it).
2. Prefer **Settings → MCP → Add server** while the Gateway is running: name `smartgate`, transport **Streamable HTTP**, URL above, header `Authorization` = `Bearer ${SMARTGATE_API_KEY}`.
3. Or stop the Gateway and run:

```bash
openclaw mcp add smartgate \
  --transport streamable-http \
  --url https://smartgate.network/api/mcp \
  --header "Authorization=Bearer ${SMARTGATE_API_KEY}" \
  --header "X-SmartGate-Agent-Platform=openclaw"
```

4. Prove it: `openclaw mcp doctor smartgate --probe` (stop the Gateway first). You should see seven `smart_*` tools.

Equivalent config (env substitution; do not put a literal `sk_live_` here):

```json
{
  "mcp": {
    "servers": {
      "smartgate": {
        "transport": "streamable-http",
        "url": "https://smartgate.network/api/mcp",
        "headers": {
          "Authorization": "Bearer ${SMARTGATE_API_KEY}",
          "X-SmartGate-Agent-Platform": "openclaw"
        }
      }
    }
  }
}
```

## Tools

| Tool | When to use | When NOT to use |
|------|-------------|-----------------|
| `smart_search` | Need web research and no URL yet | User already gave the exact URL |
| `smart_fetch` | User gave an http(s) URL | Text is already in context |
| `smart_dedup` | Several passages overlap | One string or unrelated docs |
| `smart_context_gate` | Context is too large | Short messages |
| `smart_budget_guard` | Check/count/record team token spend | General chat or as the host model |
| `smart_memory` | Persist or recall team facts across sessions | World knowledge or one-off page text |
| `smart_pipe` | Several of the above in sequence (`research` / `read` / `remember`) | A single step — call that `smart_*` tool |

Docs: https://smartgate.network/docs/tools
