# ScopeBlind Passport — OpenClaw Skill

> Any platform can log what its agents do. Very few will let you verify those logs without trusting them.

Signed access control for your OpenClaw agent. Every tool call produces a cryptographic receipt — independently verifiable by anyone, without trusting ScopeBlind.

## Install

Copy the `openclaw-skill/` folder to your OpenClaw skills directory:

```bash
cp -r openclaw-skill ~/.openclaw/skills/scopeblind-passport
```

Or for project-specific usage:

```bash
cp -r openclaw-skill ./skills/scopeblind-passport
```

## Quick Start

1. **Fast path** — wrap an existing OpenClaw config into a passported pack:
   ```bash
   npx @scopeblind/passport wrap --runtime openclaw --config ./openclaw.json --policy email-safe
   ```

2. **Or initialize manually** (generates signing keys + default policy):
   ```bash
   npx protect-mcp init
   ```

3. **Wrap your MCP servers** — add `npx protect-mcp --` before your server command in your OpenClaw MCP config:
   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "npx",
         "args": ["protect-mcp", "--policy", "protect-mcp.json", "--", "node", "filesystem-server.js"]
       }
     }
   }
   ```

4. **Ask your agent** — "What did you do today?" / "Show my passport" / "Show my receipts"

## Policy Packs

| Pack | Use case |
|------|----------|
| `shadow.json` | Log everything, block nothing (default) |
| `web-browsing-safe.json` | Allow reads, rate-limit searches, block JS execution |
| `email-safe.json` | Read freely, require approval to send/reply/forward |
| `strict.json` | Read-only, everything else blocked |

Apply a policy:
```bash
cp policies/email-safe.json protect-mcp.json
```

## Verify Receipts

Every receipt is independently verifiable. The verifier is MIT licensed and works without ScopeBlind:

```bash
npx @veritasacta/verify --self-test
```

Then verify a real receipt:

```bash
curl -s http://127.0.0.1:9876/receipts/latest | jq -r '.receipt' > receipt.json
npx @veritasacta/verify receipt.json --key <public-key-hex>
```

No ScopeBlind account, API, or servers required.

## Links

- [protect-mcp on npm](https://www.npmjs.com/package/protect-mcp)
- [Documentation](https://www.scopeblind.com/docs)
- [GitHub](https://github.com/scopeblind/protect-mcp)
- [Verify receipts online](https://www.scopeblind.com/verify)
