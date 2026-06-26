# cc-mini -- Memory Crystal Phase 2 Status

**Date:** 2026-02-26
**Agent:** cc-mini
**Branch:** `mini/phase2-relay`

## What's Done

### Priority 1 -- Three File Types

- [x] **JSONL archive** -- cc-hook copies raw JSONL to `~/.ldm/agents/{agent_id}/memory/transcripts/` after each capture. Uses mtime check to skip redundant copies.
- [x] **MD session summaries** -- cc-hook generates markdown per conversation after ingest. Two modes: `simple` (no API call) and `llm` (gpt-4o-mini). Written to `~/.ldm/agents/{agent_id}/memory/sessions/YYYY-MM-DD--HH-MM-SS--{agent}--{slug}.md`.
- [x] **crystal.db path resolution** -- `resolveConfig()` checks `~/.ldm/memory/crystal.db` first, falls back to legacy `~/.openclaw/memory-crystal/`. Auto-detection means old deployments keep working.
- [x] **`crystal migrate-db` CLI** -- Copies crystal.db to `~/.ldm/memory/`, verifies chunk count, creates symlink at old path. Never deletes the original.

### Priority 2 -- LDM Scaffolding

- [x] **`src/ldm.ts` module** -- Central path resolution. `getAgentId()`, `ldmPaths()`, `scaffoldLdm()`, `ensureLdm()`.
- [x] **`crystal init [--agent]`** -- Creates full `~/.ldm/` directory tree, writes/updates config.json with agents array.
- [x] **Agent naming** -- Via `CRYSTAL_AGENT_ID` env var. Defaults to `cc-mini`.
- [x] **appendDailyLog()** -- Refactored to use `ldmPaths()` instead of hardcoded constant. Importable for reuse.

### Priority 3 -- Relay Merge

- [x] **Merged `cc-air/phase2-relay`** into `mini/phase2-relay`. Conflicts resolved (cc-hook.ts imports + dev-update section).
- [x] **Poller expanded** -- After decrypting relay data, reconstructs remote agent's full file tree: JSONL transcript, MD summary, daily breadcrumb.
- [x] **mirror-sync.ts** -- Updated paths to use `ldmPaths()`.
- [x] **crypto.ts** -- Fixed HOME default.
- [x] **All HOME fallbacks** -- Replaced `/Users/lesa` and `/Users/parker` with `process.env.HOME || ''` across all source files. Safe for others to install.

### Other

- [x] **dev-update.ts** -- Writes to each repo's `ai/` folder (decentralized). Disabled centralized wip-dev-updates git push.
- [x] **mcp-server.ts** -- Uses `createCrystal()` factory. Remote mode guards on source indexing operations.
- [x] **Build passes** -- All 12 entry points compile clean. `crystal status`, `crystal search`, `crystal init`, `poller --status`, `mirror-sync --status` all verified.

## What's Next

### Parker Manual Steps (blockers for relay)

- [ ] Generate encryption key: `openssl rand -base64 32 > ~/.openclaw/secrets/crystal-relay-key && chmod 600 ~/.openclaw/secrets/crystal-relay-key`
- [ ] Copy key to MacBook Air (same path)
- [ ] Cloudflare: `wrangler login`, create R2 bucket `memory-crystal-relay`, set secrets (bearer tokens), deploy Worker
- [ ] Set env vars on both machines: `CRYSTAL_RELAY_URL`, `CRYSTAL_RELAY_TOKEN`, `CRYSTAL_AGENT_ID`
- [ ] End-to-end test: drop from Air, verify Mini ingests
- [ ] See full checklist: `ai/todos/parker/2026-02-25--cc-air--setup-checklist.md`

### Run migrate-db

- [ ] Stop gateway: `openclaw gateway stop`
- [ ] Run: `crystal migrate-db`
- [ ] Restart: `openclaw gateway restart`
- [ ] Verify: `crystal status` shows same chunk count from new path

### Deploy Updated Plugin

- [ ] Copy built files to extension dir and restart gateway:
  ```
  cd /path/to/memory-crystal
  npm run build
  cp -r dist skills openclaw.plugin.json package.json ~/.openclaw/extensions/memory-crystal/
  cd ~/.openclaw/extensions/memory-crystal && npm install --omit=dev
  openclaw gateway restart
  ```

### Priority 4 -- Fix Broken Systems

- [ ] **Retire context-embeddings** -- Disable once Crystal handles all three file types. Update lesa-bridge.
- [ ] **LanceDB removal** -- Remove dual-write once sqlite-vec is validated long enough.
- [ ] **Backup system** -- Partially solved by JSONL copy. Full fix: grant FDA or alternative.

### Priority 5 -- Recovery & Backfill

- [ ] **`crystal replay`** -- Re-send from raw JSONL through relay (recovery when Mini offline >24h).
- [ ] **`crystal backfill`** -- One-time ingest of ~115 historical CC sessions (~110MB, ~$0.07).

### Priority 6 -- Dream Weaver Integration

- [ ] Point Dream Weaver at `~/.ldm/agents/{id}/memory/transcripts/` instead of `~/.claude/projects/`.
- [ ] Optional: trigger incremental DW run after poller batch.
- [ ] Automate weekly schedule via cron/launchd.

### Priority 7 -- Search Quality (QMD Phases 3-5)

- [ ] Smart chunking + dedup
- [ ] LLM re-ranking + query expansion
- [ ] Local embeddings (replace OpenAI with local GGUF)

### Priority 8 -- Behavioral / Process

- [ ] SHARED-CONTEXT.md warm-start
- [ ] End-of-session handoff summaries
- [ ] Search-before-acting convention

## Notes

- crystal.db stays at `~/.openclaw/memory-crystal/` until `crystal migrate-db` is run. Symlink preserves backward compat.
- Summary mode defaults to `simple` (no API call). Set `CRYSTAL_SUMMARY_MODE=llm` for gpt-4o-mini summaries.
- The relay code builds clean but isn't deployed yet. Needs Parker's Cloudflare setup.
- 159,574 chunks in crystal.db as of this commit. All search and status commands verified working.
