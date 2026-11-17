# Sleep Shift Survivor — Circadian Planner for Shift Workers

**~20% of the workforce does shift work. The advice they get: "sleep more."**

Nurses, drivers, factory, security, IT on-call, hospitality — their bodies
have no idea when to sleep because the schedule keeps moving. Circadian
science actually has usable answers; this tool operationalizes them:

- **Anchor sleep** — a fixed window (default 04:00–08:00) present in every
  shift block; the one stable signal the circadian clock gets while naps
  flex around it. Fast rotations (≤3-day night blocks) should NOT fully
  adapt — anchor + naps beats zig-zagging
- **Forward rotation only** — phase delay is physiologically easier than
  advance; plans delay 1.5–2h/day forward, never ask you to sleep earlier
- **Strategic caffeine** — ~5-6h half-life means a 23:00 coffee is still
  ~50% active at 05:00. Cutoffs computed per shift end + sleep attempt;
  the plan prints the time out loud every day
- **Light choreography** — bright light first half of night shifts; dark
  sunglasses on the morning commute home (morning light snaps the clock
  back to day mode — the exact opposite of what you need); blackout for
  day sleep
- **Nap science** — 20 min or 90 min (never 30–60: slow-wave grogginess);
  prophylactic 90-min nap before the first night shift
- **Drowsy-drive defense** — the post-night-shift morning commute is a
  documented high-risk window; `commute` prints the countermeasure card
  with the do-not-drive threshold (sleep < 4h or any microsleep → nap
  first or don't drive)
- **Screening flags** — ≥30% of nights under 6h or quality ≤2/5 raises
  shift-work-disorder flags (informational; occupational health diagnoses)

## Quick start

```bash
python3 scripts/shift_sleep.py schedule add "hospital" --pattern 2D,2E,2N,4off \
    --day 07:00-15:00 --evening 15:00-23:00 --night 23:00-07:00
python3 scripts/shift_sleep.py plan hospital --from 2026-10-01 --days 14
python3 scripts/shift_sleep.py commute --night-ends 07:00
python3 scripts/shift_sleep.py log hospital --slept "08:30-13:30" --quality 2
python3 scripts/shift_sleep.py screen hospital
```

Informational planning, not medical advice — persistent symptoms belong
with occupational health or sleep medicine.

MIT © 2026 Denis Voronin
