# Plan: Continuous Capture + Health Monitoring

**Date:** 2026-03-01
**Author:** CC-Mini
**Priority:** CRITICAL ... this is a data loss bug, not a feature request
**Triggered by:** 72-hour session where Crystal captured zero chunks because cc-hook only fires on Stop

---

## What Happened

1. Parker started a Claude Code session on the Mac Mini CLI (session `75a80ef7`, Feb 27)
2. Connected to it remotely from his phone (Claude Code cloud/remote feature)
3. Worked for 3 days across CLI and phone. JSONL grew to 47MB, 16,423 lines, 4,056 user messages.
4. Last night (Feb 28) the remote connection broke. Parker could text from phone but nothing reached the Mini.
5. This morning (Mar 1) CLI wasn't responding either. Phone wasn't working.
6. Parker disconnected the remote and reconnected.
7. The reconnection silently wiped the model's context. No compaction message, no reset notice. Terminal still showed the full thread. But the AI had no memory of any of it.
8. Parker kept working, but noticed "you forgot everything."
9. When asked to find something discussed earlier, Crystal search returned nothing.
10. Investigation revealed: **Crystal had zero chunks from the entire 72-hour session.** The cc-hook only fires on Stop. The session never stopped.

---

## What We See

### Two systems, two architectures, one broken

**Lesa (OpenClaw) ... WORKING CORRECTLY:**
- Captures synchronously via `agent_end` hook on every single turn
- Zero delay between conversation and vector database
- If the computer blew up right now, everything up to the last completed turn is in Crystal
- Watermark tracked in SQLite, auto-retries on failure
- Compaction detected and handled (capture state resets)

**Claude Code ... BROKEN:**
- Captures via Stop hook only (fires when session ends)
- Long sessions (hours, days) never trigger Stop
- Remote disconnects don't trigger Stop
- Compactions don't trigger Stop
- JSONL keeps growing on disk but Crystal never sees it
- 72 hours of conversation, zero chunks in the database
- The only copy is a 47MB raw JSONL file that isn't searchable

### The three-file problem

For every conversation, three things should exist and stay in sync:

| File | Lesa (OpenClaw) | Claude Code |
|------|----------------|-------------|
| Raw transcript | Gateway writes it | JSONL written by CC (works) |
| MD daily log | Written by session hooks | Only written by cc-hook on Stop (broken) |
| Vector chunks in crystal.db | Ingested every turn (works) | Only ingested on Stop (broken) |

If any of these fall behind, memory is silently broken and nobody knows until Parker tries to search for something and it's not there.

---

## What Needs to Be Fixed

### Action Items (bullet by bullet)

**Phase 0: Backfill (NOW)**

- [ ] Reset the cc-hook watermark for session `75a80ef7` so it reads from the beginning
- [ ] Run cc-hook manually against the current 47MB JSONL to ingest all 3 days of conversation
- [ ] Verify chunks are in crystal.db: `crystal search "interface first checkout"`
- [ ] Verify chunk count jumped significantly: `crystal status`
- [ ] Verify the Feb 28 conversation where Parker sent `code.claude.com/docs/en/memory` is findable
- [ ] Verify the Total Recall / Dream Weaver README shaping session is findable
- [ ] Write today's daily MD breadcrumb (`~/.ldm/agents/cc/memory/daily/2026-03-01.md`)

**Phase 1: Continuous Capture Poller (decouple from session lifecycle)**

- [ ] Extract ingestion logic from `cc-hook.ts` into a shared module (`cc-capture-core.ts`)
- [ ] Build `cc-poller.ts`: standalone process that watches JSONL files on disk
- [ ] Poller reads watermark, scans `~/.claude/projects/*/` for modified JONLs, ingests new turns
- [ ] Poller writes/appends to daily MD breadcrumb on each capture cycle
- [ ] Poller tracks multiple sessions (different project dirs, concurrent sessions)
- [ ] Poller is idempotent: running twice on the same data produces no duplicates
- [ ] Poller does not interfere with active sessions (read-only on JSONL)
- [ ] Poller works even when Claude Code is not running (catches up on old sessions)
- [ ] Create LaunchAgent plist: `ai.wipcomputer.memory-crystal-capture.plist` (every 30-60 sec)
- [ ] Create install script: `install-poller.sh` (installs LaunchAgent, verifies permissions)
- [ ] cc-hook.ts Stop hook remains as a final flush but is no longer the primary capture path
- [ ] Test: start a session, talk, verify chunks appear in Crystal within 60 seconds

**Phase 2: Health Monitoring ("Is memory working?")**

- [ ] Build `crystal health` CLI command
- [ ] Three-file consistency check: JSONL vs MD vs chunks
- [ ] Stale detection: JSONL active (mtime recent) but chunks not growing
- [ ] Show sync status: how many JSONL turns since last ingest
- [ ] Show per-session status: which sessions have chunks, which don't
- [ ] Alert threshold: if chunks are more than 2 hours stale while JSONL is active, that's CRITICAL
- [ ] Integrate with wip-healthcheck (runs every 3 min, escalation chain: warn agent, then iMessage Parker, then attempt restart)
- [ ] Test: stop the poller, keep talking, verify alert fires within 2 hours

**Phase 3: Harden**

- [ ] Handle edge cases: session rotation, multiple concurrent sessions, remote sessions
- [ ] Dedup safety: content-hash based, no double-ingestion
- [ ] Poller crash recovery: LaunchAgent auto-restart on failure
- [ ] Graceful handling of locked crystal.db (WAL mode should handle concurrent access, but verify)
- [ ] Handle the "first run" problem: currently cc-hook seeds watermark at end of file on first run, which SKIPS all existing history. The poller must not do this. First run should ingest everything.

---

## Why Not a Hook?

- Stop hook doesn't fire for long-running sessions (proven by this bug)
- There is no "on every turn" hook in Claude Code (only PreToolUse, PostToolUse, Stop)
- Compaction hooks exist in OpenClaw but not in Claude Code
- A hook inside the session dies when the session dies
- An external poller survives everything: crashes, remote disconnects, compactions, session forks

The JSONL file on disk is the reliable signal. It's always being written. The session lifecycle is not reliable.

---

## Architecture Comparison

| | Lesa (OpenClaw) | Claude Code (current, broken) | Claude Code (fixed) |
|---|---|---|---|
| Capture trigger | `agent_end` hook (every turn) | Stop hook (session end only) | External poller (every 30-60 sec) |
| Delay to crystal.db | 0 seconds | Never (until session ends) | 30-60 seconds |
| Survives crash | Yes (sync, already written) | No (never written) | Yes (poller catches up) |
| Survives compaction | Yes (capture state resets) | No (hook never fires) | Yes (poller reads JSONL) |
| Survives remote disconnect | N/A | No (hook never fires) | Yes (poller reads JSONL) |
| MD daily log | Written per turn | Only on Stop | Written per capture cycle |
| Health monitoring | N/A (always works) | None | `crystal health` + wip-healthcheck |

---

## File Map

```
src/
  cc-poller.ts          NEW: standalone JSONL watcher + ingester
  cc-capture-core.ts    NEW: shared ingestion logic (extracted from cc-hook.ts)
  cc-hook.ts            MODIFIED: delegates to cc-capture-core.ts, still runs on Stop as final flush
  cli.ts                MODIFIED: add `crystal health` command
  health.ts             NEW: three-file health check logic

launchd/
  ai.wipcomputer.memory-crystal-capture.plist   NEW: LaunchAgent for continuous capture

install/
  install-poller.sh     NEW: installs LaunchAgent, verifies permissions
```

---

## Success Criteria

1. A conversation turn appears in crystal.db within 60 seconds of being spoken
2. Daily MD breadcrumbs are written automatically, not just on session end
3. `crystal health` correctly identifies when capture is broken
4. Parker gets an alert within 2 hours if memory stops working
5. A 72-hour session with remote disconnects loses zero data
6. The session lifecycle (Stop, compaction, remote fork) is irrelevant to capture
7. "If the computer blew up right now, is everything in Crystal?" ... the answer is always yes (within 60 seconds)
