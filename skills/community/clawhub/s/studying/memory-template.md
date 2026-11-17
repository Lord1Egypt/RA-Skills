# Memory Template — Studying

Create `~/Clawic/data/studying/memory.md` with this structure:

```markdown
# Studying Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Techniques
<!-- what worked / failed, with evidence level: observed (1 signal) or confirmed (2+) -->
<!-- e.g. confirmed: mind-maps help in conceptual courses (worked in bio and psych) -->
<!-- e.g. observed: group comparison rounds helped once in stats -->

## Schedule
<!-- proven block length (the logged degradation point), best time of day, days/week that actually hold -->

## Materials
<!-- format preferences: videos before reading, worked examples, past papers critical -->

## Session Log
<!-- one line per session: date · course/topic · minutes · hit rate (correct/attempted) -->

## Exams
<!-- post-mortems: what the exam tested vs predicted, format surprises, which prep hours paid -->

## Never
<!-- approaches that failed twice: no all-nighters, no group study, no music during reading -->

---
*Updated: YYYY-MM-DD*
```

## Rules

- `observed` → `confirmed` after 2+ consistent signals; confirmed entries override the skill's defaults except Core Rules 1, 2, and 6 (non-negotiable floors).
- An observation never overwrites a declared preference in `config.yaml` without the student's confirmation — config is what they said, memory is what you saw.
- The Session Log is the data source for `block_length` calibration (Session Protocol 5), the 60%/90% hit-rate adjustments (Session Protocol 4), and time-of-day placement (`scheduling.md`).
- The Exams section feeds every next countdown (`exam-countdown.md` post-mortem) and cert planning estimates (`certifications.md`).

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning this student |
| `complete` | Preferences well-established; keep logging sessions and exams |
