# Dev Update: README Overhaul + MCP Fix

**Date:** 2026-03-11
**Author:** Claude Code (cc-mini)
**Branch:** cc-mini/dev

## What Changed

### README restructured
- Stripped all technical content out of README. It's now a product page: description, teach section, what it does (4 human-readable bullets), docs links, license.
- All technical docs (Quick Start, Agent Tools API, Config Resolution, CLI Commands, Write Support, Configuration, How It Works, Security, Troubleshooting, Developer Guide) live in TECHNICAL.md.
- New description: "Give your AI secure access to 1Password. Never copy-paste an API key into a chat window again."
- Compatibility line: works with Claude Code, OpenClaw, and any MCP-compatible agent. Also ships as Node.js module.

### MCP server fixed
- `mcp-server.mjs` was crashing on startup with "Schema is missing a method literal"
- Root cause: `setRequestHandler("tools/list", ...)` used strings instead of SDK schema objects
- Fix: import `ListToolsRequestSchema` and `CallToolRequestSchema` from `@modelcontextprotocol/sdk/types.js`
- op-secrets MCP server now starts clean and connects to Claude Code

### 1Password plan requirements clarified
- Service accounts work on all plans (Individual, Family, Teams, Business)
- Headless operation confirmed on Teams and Business
- Lower-tier plans may require desktop app for initial setup
- Updated TECHNICAL.md prerequisites and SKILL.md compatibility

### Feature priority reordered
- Agent tools (read/write secrets) is now #1, not config resolver
- MCP server is #2
- Reflects actual primary value: agents accessing secrets at runtime

## Commits on cc-mini/dev
1. Update description: Give your AI secure access to 1Password
2. Simplify What It Does to one-liners, details in TECHNICAL.md
3. Update description with clear value prop and compatibility
4. Remove What It Does section from README, lives in TECHNICAL.md
5. Add human-readable What It Does section
6. Move What It Does below Teach Your AI section
7. Service accounts work on all 1Password plans
8. Clarify 1Password plan requirements: all plans, headless confirmed on Teams+

## Issues Filed (on wip-ai-devops-toolbox-private)
- #123 deploy-public: require explicit approval before running
- #124 Branch deletion must verify merged status before deleting
- #125 gh pr merge should always use --delete-branch
- #126 wip-release: block if stale remote branches exist

## Still Open
- #5 Publish to ClawHub (rate limited, retry later)
