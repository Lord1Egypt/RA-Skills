# Tire Chain Law Navigator

**"Do I need chains?" — answered before the checkpoint answers it for you.**
Winter mountain driving has a legal layer — chain law — that drivers from
out of region discover only at a checkpoint, a fine, or in a ditch. This
tool gives route+date+vehicle verdicts across US/Canada/EU-Alps
jurisdictions: what requirement level applies, whether YOUR vehicle passes,
what to install, and what it costs if you're wrong.

## The real-world problem

California posts R1/R2/R3, Colorado runs a Traction Law that can activate
*before it snows*, Washington requires chains when signed, BC mandates
winter tires Oct–Apr, and Alpine sign 267 is legally binding. Every winter,
drivers are fined, turned around, or crash because "I have AWD" — which is
true at R1 and false at R3. Nothing on your phone explains which is which
for tomorrow's route in your specific car.

## What it does

- **Verdict engine** — corridor + date + vehicle class + conditions →
  requirement level, pass/no-pass for your setup, install requirement,
  fine exposure, live info line
- **6 curated corridors**: I-70 CO, I-80 Donner, I-90 Snoqualmie,
  BC-5 Coquihalla, Alps FR/IT, Grand Canyon AZ
- **Carry vs install** distinction, AWD exemption truth-table
  (yes at R1/Traction Law, no at R3/PV Chain Law)
- **Equipment legality primer** — link chains vs cables vs AutoSock vs
  studded by jurisdiction; tight-clearance guidance
- **Dash-card** — printable glovebox one-pager with ladder, fines, phone
  numbers, and universal chain rules (25–30 mph, signed chain-up zones)

## Quick start

```bash
python3 scripts/chainlaw.py routes
python3 scripts/chainlaw.py check --route i70-co --date 2027-01-15 \
    --vehicle awd-snows --conditions active
python3 scripts/chainlaw.py dashcard --routes i70-co,donner-i80 \
    --vehicle awd-snows --out card.md
```

Stdlib-only Python 3. Curated knowledge — always confirm with the live
info line on travel day (the tool prints it).

## License

MIT © 2026 Denis Voronin
