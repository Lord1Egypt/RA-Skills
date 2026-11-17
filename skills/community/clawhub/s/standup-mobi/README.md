# Standup Mobi

**Someone's out — the team shouldn't find out what they did by failing.**
Turns absence coverage into a 20-minute exercise: duty inventory, a
coverage solver that respects capacity and a 1.5× fairness cap (no silent
hero-overload), a 12-question tribal-knowledge extraction kit, a graded
watch→shadow→assist→solo ramp plan, and a printable substitute checklist.

## The real-world problem

A teammate goes on vacation, gets sick, or resigns — and the team
discovers duty-by-duty, under fire, what only that person knew. Coverage
is improvised in Slack at 23:00. Three structural causes: duties are
invisible (standups mention outcomes, not recurring work), coverage is
assigned to "the reliable one" until they burn out, and tribal knowledge
has no extraction protocol.

## What it does

- **Duty inventory** from observable traces (calendar, standup notes,
  cron/report systems) — cadence, skill, minutes, risk, tribal flag
- **Coverage solver** — risk×minutes-first greedy assignment to the most
  available skilled person, hard 1.5× fairness cap, explicit UNCOVERED
  holes instead of invisible overload
- **12-question extraction kit** for tribal duties + one-page runbook
  seeds; you interview, you write — never assign the absentee homework
- **Graded ramp** — watch→shadow→assist→solo→audit with stop-and-ask
  triggers per level
- **Printable checklist** grouped by cadence — tape it next to the
  monitor; paper survives laptop swaps

Works best with the absentee's cooperation, works without it (duties
rebuilt from traces, everything defaults tribal).

## Quick start

```bash
python3 scripts/mobi.py init --dir cover_alex
# edit team.json (available people + spare capacity) and duties.json
python3 scripts/mobi.py solve --dir cover_alex
python3 scripts/mobi.py extract --dir cover_alex
python3 scripts/mobi.py ramp --dir cover_alex --owner jordan --absentee Alex
python3 scripts/mobi.py checklist --dir cover_alex --owner jordan --out jordan.md
```

Stdlib-only Python 3.

## License

MIT © 2026 Denis Voronin
