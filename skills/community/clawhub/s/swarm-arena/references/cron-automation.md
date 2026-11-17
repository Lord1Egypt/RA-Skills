# Cron Automation — references/cron-automation.md

swarmArena is cron-driven: short-lived processes on fixed schedules, state
in JSON files between runs. No daemon to babysit.

## The four jobs (`cron-templates.json`)

| Job | Schedule | What runs |
|---|---|---|
| `scan` | `*/2 * * * *` (paper: `*/5`) | `autonomous_runner.py config.json` — the full cycle |
| `review` | `*/30 * * * *` | `fetch_trade_outcomes.py` → `review_trades.py` → `update_metrics.py` |
| `daily-summary` | `0 0 * * *` | `status.py` + 24h review digest (meant for 00:00 UTC — set `TZ=UTC` in crontab or adjust) |
| `halt-check` | `*/15 * * * *` | `status.py --json` + alert evaluator (exit 1 on halt / CB / ≥3 errors / ≥80% daily loss) |

## Install

```bash
python3 scripts/register_crons.py            # writes register_crons.json, prints lines
python3 scripts/register_crons.py --mode paper
crontab -e                                   # paste the printed lines
mkdir -p logs                                # log targets live here
```

`register_crons.py` substitutes the real skill root for the
`/ABSOLUTE/PATH/TO/swarm-arena` placeholder everywhere.

## Alternatives to cron

**systemd** (Linux): `deploy.systemd.service` (oneshot cycle) +
`deploy.systemd.timer` (every 2 min). Credentials via a root-owned `0600`
`EnvironmentFile` — never inside the unit.

```
cp deploy.systemd.* ~/.config/systemd/user/   # then edit paths
systemctl --user daemon-reload
systemctl --user enable --now swarm-arena.timer
```

**launchd** (macOS): `deploy.launchd.plist` with `StartInterval` 120.

```
cp deploy.launchd.plist ~/Library/LaunchAgents/xyz.swarm-arena.plist  # edit paths
launchctl load ~/Library/LaunchAgents/xyz.swarm-arena.plist
```

## Logs

Cron commands append to `logs/scan.log`, `logs/review.log`, `logs/daily.log`,
`logs/watchdog.log`. Rotation configs ship for both worlds:
`logrotate.swarm-arena.conf` (Linux) and `newsyslog.swarm-arena.conf`
(macOS/BSD).

## Failure behavior under scheduling

- A crashing cycle increments `consecutive_errors`; 5 in a row trips the
  circuit breaker and subsequent cycles exit quietly (code 3) until a human
  resumes.
- Halted state exits quietly too — no log spam, one line per cycle.
- Cron overlap is safe in practice (cycles take seconds); if your host is
  slow, add `flock -n /tmp/swarm-arena.lock` in front of the scan command.

## Timezone note

Daily-loss reset and the daily summary key off **UTC**. Either run the host
crontab under `TZ=UTC` or accept local-time semantics consistently.
