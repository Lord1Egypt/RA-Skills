---
name: "signal-dreaming"
description: "Consolidate daily session logs into L2 topic files and a compact MEMORY.md index, in three bounded phases with backups, lifecycle and secret guards."
---

# Signal Dreaming

Memory consolidation in three phases: **Sense → Consolidate → Settle**.

Daily session logs accumulate raw detail. This skill reads the ones written since the last run, promotes what matters into durable topic files, and keeps the top-level index worth reading at session start.

## Memory Architecture Assumed

A two-layer memory layout:

- **Daily logs** (`memory/YYYY-MM-DD*.md`) — raw session notes, read-only, never moved or deleted
- **L2 topic files** (`memory/<topic>.md`) — curated durable knowledge per subject (e.g. `memory/clash-verge.md`)
- **Index** (`MEMORY.md`) — high-level status with pointers down to L2

If you are starting fresh, create `MEMORY.md` and `memory/dream-log.md` before the first run. L2 files are created on demand.

`memory/dream-log.md` doubles as the only state this skill keeps: entries record a **`Consolidated through:`** date — the newest daily log already folded into memory. The next run scans back for the most recent entry carrying that field to know where to resume. There is no state file, no lock file, and nothing to migrate or repair.

## Quick Start

### Manual dream

Tell your agent:

> "Run a memory dream consolidation. Follow the protocol in `<SKILL_PATH>/references/dream-protocol.md`. Workspace root: `<YOUR_WORKSPACE_PATH>`."

Or just *"run a dream consolidation"* — if this skill is loaded, the agent will know what to do.

### Automated daily dream (cron)

```json
{
  "name": "daily-dream",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "<YOUR_TIMEZONE>" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "timeoutSeconds": 1800,
    "message": "Run a memory dream consolidation. Read <SKILL_PATH>/SKILL.md and <SKILL_PATH>/references/dream-protocol.md in full, then follow the protocol phases in order. Workspace root: <YOUR_WORKSPACE_PATH>. Do not modify cron jobs, agent config, the Gateway, any daily log, or memory/dreaming/**. End your final response with a one-line dream summary — the cron delivery mechanism will auto-announce it."
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL_TYPE>", "to": "<CHANNEL_ID>" }
}
```

Set `expr` and `tz` to when your human is asleep. `timeoutSeconds` and the batch cap are a pair — lower one without the other and a batch is admitted that cannot finish.

## Three-Phase Safety Model

| Phase | Writes | Purpose |
|-------|--------|---------|
| **Sense** | ❌ None | Select logs since the watermark, plan the work |
| **Consolidate** | ✅ L2 files only | Promote content into topic files |
| **Settle** | ✅ MEMORY.md + dream-log.md | Update index, write diary entry |

Phase 1 is always read-only. An error in Sense never corrupts files.

## Quality Gates

A read-only planning checkpoint runs before any write: **topic identity** (do not merge legacy and current projects on name similarity), **lifecycle** (closed work must not reappear as an active TODO), **secret propagation** (never promote credentials into curated memory; the credential list is exhaustive and the guard is not a privacy classifier), **backup** (existing L2 files and `MEMORY.md` are copied to `<WORKSPACE_ROOT>/.backup/memory-dreams/YYYYMMDD-HHMM/` with a `.bak` suffix first), and a **post-write audit** reporting size, structure, lifecycle separation, and credential patterns without gating the run. `references/dream-audit.sh` covers the common checks; it is not full DLP.

## Failure Philosophy

This protocol is written for an agent to follow, not for a program to enforce. It fails **soft**:

- Do the work you can do, then report what you skipped and why.
- Diagnostics inform the final summary. They never block consolidation.
- An oversized `MEMORY.md` is the reason to run, not a reason to abort.
- Limits are derived from the runtime, never hard-coded into the protocol.
- Never wait on an answer that cannot arrive. A scheduled run has nobody to ask, so out-of-bounds work is dropped and reported, not blocked on.

Exactly two conditions cancel writes: a **failed backup**, or a **write plan reaching outside the allowed paths** — and the second cancels only those targets, not the run.

The secret guard is the one hard block on content — and it blocks the offending value, not the run.

## Where this sits in OpenClaw's memory stack

This skill works on the Markdown layer only — `MEMORY.md` plus `memory/*.md`. It **never reads or writes `memory/dreaming/**` or `memory/.dreams/**`**, which belong to memory-core's own built-in Dreaming, and it skips `## Light Sleep` / `## REM Sleep` blocks found inside a daily log. The two systems are independent: run this one with built-in Dreaming on or off.

How they differ, which adjacent components (`memory-wiki`, alternate backends, database-first state, automatic memory flush) are deliberately untouched, and what the version note covers: `references/memory-stack.md`.

Tool names in the protocol (`exec`, `edit`) are OpenClaw's; on another harness use its equivalents.

## Key Rules

- **Never move or delete daily logs** — archiving breaks `memory_search` indexing
- **dream-log.md is Markdown** — append text directly, never write JSON
- **Never copy credentials into curated memory** — omit/redact and alert instead. The secret list is **exhaustive**: authentication material only. This guard is not a privacy classifier; anything outside the list follows the workspace's own conventions and never raises a secret alert
- **Keep lifecycle state sticky** — closed/archived/snowed lines stay non-active
- **Back up before rewriting** `MEMORY.md` and any existing L2 file
- **MEMORY.md budget is derived, never hard-coded** — headroom = `min(bootstrapMaxChars, bootstrapTotalMaxChars − other bootstrap files)`; target = **80%** of it (`SD_INDEX_TARGET_PCT`, a knob), the remaining 20% being growth slack. Count characters, not bytes. Crossing the target means sink detail into L2 — it never blocks and never justifies deleting facts
- **Curate on every run, not only when over budget** — being under the target is not an answer to "does this still belong at index level". A target consulted only when exceeded becomes a floor the index grows to meet
- **The index is not a list of topic files** — group entries by the question a reader is asking; the topic identity guard governs L2 files, not index structure. Closed and archived work keeps one line plus its L2 pointer
- **Place every entry in a named section** — appending to the end of the file lets whatever heading happens to be last redefine what the entry means
- **Batch limit**: 32 logs or 192 KiB of **daily-log bytes** per run, cut on date boundaries. Sized so one batch fits inside the task timeout; a single date that exceeds it on its own is still processed whole. When resuming after a gap it takes the oldest first so the watermark advances contiguously. A run also reads and rewrites the L2 files it promotes into and this does not count them — leave margin, and do not gate on it, since those files are only known once the logs are read. Record log bytes, L2 bytes and wall-clock every run
- **Check reachability both ways** — every rule here walks from an index entry down to its topic file, so a file no entry names leaves this protocol's view for good. Report unreachable topic files *that sessions recently modified*; never auto-promote them
- **On the watermark date, re-read only the files that changed** — `>=` exists to catch same-day appends, not to re-admit the whole date at full size every run. Compare mtimes against the heading of the newest entry carrying `Consolidated through:`, never a later backfill heading
- **Write L2 files one at a time, and read back what you claim to have written** — batching content through one command invocation loses whole batches to encoding failures, and a step reporting success is not evidence its file changed

## Full Protocol

See `references/dream-protocol.md` for the complete three-phase workflow, quality gates, dream-log format, and safety rules.

## Version Note

**5.0.3** names what the batch cap actually counts, gives a forgotten topic file one way back into view, and reports backup growth without touching it. No change to what a run produces.

**5.0.2** aligns the cron template's `timeoutSeconds` with the batch cap it has to finish inside, and defines what a run does when 5.0.1's selection rule returns nothing at all.

**5.0.1** stops a large watermark date from blocking every later date forever, and makes two silent write failures visible. The deadlock needed all three of `>=` selection, oldest-first resumption and the unsplittable date boundary — each correct alone. Only changed files on the watermark date are re-read now.

**5.0.0** makes the index a domain-level summary rather than a mirror of the L2 topic list, and curates on every run rather than only when the index is over budget.

Both halves change what this skill produces, so an existing workspace will see its `MEMORY.md` restructured on the first run after upgrading. That rewrite is backed up like any other (Phase 3.1), but it is not something the human asked for on that day — hence the major version. **Run it manually the first time, with someone watching**, then hand it back to the schedule; later runs only touch the increment.

Full release history, with the reasoning behind each change: `references/changelog.md`.
