---
name: tibber-energy
description: "Use Tibber API data to fetch hourly spot prices, plan cheapest appliance or EV charging windows, detect consumption anomalies, and trigger smart-home actions from price thresholds."
homepage: https://developer.tibber.com
metadata:
  openclaw:
    emoji: "⚡"
    primaryEnv: TIBBER_ACCESS_TOKEN
    requires:
      env:
        - TIBBER_ACCESS_TOKEN
      bins:
        - python3
---

# Tibber Energy

## When to use

Use when the user asks about:
- Current or upcoming electricity spot prices
- Cheapest time to run a load (dishwasher, laundry, EV charging)
- Suspicious consumption spikes
- Device actions based on price thresholds

## Setup

Set environment variables before running:

```bash
export TIBBER_ACCESS_TOKEN="your_tibber_token"
export TIBBER_HOME_ID="optional_home_id"
```

`TIBBER_HOME_ID` is optional if the account has one home.

You can also copy `.env.example` to `.env` and fill values locally:

```bash
cp .env.example .env
```

Alternatively, for shareable/persistent configuration, create:
`~/.config/tibber-energy/config.json`

You can copy the template from this repo:
```bash
cp config.json.example ~/.config/tibber-energy/config.json
```

The scripts will use credentials in this order:
1) environment variables (`TIBBER_*`)
2) `~/.config/tibber-energy/config.json`
3) interactive prompt (only if you pass `--prompt-missing-secrets`)

## Run

Use the wrapper from the skill directory:

```bash
bash run.sh prices
```

## Commands

### 1) Fetch current and upcoming hourly spot prices

```bash
bash run.sh prices --hours 36
```

### 2) Find optimal time for appliance or EV charging

Estimate hours from `kwh / power-kw`, then find cheapest contiguous block:

```bash
bash run.sh optimize \
  --kwh 28 \
  --power-kw 11 \
  --window-start "2026-04-27T18:00:00+02:00" \
  --window-end "2026-04-28T08:00:00+02:00"
```

For fixed duration instead of kWh:

```bash
bash run.sh optimize --duration-hours 2
```

### 3) Monitor consumption and flag anomalies

```bash
bash run.sh anomalies --lookback-hours 168 --sigma 2.5
```

### 4) Control smart-home devices by price threshold

Use shell commands for your automation endpoint, Home Assistant script, or smart plug CLI.

Dry-run:

```bash
bash run.sh control \
  --price-below 0.15 \
  --on-command "ha service call switch.turn_on --entity_id switch.ev_charger" \
  --off-command "ha service call switch.turn_off --entity_id switch.ev_charger"
```

Execute commands:

```bash
bash run.sh control \
  --price-above 0.35 \
  --on-command "ha service call switch.turn_on --entity_id switch.boiler" \
  --off-command "ha service call switch.turn_off --entity_id switch.boiler" \
  --execute
```

## Notes

- Prices are read from `currentSubscription.priceInfo` (`today` + `tomorrow`).
- Consumption anomaly detection compares latest hour against lookback mean/stdev.
- Start with dry-run control mode and verify commands before `--execute`.

## Safety

- Never commit or publish `.env` with real access tokens.
- Keep `--execute` off until threshold logic is verified in dry-run.
- Treat `--on-command` and `--off-command` as trusted input only (they run as shell commands).
- By default the scripts are non-interactive; pass `--prompt-missing-secrets` only when you want to enter credentials interactively.

## Publisher Checklist (ClawHub)

- Include: `SKILL.md`, `run.sh`, `tibber_energy.py`, `.env.example`, `config.json.example`, `.gitignore`
- Exclude: `.env`, `__pycache__/`, local logs, temporary files
- Validate from a clean shell:
  - `cp .env.example .env` and fill valid credentials
  - `bash run.sh prices --hours 6`
  - `bash run.sh optimize --duration-hours 2`
  - `bash run.sh anomalies --lookback-hours 168 --sigma 2.5`
  - `bash run.sh control --price-below 0.15 --on-command "echo on" --off-command "echo off"`
