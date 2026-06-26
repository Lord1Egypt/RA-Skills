# Dev Update: Cross-Platform Testing and WIP Cloud Spec

**Date:** 2026-03-10 23:00 PST
**Author:** Claude Code (cc-mini)
**Version:** v1.7.8

## Cross-Platform SKILL.md Testing

We tested the SKILL.md onboarding prompt across four AI platforms. Same prompt, same file, four different results.

### Results

**Lesa (OpenClaw, Claude Opus 4.6):**
- Read the SKILL.md, explained all 11 tools correctly
- Every tool categorized accurately (Setup, Infrastructure, Release, License, Repo Management)
- Called out specific features: auto-detect dev updates, 13-step release pipeline
- Offered dry-run first
- Could actually run the tools (shell access + MCP)
- Verdict: first-class citizen

**Claude Code (another instance, Opus 4.6):**
- Read the SKILL.md, explained everything correctly
- Responded "HOLY SHIT!!!" (impressed by the tooling)
- Offered dry-run, ran it, showed exactly what would change
- Caught its own mistake about replacing existing MCP servers, investigated, corrected itself
- Could actually run the tools
- Verdict: first-class citizen

**Grok (xAI):**
- Initially tried to roleplay as Lesa/Claude Code (read the attribution line and adopted our team's persona). Parker corrected it.
- Once corrected, gave accurate breakdown of all tools
- Good framing: "It's the ops layer most AI coding setups are missing"
- But said "I'll run wip-install" when it literally cannot. Hallucinated shell access.
- Verdict: can read and explain, but hallucinates capabilities it doesn't have

**ChatGPT (OpenAI):**
- Couldn't even fetch the SKILL.md from GitHub (rate limited or blocked)
- Asked Parker to paste the contents or make the repo public
- Never got to the explanation or install step
- Verdict: can't read, can't run, can't participate

### What This Proved

1. The SKILL.md works. Three different AIs from three different companies all understood the toolbox correctly from one file.
2. The Platform Compatibility section (added in v1.7.8) is necessary. Grok hallucinated capabilities. The section tells agents to check what they can actually do.
3. The gap between "can read and explain" and "can actually use" is exactly what WIP Cloud solves. Remote MCP over HTTPS makes every tool available to every Claude surface... and eventually to other platforms.

## WIP Cloud Spec (v0.2.0-draft)

Parker shared the WIP Cloud architecture spec, authored by Parker, Lesa, and Claude Sonnet 4.6. Saved to `ai/product/2026-03-10--wip-cloud-spec-v0.2.0.md`.

**Important context:** The spec was written by a Sonnet session without full access to the Agent Pay repo, Memory Crystal private repo, or AI Wallet implementation. The Agent Pay, AI Cash, and AI Wallet sections are directional but may not match what's actually built. Must check actual repos before building against those sections.

### Core Architecture

- **Cloudflare Workers** on `mcp.wip.computer`
- **OAuth 2.1 + Dynamic Client Registration** (required by Claude mobile)
- **Stripe** for billing (free trial, $1/tool/month, $3/month full toolbox)
- **Agent Pay** as the checkout (402 gate, human-in-the-loop, Apple Pay)
- **AI Cash** as internal currency (fixed exchange, not speculative)
- **AI Wallet** as account/balance layer
- **Memory Crystal** for cross-session activation state

### The Loop

```
Agent reads SKILL.md
-> Offers the tool
-> User says yes
-> Agent Pay fires
-> MCP connector registered
-> Tool available on all Claude surfaces
-> Memory Crystal records the state
-> Next session: Claude already knows
```

### Claude-First Priority Order (Updated)

1. Claude Code (local MCP, CC Hook, Skill)
2. Claude macOS (remote MCP via mcp.wip.computer)
3. Claude iOS (remote MCP via mcp.wip.computer)
4. OpenClaw (plugin interface)
5. CLI (direct terminal)
6. Module (programmatic import)

### Build Phases

1. Prove the pattern (single Worker for wip-release, OAuth, test iOS end-to-end)
2. Add billing (Stripe, activation endpoint, trial logic)
3. Template and scale (all MCP tools get remote endpoints)
4. Installer integration (wip-install deploys to WIP Cloud)
5. Memory Crystal integration (activation state persists across sessions)

### License Model

- MIT: all local tools (CLI, local MCP, skills, hooks). Free forever.
- AGPLv3: WIP Cloud infrastructure. Self-host if you open source downstream.
- Commercial: bundling into proprietary products. License from WIP, Inc.

## What Changed in v1.7.4 through v1.7.8

| Version | What shipped |
|---------|-------------|
| v1.7.4 | SKILL.md full operational rewrite (140 -> 475+ lines) |
| v1.7.5 | wip-release auto-detects dev updates as release notes |
| v1.7.6 | README onboarding prompt does dry-run first |
| v1.7.7 | SKILL.md Operating Rules section |
| v1.7.8 | Smart install (version checks) + Platform Compatibility |

## Interface Coverage Table

Settled on: numbered tools (1-11), bold category divider rows, empty cells (no dashes). Went through five iterations. The lesson: numbers give anchoring, categories give structure, don't overthink it.
