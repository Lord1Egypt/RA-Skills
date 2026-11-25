# Output template

## Report layout (full scan)

1. **Snapshot**: date/time, timezone, sources used, data freshness.
2. **Macro scan**: the dated list from `macro-checklist.md` (collapsed to the
   10 to 20 most relevant lines) and the 2-week calendar.
3. **Theses**: 2 to 4, each with claim, evidence, counter-evidence, horizon,
   kill condition.
4. **Bias check**: only the `bias-checklist.md` items that flagged something and
   what was done about each, or "no flags". Always show the "priced in?"
   answer for each thesis.
5. **Idea cards**: one per idea (below), core ideas first, hedges last.
6. **Portfolio fit**: overlap with open positions, correlation, concentration
   flags.
7. **What I would watch**: the 3 to 5 data points that would change the view,
   plus 0 to 2 loose threads: a dated scan fact that fits no thesis, with one
   concrete question asking for the user's view. None is better than a weak one.
8. **Logged**: where the ideas were recorded (idea log path, or the journal commands run), or "not saved" if the user declined.
9. **Disclaimer** (`disclaimer.md`).

## Idea card

```
### <idea-YYYYMMDD-slug>: <instrument> <direction>
Thesis:        <one sentence, link to thesis #>
Tags:          ai-idea, ai-<bullish|bearish|neutral>, ai-<macro|news|technical|event>, <strategy tags>, <idea id>
Reference:     <price> @ <time, tz> (<source>)
Entry zone:    <range or condition>
Stop:          <level>  (<why this level; % from reference>)
Targets:       T1 <level>, T2 <level>  (R multiple at T1: <x>)
Horizon:       <tactical | medium | structural>, time stop <date>
Exit triggers: <thesis-level events that end the idea regardless of price>
Events:        <dated binary events inside the horizon, user timezone>
Variants:      plain: ... | smaller/hedged: ... | leveraged (if any): size factor, max days, decay
Risks:         <top 3>; what would make this wrong
Event check:   "If the key decision-maker says the opposite tomorrow": <impact>
Confidence:    <1-5>, <one line why>
```

Rules for cards:
- Prices must carry a timestamp and a source. If you only have a stale price,
  say "stale" and do not compute R multiples from it.
- Percentages from the reference price, not from an imagined fill.
- No position sizes in currency unless the user has stated their own sizing
  rule; then show the rule applied (e.g. "your 30% cap × 0.5 event factor").
