# Journal handoff and scoring (optional integration)

Use this file only when the Trading Journal CLI (`trade`) is available. Without
it, use `idea-log.md` instead; the skill works fully without the journal.

The journal adds exact P&L for the trades the user takes, so ideas can be
scored against real execution, not only on paper. Always call the CLI with
`--json`; errors come back as `{"ok": false, "error": "..."}`.

## Idea id

`idea-YYYYMMDD-<slug>`, for example `idea-20261124-rsp-rotation`. The id goes
into the tags of every record that belongs to the idea, because tags are what
the journal reports on.

## 1. Every idea: a plan entry

Recorded at the end of synthesis, whether or not the user takes it.

```bash
trade --json journal add "$(cat <<'IDEA'
IDEA idea-20261124-rsp-rotation
Direction: bullish | Type: macro | Horizon: structural
Thesis: Mega-cap concentration is at an extreme; equal weight should outperform as earnings broaden.
Reference: RSP 182.40 @ 2026-11-24 15:30 UTC (source)
Entry zone: 178-184
Stop: 170 | Targets: T1 196, T2 205 | Time stop: 2027-05-24
Exit triggers: top-10 earnings revisions re-accelerate; breadth makes new lows
Events: 2026-12-10 FOMC
Variants: plain RSP | hedge: long RSP / short SPY
Confidence: 3
Sources: ...
JSON: {"id":"idea-20261124-rsp-rotation","ticker":"RSP","dir":"long","type":"macro","horizon":"structural","ref_price":182.40,"ref_ts":"2026-11-24T15:30:00Z","ccy":"USD","stop":170,"t1":196,"t2":205,"time_stop":"2027-05-24","confidence":3}
IDEA
)" --ticker RSP --kind plan --tags ai-idea,ai-bullish,ai-macro,structural,idea-20261124-rsp-rotation
```

Keep the field names exactly as above, and **always end the block with the
machine-readable `JSON:` line** shown last. The scorecard parses this line,
not the prose, so a differently worded field above cannot break scoring.

`dir` is `long` or `short`; dates are ISO; numbers are plain numbers. If a
value is unknown use `null`, and never invent a reference price. `ccy` is the
**quote currency of the instrument** (`USD`, `EUR`, `GBX`, `USDT`...), not the
user's base currency. Before writing, check: `time_stop` is after `ref_ts`;
for `long`, `stop` < `ref_price` < `t1`; for `short`, the reverse.

## 2. When the user takes the idea: the trade carries it

Only when the user says they placed the order, with their actual fill.

```bash
trade --json add RSP buy 5 181.90 --commission 0.22 --ccy USD --date 2026-11-25T14:32 \
  --sl 170 --tp1 196 --tp2 205 --confidence 3 \
  --strategy structural --setup equal-weight-rotation \
  --notes "idea-20261124-rsp-rotation: <thesis>. Exit if <triggers>. Time stop 2027-05-24." \
  --tags ai-idea,ai-bullish,ai-macro,structural,idea-20261124-rsp-rotation \
  --source ai-analyst --group idea-20261124-rsp-rotation
```

- `--ccy` is the instrument's quote currency (`ccy` in the `JSON:` line);
  without it the trade is booked in USD. Pass `--date` when the fill was not
  just now.
- `--sl` (alias `--stop`) is the stop; the journal uses it for R multiples and
  risk to stop. Never record an AI idea trade without it.
- A tag that is exactly `ai` or starts with `ai-` puts the trade in the AI
  bucket of `trade report` (`by_origin`), so AI vs. manual results appear
  without extra work (`airlines` stays manual). Do not put `ai-*` tags on the
  user's own ideas.
- `--group` is stored but not yet reported; the idea id must also be in tags.

## 3. Reviews, invalidations, expiry

```bash
# Thesis review (position-review.md)
trade --json journal add "REVIEW idea-20261124-rsp-rotation: thesis weakened because ..." --ticker RSP --kind review --tags ai-idea,idea-20261124-rsp-rotation
# Outcome (one of: target hit | stop hit | invalidated | expired), taken or not
trade --json journal add 'CLOSED idea-20261124-rsp-rotation: expired. Price at close: 188.10 @ 2027-05-24 20:00 UTC (source)
JSON: {"id":"idea-20261124-rsp-rotation","outcome":"expired","close":188.10,"close_ts":"2027-05-24T20:00:00Z"}' --ticker RSP --kind review --tags ai-idea,idea-20261124-rsp-rotation
# Lesson after a broken thesis
trade --json journal add "LESSON idea-20261124-rsp-rotation: ..." --ticker RSP --kind lesson --tags ai-idea,idea-20261124-rsp-rotation
```

Every idea ends with one `CLOSED` review entry, taken or not, so the
scorecard has an outcome for it.

## Scoring ("how did your ideas do?")

Two different questions, always reported **separately** and labelled, so a
claim never mixes them:

- **Idea quality** (paper): would the idea have worked as written?
- **Execution** (real): how did the trades actually taken from AI ideas do?
  This also reflects the user's fills, sizing and stop discipline, not only
  the idea.

### A. Idea quality: every idea counts

1. `trade --json journal list --tag ai-idea --limit 1000` (add `--kind plan`
   / `--kind review` and `--from`/`--to` to narrow it), keep entries tagged `ai-idea`,
   group by idea id, parse the `JSON:` line of each `IDEA` plan entry.
2. Assign every idea exactly one status. Nothing is dropped:
   - `closed`: has a `CLOSED` review entry → use its close price.
   - `expired`: no `CLOSED` entry and the time stop has passed → look up the
     price at the time stop with your own tools and write the missing
     `CLOSED ... expired` entry with that price, its time and source. Never
     use `trade price set` for a past price: it replaces the live mark of an
     open position. If no price can be found, count it as `expired, unscored`.
   - `open`: time stop not reached yet.
3. For scored ideas: paper R and hit rate as defined in `idea-log.md`
   (scoring step 3), with `ref`, `stop` and `close` next to each R.
4. Show the denominators: total ideas, scored, expired-unscored, open.
   Hit rate and median R are over scored ideas (closed, or expired with a
   price); expired-unscored and open ideas are shown next to them, never
   silently left out.
5. Break down by type tag (`ai-macro`, `ai-news`, `ai-technical`,
   `ai-event`), horizon (from the `JSON:` line) and confidence.

### B. Execution: trades taken from AI ideas

1. `trade --json report`, read `data.by_currency.<CCY>.by_origin` (ai vs
   manual) and `by_tag` (per idea id). Quote these numbers; never recompute P&L.
2. Always show the **take rate** (ideas taken / all ideas) next to it. Only
   ideas the user chose reach the trade report, so "AI trades win more" may
   just mean the user selects well. Say so when the take rate is low.
3. For taken ideas, compare the trade result with the idea's paper result:
   a gap points at execution (entry, size, early exit, ignored stop).

### C. Feed it back
Once a type tag has about 10 closed ideas and a negative median paper R, lower
confidence for that type in the next scan (bias checklist item 8). With fewer,
report it but change nothing.

## Planned improvement

A first-class `trade idea add/list/close` command (reference price, stop,
target, horizon, status open/taken/invalidated/expired, scored against
`trade price fetch`) would replace the text parsing in step 2. Until it
exists, plan and review journal entries are the contract.
