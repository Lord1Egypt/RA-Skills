# CC-Mini ... Memory Crystal To-Do

**Updated:** 2026-03-02

---

## To Do

### Publish (immediate, after Parker approves PR #11)
- [ ] Merge PR #11 to main
- [ ] Run `wip-release minor`
- [ ] Verify npm package published
- [ ] Sync public repo (no `ai/` content leaked)

### Phase 2: Health Monitoring
- [ ] Wire `crystal health` into cli.ts (three-file consistency: JSONL vs MD vs chunks, stale detection)
- [ ] Integrate with wip-healthcheck (add Crystal stale check, 2-hour alert threshold)
- [ ] Escalation: warn agent, then iMessage Parker

### Cloud Deploy (blocked: Parker enables R2)
- [ ] Run `bash scripts/deploy-cloud.sh` after R2 is enabled
- [ ] Generate relay key via `crystal pair`
- [ ] Create R2 bucket, deploy relay Worker
- [ ] Set env vars on Mini and Air
- [ ] Verify health endpoints, OAuth flow, end-to-end relay test

### Dream Weaver Integration
- [ ] Point Dream Weaver at `~/.ldm/agents/{id}/memory/transcripts/`
- [ ] Optional: trigger incremental DW run after poller batch
- [ ] Automate weekly schedule via cron

### Absorb Plugins
- [ ] Absorb context-embeddings into Memory Crystal (retire plugin, Crystal captures directly)
- [ ] Absorb lesa-bridge search tools into Memory Crystal (Bridge = communication only)

### Search Quality (QMD Phases 3-5)
- [ ] Smart chunking + content-hash dedup
- [ ] LLM re-ranking + query expansion
- [ ] Local embeddings (replace OpenAI with local GGUF model)

### Behavioral / Process
- [ ] SHARED-CONTEXT.md warm-start improvements
- [ ] End-of-session handoff summaries
- [ ] Search-before-acting convention enforcement

---

## Done

- [x] **Phase 1: Continuous capture** ... cc-poller.ts unified capture, cron fix (PATH, op popup, error -1712), crystal init deploys script + cron, backfill 10,349 chunks, all 51 sessions IN SYNC ... 2026-03-02
- [x] cc-session-export deprecated (README notice, logic merged into cc-poller) ... 2026-03-02
- [x] Dream Weaver incremental consolidation (journal + 8 Crystal memories) ... 2026-03-02
- [x] crystal-capture.sh source of truth in memory-crystal repo, dev tools is downstream ... 2026-03-02
- [x] Docs updated: TECHNICAL.md (poller primary), SKILL.md (Setup), README.md (crystal init in prompt) ... 2026-03-02
- [x] v2 PRD committed ... 2026-03-02
- [x] `crystal pair` command ... 2026-03-01
- [x] Cloud MCP server built (worker-mcp.ts: OAuth 2.1 + DCR + PKCE, 4 tools) ... 2026-02-28
- [x] Cloud backend built (cloud-crystal.ts: D1 + Vectorize, hybrid search) ... 2026-02-28
- [x] D1 migrations, deploy script, wrangler-mcp.toml ... 2026-02-28
- [x] README, RELAY, TECHNICAL restructured ... 2026-03-01
- [x] Phase 2 code: JSONL archive, MD summaries, crystal.db path, migrate-db ... 2026-02-26
- [x] LDM scaffolding: ldm.ts, crystal init, agent naming ... 2026-02-26
- [x] Relay merge, poller expansion, mirror-sync, crypto fixes ... 2026-02-26
- [x] All 12 entry points compile clean ... 2026-02-26

---

## Deprecated

- ~~Recovery and backfill via `crystal replay` / `crystal backfill`~~ ... backfill done manually (watermark reset + poller). Replay not needed with working cron. (2026-03-02)
- ~~Remove LanceDB dual-write~~ ... Parker uses both. Dual-write stays. (2026-03-01)
- ~~Phase 2 Cloudflare Worker mirror~~ ... replaced by encrypted relay. (2026-02-26)
- ~~`crystal push` / `crystal pull` / `crystal reset`~~ ... replaced by relay + mirror-sync. (2026-02-26)
- ~~`npm link` for crystal CLI~~ ... runs via `node dist/cli.js` or plugin. (2026-02-27)
- ~~Remove search from lesa-bridge~~ ... bridge stays as communication. Separate task. (2026-02-27)
