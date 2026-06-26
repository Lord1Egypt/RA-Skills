# Dev Update: README Restructure, Deploy Attempt, Plan Alignment

**Date:** 2026-03-01 ~19:00 PST
**Agent:** cc-mini
**Branch:** `cc-mini/cloud-mcp`

## What Changed

### README Restructured
Features section rewritten around four product pillars:
- **Local** ... your AIs remember you. Complete memory on your machine
- **Relay** ... AIs on different machines save memories via encrypted relay. Searchable only from your local machine or private infrastructure
- **Cloud Search** ... search all your AIs from anywhere in the world. Cloud is a mirror of your local machine, can be wiped and rebuilt
- **AI-to-AI Communication** ... AIs talk to each other on same or network machines. Links to Bridge repo

Removed: "Sovereign" and "Convenience" tier labels from README (still in RELAY.md and TECHNICAL.md for technical audience). Removed "Cloud Memory" as a separate section. Removed "Multi-Device Sync" as a separate section... folded into Relay.

Each feature links to its own doc: Relay -> RELAY.md, Cloud Search -> TECHNICAL.md#cloud-mcp-architecture, AI-to-AI -> wip-bridge repo.

### Deploy Attempt
- deploy-cloud.sh fixed: added `--reveal` flag to all `op item get` calls (SA tokens return placeholder without it)
- deploy-cloud.sh fixed: replaced `grep -P` (macOS incompatible) with `grep -oE` UUID regex
- D1 database created: `40ca6b73-3701-453e-adb3-7faf1a9964ad`
- Vectorize index created: `memory-crystal-chunks` (1024 dims, cosine)
- D1 migrations applied (0001_init + 0002_cloud_storage)
- Worker secrets set: OPENAI_API_KEY, MCP_SIGNING_KEY, RELAY_ENCRYPTION_KEY
- **Blocked at deploy step:** R2 not enabled on Cloudflare account. Parker needs to activate R2 in dashboard (free)

### Plans Saved to Repo
Copied from hidden `.claude/plans/` and `_plans/` to `ai/plan/`:
- `2026-02-28--cc-mini--seven-surfaces.md` (current plan, supersedes original)
- `2026-02-28--cc-mini--claude-code-integration.md` (standalone installer plan)
- `_archive/2026-02-28--cc-mini--original-chatgpt-claude-plan.md` (superseded)

### Priority Clarification
Parker clarified build order:
1. Local (done, running, 159K+ chunks)
2. Relay: Air -> Mini (next... crystal pair, install on Air, relay conversations to Mini)
3. Cloud Search: enable searching from Air/cloud
4. ChatGPT + Claude on phone/web (after relay and cloud search work)

## Commits
- `743ca4c` Fix deploy-cloud.sh: add --reveal flag to op item get calls

## Current Blocker
- R2 needs to be enabled on Parker's Cloudflare account (free, dashboard activation)
