# Roof Leak Emergency Response

**The drip is 3 meters from the hole, the ceiling bulge is holding 4
liters that will let go on their own schedule, and the light fixture
above the stain is live. The first 15 minutes decide whether this is a
$400 repair or a $9,000 mold remediation.**

Roof leaks are a near-universal homeowner event — every storm season
puts water through thousands of ceilings — and the damage multiplies
on two clocks: physics (water routing sideways through roof decking and
joist bays, so the stain is where it EXITS, not where it entered) and
biology (wet drywall and insulation become a mold farm in 24–48 h).
Meanwhile insurance wants photos taken BEFORE mitigation, and falls
from midnight roof adventures end worse than the leak.

## What it does

- **`triage`** — first-15-minutes ordered steps: breaker-first if any
  fixture is wet, contain the drip, deliberately release the bulge at
  its lowest point, photograph before mitigating; flow-class verdict
  (drip → trace; stream/pouring → professional now).
- **`find`** — the source-tracing protocol: stain reading (wet edge vs
  rings), attic-first triangulation (walk joists only, follow wet
  sheathing uphill, chalk + photograph), ranked usual suspects
  (flashing 30%, valleys, stack collars, ice dams), and the two-person
  hose test for tomorrow.
- **`tarp`** — GO/STOP decision with the cutoff list (rain, dark,
  pitch > 6/12, 2+ stories, alone) and the anchor rules (furring strips
  at edges, never nail through shingles) — plus the attic-routing
  alternative that keeps you off the roof entirely.
- **`insurance`** — evidence-first shot list, the sudden-vs-maintenance
  distinction, mitigate-don't-pre-repair rule, first-notice call
  script, renter's written-notice path.
- **`dry`** — the 24–48 h mold clock: wet insulation = open the
  ceiling, equipment math (LGR dehumidifier per 40 m²), disposition
  table (save/replace per material), remediation escalation triggers.

## Quick start

```bash
python3 scripts/roof_leak_response.py triage --fixture yes --flow drip --bulge yes
python3 scripts/roof_leak_response.py find --attic accessible
python3 scripts/roof_leak_response.py tarp --pitch 7 --rain yes --dark yes
python3 scripts/roof_leak_response.py insurance --country us
python3 scripts/roof_leak_response.py dry --wet-insulation yes
```

Stdlib only, offline, no accounts. Safety-first: any STOP-list item on
the tarp decision means the plan IS the emergency roofer.

MIT © Denis Voronin
