---
name: site-mcp-consumer
description: Wire one site-scoped read-only MCP sidecar to a local Campus Copilot snapshot.
---

# Site MCP Consumer

Use this skill when you want to wire one of the site-scoped read-only MCP sidecars into Codex, Claude Code, Claude Desktop, or another **local** MCP-capable runtime that should keep Campus Copilot on the snapshot-first side.

## Pick the right surface first

- If you need cross-site health, provider status, `ask_campus_copilot`, or export tools, start with the generic server examples under `examples/integrations/` instead of a site sidecar.
- If you only need one site's records from a snapshot, keep using this skill and `@campus-copilot/mcp-readonly`.

## Inputs

- one site name: `canvas`, `gradescope`, `edstem`, or `myuw`
- one snapshot path such as `examples/workspace-snapshot.sample.json`
- one local consumer that can launch a stdio MCP sidecar

## Steps

1. Choose one site MCP binary:
   - `campus-copilot-mcp-canvas`
   - `campus-copilot-mcp-gradescope`
   - `campus-copilot-mcp-edstem`
   - `campus-copilot-mcp-myuw`
2. Point `CAMPUS_COPILOT_SNAPSHOT` at a snapshot JSON file.
3. Run the sidecar with `pnpm --filter @campus-copilot/mcp-readonly start:<site>`.
4. Start with `get_site_overview`, then move to the site-specific list tools.
5. If your consumer wants a JSON config example, reuse:
   - `examples/mcp/codex.example.json`
   - `examples/mcp/claude-desktop.example.json`
   - `examples/mcp/codex-repo-root.example.json`
   - `examples/mcp/claude-desktop-repo-root.example.json`
6. If your runtime is OpenClaw-style or another local operator shell, treat those config files as reusable only when it explicitly supports the same `mcpServers` shape. Otherwise, use the sidecar command directly and follow `examples/openclaw-readonly.md`.
7. Keep all claims snapshot-scoped and read-only.

## Good fit

- inspect one site's current assignments, messages, or events
- keep a coding-agent workflow grounded in one snapshot instead of raw browser state
- test builder-side integration without reopening live campus sessions

## Not a fit

- live browser takeover
- posting, replying, or submitting on external services
- inventing a write-capable plugin contract

## Recommended repo-local references

- `examples/integrations/codex-mcp.example.json`
- `examples/integrations/claude-code-mcp.example.json`
- `examples/mcp/claude-desktop.example.json`
- `examples/mcp/codex-repo-root.example.json`
- `examples/mcp/claude-desktop-repo-root.example.json`
- `examples/openclaw-readonly.md`
