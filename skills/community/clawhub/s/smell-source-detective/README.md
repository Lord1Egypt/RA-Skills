# Smell Source Detective

**Find the source of that mystery smell — ranked by evidence, not by
blog-list length.**

Every house eventually produces a smell nobody can locate. Generic
advice is a list of 30 possible causes. This tool is a triage engine:
you give it the smell family, the room, and the timing trigger, and it
ranks probable sources, separates the four DANGER smells (gas,
electrical "fish", sewage backup, dead animal) that need immediate
action, and walks you through a no-tools localization protocol —
cheapest, most discriminating test first.

## What it does

- **diagnose** — 12 smell families, 17 sources with base rates,
  location affinity and timing triggers; every hypothesis comes with
  a confirming CHECK and a FIX. Nothing is "diagnosed" until its
  check passes.
- **danger** — act-now protocols: gas (no switches, leave, call from
  outside), electrical fish smell (precursor to fires), sewage
  backup (water appearing = stop running water), dead animal urgency
  rules.
- **localize** — sniff-mapping gradients, dry-trap pour test,
  fixture elimination, appliance isolation, wall-void sniffing via
  electrical boxes.
- **kill** — source-specific protocols: dry P-traps (mineral oil
  cap), enzymatic-vs-bleach rules, mold decision line (DIY ≤ 1 m² vs
  professional), dead-rodent desiccation clock.
- **log** — episode journal; after 5 entries it surfaces patterns
  ("all after vacation" = dry traps; "all after rain" = vent or
  moisture path). Doubles as landlord/habitability evidence.

## Quick start

```bash
python3 scripts/smell_detective.py diagnose --smell sewage --location basement --timing mornings
python3 scripts/smell_detective.py danger --smell gas
python3 scripts/smell_detective.py kill --source "dead animal in wall"
```

Stdlib-only Python 3, offline, no dependencies. Not a substitute for
gas/fire emergency response.

## License

MIT
