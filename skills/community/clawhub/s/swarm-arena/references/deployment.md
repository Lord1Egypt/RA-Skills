# Deployment — references/deployment.md

## Requirements

- Python **3.10+** (paper/approval modes: stdlib only)
- `lighter-sdk` for `live` / `autonomous_live` (`pip install -r requirements.txt`)
- cron, systemd --user, or launchd for scheduling
- outbound HTTPS to the Lighter API

## Install from scratch

```bash
cd skills/swarm-arena
bash install.sh                          # preflight
cp config.example.json config.json       # or run the wizard:
python3 scripts/onboarding.py            # verifies live creds when relevant
python3 scripts/register_crons.py        # prints crontab lines
crontab -e                               # paste them
mkdir -p logs
```

## Directory contract

```
skills/swarm-arena/
  config.json        ← yours (0600), never committed
  state.json         ← runtime state, created on first cycle
  trades.json        ← append-only journal, created on first decision
  register_crons.json← rendered cron manifest
  logs/              ← scan/review/daily/watchdog logs
  scripts/           ← 27 tools
  references/        ← these docs
```

`state.json` and `trades.json` default to beside `config.json`; override with
`--state` / `--trades` where a script accepts them.

## Credential handling

- Environment variables only: `LIGHTER_API_PRIVATE_KEY`,
  `LIGHTER_API_KEY_INDEX`, `LIGHTER_ACCOUNT_INDEX`, optional
  `LIGHTER_L1_ADDRESS`, optional `LIGHTER_BASE_URL`.
- Cron runs with a stripped environment — export credentials via
  `crontab` lines, a wrapper script, systemd `EnvironmentFile` (0600,
  root-owned), or a launchd wrapper.
- Nothing secret ever lands in `config.json`, state, journals, or logs;
  output masks to the last 4 characters.

## File permissions

```
chmod 600 config.json
chmod 700 scripts/*.py   # optional; they run via python3 either way
```

## Mode progression (recommended)

1. **paper** — days to weeks. Watch `status.py`, `review_trades.py`, and the
   journal. Confirm the pipeline behaves on your markets.
2. **approval** — proposals without execution. Practice the approval flow.
3. **live** with `require_human_approval_for_live_orders: true` — real but
   supervised.
4. **live** ungated, then **autonomous_live** — only when the first three
   earned your trust. autonomous_live requires typing `ACCEPT` in onboarding.

Each downgrade is one edit away; each upgrade should be earned.

## Upgrades

```
python3 scripts/halt.py config.json --reason "upgrade"
# replace skill files; KEEP config.json, state.json, trades.json, logs/
bash install.sh
python3 scripts/resume.py config.json
```

## Uninstall

```
python3 scripts/halt.py config.json --cancel-orders   # live modes
crontab -e                                            # remove the 4 jobs
# delete skills/swarm-arena/ (config/state/trades/logs are inside)
```

## Hardening checklist

- [ ] `config.json` is 0600 and outside any public web root
- [ ] credentials only in env / 0600 `EnvironmentFile`
- [ ] `max_daily_loss`, `max_total_exposure`, `max_notional_per_trade` set to
      values you can actually afford
- [ ] halt-check cron alerts reach you (verify with `halt.py`, then `resume.py`)
- [ ] logs rotate (logrotate / newsyslog config installed)
- [ ] backups exclude credentials; include `trades.json` if you care about the
      learning history
