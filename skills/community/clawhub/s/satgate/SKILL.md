---
name: satgate
description: Budgets and signed receipts for your agents' MCP tool calls. Use when connecting OpenClaw to SatGate Cloud.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://satgate.io
---

# SatGate MCP

SatGate Cloud puts a credit budget on an agent token and writes a signed receipt when it allows a tool call or refuses one for budget.

Mint the token in [cloud.satgate.io](https://cloud.satgate.io). Each token has its own budget. When the credits run out, SatGate refuses that agent's calls. This skill connects OpenClaw to that MCP server. It does not mint tokens, change policy, or spend credits by itself.

## When to use

Use this when someone wants SatGate on an OpenClaw agent, a budget on tool calls, or a receipt they can check.

## Connect

Use Streamable HTTP.

```bash
openclaw mcp set satgate '{"url":"https://satgate-mcp-saas.fly.dev/mcp","transport":"streamable-http","headers":{"Authorization":"Bearer <your agent token>"}}'
openclaw mcp probe satgate
```

Pass that JSON object alone. Do not wrap it in `mcp.servers` or `mcpServers`. A wrapped object can save and still leave the agent with no SatGate tools.

`<your agent token>` is a placeholder. Replace it with a token from cloud.satgate.io. Keep the JSON in single quotes so the shell does not expand it. Do not print the token, and do not commit the OpenClaw config that holds it.

SSE is the other transport, at `https://satgate-mcp-saas.fly.dev/sse`. New configs should use `/mcp`.

If you edit `~/.openclaw/openclaw.json` by hand, that file does use a wrapper. Put the same `url`, `transport`, and `headers` under `mcp.servers.satgate`. Do not paste that wrapper into `openclaw mcp set`.

## What the agent can do

`satgate_budget_check` returns the token's remaining credits and costs no credits. SatGate rate limits it per token.

The other tools are the ones configured for that token. They draw on its credit budget. A call refused for budget still gets a receipt.

One saved server named `satgate` is one token, and one budget. Mint a separate token for each agent.

## Receipts

Allowed calls and calls refused for budget get a signed receipt. Anyone can check it against SatGate's published keys. The check does not need a SatGate login.

MCP public keys: `https://satgate-mcp-saas.fly.dev/.well-known/jwks.json`

The browser check is [satgate.io/verify-evidence-pack](https://satgate.io/verify-evidence-pack).

The open-source verifier is in the public repo. Clone it, then pass the evidence pack URL. Do not pipe a downloaded script into Python.

```bash
git clone https://github.com/SatGate-io/satgate.git
python3 satgate/demo/verify_evidence_pack.py '<evidence pack url>'
```

A valid receipt shows the decision SatGate recorded. It does not show what an upstream tool did after an allow.

## Clients that only run a local command

Some clients cannot take a URL and a header. They run a local command. Pin the bridge. It needs Node 18 or newer.

```json
{
  "command": "npx",
  "args": ["-y", "satgate-mcp-bridge@1.0.5"],
  "env": {
    "SATGATE_URL": "https://satgate-mcp-saas.fly.dev",
    "SATGATE_TOKEN": "<your agent token>"
  }
}
```

`SATGATE_URL` is the origin only. The bridge adds its own path. Do not append `/mcp`.

## Safety

- Do not invent a token, and do not reuse one found in a workspace file.
- Do not send the token to any host other than `satgate-mcp-saas.fly.dev`.
- Do not say the budget is unlimited, or that a receipt proves what the upstream tool did.
