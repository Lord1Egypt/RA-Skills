# Snow Shoveling Strategist

**25 cm of wet snow on a 2-car driveway is 4.7 tonnes — 2,700 shovel
loads. That's not a chore, that's a workload your heart should see
planned.**

Every storm, emergency rooms fill with two predictable groups: cardiac
events from cold-air + static-grip shoveling (middle-aged, mostly men,
mostly untrained for the load), and backs destroyed by full-depth lifts
of wet snow. Both are preventable with arithmetic: know the tonnage,
pick the tool, layer the depth, cycle the effort, and place the snow so
it moves exactly once.

## What it does

- **`plan`** — area × depth × density → total tonnes and shovel-load
  count; tool verdict per depth/condition; layered-clearing pass count;
  storm timing (clear twice vs once); placement plan (stack line,
  downwind, no re-handling); order of operations (exit path → surface →
  car → plow ridge LAST).
- **`pace`** — Tanaka max-HR, effort cap by fitness and cardiac risk
  factors, 2–3 min work / 2 min rest cycles, talk test, and the
  stop-now-call-emergency red-flag list (incl. atypical presentations).
- **`salt`** — pavement temperature (not air) + surface type → melter
  choice with exact g/m² rate, surface compatibility (new concrete,
  brick, pets), and pre/post-treat strategy.

## Quick start

```bash
python3 scripts/snow_plan.py plan --area 6x9 --depth 25 --snow wet --ends 07:00 --now 05:30
python3 scripts/snow_plan.py pace --age 55 --fitness moderate --risk-factors 1 --alone
python3 scripts/snow_plan.py salt --pavement-temp -6 --surface concrete-3yr --pets
```

Stdlib-only Python 3. Offline.

## Layout

- `SKILL.md` — triggers, physics tables, pitfalls
- `references/technique-and-safety.md` — cardiac physiology, biomechanics,
  layered method, clothing, red flags
- `references/ice-melt-chemistry.md` — melter table, surface rules, rates,
  pets/plants, strategy
- `scripts/snow_plan.py` — the planner

## License

MIT © Denis Voronin
