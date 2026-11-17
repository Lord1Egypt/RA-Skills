# Schengen Clock

**The rolling 90/180 rule, computed exactly — so a counting error never becomes an entry ban.**

## The problem

Non-EU travelers to Europe may spend at most **90 days inside any rolling
180-day window**. The rule sounds simple; applying it is not:

- The window slides **every day** — a long trip from 7 months ago still
  constrains today.
- Entry day **and** exit day both count as presence.
- A weekend outside doesn't "reset" anything.
- Most people discover their arithmetic was wrong **at the boarding gate** or
  at passport control — where the penalty is a refused entry, a fine, or a
  multi-year entry ban.

EES (the EU's biometric Entry/Exit System) now computes this automatically at
every border. The era of sloppy counting is over.

## What it does

| Command | Answer it gives |
|---|---|
| `status` | Days used / remaining in the window ending today (or `--on DATE`) |
| `maxstay --entry D` | Enter date D → **exact** longest legal stay + must-exit-by date |
| `plan --entry D --exit D` | Is this trip legal? Verdict + tightest window + fixes |
| `traps` | Back-to-back stays, thin margins, recorded overstays, nomad-pattern flags |
| `letter` | Border-interview one-pager with the rolling-window math |
| `stay add/rm/list` | Registry of entries/exits parsed from passport stamps |

## Quick start

```bash
python3 scripts/schengen.py stay add --entry 2026-05-10 --exit 2026-06-02 --country IT
python3 scripts/schengen.py stay add --entry 2026-07-01 --exit 2026-08-30 --country ES
python3 scripts/schengen.py status                 # used / remaining today
python3 scripts/schengen.py maxstay --entry 2026-10-12
python3 scripts/schengen.py plan --entry 2026-11-01 --exit 2026-12-12
```

100% offline — travel history stays in one local `schengen.json`.

## Who needs this

~60 visa-exempt nationalities, digital nomads, snowbirds, multi-trip
business travelers, and anyone who has ever done 90/180 math on a napkin at
an airport gate.

## Honest limits

Arithmetic, not legal advice. D-visas, residence permits, and working-holiday
schemes follow different rules this tool does not model. When math and border
authorities disagree, the authorities win.

MIT License. © 2026 Denis Voronin
