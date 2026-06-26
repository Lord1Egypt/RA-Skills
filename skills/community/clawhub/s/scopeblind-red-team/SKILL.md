---
name: scopeblind-red-team
description: >
  Policy benchmarking runner for MCP security policies. Runs attack suites
  against protect-mcp policy packs, produces signed receipts and badges.
metadata:
  emoji: ⚔️
  requires:
    bins:
      - npx
    env: []
  install: |
    npm install -g @scopeblind/red-team@latest protect-mcp@latest
  license: MIT
  allowed-tools:
    - Bash
    - Read
---

# ScopeBlind Red Team — Policy Benchmarking

## What This Skill Does

Runs deterministic attack suites against your protect-mcp policies to verify
they block what they should and allow what they should.

## Quick Start

```bash
# Run the default attack suite against a policy
npx scopeblind-red-team --policy protect-mcp.json

# Run against a specific incident policy
npx scopeblind-red-team --policy node_modules/protect-mcp/policies/clinejection.json
```

## Links

- npm: https://npmjs.com/package/@scopeblind/red-team
- Docs: https://scopeblind.com/docs/red-team
