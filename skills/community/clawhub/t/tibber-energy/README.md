# tibber-energy

Skill package for Tibber price and consumption automation.

It provides CLI commands to:
- Show upcoming hourly prices
- Find the cheapest contiguous charging/runtime window
- Detect consumption anomalies
- Trigger on/off commands from price thresholds

## Requirements

- Python 3
- Tibber personal access token (`TIBBER_ACCESS_TOKEN`)

## Quick Start

```bash
cp .env.example .env
# edit .env with your token
bash run.sh prices --hours 24
```

Alternative (recommended for shared installs): create a persisted config file:
`~/.config/tibber-energy/config.json`

```bash
cp config.json.example ~/.config/tibber-energy/config.json
```

By default the commands are non-interactive; if credentials are missing, you can run with:
`bash run.sh prices --prompt-missing-secrets --hours 24`

## Common Commands

```bash
# Upcoming prices
bash run.sh prices --hours 36

# Cheapest 2-hour window
bash run.sh optimize --duration-hours 2

# Cheapest window for energy target (kWh / kW => duration)
bash run.sh optimize --kwh 28 --power-kw 11

# Consumption anomaly detection
bash run.sh anomalies --lookback-hours 168 --sigma 2.5

# Dry-run control
bash run.sh control \
  --price-below 0.15 \
  --on-command "echo on" \
  --off-command "echo off"
```

## Safety

- `.env` is local-only and ignored by git.
- Keep control in dry-run first; only add `--execute` after validating thresholds.
- `--on-command`/`--off-command` run shell commands, so only use trusted command strings.

## Files

- `SKILL.md`: skill metadata and usage instructions
- `run.sh`: launcher that loads local env and executes Python script
- `tibber_energy.py`: API + optimization/anomaly/control logic
- `.env.example`: template for local secrets
- `config.json.example`: template for persisted credentials
