# Toddler Meltdown Decoder

It's 17:40. Your 2-year-old is on the kitchen floor, screaming
about a banana — no wait, the banana is now wrong BECAUSE it's
peeled. Nothing you say lands. You're guessing: hungry? tired?
Is this normal? Should I be doing something different?

## The Problem

- Toddler meltdowns (1-4 yrs) are near-universal — most healthy
  toddlers have them — yet every single one feels like an
  emergency and a parenting verdict.
- The effective response differs BY TRIGGER CLASS: the right
  move for hunger (feed, now) is the wrong move for
  overstimulation (fewer inputs, no choices). Parents apply one
  protocol to seven different problems.
- Mid-meltdown, nobody thinks clearly. What's needed is a
  10-second triage card, not a parenting book.
- The real win is upstream: most families have a pattern (the
  17:30 hungry-tired spike) that a simple log exposes in a week
  — and a snack at 17:00 fixes more than any de-escalation.

## What This Skill Does

- **triage** — you enter what you OBSERVE (eye-rub, ear-grab,
  "me do it", 17:40, post-playdate). It scores 7 trigger classes
  with cue weights + time-of-day priors, prints the top class
  (and the stacked second), each with a NOW / NEVER / PREVENT
  script.
- **log / stats** — episodes (full and averted) go into a local
  JSON; stats prints hour-of-day hotspots, class frequency, and
  which interventions actually averted meltdowns.
- **red flags** — self-injury, breath-holding with fainting,
  total inconsolability, joint-attention/language red flags are
  surfaced as "pediatrician conversation," explicitly framed as
  not-a-parenting-failure.
- **parent check** — every triage prints the one-liner the
  parent needs more than the child's diagnosis: your calm is the
  intervention; tag out if you're maxed.

## Example

```
$ python3 scripts/meltdown_triage.py triage \
    --cues "rubbing-eyes,clumsy,17:40,melts-at-minor" --age 2
1. TIRED   score 6  (60% share)
NOW: zero demands. 'We're going home.' Carry, don't walk-and-argue...
NEVER: 'one more thing'; fight the nap with activity.
PARENT CHECK: ... your calm IS the intervention.

$ python3 scripts/meltdown_triage.py log --cues "..." --class tired \
    --duration 12 --intervention "bedtime -20min" --averted
$ python3 scripts/meltdown_triage.py stats   # hour hotspots, what works
```

## Who Needs This

Any parent, grandparent, or caregiver of a 1-4 year old —
meltdown frequency peaks around age 2 precisely when the child
has no language to explain. Also excellent for the
second-child-is-completely-different parent: same classes,
different cue weights, re-log from zero.

Not medical advice; red-flag output routes to professionals,
never replaces them.

MIT License. Data stays local (`scripts/data/meltdowns.json`).
