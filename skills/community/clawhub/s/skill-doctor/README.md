# 🩺 Skill Doctor

A check-up for your ClawHub portfolio.

Skill Doctor pulls live data for every skill and plugin you've published on
ClawHub, runs it through a rule-based diagnostic engine, and hands you a
prioritized prescription — what's healthy, what's at risk, and what to do
about it this week.

Optional AI-narrated analysis available via the Anthropic API.

## Quick Start

```bash
clawhub install skill-doctor
```

First run — tell it what to track:

```bash
python3 scripts/checkup.py --all
# Edit ~/.skill-doctor/config.json to add your slugs/plugins
```

Then:

```bash
python3 scripts/checkup.py --all          # full portfolio check-up
python3 scripts/checkup.py --slug my-skill # single skill
python3 scripts/checkup.py --all --deep   # + AI narrative (needs API key)
python3 scripts/checkup.py --all --chart  # + trend chart PNG
```

## What It Checks

- **Trust** — moderation verdict (clean / pending / suspicious / malware)
- **Conversion** — downloads → installs ratio
- **Momentum** — growth vs. last check-up
- **Risk** — active-install drops (possible breaking changes)
- **Staleness** — version age vs. ongoing download activity

See `SKILL.md` for full usage and `references/diagnostic-rules.md` for the
exact rules and thresholds.

## Requirements

- `clawhub` CLI installed and authenticated
- Python 3.10+
- Optional: `matplotlib` for `--chart` (`pip install matplotlib --break-system-packages`)
- Optional: Anthropic API key for `--deep`

## Support This Skill

If Skill Doctor saved you time, consider sending a few sats:

⚡ Lightning: `welove@blink.sv`

## License

MIT
