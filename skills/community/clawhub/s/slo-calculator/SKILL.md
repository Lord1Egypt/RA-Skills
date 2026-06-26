---
name: slo-calculator
description: Calculate SLO/SLA error budgets, allowed downtime, burn rates, and uptime metrics. Use when asked about SLO targets, error budgets, uptime calculations, nines of availability, burn rate analysis, or SLA compliance. Triggers on "SLO", "SLA", "error budget", "uptime", "nines", "availability", "downtime budget", "burn rate".
---

# SLO/Error Budget Calculator

Calculate uptime targets, allowed downtime, error budgets, and burn rates for SLO/SLA management.

## Error Budget

```bash
# All periods
python3 scripts/slo.py budget 99.9

# Specific periods
python3 scripts/slo.py budget 99.9 month week day

# Named aliases
python3 scripts/slo.py budget three-nines
```

## Burn Rate

```bash
# Consumed 15m downtime in first 15 days of month
python3 scripts/slo.py burn 99.9 15m --period month --elapsed 15d

# Simple: consumed 2h this month
python3 scripts/slo.py burn 99.9 2h
```

## Compare Targets

```bash
python3 scripts/slo.py compare 99 99.9 99.99 99.999 --period month
```

## Observed Uptime

```bash
# From downtime
python3 scripts/slo.py uptime --downtime 45m --period month

# From uptime
python3 scripts/slo.py uptime --uptime-seconds 2589300 --period month
```

## Multi-Window Analysis

```bash
python3 scripts/slo.py multi-window 99.9 month:15m week:3m day:30s
```

## Reference Table

```bash
python3 scripts/slo.py table
python3 scripts/slo.py table --period year
```

## Output Formats

All commands support `--format text|json|markdown`:

```bash
python3 scripts/slo.py budget 99.9 -f json
python3 scripts/slo.py table -f markdown
```

## Duration Syntax

Durations use: `30s`, `5m`, `2h`, `1d`, `2h30m`, `1d12h`. Raw seconds also accepted.

## SLO Aliases

- `99`, `99.9`, `99.95`, `99.99`, `99.999` — direct percentages
- `two-nines`, `three-nines`, `four-nines`, `five-nines` — named aliases
