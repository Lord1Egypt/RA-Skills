# Memory Crystal v0.7.4 ... MCP Fix + AgentId Config

**Date:** 2026-03-11
**Authors:** Parker Todd Brooks, Lēsa, Claude Code

---

## What's in this release

### Agent identity reads from config, not hardcoded strings

The agent_id used when ingesting conversations was hardcoded in three places: `cc-mini` in the CC hook, `main` in the OpenClaw plugin, and `cc-mini` as the fallback in `ldm.ts`. This caused ID drift. The same agent got recorded under multiple IDs, and we had to manually merge 141K+ chunks in the database.

Now `getAgentId()` scans `~/.ldm/agents/*/config.json` for a matching harness type. The CC hook passes `'claude-code'`, the OC plugin passes `'openclaw'`, and the config file is the source of truth. `CRYSTAL_AGENT_ID` env var still works as an override.

New exports: `AgentConfig`, `loadAgentConfig()`, `saveAgentConfig()`. The installer writes `agentId` to config.json during `crystal init`.

**Closes #33.**

### MCP registrations moved to user-level

MCP server registrations moved from project-level `~/.openclaw/.mcp.json` to user-level `~/.claude.json`. The old file was a Claude Code convention that only loaded when running from `~/.openclaw/`. Now all 4 MCP servers (memory-crystal, lesa-bridge, wip-agent-pay, wip-repos) load from any directory as "User MCPs".

OpenClaw doesn't read `.mcp.json` at all. It uses its own plugin system. The file was moved to `~/.openclaw/_trash/`.

### OPENCLAW_HOME env var fix (v0.7.3)

The MCP server registration was missing the `OPENCLAW_HOME` env var. Without it, the memory-crystal MCP server couldn't find Lēsa's OpenClaw installation for private-mode checks. Fixed in v0.7.3, deployed in this release.

### Branch cleanup

33 stale branches renamed with `--merged-` suffix. Zero active branches besides main.

### QMD v1.1.6 analysis documented

Deep analysis of the search quality system with four recommendations: intent parameter for search, structured search API, persistent reranker cache, and explain mode for debugging. See `ai/product/notes/2026-03-09--cc-mini--qmd-v1.1.6-analysis-and-recommendations.md`.

---

## Files changed

| File | What |
|------|------|
| `src/ldm.ts` | `AgentConfig` interface, `loadAgentConfig()`, `saveAgentConfig()`, `getAgentId()` now scans config |
| `src/cc-hook.ts` | Uses `getAgentId('claude-code')` instead of hardcoded fallback |
| `src/openclaw.ts` | Uses `OC_AGENT_ID` instead of `'main'` fallback |
| `src/installer.ts` | Writes `agentId` to config.json during install |

---

## Install

```bash
npm install -g memory-crystal@0.7.4
```

Or update your local clone:
```bash
git pull origin main
```

---

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
