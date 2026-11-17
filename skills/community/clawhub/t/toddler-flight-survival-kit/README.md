# Toddler Flight Survival Kit

**The problem.** Flying with a toddler is the single most-dreaded parenting travel event — a 3–8 hour contained emergency. But the failure modes are known and mostly preventable: the meltdown at the wrong altitude phase, ear pain on descent, the boredom cliff at 90 minutes when the snack pipeline runs dry, the lap-vs-ticketed seat decision made wrong at booking, the restraint a gate agent rejects. Every airline parenting forum is the same 20 stories, which means this is a *plannable event, not a lottery*.

The insight most parents miss: **toddlers don't experience flight time, they experience transitions** — boarding, door close, taxi, takeoff, meal service, descent, landing, deplaning. A plan that stages entertainment and food across those transitions beats a bag of random toys every time.

**What this does.**

- **`plan`** — age band + duration band + departure time + home nap window → a named strategy (NAP-CONTAINED / AWAKE-ENTERTAINED / NIGHT-ALIGNED) with a timeline: boarding approach (board LAST, not with pre-boarding — patience burn), target sleep start, descent protocol with clock times (T-40 diaper, T-35 sucking starts, T-30 calm-object), and the meltdown ladder
- **`pack`** — quantities, not vibes: 3 distinct snacks per awake hour, 1 wrapped novelty per 30–45 min (half never-seen-before), wipes/diapers per hour, 2 clothing changes, offline-tested downloads ×2 content, ONE calm-object sealed for descent
- **`seats`** — window-pairing doctrine, bulkhead trade-offs (bassinet space vs no car seat / no storage), FAA restraint rules (approved car seat label, CARES harness 22–44 lb, boosters never), lap-eligible economics with the honest "buy the seat by 18 months for sanity" note

Plus the three hardest windows with protocols: boarding→takeoff+20 (containment shock), the 90-minute boredom cliff (staged novelty calendar), and descent→landing (ears + strapped + everyone done — sucking not gum, which is a choking risk under 4).

**Example.** 30-month-old, 5.5-hour transcon departing 13:10, naps 13:00–15:00: the plan detects 1.8 h of nap overlap → NAP-CONTAINED strategy, early lunch, no car nap on the way, sleep sack at wheels-up+20, landing 18:40 with descent starting 18:05 — the exact minute the sealed calm-object gets deployed. The 16-month-old on a 8:00 short-haul: AWAKE-ENTERTAINED, gate-area energy burn, staged snacks.

## Quick start

```bash
python3 scripts/flight_kid.py plan --age-months 30 --duration-h 5.5 --depart 13:10 --nap 13:00-15:00
python3 scripts/flight_kid.py pack --age-months 30 --duration-h 5.5 --awake-h 4
python3 scripts/flight_kid.py seats --age-months 16
```

## Files

- `SKILL.md` — the model (age/duration/timing bands), three-hardest-windows protocols, packing quantities, pitfalls
- `references/flight-day-playbook.md` — transition-by-transition scripts, ears physiology, germ layer, jet-lag-lite, special cases
- `scripts/flight_kid.py` — planner/packer/seat-strategist (stdlib only)

## License

MIT © 2026 Denis Voronin
