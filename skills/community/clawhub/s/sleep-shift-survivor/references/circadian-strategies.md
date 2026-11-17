# Shift-Work Circadian Science — Reference

## The core problem

The human circadian clock runs slightly longer than 24h and adapts by
phase **delay** much more easily than phase **advance** (~1.5h/day delay
capacity vs ~1h/day advance, and advance costs more subjective strain).
Night work demands the clock point the wrong way; the body's sleep
pressure system (adenosine) follows time-awake, while the circadian alerting
signal follows the clock — when they disagree, you get a night worker
sleepy at 03:00 (no alerting signal) and awake at 09:00 (alerting signal
rising into their intended sleep).

Two consequences drive everything:

1. **Full adaptation to nights is possible but fragile** — it requires
   consistent night-oriented living including days off, which most people
   won't do (and socially shouldn't have to).
2. **For rotating schedules, partial strategies win** — anchor sleep keeps
   one stable circadian signal while naps handle the rest.

## Anchor sleep

A fixed sleep window (commonly 4 hours, e.g. 04:00–08:00) maintained
across ALL shift blocks. Research on rotating hospital schedules shows
anchor sleep reduces circadian disruption versus unstructured sleep, at
the cost of never fully adapting to any block. Rule of thumb:

- **Fast rotation** (block ≤ 3 days): anchor sleep + per-block main/nap
  windows. Do NOT try to adapt.
- **Slow rotation** (block ≥ 1 week): adapt per block (delay forward);
  anchor matters less.

## Naps

- **20 minutes** before slow-wave sleep kicks in — refreshment without
  grogginess (set alarm +15; the last 5 are falling asleep).
- **90 minutes** — one full cycle, waking near light sleep again.
- **30–60 minutes** is the worst zone: slow-wave wake = sleep inertia.
- A prophylactic nap **before** the first night shift measurably improves
  02:00–04:00 alertness.

## Light

Light is the primary circadian zeitgeber (time-giver):

- **During night shifts**: bright light in the first half helps delay the
  clock toward night orientation; avoid in the last ~2h (it hits the
  morning phase-response region and does the wrong thing).
- **Morning commute home after nights**: this light ADVANCES the clock
  (day direction) — the opposite of adaptation. Dark sunglasses on the
  commute are a classic countermeasure.
- **Day sleep**: blackout curtains + cool room; the alerting signal peaks
  in the evening and troughs pre-dawn — day sleep competes with a rising
  core temperature curve and needs all the help it can get.

## Caffeine

Half-life ~5-6h (individual variation 3-7h; slower in some metabolizer
types). The planning rule: cutoff = intended sleep time − 6h minimum. For
a night shift ending 07:00 with sleep attempted at 08:30, cutoff is
~02:00. Timing caffeine EARLY in the shift (23:00) is the classic
self-sabotage: ~50% still active at 05:00, wrecking the only sleep window
available. Strategic dosing: 100-200mg at shift start and mid-point, none
after cutoff.

## Transitions between blocks

- **Forward (day → evening → night)**: delay sleep 1.5-2h/day. Two to
  three transition days between blocks is the humane minimum.
- **Backward (nights → days)**: don't advance slowly — either keep
  delaying around the clock (needs a long break) or do one hard reset:
  stay awake through the day with light activity + evening melatonin-
  timing question for a doctor, sleep a normal night. The plan inserts
  the reset when the off-block is ≥ 48h.
- **Long breaks (≥ 1 week off)**: reset to normal nights immediately; do
  not preserve night orientation "to be ready" — recovery is the point.

## Drowsy driving

Post-night-shift morning drives are a documented high-risk window —
sleepiness impairment after a full night shift without sleep parallels
legally-intoxicated performance in lane-keeping studies. Countermeasure
stack (what `commute` prints):

1. Sleep < 4h in the last 24h or any microsleep episode → **do not
   drive**: nap 20 min in the car first, take transit, or get a ride.
2. Otherwise: 20-min nap + coffee before departure (caffeine needs
   ~20-30 min to engage).
3. Conversation passenger, cool cabin, no highway hypnosis music.
4. Any drowsiness signs → pull over immediately; microsleeps are not
   survivable by willpower.

## Shift-work disorder screening (informational)

Flag criteria used by `screen` (simplified, not diagnostic):
- insomnia and/or excessive sleepiness for ≥ 3 months, tied to the shift
  schedule, with ≥ 7h sleep opportunity still producing symptoms.

Persistent flags → occupational health or sleep medicine. SWD is treatable
(bright-light therapy, timed melatonin, schedule redesign are the standard
tools) — but only if someone looks.

## On-call specifics

Fragmented sleep is the on-call reality: anchor window as the spine,
pre-call nap if warned, post-call recovery nap capped at 90 min to protect
the next anchor night, caffeine cutoff computed on the *anchor* sleep, not
the interruptions.
