# Memory Crystal ... Punchlist

**Updated:** 2026-02-27
**Repo:** `wipcomputer/memory-crystal-private`

## Active

### Release
```bash
cd ~/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude\ Code\ -\ Mini/repos/ldm-os/components/memory-crystal-private
git checkout main && git pull
wip-release minor --notes="Phase 2: LDM scaffolding, JSONL archive, MD summaries, relay merge"
```
- [ ] `wip-release minor`

## Architecture Direction

Three features, one product:
1. **Memory** ... remember, search, forget. One SQLite DB. Any AI tool.
2. **Bridge** ... local agent-to-agent communication. All messages saved to crystal.
3. **Relay** ... multi-device sync. Remote agents communicate and share memory.

All writes go to the crystal. Always. No matter which layer.

Key merges:
- Lesa Bridge search tools absorbed into Crystal (Bridge = communication only)
- Context Embeddings absorbed into Crystal (Crystal captures conversations directly)

## Next up (not blocking ship)

- [ ] Absorb lesa-bridge into Memory Crystal as Bridge feature
- [ ] Absorb context-embeddings into Memory Crystal (retire plugin)
- [ ] Cloudflare relay setup (key, R2 bucket, Worker deploy, env vars)
- [ ] Remove LanceDB dual-write
- [ ] `crystal backfill` for ~115 historical sessions
- [ ] Point Dream Weaver at `~/.ldm/` transcripts

## Completed

- [x] Push `mini/phase2-relay` ... 2026-02-26
- [x] Create PR #2, squash-merge to main ... 2026-02-26
- [x] Deploy build to `~/.ldm/extensions/memory-crystal/` ... 2026-02-27
- [x] Migrate crystal.db to `~/.ldm/memory/crystal.db` (159K+ chunks, symlink at old path) ... 2026-02-26
- [x] Fix lesa-bridge session routing (`user: "claude-code"` for dedicated TUI-visible session) ... 2026-02-27
