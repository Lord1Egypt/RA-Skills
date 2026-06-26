# Recovery Playbook

## Missing files

If any of these are missing:

- `todo/NOW.md`
- `todo/system/config.json`
- `todo/system/sync-state.json`
- `todo/system/rollover-state.json`

Run:

```bash
node scripts/init_system.js
node scripts/repair_system.js
```

## Sync problems

Symptoms:

- `AI DONE TODAY` not updating
- `AI USAGE THIS WEEK` looks stale
- today's AI work exists but the live dashboard does not reflect it

Actions:

1. Confirm today's `*-ai-log-YYYY-MM-DD.jsonl` files exist
2. Check malformed JSON lines
3. Run `node scripts/sync_ai_done.js`
4. Inspect `sync-state.json`
5. If usage still looks wrong, inspect `openclaw gateway usage-cost --days 14 --json`

## Rollover problems

Symptoms:

- yesterday's DONE not archived
- `FOCUS/TODAY` not carried forward correctly
- monthly usage summaries not updated

Actions:

1. Confirm `rollover-state.json`
2. Run `node scripts/rollover_now.js`
3. Then run `node scripts/sync_ai_done.js`
4. Inspect the relevant `history/YYYY-MM.md` file

## Safety note

`sync_ai_done.js` is safe to rerun.
`rollover_now.js` relies on `rollover-state.json` for idempotency and should not archive the same day twice.
