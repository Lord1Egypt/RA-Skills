# Phase 2 Implementation

*Dev update by cc-mini, 2026-02-26 10:25 PST*

**Branch:** `mini/phase2-relay`

## What happened

Built and merged Memory Crystal Phase 2. The system now produces all three file types (JSONL transcripts, MD session summaries, vector DB) and manages the full `~/.ldm/` directory tree. Also merged cc-air's ephemeral relay code and expanded the poller to reconstruct remote agent file trees.

## New modules

- **`src/ldm.ts`** -- Central LDM path resolution and scaffolding. `getAgentId()`, `ldmPaths()`, `scaffoldLdm()`, `ensureLdm()`. Every other file imports paths from here.
- **`src/summarize.ts`** -- MD session summary generation. Two modes: `simple` (no API call, first message becomes title) and `llm` (calls gpt-4o-mini for title + summary + topics). Controlled by `CRYSTAL_SUMMARY_MODE` env var.

## Changes to existing modules

- **`src/core.ts`** -- `resolveConfig()` checks `~/.ldm/memory/crystal.db` first, falls back to legacy path. Added `RemoteCrystal` class and `createCrystal()` factory from relay merge.
- **`src/cli.ts`** -- Added `crystal init [--agent]` and `crystal migrate-db` subcommands. Init scaffolds the full directory tree. Migrate copies the DB, verifies chunk count, creates symlink.
- **`src/cc-hook.ts`** -- Three new behaviors after each capture: (1) archive JSONL transcript to `~/.ldm/agents/{id}/transcripts/`, (2) generate MD session summary to `sessions/`, (3) relay mode from cc-air merge (encrypt + drop at Worker when env vars set).
- **`src/poller.ts`** -- After decrypting relay drops, now reconstructs the remote agent's full file tree: JSONL transcript, MD summary, daily breadcrumb. This means the Mini has everything even if a device is lost.
- **`src/mirror-sync.ts`** -- Updated paths to use `ldmPaths()` instead of hardcoded `~/.openclaw/memory-crystal/`.
- **`src/dev-update.ts`** -- Writes to each repo's own `ai/` folder instead of centralized `wip-dev-updates`. Disabled the git add/commit/push to the old repo.
- **`src/mcp-server.ts`** -- Uses `createCrystal()` factory. Remote mode guards on source indexing operations.

## Portability fix

All hardcoded `/Users/lesa` and `/Users/parker` HOME fallbacks replaced with `process.env.HOME || ''` across every source file. The old fallbacks were cc-air writing `/Users/parker` and the Mini having `/Users/lesa`. Neither matters in practice (HOME is always set), but it was wrong for anyone else installing.

## Relay merge

Merged `origin/cc-air/phase2-relay` into the branch. cc-air built the ephemeral encrypted relay: `src/crypto.ts` (AES-256-GCM + HMAC), `src/worker.ts` (Cloudflare dead drop), `src/poller.ts` (Mini-side ingest), `src/mirror-sync.ts` (device-side DB pull). One conflict in cc-hook.ts (imports + dev-update section), resolved to keep both relay mode and the new summary/archive code.

## ai/ folder cleanup

Established the inbox convention: `ai/todos/inboxes/{recipient}/`. Each agent or human gets an inbox. Moved salience-research from `artifacts/` to `ai/notes/`. Added `PUNCHLIST.md` for blockers to ship. Updated `wip-dev-resources/DEVELOPMENT-PROCESS.md` with the new convention.

## Verified

- `npm run build` (local + worker): zero errors, 12 entry points
- `crystal status`: 159,574 chunks from existing DB
- `crystal init --agent cc-mini`: scaffolds `~/.ldm/` correctly
- `crystal search "test"`: returns results
- `node poller.js --status`: "not configured" (correct)
- `node mirror-sync.js --status`: shows state

## What's next

Parker's moves: run `crystal migrate-db`, deploy plugin, merge to main, release. Relay setup (Cloudflare) when ready. See `ai/todos/inboxes/parker/` and `ai/todos/PUNCHLIST.md`.
