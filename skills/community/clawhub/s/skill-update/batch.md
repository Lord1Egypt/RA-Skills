# Batch Updates — Many Skills at Once

"Update everything" is one sentence of consent covering many behavior changes. The job is to keep the batch honest: cheap updates flow, risky ones get singled out.

## Triage First

```bash
npx clawic list    # installed + versions; compare against published
```

Split every pending update into three buckets before touching anything:

| Bucket | Contents | Handling |
|---|---|---|
| Flow | Patches and minors, clean diffs, no local edits | Batch together: one combined preview, one approval |
| Single out | Majors, breaking signals, migrations, local edits detected | Each gets its own preview and its own yes — pulled OUT of the batch |
| Skip | `pinned_skills`, skills mid-use in active work | Named in the report as skipped, with the reason |

`update --all` is only safe when the "single out" bucket is empty. Otherwise: update the flow bucket per-skill (or `--all` after the risky ones are excluded by handling them first), then walk the singled-out ones one by one.

## The Combined Preview

One message, three parts, in this order:

1. **Singled out** (needs individual decisions): slug, delta, one line on why it left the batch.
2. **Flowing** (one yes covers these): slug + delta + one-line summary each. A skill whose one-line summary can't honestly say "no behavior change that touches you" belongs in the singled-out list.
3. **Skipped**: slug + reason (pinned, in use).

Backups still happen per skill — one timestamped folder each (SKILL.md, Backup & Update Log), one update-log line each. Batch consent never batches the backups away.

## Order Within the Batch

- Related sets move together: skills that reference each other (`Related Skills`, shared data conventions) update in the same batch or not at all — half-updated pairs are where cross-skill references break.
- A skill whose update changes its data format goes LAST in its set: migrate once, after everything reading that data is current.
- Otherwise order doesn't matter; don't invent ceremony.

## Mid-Batch Failure

One skill fails at position k of n:

1. Stop the batch — do not "finish the rest and come back".
2. Report the split: 1..k-1 applied, k failed (with the error), k+1..n untouched.
3. Offer rollback for the failed skill only; the already-applied ones stay unless the user says otherwise.
4. Resume the remainder only on a fresh go-ahead — the failure may have changed the user's appetite.

## Verify After a Batch

One real task per singled-out skill; for the flow bucket, one task on the skill the user uses most is the honest floor — say which skills were verified and which weren't, instead of implying all were.

## Batch Report

Close with a table the update log mirrors: slug · old→new · applied/failed/skipped · backup path. The user should be able to reconstruct the whole batch from this one table a week later.
