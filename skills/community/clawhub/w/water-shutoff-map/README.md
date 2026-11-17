# Water Shutoff Map

**Know where every water shutoff in your home is — before the pipe bursts. A guided hunt, a durable registry, a printable fridge card, and a 60-second quarterly drill.**

When a supply line lets go, water flows at 2–5 gallons *per minute*. The average burst-pipe insurance claim runs over $10,000, and the single biggest controllable factor is how fast someone in the house finds and closes the right valve. Most people have never turned their main shutoff and couldn't say where it is. Panic is a terrible time to learn your home's plumbing geography.

## The real-world problem

- **Nobody knows where their main shutoff is.** It's in the basement / crawlspace / garage box / behind an access panel — depends on the house — and the knowledge lives with one adult, maybe.
- **Valves that are never exercised seize open.** The classic gate valve that sat open for a decade won't close when you need it. Testing takes 2 minutes; finding out takes a flood.
- **Emergencies happen to whoever is home** — partner, teen, babysitter, guest. Memory doesn't scale; a printed card on the fridge does.
- **People confuse house main / irrigation main / water heater inlet**, and close the wrong one while the leak keeps flowing.

## What it does

```bash
# 1. Hunt: where shutoffs hide for your home type
python3 scripts/shutoff_registry.py hunt --home slab

# 2. Record what you find
python3 scripts/shutoff_registry.py add --id main --label "Main shutoff" \
  --location "Garage, pipe from slab behind water heater" --type gate \
  --direction clockwise --tool "12in crescent wrench" --tested 2026-08-30

# 3. Validate completeness + staleness (exit 1 if something must be fixed)
python3 scripts/shutoff_registry.py validate

# 4. Print the fridge card — 3-step first response + your valve table
python3 scripts/shutoff_registry.py card > shutoff-card.txt

# 5. Quarterly 60-second drill (exercise valves so they don't seize)
python3 scripts/shutoff_registry.py drill
```

The registry is plain JSON (`~/.shutoff-registry.json`), exportable for backup. `validate` flags missing core entries (main, water heater, meter), untested or stale valves (>1 year), gate valves with no tool logged, and entries marked seized. `references/locating-shutoffs.md` is a full hunting guide: where mains hide by home type (basement/slab/crawlspace/condo), every fixture and appliance stop, valve identification, the safe 2-minute test procedure, freezing-weather prep, and insurance-claim notes.

## Who needs this

- **Anyone who just moved** — the first weekend, before the boxes
- **Homeowners in freezing climates** (burst-pipe season) and anyone leaving town in winter
- **Renters** — your unit's valve is yours to know; the building riser is not
- **Landlords** — hand tenants a printed card; it's cheaper than any flood
- **Anyone doing DIY plumbing** — isolate at the fixture stop before you touch a supply line

## Install

Python 3.8+ standard library only.

```bash
python3 scripts/test_shutoff_registry.py   # verify the build
```

## License

MIT © Denis Voronin
