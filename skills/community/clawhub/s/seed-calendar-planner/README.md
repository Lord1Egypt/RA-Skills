# Seed Calendar Planner

**Know exactly when to start every seed in your vegetable garden — for your frost dates, your crops, and your family's size.**

Every seed packet says *"sow after all danger of frost has passed."* That's not a plan. This tool turns two dates — your last spring frost and first fall frost — into a complete dated calendar: when to start tomatoes indoors (7 weeks before last frost), when peas go in the ground (6 weeks *before* it), when to re-sow lettuce so salad doesn't all mature at once, and the July deadline for fall carrots.

## The real-world problem

- **Beginners lose whole crops to timing.** Peppers transplanted into cold soil stall for weeks. Seedlings started too early get leggy and root-bound. Tender cucurbits direct-sown into cool soil rot in the ground.
- **"Plant everything in May" is the default and it's wrong.** Hardened-off brassicas can go out a month before your frost date; tender crops need to wait two weeks after it. A 6-week spread, not one weekend.
- **Nobody plans the fall garden in July** — the single biggest missed opportunity in temperate vegetable gardening. Fall carrots, beets, and broccoli are sweeter than spring's.
- **Tray logistics bite in March.** If you don't know you need 2 flats of 72 cells for the tomatoes alone, you discover it the weekend you're sowing.

## What it does

```bash
# Whole-garden calendar for a family of 4
python3 scripts/seed_calendar.py garden \
  --crops "tomato,pepper,lettuce,carrot,pea,bush-bean,kale,zucchini,broccoli" \
  --last-frost 2026-05-15 --first-frost 2026-10-05 --people 4
```

Output: every dated event (SOW-INDOORS / POT-UP / HARDEN-OFF / TRANSPLANT / SOW-DIRECT / succession SOW #n / SOW-BY-FALL / HARVEST), a seed-tray table (cells needed at 72/50/32-cell flats with a 20% germination buffer), and row-footage per crop with aisle overhead.

Also included:

- `crops` — browse the 35-crop parameter library (maturity, spacing, succession interval, plants-per-person)
- `plan --crop tomato` — full single-crop timeline with culture notes
- `succession --crop lettuce` — re-sow schedule with frost stop-rule enforcement
- `frost --zone 6b` — rough zone→frost-date estimate (with a loud disclaimer to verify locally)
- `--moon` — traditional waxing/waning annotations, clearly labeled folklore

## How it works

Each crop carries: indoor-start weeks, transplant delay relative to last frost, days-to-harvest, hardiness class (→ sow window and fall buffer), succession interval, plants-per-person, and in-row spacing. All events are derived from those numbers and your two frost anchors. Full data sources and derivations: `references/seed-crop-library.md`.

## Who needs this

- **First-time vegetable gardeners** who don't know tomatoes are started indoors (or when)
- **Experienced gardeners in a new climate** — moving from zone 8 to zone 5 invalidates every date you knew
- **Anyone with a short season** — zone 3–5 gardens live and die by the calendar; a 2-week error means no ripe peppers
- **Families planning a serious kitchen garden** — the plants-per-person and row-feet tables size the garden before you buy seeds

## Install

No dependencies — Python 3.8+ standard library only.

```bash
python3 scripts/seed_calendar.py crops          # explore
python3 scripts/test_seed_calendar.py           # verify the build
```

## License

MIT © Denis Voronin
