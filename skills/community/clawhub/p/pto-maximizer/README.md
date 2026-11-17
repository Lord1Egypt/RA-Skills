# PTO Maximizer

**15 vacation days shouldn't buy 15 days off. They should buy 45.**

Most workers spend PTO reactively — a random Friday here, a sick-ish day
there — then discover in November they're sitting on unused days heading
into a use-it-or-lose-it deadline. The fix is arithmetic: holidays fall on
known weekdays, weekends stitch to them, and a single well-placed PTO day
buys a 4-day weekend.

```
US 2026, 15-day budget, plan output:
  Jan 02  [1 PTO] → Jan 1–4   4 days off  (New Year)
  Jan 20  [1 PTO] → Jan 17–20 4 days off  (MLK)
  ...10 bridges...
  TOTAL: 12 PTO days → 45 consecutive days off (avg efficiency 3.8)
  Unallocated: 3 days for spontaneity
```

## What it does

- Computes public holidays for **US / UK / DE / FR** for any year — fixed
  dates, weekday rules (Thanksgiving, bank holidays), Easter-dependent
  feasts, and **observance shifts** (Sat→Fri, Sun→Mon, UK substitution)
- Generates every bridge candidate (1–4 PTO days before/after each holiday),
  deduplicates, and scores by **efficiency = days off ÷ PTO spent**
- Greedy annual plan with **quarter balancing** (no quarter > 45% of budget)
  and `--reserve-summer` to hold days for one real week off
- Blackout warnings (US retail Q4 freeze, UK school-summer pricing, DE
  Betriebsferien, FR August shutdown)
- **ICS export** — import the plan straight into Google/Outlook/Apple

## Quick start

```bash
python3 scripts/pto_planner.py --country US --year 2026 --budget 15
python3 scripts/pto_planner.py --country UK --year 2026 --budget 25 --ics pto.ics
python3 scripts/pto_planner.py --country US --year 2026 --budget 10 --reserve-summer 5 --min-eff 3.0
```

## Who needs this

- Anyone with paid time off and a calendar. US workers alone forfeit
  hundreds of millions of PTO days annually; the average worker takes fewer
  days than in the 1990s
- New hires mapping a first year of PTO
- "I have N days left and it's October" rescue planning
- Managers encouraging teams to actually disconnect (bridge days are the
  cheapest staffing days to lose)

## What's inside

- `SKILL.md` — bridge math table, efficiency doctrine, pitfalls
- `references/pto-strategy.md` — holiday shift rules per country, forfeiture
  stats, manager-negotiation playbook
- `scripts/pto_planner.py` — stdlib-only CLI, JSON mode, ICS export

Stdlib Python only. No network, no accounts.

## License

MIT © Denis Voronin
