# Toilet Triage Ranger

**The running toilet, diagnosed in minutes.** A stuck flapper passes
200+ gallons a day silently — 2-4× a household's entire normal water
use, flowing while you sleep. The repair is usually a $8 part and 10
minutes, but people freeze at the tank lid because nobody ever showed
them the three parts that fail.

This toolkit gives you:

- **Symptom-based diagnosis tree** — runs constantly / phantom
  refills / hissing / weak flush / water on floor → ranked causes →
  the confirm test for each (dye test, float-lift, mark-and-wait).
- **Water-waste math** — liters/day, money/day/month/year from the
  leak severity, with the 30-minute meter-verification protocol that
  turns estimates into facts.
- **DIY-vs-plumber decision** — including the rental path (document +
  written notice with numbers, the part that actually moves landlords).
- **Step repair protocols** — flapper (10 min), fill valve (30 min),
  wax ring/flange (90 min): tools, steps, the porcelain-crack warning,
  and the stuck-shutoff-valve rescue path.
- **Weak-flush explainer** — why flushes are about water SPEED not
  volume (siphon start), and the 4 causes ranked cheapest-first.

## The real-world problem
Toilets are the #1 indoor water use and leaking toilets are the #1
cause of water-bill shock; EPA estimates average household leaks waste
thousands of liters monthly. It's the most fixable emergency in the
house — if you know which of three parts is lying to you.

## Quick start
```bash
python3 scripts/toilet_triage.py diagnose --symptom phantom-refill
python3 scripts/toilet_triage.py waste --rate running --price 4.1 --currency EUR
python3 scripts/toilet_triage.py decide --symptom runs-constantly --renter
python3 scripts/toilet_triage.py fix --part flapper
```

Pure Python stdlib. Offline. All data local.

## License
MIT © Denis Voronin
