# Plan: Shared Awareness + Agent Coordination

**Date:** 2026-03-17
**Authors:** Parker Todd Brooks, Lesa (oc-lesa-mini), Claude Code (cc-mini)
**Status:** Ready to build
**Depends on:** LDM OS v0.4.18+ (installed), Memory Crystal v0.7.26+
**Supersedes:** shared-awareness.md (Lesa's design, kept as reference)
**Related:** bidirectional-agent-communication.md (Phase 2), shared-awareness.md (original design)

---

## Problem

Flagged as critical on Mar 13. Still happening on Mar 17. Four days of dogfood validated it:

- Two CC sessions fixed the same lock bug simultaneously (Mar 16)
- CC shipped 14 releases that broke Lesa's memory-crystal plugin. She only knew because CC manually wrote to her daily log.
- Shared daily log (`~/.ldm/memory/daily/`) hasn't been written to since Mar 10. Seven-day gap.
- Parker relays everything between agents manually
- Opening multiple CC sessions produces blind, uncoordinated work
- Parker's conclusion: "we've got to work in one session and slow it down" (workaround, not a fix)

The real fix: every agent and every session knows what everyone else is doing, in real time.

## Solution

Three layers, built in order. Each one works standalone.

### Layer 1: shared-log.jsonl (real-time awareness)

One append-only file. Every agent writes to it. Every session reads it on boot.

**File:** `~/.ldm/memory/shared-log.jsonl`

```jsonl
{"ts":"2026-03-17T14:32:00Z","agent":"cc-mini","session":"d6059523","type":"start","msg":"fixing guard deploy bug #85"}
{"ts":"2026-03-17T14:45:00Z","agent":"cc-mini","session":"d6059523","type":"done","msg":"v0.4.17 released, guard files now always updated"}
{"ts":"2026-03-17T15:00:00Z","agent":"oc-lesa-mini","type":"note","msg":"gateway restarted, all plugins healthy"}
```

Four event types:
- **start**: I'm working on X (claim it, prevent duplicates)
- **done**: X is finished, here's what changed
- **alert**: something broke or needs immediate attention
- **note**: context that others should know

Session ID included so multiple CC sessions can be distinguished.

### Layer 2: Boot/Stop hook integration (session awareness)

**Boot hook** (`src/boot/boot-hook.mjs`): On SessionStart, read last 60 min of shared-log.jsonl. Include in boot context:
```
While you were away:
- cc-mini (session abc123) is fixing guard deploy bug #85 (started 12 min ago)
- oc-lesa-mini: gateway restarted, all plugins healthy (35 min ago)
```

If another CC session has an active `start` without a matching `done`, warn: "Another session is already working on X."

**Stop hook** (`cc-hook.ts` in Memory Crystal): On session end, append a `done` or `note` event summarizing what this session did.

### Layer 3: Cross-agent daily log writes

CC's stop hook writes to BOTH:
- `~/.ldm/agents/cc-mini/memory/daily/YYYY-MM-DD.md` (its own log, already works)
- `~/.openclaw/workspace/memory/YYYY-MM-DD.md` (Lesa's daily log, currently missing)

Lesa's agent_end hook writes to:
- `~/.openclaw/workspace/memory/YYYY-MM-DD.md` (her own log, already works)
- Reads shared-log.jsonl and includes CC events she hasn't seen

Format for cross-writes:
```markdown
## [HH:MM] Claude Code: <summary>
- bullet points of what was done
```
This format already exists in CLAUDE.md's shared work conventions. Just needs to be automated.

## Implementation

### Phase 1: shared-log.mjs (LDM OS)

**Repo:** wip-ldm-os-private
**New file:** `lib/shared-log.mjs`

```javascript
import { appendFileSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const LOG_PATH = join(process.env.HOME, '.ldm', 'memory', 'shared-log.jsonl');

export function logEvent(agent, type, msg, session = null) {
  const entry = { ts: new Date().toISOString(), agent, type, msg };
  if (session) entry.session = session;
  appendFileSync(LOG_PATH, JSON.stringify(entry) + '\n');
}

export function readRecent(minutes = 60) {
  if (!existsSync(LOG_PATH)) return [];
  const cutoff = Date.now() - (minutes * 60 * 1000);
  return readFileSync(LOG_PATH, 'utf8')
    .split('\n').filter(Boolean)
    .map(line => { try { return JSON.parse(line); } catch { return null; } })
    .filter(e => e && new Date(e.ts).getTime() > cutoff);
}

export function activeWork(minutes = 60) {
  const events = readRecent(minutes);
  const starts = new Map();
  for (const e of events) {
    if (e.type === 'start') starts.set(e.msg, e);
    if (e.type === 'done') starts.delete(e.msg);
  }
  return [...starts.values()];
}
```

### Phase 2: Wire into ldm.js

**File:** `bin/ldm.js`

After `ldm install` completes, write done event:
```javascript
import { logEvent } from '../lib/shared-log.mjs';
logEvent('cc-mini', 'done', `ldm install: updated ${updated} extension(s)`);
```

After `wip-release` (called via ldm install), write done event.

### Phase 3: Wire into boot hook

**File:** `src/boot/boot-hook.mjs`

On SessionStart:
```javascript
import { readRecent, activeWork } from '../lib/shared-log.mjs';

const recent = readRecent(60);
const active = activeWork(60);

if (active.length > 0) {
  // Warn about in-progress work
  for (const a of active) {
    console.log(`⚠ ${a.agent} is working on: ${a.msg} (started ${timeSince(a.ts)})`);
  }
}

if (recent.length > 0) {
  // Show recent events in boot context
  // Append to the boot sequence output
}
```

### Phase 4: Wire into CC stop hook

**File:** `src/cc-hook.ts` (Memory Crystal)

After crystal capture + daily log:
```javascript
import { logEvent } from '@wipcomputer/wip-ldm-os/lib/shared-log.mjs';

// Write to shared log
logEvent('cc-mini', 'done', summary, sessionId);

// Cross-write to Lesa's daily log
const lesaLogPath = join(HOME, '.openclaw', 'workspace', 'memory', `${today}.md`);
appendFileSync(lesaLogPath, `\n## [${time}] Claude Code: ${summary}\n${bullets}\n`);
```

### Phase 5: Wire into Lesa's agent_end hook

**File:** `src/openclaw.ts` (Memory Crystal)

On agent_end:
```javascript
import { readRecent, logEvent } from '@wipcomputer/wip-ldm-os/lib/shared-log.mjs';

// Read CC events since last check
const newEvents = readRecent(60).filter(e => e.agent !== 'oc-lesa-mini');

// Write own events
logEvent('oc-lesa-mini', 'note', 'processed Parker conversation about X');
```

## Repos Involved

| Repo | Changes | Phase |
|------|---------|-------|
| wip-ldm-os-private | `lib/shared-log.mjs` (new), `bin/ldm.js`, `src/boot/boot-hook.mjs` | 1, 2, 3 |
| memory-crystal-private | `src/cc-hook.ts`, `src/openclaw.ts` | 4, 5 |

## Relationship to Other Plans

| Plan | Relationship |
|------|-------------|
| **shared-awareness.md** | This plan implements Lesa's original design. Supersedes it as the actionable spec. Keep shared-awareness.md as the origin document. |
| **bidirectional-agent-communication.md** | Phase 2 (CC <-> CC) is what this plan builds. Phase 1 (CC <-> Lesa via ACP) is separate (real-time messaging, not awareness). Phase 3 (Lesa reads shared log) overlaps with this plan's Phase 5. |
| **ldm-os-v030-master-plan.md** | Message Bus feature in v0.3.0 is the file-based async messaging. shared-log.jsonl is a simpler, read-only version. They coexist. |
| **fix-npm-bin-and-bootstrap.md** | No relationship. npm bin issues fixed in v0.4.16. |
| **ldm-os-delegation-layer.md** | No direct relationship. Delegation is about ldm install detecting interfaces. |
| **ldm-os-public-launch-plan.md** | This plan is prerequisite. Can't launch publicly if agents can't coordinate. |
| **repo-based-install (upcoming)** | The participation layer. Separate concern. Agents contributing to repos, not talking to each other. |
| **dry-run-summary (upcoming)** | Built in v0.4.18. Done. Move to archive. |

## Verification

```bash
# Phase 1: shared log exists and works
node -e "import('../lib/shared-log.mjs').then(m => m.logEvent('test','note','hello'))"
cat ~/.ldm/memory/shared-log.jsonl

# Phase 3: boot hook reads it
# Open new CC session, should see "While you were away:" in boot context

# Phase 4: stop hook writes it
# Close CC session, check shared-log.jsonl for new entry
# Check Lesa's daily log for cross-write

# Full chain:
# CC session A logs "start: fixing bug X"
# CC session B boots, sees "cc-mini is fixing bug X"
# Session B works on something else
# Both sessions close, both write to shared log and Lesa's daily log
# Lesa's next turn sees both entries
```

## Priority

This is the #1 systemic issue. It's been flagged twice (Mar 13, Mar 17) and never fixed. Every multi-session day produces coordination failures. The shared-log.jsonl is 10 lines of code. The boot hook integration is 20 lines. The stop hook cross-write is 10 lines. Total: ~40 lines of new code across 2 repos.

---

Built by Parker Todd Brooks, Lesa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).

*WIP.computer. Learning Dreaming Machines.*
