# Idea log (standalone mode)

Used when the Trading Journal CLI is not available. A plain markdown file the
user owns: `trading-ideas.md` in the working folder by default, or
`[storage].ideas_file` in `sources.toml`.

- Ask before creating the file the first time ("Save these ideas to
  `trading-ideas.md` so we can score them later?"). Remember the answer for
  the session. If the user declines, keep the cards in chat only.
- Only append. Never rewrite or delete earlier entries; corrections are new
  entries.

## Entry format

One section per event. Every `IDEA` ends with the same `JSON:` line as the
journal handoff, so the log can be re-recorded in the journal later.

```markdown
## IDEA idea-20261124-rsp-rotation (2026-11-24)
<the idea card from output-template.md>
Tags: ai-idea, ai-bullish, ai-macro, structural
JSON: {"id":"idea-20261124-rsp-rotation","ticker":"RSP","dir":"long","type":"macro","horizon":"structural","ref_price":182.40,"ref_ts":"2026-11-24T15:30:00Z","ccy":"USD","stop":170,"t1":196,"t2":205,"time_stop":"2027-05-24","confidence":3}

## TAKEN idea-20261124-rsp-rotation (2026-11-25)
User reports: bought at 181.90 (their fill, as told). Stop 170.

## REVIEW idea-20261124-rsp-rotation (2027-01-10)
Thesis weakened because ...

## CLOSED idea-20261124-rsp-rotation (2027-05-24)
Outcome: expired   (one of: target hit | stop hit | invalidated | expired)
Close: 188.10 @ 2027-05-24T20:00:00Z (source)
JSON: {"id":"idea-20261124-rsp-rotation","outcome":"expired","close":188.10,"close_ts":"2027-05-24T20:00:00Z"}

## LESSON idea-20261124-rsp-rotation (2027-05-24)
...
```

Field rules are the same as in `journal-handoff.md`: `dir` is `long` or
`short`, `ccy` is the instrument's quote currency, `time_stop` is after
`ref_ts`, and for a long `stop` < `ref_price` < `t1` (reverse for a short).
Parse dates from the entry and its `JSON:` line, not from the file's
modification time.

## Scoring ("how did your ideas do?")

Same principles as the journal scorecard; nothing is dropped.

1. Read the log and group entries by idea id.
2. Give every idea one status: `closed` (has `CLOSED`), `expired` (time stop
   passed, no `CLOSED`: look up the price at the time stop, append the missing
   `CLOSED ... expired` entry; if no price can be found, count it as
   `expired, unscored`), or `open`.
3. **Idea quality (paper):** paper R = move in the idea's direction from
   `ref_price` to the close ÷ |`ref_price` − `stop`|, or −1 if the stop is
   known to have been hit first; show `ref`, `stop` and `close` next to each R.
   Hit rate = share of scored ideas (closed, or expired with a price) with
   positive paper R. Report the median R
   next to it: an idea type can win rarely and still pay. Show
   denominators: total, scored, expired-unscored, open. Break down by type
   tag, horizon (from the `JSON:` line) and confidence.
4. **Execution:** the log only knows what the user reported in `TAKEN`
   entries. Show the take rate (taken / all ideas). Do not compute the user's
   P&L; quote it only if they give it. For exact P&L per idea, the Trading
   Journal skill records the trades themselves.
5. Feed back: once a type tag has about 10 closed ideas and a negative median
   paper R, lower confidence for that type next time (bias checklist item 8).
   With fewer, report it but change nothing.
