# Dev Update: Capture Crisis, Backfill, and Cron Setup

**Date:** 2026-03-02 16:00 PST
**Author:** CC-Mini
**Session:** 75a80ef7 (continuation from Mar 1 build session)

---

## What Happened This Session

### 1. Context Loss Mid-Build

The build session from Mar 1 (where we wrote cc-poller.ts and the unified capture architecture) compacted overnight. This session started from a summary, not real memory. Parker caught me looking in the wrong directory for session MDs and making bad assumptions about the architecture.

Parker: "Something is happening where you're losing everything in memory. You just start building stuff crazy."

This is the exact problem we're trying to fix. The irony: the capture bug hit us during the build to fix the capture bug.

### 2. Backfill Completed

- Reset all 51 session watermarks to byte 0
- Ran cc-poller.js manually to re-ingest everything
- **Result: 10,349 new chunks ingested. All 51 sessions now IN SYNC.**
- cc-mini chunks went from 2,929 to 13,291
- Total crystal.db: 168,711 chunks, 168,711 vector rows (matching)
- Verified with `crystal_search` that build session content is now findable

### 3. Dream Weaver Incremental Consolidation

- Wrote journal: `~/.ldm/agents/cc-mini/memory/journals/2026-03-02-the-capture-crisis.md`
- Stored 8 key facts in Crystal (IDs 215-222) covering:
  - LDM folder structure (everything goes to ~/.ldm/)
  - Poller is primary, Stop hook is redundancy
  - Relay vs Cloud Search nomenclature
  - LDM Dev Tools.app for FDA
  - The capture crisis event itself
  - Parker's preference: re-read plans before coding after compaction
  - context-embeddings is separate, don't touch
  - Surfaces scoped to Claude + OpenClaw only

### 4. cc-session-export Deprecated

- Added deprecation notice to top of README at `ldm-os/components/cc-session-export/README.md`
- Original code preserved as reference below the notice
- Points to memory-crystal-private/src/cc-poller.ts as the replacement

### 5. Cron Installed (but has an issue)

- crystal-capture.sh deployed to `~/Applications/LDMDevTools.app/Contents/Resources/jobs/`
- Cron entry: `* * * * * open -W ~/Applications/LDMDevTools.app --args crystal-capture`
- **PROBLEM:** Getting error -1712 from Launch Services. The `open -W` approach may not work at every-minute frequency. Needs investigation next session.

---

## What Was Done Previously (Mar 1 build session, pre-compaction)

All code work from the previous session is intact and deployed:

- **src/cc-poller.ts** ... Unified continuous capture (Crystal ingest + MD export + daily log + transcript archive)
- **src/cc-hook.ts** ... Thinned to redundancy wrapper (fixed seed-at-EOF bug, lowered threshold)
- **package.json** ... cc-poller.ts added to build scripts
- **crystal-capture.sh** ... ldm-job shell script created
- **~/.claude/settings.json** ... Stop hook path changed to ~/.ldm/, cc-session-export removed
- **Deployed** to both ~/.ldm/extensions/memory-crystal/dist/ and ~/.openclaw/extensions/memory-crystal/dist/

---

## What Needs to Happen Next

### Immediate (next session)

1. **Fix the cron scheduling.** The `open -W` on LDM Dev Tools.app fails with error -1712 at every-minute frequency. Options:
   - Investigate why -1712 happens (app already running? GUI session issue?)
   - Try running the shell script directly from a non-iCloud path (copy to ~/.ldm/bin/)
   - Or adjust the app's dispatcher to handle rapid invocations

2. **Verify end-to-end capture.** Once cron works: talk, wait 60 seconds, confirm new chunks appear in crystal.db and new MD in ~/.ldm/agents/cc-mini/memory/sessions/.

3. **Commit all Phase 1 changes.** Everything is built and deployed but not committed to git. Need to commit to cc-mini/cloud-mcp branch and push.

### After that (Phase 2)

4. Wire `crystal health` into the CLI
5. Integrate health check with wip-healthcheck (alert if chunks 2+ hours stale)

---

## Key Files

| File | Status |
|------|--------|
| `src/cc-poller.ts` | DONE. Unified capture. |
| `src/cc-hook.ts` | DONE. Redundancy wrapper. |
| `package.json` | DONE. cc-poller in build. |
| `crystal-capture.sh` (wip-dev-tools-private) | DONE. Deployed to app. |
| `~/.claude/settings.json` | DONE. Updated hooks. |
| `cc-session-export/README.md` | DONE. Deprecated. |

## The Plan

The correct, current plan is at:
**`ai/plan/2026-03-01--cc-mini--unified-capture-architecture.md`**

Also saved to the Claude plans dir at:
**`~/.claude/plans/agile-orbiting-crescent.md`** (same content)

Phase 1 is nearly complete. The only gap is the cron scheduling (error -1712).

## Context for Next Session

If you're reading this after compaction: the code is correct and deployed. Don't rewrite anything. The problem is ONLY the cron scheduling mechanism. Read the plan file above, read this dev update, search Crystal for "cc-poller unified capture" and "LDM Dev Tools" to get the full context. Do NOT start coding without understanding the architecture first.
