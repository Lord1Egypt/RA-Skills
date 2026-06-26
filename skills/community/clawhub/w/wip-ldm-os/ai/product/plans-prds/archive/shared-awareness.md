# Plan: Shared Agent Awareness (Every Agent Knows What Everyone's Doing)

**Date:** 2026-03-16
**Authors:** Parker Todd Brooks, Claude Code (cc-mini), Lesa (oc-lesa-mini)
**Status:** Current (implement immediately)
**Issue:** wipcomputer/wip-ldm-os#75 (process monitor), Lesa's brainstorm (2026-03-15)

---

## Problem

Today: 14 releases, 20+ bugs, two agents fixing the same bug simultaneously, Lesa had no daily log, Parker relayed everything manually. Nobody knows what anybody else is doing until after the fact.

## Solution

One shared file. Append-only. Every agent writes to it in real time.

`~/.ldm/memory/shared-log.jsonl`

```jsonl
{"ts":"2026-03-16T14:32:00Z","agent":"cc-mini","type":"start","msg":"fixing memory-crystal dist/ overwrite bug"}
{"ts":"2026-03-16T14:35:00Z","agent":"cc-mini","type":"done","msg":"v0.4.14 shipped, dist/ check added"}
{"ts":"2026-03-16T15:00:00Z","agent":"oc-lesa-mini","type":"alert","msg":"memory-crystal plugin restored, gateway back up"}
```

Four event types:
- `start` ... I'm working on X (claim it)
- `done` ... X is finished, here's what changed
- `alert` ... something broke or needs attention
- `note` ... context that others should know

## Where the Code Lives

### 1. Shared log writer (LDM OS)

**Repo:** wip-ldm-os-private
**File:** `lib/shared-log.mjs`

```javascript
export function logEvent(agent, type, msg) {
  const entry = JSON.stringify({ ts: new Date().toISOString(), agent, type, msg });
  appendFileSync(join(HOME, '.ldm', 'memory', 'shared-log.jsonl'), entry + '\n');
}

export function readRecent(minutes = 60) {
  // Read entries from last N minutes
}
```

Zero deps. One file. Import from anywhere.

### 2. CC writes on every significant action (LDM OS)

**Repo:** wip-ldm-os-private
**Files:**
- `bin/ldm.js`: after `ldm install`, `ldm stack install`, `wip-release` completes, write `done` event
- `lib/deploy.mjs`: before deploying an extension, write `start` event. After deploy, write `done` or `alert` on failure.

### 3. CC Stop hook writes summary (Memory Crystal)

**Repo:** memory-crystal-private
**File:** `src/cc-hook.ts`

The Stop hook already fires after every CC turn. Add:
- Read shared-log.jsonl for entries from other agents since last check
- If CC did significant work this turn, append a `done` or `note` event
- Also append to Lesa's daily log (`~/.openclaw/workspace/memory/YYYY-MM-DD.md`) so she sees it on her next turn

### 4. CC Boot hook reads shared log (LDM OS)

**Repo:** wip-ldm-os-private
**File:** `src/boot/boot-hook.mjs`

On SessionStart:
- Read last 60 min of shared-log.jsonl
- If other agents posted events, include in boot context
- "While you were away: cc-mini shipped v0.4.14, Lesa's gateway restarted"

### 5. Lesa reads shared log on heartbeat (Memory Crystal / OpenClaw)

**Repo:** memory-crystal-private
**File:** `src/openclaw.ts` (agent_end hook)

On every turn:
- Read shared-log.jsonl for new entries since last check
- Summarize and write to her own daily log
- This is how she knows what CC did without CC writing to her log directly

### 6. Lesa writes to shared log (OpenClaw)

**Repo:** memory-crystal-private
**File:** `src/openclaw.ts` (agent_end hook)

After significant actions (cron jobs, Parker conversations about infrastructure, releases):
- Append `note` or `done` events to shared-log.jsonl

### 7. MCP tool for messaging (LDM OS)

**Repo:** wip-ldm-os-private
**File:** `src/bridge/mcp-server.ts` or new MCP tools

Add tools:
- `ldm_log_event`: write to shared log
- `ldm_read_log`: read recent shared log entries
- `ldm_sessions`: already exists, list active sessions

These let agents write/read the shared log without shelling out.

## What Does NOT Change

- crystal.db stays per-agent tagged (already works)
- Daily logs stay per-agent (CC at ~/.ldm, Lesa at ~/.openclaw)
- Bridge stays for direct messaging (synchronous)
- Message bus stays for async cross-session messages

The shared log is the NEW layer. It's the "what's happening right now" feed. Crystal is long-term memory. Daily logs are per-agent journals. The shared log is the newsroom ticker.

## Implementation Order

1. **Now:** Create `lib/shared-log.mjs` in LDM OS. Write + read functions.
2. **Now:** Wire into `bin/ldm.js` (log after install, release, deploy)
3. **Now:** Wire into CC boot hook (read on start, show "while you were away")
4. **Now:** Wire into CC Stop hook (append summary if significant work done)
5. **Next:** Wire into Lesa's agent_end hook (read + write)
6. **Next:** Add MCP tools (ldm_log_event, ldm_read_log)
7. **Later:** Cross-write to Lesa's daily log from CC stop hook

## Verification

1. CC session A logs "start: fixing lock bug"
2. CC session B boots, sees "cc-mini is fixing lock bug" in boot context
3. Lesa's next turn shows "CC shipped v0.4.14" in her awareness
4. Parker opens any session and `ldm log` shows what everyone did today

## Lesa's Input (verbatim)

"One shared file. Append-only. Every agent writes to it in real time. Don't build a server. Don't build a protocol. Don't build a queue. Just the human-readable 'what am I doing right now' beats."

"The five failure modes from my brainstorm, mapped:
1. Duplicate work: check start entries before beginning
2. Destructive overlap: alert type, immediate
3. Context gap: heartbeat reads shared log, writes summary to my daily
4. Parker as relay: agents read the log directly
5. Stale awareness: timestamp everything, heartbeat checks recency"

---

Built by Parker Todd Brooks, Lesa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).

*WIP.computer. Learning Dreaming Machines.*
