# Stall Solver — Restroom Queue Math

**Will the halftime line be survivable? Code tables size restroom fixtures for steady-state; queues are born in bursts.**

A venue can be 100% plumbing-code compliant and still have a
25-minute women's-room line at intermission — because codes size for
sustained occupancy while events dump 40% of attendees into a
15-minute break window. Stall Solver runs both checks: Erlang-C
queueing math (utilization, expected wait, drain time) and fixture
audits against IPC-style code minimums.

## What it does

- **demand** — sustained profile: arrivals vs fixtures, utilization
  %, average wait, per fixture class (stalls/urinals)
- **event** — burst simulation for halftime/intermission: burst
  utilization, expected wait, total drain time, verdict per class
  (OK / TIGHT / FAIL)
- **audit** — fixture counts vs code-minimum ladder for the stated
  occupancy, with per-type SHORT/OK verdicts

## The problem in numbers

- Urinal: ~35 s occupancy → ~103 visits/hr/fixture
- Stall: ~95 s occupancy → ~38 visits/hr/fixture
- Equal populations ⇒ stalls need **~2.7x the fixtures** for equal
  waits — the arithmetic behind every "potty parity" law
- Burst utilization ≥ 100% means the queue **never clears** within
  the break window

## Quick start

```bash
python3 scripts/stall_detector.py event --venue sports \
    --attendees 400 --fixtures 6 --urinals 4 --burst-share 0.5
```

```
stall  :  6 fixtures | burst utilization 176% | avg wait OVERLOAD | drains in 26.4 min | FAIL
urinal :  4 fixtures | burst utilization  97% | avg wait 56.7 min | drains in 14.6 min | TIGHT

VERDICT: expect queues. Add fixtures or stagger the break.
```

```bash
python3 scripts/stall_detector.py audit --venue conference --occupancy 350 \
    --f-wc 8 --m-wc 3 --m-ur 2 --f-lav 6 --m-lav 4
```

```
female water closets  : 8 provided / 12 required  -> SHORT 4
...
VERDICT: BELOW code minimum by 10 fixtures total.
```

## Install

No dependencies. Python 3.8+.

## License

MIT © Denis Voronin
