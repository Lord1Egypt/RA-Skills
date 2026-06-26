---
name: wip-license-hook
description: License rug-pull detection. Scans dependencies and forks for license changes, gates upstream merges, maintains a license ledger, and generates a public compliance dashboard.
license: MIT
interface: [cli, module, mcp]
metadata:
  display-name: "License Rug-Pull Detection"
  version: "1.0.0"
  homepage: "https://github.com/wipcomputer/wip-ai-devops-toolbox"
  author: "Parker Todd Brooks"
  category: dev-tools
  capabilities:
    - license-scanning
    - rug-pull-detection
    - compliance-gating
    - license-ledger
  requires:
    bins: [node, git, npm]
  openclaw:
    requires:
      bins: [node, git, npm]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-license-hook"
        bins: [wip-license-hook]
        label: "Install via npm"
    emoji: "🛡️"
compatibility: Requires git, npm, node. Node.js 18+.
---

# wip-license-hook

Detect license rug-pulls before they reach your codebase.

## Commands

### Initialize ledger for a project
```bash
wip-license-hook init --repo /path/to/repo
```
Scans all current dependencies and forks, records their licenses, creates `LICENSE-LEDGER.json`.

### Scan all dependencies
```bash
wip-license-hook scan --all
```
Checks every dependency and fork against the ledger. Updates `last_checked`. Flags any changes.

### Pre-merge gate
```bash
wip-license-hook gate --upstream <remote>
```
Fetches upstream without merging. Checks license. Returns exit code 0 (safe) or 1 (changed/blocked).

Use in git hooks or CI.

### Generate report
```bash
wip-license-hook report
```
Outputs a human-readable license health report.

### Generate dashboard
```bash
wip-license-hook dashboard --output ./docs
```
Creates a static HTML dashboard from the ledger. Deploy to GitHub Pages.

## Daily Cron Usage

Add to HEARTBEAT.md or as a cron job:
```
wip-license-hook scan --all --alert
```

If any license changed, sends alert via configured channel (email, iMessage, Discord).

## What It Detects

- LICENSE file content changes
- package.json license field changes
- SPDX header changes
- License removal (file deleted)
- License downgrade (permissive → restrictive)

## What It Does NOT Do

- It does not legal advice make
- It does not auto-merge anything ever
- It does not modify upstream code

## Alert Levels

- 🟢 **Clean** — license unchanged since adoption
- 🟡 **Warning** — license metadata inconsistency (e.g., LICENSE file says MIT but package.json says ISC)
- 🔴 **Blocked** — license changed from what was adopted. Merge blocked. Human review required.

## MCP

Tools: `license_scan`, `license_audit`, `license_gate`, `license_ledger`

Add to `.mcp.json`:
```json
{
  "wip-license-hook": {
    "command": "node",
    "args": ["/path/to/tools/wip-license-hook/mcp-server.mjs"]
  }
}
```
