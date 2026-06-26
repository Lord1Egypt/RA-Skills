# Runtime Lifecycle

## 1. Initialization

A new installation creates:

- `todo/NOW.md`
- `todo/history/YYYY-MM.md`
- `todo/system/config.json`
- `todo/system/sync-state.json`
- `todo/system/rollover-state.json`
- today's empty `reports/<agent>-ai-log-YYYY-MM-DD.jsonl` files for enabled agents

Initialization is performed by:

- `scripts/init_system.js`

Initialization also attempts to install or refresh managed AI logging rules in configured agent `AGENTS.md` files.

## 2. Daytime operation

### Human side
The human or coordinator edits:

- `FOCUS`
- `TODAY`
- `UP NEXT`
- `DONE`

### AI side
Execution agents append one JSON line per completed work unit containing:

- timestamp
- agent name
- one-line task description
- optional token metadata

### Sync
Coordinator heartbeat runs `sync_ai_done.js`.
The script:

- reads config
- reads today's logs
- queries OpenClaw usage summary
- rebuilds `AI USAGE THIS WEEK`
- rebuilds `AI DONE TODAY`
- updates `sync-state.json`

## 3. Nightly flow

Recommended order:

1. 00:05 generate the previous-day report while `NOW.md` still reflects yesterday's end-of-day snapshot
2. 00:15 run `rollover_now.js`

The rollover script:

- collects explicit completed items from active sections
- archives human done items into the month file
- archives the full `AI DONE TODAY` snapshot into the month file
- places each archived day under the clipped week section for that month
- updates that week section's `AI Usage Weekly Summary`
- clears `DONE`
- resets `AI DONE TODAY`
- rebuilds weekly usage for the new current week
- moves unfinished `FOCUS` + `TODAY` into the new day's `TODAY`
- keeps unfinished `UP NEXT`
- clears `FOCUS`
- writes `rollover-state.json`

## 4. Recovery paths

If heartbeat misses a cycle:

- the next sync rebuilds live AI sections from logs and usage data

If cron misses rollover:

- the next manual or automated rollover should archive the previous day before continuing

If one log line is malformed:

- sync skips the malformed line and continues

If runtime files are missing:

- run `scripts/repair_system.js`
- if installation is incomplete, run `scripts/init_system.js`

## 5. Long-term operation

Over time:

- `history/YYYY-MM.md` grows monthly
- daily AI logs accumulate by date
- sync state and rollover state remain small and replaceable
- current visibility stays concentrated in `NOW.md`
- historical usage and AI daily snapshots remain inside month files
