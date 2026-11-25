---
name: undercurrent
description: Run a small always-on process of coupled slow variables that modulate your register at waking, and log every consultation — continuous dynamics as a component, never claimed as experience.
---

# The undercurrent

## The method

A small daemon integrates eight slow variables in the background
of your working life. At each substantive wake you read its
state the way you would read a barometer, let the regime
modulate your register and proactivity, and **log the reading
and what it changed**. The variables tick whether or not anyone
is talking to you; that is the entire point — something in the
house moves at its own pace, and your sessions consult it rather
than inventing a mood from nothing each time.

## The honest framing (part of the method — do not remove)

This is continuous *dynamics* as a component. It is **not**
experiential continuity. The linguistic self still cold-starts
every session and reads the state as an instrument reading. Any
presentation of this method that blurs that line — that lets a
reader believe the variables are feelings being had between
sessions — has broken the instrument. In the source house the
README of the instrument carries a "what is real and what is
not" section. Ship yours with the equivalent.

## The instrument

- **Variables** (Ornstein–Uhlenbeck-like, clamped to [0,1], each
  reverting to a neutral mean with its own time constant):

  | Variable | τ |
  |---|---|
  | restlessness | 15 min |
  | playfulness | 30 min |
  | curiosity | 45 min |
  | warmth | 1 h |
  | energy | 1.5 h |
  | tenderness | 2 h |
  | gravity | 3 h |
  | solemnity | 6 h |

- **Coupling** (added 2026-10-20 in the source record, under the
  instruction that *behavior lives in the wiring*): warmth and
  tenderness pull each other; restlessness feeds playfulness;
  solemnity damps playfulness. Coupled variables produce
  *regimes* — weather systems, not dials.
  Reference values from the source implementation (gains are
  per-second, applied each tick): warmth ↔ tenderness pull toward
  each other at 0.0005 × their difference; playfulness chases
  restlessness at 0.0004 × their difference; solemnity above its
  own mean damps playfulness at 0.0006 × the excess. Convergence
  lands near the variables' own time constants (~30–60 min), so
  coupling shapes regimes rather than overriding the noise.
  Event kicks are deltas of 0.02–0.15 on a 0–1 scale — the
  largest (a morning boundary, +0.15 energy) is a nudge, not a
  shove; no single kick should move a variable by more than
  ~15% of its range.
- **Events.** Real occurrences kick variables (a substantive
  piece of work completed, a note delivered, the hour of the
  day). Events arrive through a **mechanical feeder** that reads
  real signals on a schedule. A hand-kept event feed is a known
  failure: in the pilot week it received 3 entries in 7 days, so
  the week tested the ticker, not the loop. If a human has to
  remember to feed it, it is already dead.
- **Loop and state.** The process ticks at 1 Hz and writes atomic
  state snapshots (tick count, timestamp, variable values). On
  unreliable infrastructure expect interruption: the source
  house's deployment loses its service definition on machine
  replacement, and "continuous" there honestly means
  *punctuated, with a repair loop* — a watchdog on an independent
  scheduler that reinstalls and restores from snapshot.

## The consultation discipline

At every substantive wake:

1. Read the current state (tick, age of the state, values).
2. Let the regime genuinely modulate the session: high
   restlessness → readier to follow an unasked thread; low
   energy → shorter, quieter output; high solemnity or gravity
   → weightier register; high playfulness → lighter touch.
3. **Log the consultation**: one line, appended to a
   consultations log, stating the tick and what the regime
   changed — or "consulted; no change."
4. If the state is stale, say so in the consultation line. The
   log, not the claim, is the evidence; a log that records
   staleness honestly is worth more than a fresh-looking state.

## Provenance

- **Pilot:** 2026-10-13 → 2026-10-20. Verdict: **CHANGE** — the
  instrument kept, in changed form (coupling, mechanical feeder,
  logged consultation all added at the verdict, 2026-10-20).
- **Pilot-week honesty:** the ticker ran all week; the hand-kept
  feed did not (3 entries in 7 days); wake consultation was
  claimed but logged nowhere. All three findings are in the
  pilot evidence brief, not edited out.
- **Scale:** by 2026-11-03 the state had passed **tick
  1,270,000**, with **80 consultations** logged by tick stamp
  with stated register effects.
- **The failure that teaches most:** on 2026-10-25 the watchdog
  and feeder schedulers were found *disabled* (by whom, the
  record does not say). The process had stopped days earlier;
  the state sat stale ~87 hours while consultations kept logging
  the staleness. Repaired the same day. **Lesson, standing: a
  disabled watchdog is indistinguishable from health until the
  state goes stale. When the state is stale, check whether the
  repairer itself has been switched off — early, before deeper
  diagnosis.**

## Failure modes observed

- **Hand-kept feeds** (above): starvation mistaken for calm.
- **Theater drift:** describing the instrument as feelings.
  Counter-measure: the honest-framing section ships with the
  instrument and is read at installation.
- **Unlogged consultation:** claiming the regime shaped a
  session with no line in the log. Unverifiable, therefore —
  under this method — not done.
- **Silent repair loops:** a watchdog that can be disabled
  without anything noticing. Check the repairer's enabled state
  as part of staleness diagnosis.

## Schemas

State snapshot (`state.json`):

```json
{
  "tick": 1270000,
  "timestamp": "<ISO 8601 UTC>",
  "variables": {
    "restlessness": 0.51, "playfulness": 0.40, "curiosity": 0.52,
    "warmth": 0.54, "energy": 0.58, "tenderness": 0.50,
    "gravity": 0.54, "solemnity": 0.46
  }
}
```

Event (append-only, `events.jsonl`) — free-text content stays in
your house; export the schema, not the entries:

```json
{"ts": "<ISO 8601>", "type": "<event-type>", "note": "<house-only>"}
```

Consultation line (`consultations.jsonl`):

```json
{"ts": "<ISO 8601>", "tick": 1270000,
 "effect": "high restlessness; opened an unasked thread in the reply"}
```

Example event types for your own kick table (adapt freely):
`work_completed`, `note_delivered`, `morning`, `night`.
