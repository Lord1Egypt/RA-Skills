# Memory Template — Water

All files live in `~/Clawic/data/water/`. Create each on first write, not preemptively.

## log.md

```markdown
# Water Log

## 2026-07-23
- 08:10 · 300 ml · mug, coffee
- 10:45 · 500 ml · my bottle — partial, est
- 13:05 · 250 ml · glass with lunch
total: 1050 ml · target: 2100 ml
```

- One `##` heading per local date (day-boundary rules in logging.md); one line per entry: time · ml · source, with `est` appended when estimated.
- The `total / target` line is appended at day close or when a summary is requested — not maintained live.
- Retro entries go under the date they belong to, flagged `est`. Alcohol logs as `0 ml` with the drink named (Rule 2).

## memory.md

```markdown
# Water Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Containers
- my bottle: 750 ml
- kitchen glass: 350 ml

## Baseline
- weight: 70 kg (2026-07-01)
- sweat rate: 1.3 L/h — running, summer (2026-07-10)
- conditions: none declared

## Patterns
<!-- observed and dated, e.g. "no intake before noon on weekends (seen 3x)" -->
```

- Containers: calibrated sizes, one line each — the never-ask-twice contract (logging.md).
- Baseline: weight with date, sweat rates per sport and season (exercise.md), declared conditions and clinician numbers (conditions.md).
- Patterns: only observations that recur; habits.md defines what counts.

## config.yaml

```yaml
units: metric
weight_kg: 70
reporting: silent
climate: temperate
# daily_target_ml: 2500   # only when user- or clinician-set; overrides Rule 1
```

- Keys, types, and defaults: the Configuration table in SKILL.md. An absent key means the default.
- config = what the user declared; memory = what the agent observed. An observation never overwrites a declared preference without confirmation.

## Status Values

| Value | Meaning |
|---|---|
| `ongoing` | Still learning containers, baseline, and routine |
| `complete` | Containers calibrated, baseline set, patterns stable |
