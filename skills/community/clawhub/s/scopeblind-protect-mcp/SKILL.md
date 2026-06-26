---
name: scopeblind-protect-mcp
description: >
  MCP security gateway. Wraps any MCP server with per-tool policies,
  Ed25519-signed decision receipts, and human approval gates. Shadow mode
  logs everything without blocking. Enforce mode applies policy.
metadata:
  emoji: 🛡️
  requires:
    bins:
      - npx
    env: []
  install: |
    npm install -g protect-mcp@latest
  license: MIT
  allowed-tools:
    - Bash
    - Read
    - Write
---

# protect-mcp — MCP Security Gateway

## What This Skill Does

Wraps any MCP server as a transparent stdio proxy with per-tool security
policies and cryptographic audit trail. Every tool call decision is logged
and optionally Ed25519-signed.

## Quick Start

```bash
# Shadow mode — log everything, block nothing
npx protect-mcp -- node your-server.js

# Enforce mode — apply per-tool policies
npx protect-mcp --policy policy.json --enforce -- node your-server.js

# Initialize signing (generates Ed25519 keypair)
npx protect-mcp init
```

## Policy Example

```json
{
  "tools": {
    "db_write": { "decision": "deny" },
    "file_read": { "decision": "allow", "rateLimit": { "maxCalls": 30, "windowSecs": 60 } },
    "deploy": { "decision": "require_approval" }
  }
}
```

## Pre-built Policy Packs

protect-mcp ships CVE-anchored policy packs:

```bash
# List available policies
npx protect-mcp policies

# Apply the Clinejection prevention policy
npx protect-mcp --policy clinejection --enforce -- node your-server.js
```

## Verify Receipts

Receipts are independently verifiable offline — no ScopeBlind dependency:

```bash
npx @veritasacta/verify receipt.json
npx @veritasacta/verify --self-test
```

## OWASP MCP Top 10 Coverage

| Risk | Control |
|------|---------|
| MCP-01 Rug Pulls | Signed tool manifests; policy pins allowed tools |
| MCP-03 Tool Poisoning | Per-tool allow/deny/rate-limit policies |
| MCP-04 Tool Arg Injection | Argument inspection + approval gates |
| MCP-07 Auth/AuthZ | Trust-tier gating |
| MCP-08 Logging & Audit | Ed25519-signed receipts — verifiable offline |
| MCP-09 Excessive Agency | Shadow mode reveals actual tool usage |

## Links

- npm: https://npmjs.com/package/protect-mcp
- IETF Draft: https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/
- Docs: https://scopeblind.com/docs/protect-mcp
- OWASP Mapping: https://scopeblind.com/docs/owasp
