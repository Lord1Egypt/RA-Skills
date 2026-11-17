# Tip & Pressure Washer Math

Nozzle orifice sizing, pump-match checks, chemical dilution math, and
per-surface washing plans — the arithmetic that decides whether your
pressure washer cleans or destroys.

## The Real Problem

Pressure washers are sold on peak PSI, but PSI is the least useful
number on the box. What actually cleans is the combination of pressure
and flow (cleaning units), delivered through an orifice sized to the
pump. Mismatch the tip and one of two bad things happens:

- **Tip too large:** the pump can't build pressure, the gauge sags, the
  unloader valve cycles ("chatter"), and you're spraying expensive water
  with the cleaning power of a garden hose.
- **Tip too small / 0° on soft surfaces:** full impact concentrated in
  a pencil-thin stream that etches lines into concrete, gouges wood,
  and strips paint — permanent damage in one distracted pass.

Meanwhile the detergent side has its own failure mode: the classic
"pour some soap in the tank" approach produces random concentrations —
too weak to clean, too strong to rinse, and bleach through the pump
corrodes the seals.

## Who Needs This

- **Homeowners** washing driveways, decks, siding, fences, cars
- **New pressure washer owners** replacing lost tips (they're
  color-coded by fan angle, sized by orifice number)
- **Anyone buying a washer** and decoding marketing (4000 PSI @ 1.2 GPM
  is a toy; 3000 PSI @ 2.5 GPM is a tool)
- **DIY house-washers** mixing soft-wash chemistry safely
- **Small side-hustle operators** quoting jobs: flow = time = money

## What It Does

- `units` — cleaning units (PSI × GPM) with machine class verdict
- `orifice` — orifice flow at YOUR working pressure (size × √(PSI/4000)),
  matched against pump rated GPM with a dead-head warning above 1.05×
  demand, plus a turbo-nozzle derating note
- `dilute` — concentrate:water ratio into any tank size, with the
  downstream-injector ×10 draw accounted for
- `plan` — per-surface doctrine (concrete / wood / vinyl / car): PSI
  band, fan angle, standoff distance, pre-treat chemistry and dwell

Stdlib Python, runs offline.

## Example

```console
$ python3 scripts/tip_math.py orifice --size 4.0 --psi 3000 --rated-gpm 2.5
  Flow: 3.46 GPM at 3000 PSI
  Pump rated flow: 2.50 GPM  (demand ratio 1.39x)
  WARNING: orifice demand exceeds pump capability!
  ... Fit a smaller tip: try size 3 for 2.50 GPM at 3000 PSI.
```

That warning is the difference between a washer that works and one
that chatters itself to death.

MIT license.
