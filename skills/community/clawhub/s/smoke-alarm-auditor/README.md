# Smoke Alarm Auditor

**It's 3AM and something on the ceiling is beeping. What is it saying?**

Smoke alarms chirp in a language almost nobody has memorized — one
chirp/minute is a battery, three fast beeps repeating means SMOKE, four
beeps (or a voice) means CARBON MONOXIDE, and a chirp that survives a
fresh battery means the unit itself expired. Meanwhile two-thirds of
homes have at least one alarm past its 10-year sensor life, and the
classic killer pattern is a kitchen false-alarm unit that got its battery
ripped out months ago.

This skill is the decoder and the auditor:

- **Chirp decoder** — pattern → meaning → immediate action, with the
  First Alert/Kidde variance notes
- **House audit** — feed it your units (kind + install date), get ages
  against the 10-year smoke / 7-year CO limits, an ordered replacement
  plan, oldest-risk first
- **Coverage planner** — bedroom/floor count → NFPA-72-style unit list
  (every bedroom, outside sleeping areas, per floor, interconnected)
- **Placement anti-patterns** — kitchen 10-ft rule, dead-air corners,
  garage = heat detector only, the CO-height myth
- **CO event script** — what to do the minute a CO alarm sounds

## Quick start

```bash
python3 scripts/alarms.py chirp --pattern "1 beep every minute"
python3 scripts/alarms.py audit --units unit.json
python3 scripts/alarms.py coverage --bedrooms 3 --floors 2 --basement
python3 scripts/alarms.py placement --room kitchen
python3 scripts/alarms.py co
```

`unit.json`: `[{"id":"hall-1","kind":"smoke","installed":"2015-04"}]`
(kind: smoke/co/combo; add "battery" if you like.)

Stdlib-only Python 3, offline.

## Example

Audit of a real-looking house, 2026-10-04:

```
basement     co     installed 2017-11  age 8.9y / limit 7y  EXPIRED <<< REPLACE
hall-1       smoke  installed 2015-04  age 11.5y / limit 10y EXPIRED <<< REPLACE
master-br    combo  installed 2019-08  age 7.2y / limit 7y  EXPIRED <<< REPLACE
kids-br      smoke  installed 2021-03  age 5.6y / limit 10y  4y left
```

Three of four units dead-on-arrival — the normal state of most homes.
Full beep tables, placement geometry, and the maintenance calendar in
`references/alarm-reference.md`.

*Encodes widely-published NFPA consumer guidance; codes vary by
jurisdiction. A sounding smoke/CO pattern means act first, decode after.*
