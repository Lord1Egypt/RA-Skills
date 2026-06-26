---
name: read-only-workspace-audit
description: Audit whether one imported workspace snapshot is rich enough for export, cited AI, or MCP consumption.
---

# Read-Only Workspace Audit

Use this skill when you have an imported Campus Copilot workspace snapshot and need to answer:

- what is currently open
- which site carries which evidence
- whether the current snapshot is rich enough for export or cited AI

Rules:

- stay read-only
- operate on imported snapshots or exported current-view artifacts
- do not claim live browser/session truth from snapshot-only evidence
- keep Campus Copilot positioned as a local-first academic decision workspace

Suggested toolchain:

1. `campus-copilot summary --snapshot <path>`
2. `campus-copilot site --snapshot <path> --site <canvas|gradescope|edstem|myuw>`
3. `pnpm --filter @campus-copilot/mcp-server start` for the generic BFF + snapshot MCP flow, or one of the site-scoped `pnpm --filter @campus-copilot/mcp-readonly start:<site>` commands for snapshot-only reads

Companion examples:

- `examples/integrations/codex-mcp.example.json`
- `examples/integrations/claude-code-mcp.example.json`
- `examples/workspace-snapshot.sample.json`

Good fit:

- Codex / Claude Code evaluation of the read-only toolbox
- OpenClaw-style local consumers that need a strict audit trail
- repo-local verification of whether one snapshot is ready for export, cited AI, or MCP consumption
