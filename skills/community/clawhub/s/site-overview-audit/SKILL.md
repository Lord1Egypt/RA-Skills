---
name: site-overview-audit
description: Summarize one supported site's current snapshot records and highest-signal items.
---

# Site Overview Audit

Use this skill when you want a read-only answer to the question:

- what does one supported site currently look like in the imported workspace

This is the narrowest skill for one-site snapshot inspection.

## Inputs

- one snapshot path
- one site name: `canvas`, `gradescope`, `edstem`, or `myuw`

## Steps

1. Load the site overview from `@campus-copilot/site-sdk`, `@campus-copilot/mcp-server`, or one of the site-scoped `@campus-copilot/mcp-readonly` sidecars.
2. Report counts, the top assignments/messages/events, and current recent updates.
3. Keep the output read-only and grounded in normalized entities.

## Good fit

- one-site Codex or Claude inspection over a snapshot
- validating that one site's records are rich enough for export, cited AI, or MCP consumption
- OpenClaw-style local consumers that want one smaller site-scoped context card

## Hard boundary

- do not mutate site state
- do not claim live browser truth from a snapshot alone
- do not present private/session-backed collectors as public site APIs

## Companion references

- `examples/workspace-snapshot.sample.json`
- `examples/mcp/codex.example.json`
- `examples/mcp/claude-desktop.example.json`
- `skills/site-mcp-consumer/SKILL.md`
