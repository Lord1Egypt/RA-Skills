# Dev Update: 2026-03-01 ~23:30 PST

**Author:** CC-Mini
**Branch:** cc-mini/cloud-mcp (memory-crystal-private)
**Priority:** CRITICAL ... data loss bug fix

---

## What Happened This Session

### CRITICAL BUG: 72-hour session, zero Crystal chunks

Parker worked a 72-hour Claude Code session (session `75a80ef7`, Feb 27 to Mar 1). Used remote connection from his phone. JSONL grew to 47MB, 16,423 lines, 4,056 user messages.

**What went wrong:**
1. cc-hook only fires on Claude Code's Stop hook (session end)
2. Session never ended. Remote connection ran for 3 days.
3. Crystal captured zero chunks from the entire period.
4. Last night (Feb 28) the remote connection broke. Neither CLI nor phone responded.
5. Parker disconnected and reconnected the remote.
6. Reconnection silently wiped model context. No compaction message. Terminal still showed the full thread. But the AI had no memory of any of it.
7. When asked to search for something discussed earlier, Crystal returned nothing.
8. Investigation confirmed: zero chunks from the session in crystal.db.

**Two bugs:**
- (a) Claude Code remote reconnection silently wipes context without indication
- (b) Crystal cc-hook only fires on Stop, so long sessions never get captured

### Backfill completed

- Reset watermark for session 75a80ef7 from byte 47,781,334 to byte 0
- Ran cc-hook manually against the full 47MB JSONL
- Ingested 1,455 new chunks (session total went from 1,562 to 3,017)
- Verified: Parker's Feb 28 message about `code.claude.com/docs/en/memory` now surfaces as #1 result in crystal_search
- Verified: embeddings exist for all chunks (157,981 vec rowids = 157,981 total chunks)

### Built cc-poller.ts (the fix)

New standalone continuous capture poller that decouples ingestion from session lifecycle.

**Architecture:**
- External process watches all JSONL files across `~/.claude/projects/*/`
- Uses shared watermark file (same as cc-hook)
- Runs via LaunchAgent every 30-60 seconds, or in --watch mode
- On first encounter of a JSONL, starts from byte 0 (NOT seed-at-end like cc-hook)
- Lower token threshold (100 vs cc-hook's 500) for more responsive capture
- Lazy Crystal init (only connects to crystal.db when there's data to ingest)
- Idempotent: running twice on same data produces no duplicates
- Read-only on JSONL files, doesn't interfere with active sessions

**CLI modes:**
- Default: single run (scan all JONLs, ingest new turns, exit). LaunchAgent compatible.
- `--watch`: continuous mode with configurable interval
- `--status`: show watermark state per session
- `--health`: three-file consistency check (JSONL vs MD vs chunks)

**Why not a hook?**
- Stop hook doesn't fire for long sessions (proven by this bug)
- No "on every turn" hook in Claude Code (only PreToolUse, PostToolUse, Stop)
- Compaction hooks exist in OpenClaw but not in Claude Code
- A hook inside the session dies when the session dies
- An external poller survives everything: crashes, remote disconnects, compactions, session forks

### Anthropic launched claude.com/import-memory

Anthropic released a memory import feature on March 1. Copy-paste prompt that dumps memories from other AIs into Claude.

Created comparison note: `ai/product/product-ideas/claude-import-memory-comparison.md`

Key difference: Anthropic's is a one-time copy-paste migration between walled gardens. Memory Crystal's Total Recall connects to APIs, pulls full history, and runs it through Dream Weaver Protocol. Different category.

### Plan documented

Full plan at `ai/plan/2026-03-01--cc-mini--continuous-capture-and-health-monitoring.md`:
- Phase 0: Backfill (DONE)
- Phase 1: Continuous Capture Poller (cc-poller.ts written, needs compile/install/test)
- Phase 2: Health Monitoring (`crystal health` CLI command)
- Phase 3: Harden (edge cases, dedup, crash recovery)

---

## Files Created/Modified

| File | Status |
|------|--------|
| `src/cc-poller.ts` | NEW ... standalone continuous capture poller |
| `ai/plan/2026-03-01--cc-mini--continuous-capture-and-health-monitoring.md` | NEW ... full plan |
| `ai/product/product-ideas/claude-import-memory-comparison.md` | NEW ... Anthropic comparison |
| `~/.openclaw/memory/cc-capture-watermark.json` | MODIFIED ... reset session 75a80ef7 for backfill |

---

## What's NOT Done Yet

1. **Compile cc-poller.ts** ... add to package.json build, verify it compiles
2. **LaunchAgent plist** ... `ai.wipcomputer.memory-crystal-capture.plist` (every 30-60 sec)
3. **Install script** ... `install-poller.sh`
4. **Add to CLI** ... `crystal poll`, `crystal health` commands in cli.ts
5. **Test end-to-end** ... start session, talk, verify chunks appear within 60 seconds
6. **Integrate with wip-healthcheck** ... add memory health to existing LaunchAgent
7. **Extract shared ingestion logic** ... `cc-capture-core.ts` from cc-hook.ts (cc-poller currently duplicates some logic)

---

## Next Session Pickup

1. Compile and test cc-poller.ts
2. Create LaunchAgent plist and install script
3. Install poller on the Mini
4. Verify continuous capture is working (chunks appear within 60 seconds)
5. Add `crystal health` to CLI
6. PR #11 still open for review (the earlier commit batch)
7. Everything from the previous dev update's "Next Session Pickup" still applies (R2, deploy, consent page rework)
