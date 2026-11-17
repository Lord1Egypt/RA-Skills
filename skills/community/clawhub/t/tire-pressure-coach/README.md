# tire-pressure-coach

Cold/hot tire-pressure physics, placard-vs-sidewall myth-busting, tread-depth
safety verdicts (wet-grip aware, not just legal minimum), TPMS decode, and a
monthly check log that catches slow leaks weeks before the warning light.

## The real-world problem

Tires are the only thing between the car and the road, and almost everyone
sets pressure wrong: they target the sidewall max instead of the door
placard, check tires warm at a gas station (systematically underfilling),
miss the −2 psi autumn drop that triggers TPMS lights fleet-wide every
October, and ride tires down to the 1.6 mm legal minimum even though wet
braking degrades steeply below 4 mm. The physics is simple (≈1 psi per
10°F), the protocol is five minutes a month — this skill runs both.

## Quick start

```bash
cd scripts
python3 tire_coach.py placard --vehicle "Mazda3" --front 33 --rear 33 --spare 60
python3 tire_coach.py check --vehicle "Mazda3" --lf 30.5 --rf 30.7 --lr 32.0 --rr 32.2 --temp-c 8
python3 tire_coach.py check --vehicle "Mazda3" --hot --lf 34 --rf 34 --lr 35 --rr 35
python3 tire_coach.py tread --vehicle "Mazda3" --lf 5 --rf 4.9 --lr 3.2 --rr 3.1
python3 tire_coach.py schedule --vehicle "Mazda3"
python3 tire_coach.py log --vehicle "Mazda3"
```

Python 3.9+, stdlib only. Store: `tire_coach.json` next to the script.

## What it computes

- **Cold target** — placard value (door jamb, never the sidewall max),
  optionally corrected for ambient temperature (ideal-gas math on absolute
  pressure) and altitude.
- **Hot fill-to** — when you must fill warm tires, the exact number to fill
  to so the morning-cold reading lands on placard.
- **Per-tire verdicts** — OK / ADD n psi / BLEED n psi with fill-to numbers;
  side-to-side axle gaps > 2 psi flag leaks or alignment.
- **Tread verdicts** — four bands: OK / caution at the 4 mm wet-grip cliff /
  urgent / below legal — with the winter-tire 4–5 mm practical minimum.
- **Leak radar** — the check log computes per-tire psi-loss per month; a
  tire losing >1 psi/month while its axle-mate holds is a slow leak, found
  before the TPMS light (which only fires at 25% below placard).

## License

MIT © Denis Voronin
