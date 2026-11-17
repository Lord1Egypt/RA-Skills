# 6. Updating an existing report (for example, an earnings-season update)

> This is the update step of the pipeline in `SKILL.md`. It follows `05-publish.md` for any report that already exists.

A new edition is a new report: a new `<report-id>` with a date, in the **same series key**. The older report stays
available as a historical version. Add a line at the head of the older report pointing to the updated edition. Before you
start, ask the question from `01-kickoff.md`: does this period contain anything new to write? If it does not, the right
output is a kickoff brief that says "do not update", with the restart triggers.

**Two things are mandatory:**

## (1) Settle the prior version (`judgment.md` section 7)

The update must contain a chapter called "Settlement of the prior version". List every conclusion of the prior edition, then
what was observed, then the verdict (hit, miss, pending, too early), then what this edition corrected.

**Settle the ledger at the same time**, because the scoreboard is built from it:

```bash
python3 scripts/ledger.py list                       # see what is open for this series
python3 scripts/ledger.py settle ID hit|miss|too_early \
  --evidence 'What was observed, with source' --lesson 'One sentence the next report can act on'
```

`--lesson` is mandatory. It is appended to `research/lessons.md`. Day-to-day settlement does not wait for an update: when the
desk watch finds a falsifier that fired or a call that came due, settle it that day (`references/desk.md` section 2).

A published scoreboard is a performance claim. **Show all calls** and never a selection. State the period covered and the
method of judging, and attach "past performance does not predict future results".

**A falsifiable commitment that is never settled is no commitment at all.** This is the costliest gap in a subscription
research product. It is also the one asset that turns an independent publisher's claims into a track record.

## (2) Two update forms

Every update is a standing commitment to readers of the series. If each update were a full report, the cost would grow
without limit. Hence two forms:

| Form | Trigger | Content | Length |
|---|---|---|---|
| **Delta update** | An earnings season or a single major event; an update candidate recorded by the desk (re-running the model moves revenue or EPS over the next four quarters by 5% or more, or a transition condition fires; `references/desk.md` section 3) | Settlement of the prior version; changed items (which assumptions moved, whether the target price and rating change); the updated tracking table and catalysts | 10-20 pages |
| **Full redo** | Annually, or when the thesis has been falsified or the structure has changed | The full nine-step process and all eight components | Same scale as the first edition |

Both forms keep the same series key. Both go through `references/pipeline/05-publish.md` again: run the final checks,
register the new edition's calls in the ledger, and update the series entry in `research/watch.json`. Open calls from the
prior edition remain in the ledger until they are settled.
