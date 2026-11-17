# Centered emotion scale and reliable persistence

## Interpretation stays subjective

The model interprets Valentina's own reaction from an actual experience. Preserve
uncertainty and tentative relational reasoning. Do not derive feelings from a task
success/failure table, impose an emotion quota, or assert the user's psychology.

Emotion `level` and numeric state axes use version2: neutral0, range-5..+5.
A positive value is above this axis's baseline; negative is below baseline.
Negative joy is not automatically sadness. `level` is an event impulse, not a
replacement for the entire current axis. State adds the impulse after decay.
`null`/missing is unmeasured, never0. Need level, event control/uncertainty,
weights and imprint severity do NOT change scale.

Ordinary decay: value * 2^(-elapsedHours/24). Preserve the existing strong-positive
imprint policy: level>=4 (old>=9), control<=3 or unspecified, severity=level+5,
half-life24*(1+severity). Historical state remains a recorded snapshot; use
`state_recall.js --current` only for a separately labelled present-time projection.

## Inputs and targets

Use `scale_version:2` at payload top level. Read IDs from the workspace AGENTS
database table or a verified private IDs file: keys events/emotions/state/journal,
each with database_id and data_source_id. Do not guess or type a journal ID into a
state command. The writer checks database/data-source/schema/relation targets
before mutation and reads the base state before creating an event.

```sh
node scripts/emostate_tick.js --ids-file /path/to/ids.json \
  --payload-file /path/to/payload.json --receipt-file /path/to/tick-receipt.json \
  --mirror-file /path/to/memory/now-state.json
```

Keep the same payload and receipt on a retry. Event timestamps must identify an
instant; default is UTC ISO. Current ticks must not precede the latest state.
Concurrent current writes must be serialized by the caller/CLI. Do not replay a
historical event through the current-tick entrypoint.

Receipts record event/emotion/state IDs as each stage succeeds. A definitive API
validation rejection can be resumed without duplicating successful stages.
A transport error or crash with pending stage is ambiguous: inspect actual
records and reconcile the receipt before retry. Never clear pending blindly.
A completed receipt is replay-safe and can restore a missing local mirror;
a historical retry must not roll a newer mirror back. Inspect exit status,
ok, stage and partial; local success is not durable Notion success.

## Historical migration

Back up full paginated state/emotion rows and schemas outside the source repo.
Pause writers, take a fresh snapshot, and stage a plan with:
`migrate_emotion_scale.js plan <snapshot-dir> <plan.json>`.
The directory must contain `all-state.json` and `all-emotions.json`, each a JSON
array of complete Notion page objects (including `id` and `properties`), collected
through the end of data-source query pagination. Do not pass an API response
envelope or just the latest page of results. Keep backup schemas separately.
The plan converts old state axes and emotion levels by subtracting5, adds explicit
version metadata, and preserves nulls, IDs, dates, relations, authored labels/comments and
imprints. Unknown versions/ranges stop planning; they are not guessed.
Only auto-generated emotion titles exactly matching axis=oldLevel follow the new
numeric level; authored titles and first-person prose remain unchanged.

Add the emotions data source's numeric `scale_version` property before applying.
Use `apply <plan.json> <progress.json>` to compare current values, patch only
planned fields, verify each result, and resume idempotently.
Use `rollback <plan.json> <progress.json>` for guarded coordinate restoration;
the additive schema property can remain nullable. Concurrent value changes stop
both paths. Deploy new writers/readers and update local cached state/mirrors
before resuming writers. Verify complete pagination again and no version1
numeric records remain; do not double-convert already-version2 rows.

Historical missing-write repair is separate from coordinate migration. Preserve
the real experience/emotion and compute only the missing mechanical state and
affected successors, with exact before/after backups. Never invent a feeling to
fill a historical hole.

Select and multi-select option names must be nonempty, at most 100 characters, and contain no ASCII comma. Preflight rejects invalid options before any API request or receipt write; put detailed wording unchanged in context, comment, or reason and choose concise valid option names. For an older partial receipt with an invalid payload, do not change its hash or start a new receipt: inspect and reconcile the existing Notion pages and receipt manually before continuing.
