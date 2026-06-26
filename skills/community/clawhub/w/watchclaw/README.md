# 🦞 Watchclaw 👼

<p align="center">
  <img src="assets/logo.jpg" alt="Watchclaw Logo" width="140">
</p>

**A watchdog CLI for your [OpenClaw](https://github.com/openclaw/openclaw) gateway. No more lobster suicide.**

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Shell-Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white" alt="Bash">
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Linux-lightgrey?style=for-the-badge" alt="macOS | Linux">
</p>

---

The idea came from those countless moments where you ask your OpenClaw agent to upgrade but it ends up killing itself, perhaps due to a bad config change, who knows? Suddenly, the gateway crashes, your channels become slient — WhatsApp, Telegram, Discord, all of them. You have to drop your coffee, unlock your Mac Mini or SSH in somewhere and scratch your head to fix it.

Enough!

**Watchclaw is the guarding angle for your lobster.** It monitors gateway health, auto-recovers from bad configs using the last "known-good" commit in the git history, and alerts you when things go sideways.

## ✨ Features

- **Auto-recovery** — Detects gateway crashes and restarts automatically
- **Config rollback** — Uses git to revert bad config commits to the last known-good state
- **Smart diagnosis** — Distinguishes config errors from transient crashes
- **Docker support** — Monitor containerized gateways with `docker restart` recovery
- **Pluggable alerts** — iMessage, webhooks (Slack/Discord/etc.), or any shell command
- **Probation system** — New configs must prove stable before earning "known-good" status
- **Agent-friendly** — `watchclaw status` outputs structured info your claw can read
- **Zero dependencies** — Pure bash. Just `curl`, `git`, and your OpenClaw install

## 📦 Quick Start

```bash
# Clone
git clone https://github.com/jarvis4wang/watchclaw.git
cd watchclaw

# Create your config
cp watchclaw.conf.example watchclaw.conf
vim watchclaw.conf   # Set GATEWAY_PORT, GATEWAY_CONFIG_DIR, alerts, etc.

# Make sure your OpenClaw config dir is a git repo
# (Watchclaw needs git history to revert bad changes)
cd ~/.openclaw
git init && git add -A && git commit -m "initial config"
cd -

# Start watching (gateway must be running)
./watchclaw start
```

> **First run:** Watchclaw enters a probation period to validate the current config before tagging it as `known-good`. Once promoted, that's your safe rollback point.

## 🔧 Prerequisites

| Requirement | Notes |
|-------------|-------|
| `bash` 4+ | Default on macOS and Linux |
| `curl` | For health checks |
| `git` | Config dir must be a git repo with ≥1 commit |
| `openclaw` | On PATH, or set `OPENCLAW_BIN` in config |
| `docker` | Only needed for Docker restart mode |

## 🖥️ CLI

```
watchclaw start [--config PATH] [--foreground]   Start the daemon
watchclaw stop  [--config PATH]                  Stop the daemon
watchclaw restart [--config PATH]                Stop + start
watchclaw status [--config PATH]                 Show watchclaw & gateway status
watchclaw logs [--config PATH] [-f] [--tail N]   View watchdog logs
watchclaw config [--config PATH]                 Print resolved configuration
watchclaw version                                Print version
watchclaw help                                   Show help
```

### Options

| Flag | Description |
|------|-------------|
| `--config PATH` | Path to config file |
| `--foreground` | Run in foreground (start only) |
| `-f`, `--follow` | Follow log output in real-time (logs only) |
| `--tail N` | Number of log lines to show (default: 50) |

### Config Search Order

1. `--config PATH`
2. `$WATCHCLAW_CONF` environment variable
3. `./watchclaw.conf` (next to the binary)
4. `~/.config/watchclaw/watchclaw.conf`

### Status Output

```
$ ./watchclaw status
Watchclaw: vX.X.X

── Watchclaw ──────────────────────────
  State:          HEALTHY
  Uptime:         2:14:30
  PID:            12345
  Config:         ./watchclaw.conf
  Alert hook:     webhook
  Dry-run:        False
  Retries:        0/3

── Gateway ────────────────────────────
  Health:         200 OK
  Port:           18790
  Known-good commit: a1b2c3d
  Gateway conf dir:  /home/user/.openclaw
```

Your claw can run `watchclaw status` via exec to check gateway health and report issues proactively.

## 🧠 How It Works

### State Machine

```
                    ┌─────────┐
          start ──▶ │ HEALTHY │ ◀── probation passed
                    └────┬────┘
                    │    │ health check fails
     config changed │    ▼
       (H3: HEAD ≠  │ ┌──────────────┐
        known-good) │ │  RESTARTING  │ ── simple restart succeeds ──▶ PROBATION
                    │ └──────┬───────┘
                    ▼        │ restart fails (or config error in log)
              ┌───────────┐  ▼
              │ PROBATION │ ┌──────────────┐
              └───────────┘ │  DIAGNOSING  │
                            └──┬───┬───┬──┘
                               │   │   │
                      U1 ──────┘   │   └────── U3
                   git stash       │        retry loop
                               U2 ─┘
                            git revert
                                   │
                                   ▼
                            ┌──────────────┐     recovers     ┌───────────┐
                            │  RETRY LOOP  │ ───────────────▶  │ PROBATION │
                            └──────┬───────┘                   └─────┬─────┘
                                   │ exhausted                       │ stable for
                                   ▼                                 │ PROBATION_DURATION_SEC
                              ┌─────────┐                            ▼
                              │  ALERT  │ ◀─── H1: dies      promote known-good
                              └─────────┘      during              │
                                   │           probation           │
                                   │                               ▼
                                   └───── gateway comes back ──▶ HEALTHY
```

### Recovery Cases

| Case | Trigger | What Watchclaw Does |
|------|---------|---------------------|
| **Simple** | Gateway down, config OK | Restart → probation → healthy |
| **U1** | Dirty (uncommitted) config changes | `git stash` → restart → probation |
| **U2** | Committed bad config | Tag as `broken-<hash>` → `git revert` to known-good → restart |
| **U3** | Config is at known-good but still fails | Retry loop → alert (not a config problem) |
| **H1** | Gateway dies during probation | Re-enter retry loop |
| **H3** | Config changed while healthy | Enter probation → promote new known-good if stable |

### Known-Good Anchoring

Before monitoring, Watchclaw validates that a safe rollback point exists:

| Condition | Action |
|-----------|--------|
| `known-good` tag exists | ✅ Start monitoring |
| No tag + healthy + clean tree | Enter probation → promote on success |
| No tag + dirty tree | ❌ Exit — clean your tree first |
| No tag + gateway down | ❌ Exit — start the gateway first |

## 🔔 Alert Hooks

Watchclaw alerts are pluggable. Set `ALERT_HOOK` in your config:

### `none` (default)
Log-only. No external notifications.

### `imsg` — iMessage (macOS)
Requires [`imsg`](https://github.com/steipete/imsg) CLI.
```bash
ALERT_HOOK="imsg"
ALERT_IMSG_TO="you@icloud.com"   # or phone number
```

### `webhook` — Slack, Discord, Telegram, etc.
Posts `{"text": "..."}` to any URL.
```bash
ALERT_HOOK="webhook"
ALERT_WEBHOOK_URL="https://hooks.slack.com/services/T.../B.../xxx"
```

### `command` — Anything
Runs a shell command with the alert message as `$1`.
```bash
ALERT_HOOK="command"
ALERT_COMMAND="ntfy pub my-alerts"
# or: ALERT_COMMAND="telegram-send"
# or: ALERT_COMMAND="/path/to/my-custom-alert.sh"
```

### Dry Run
Test your setup without sending real alerts:
```bash
DRY_RUN=1
```
Alerts are logged as `[DRY-RUN]` instead of being sent.

## ⚙️ Configuration

```bash
# ── Gateway ──────────────────────────────────────────────────────────
GATEWAY_PORT=18790              # Port to monitor
GATEWAY_CONFIG_DIR="$HOME/.openclaw"    # Must be a git repo
GATEWAY_LOG="/tmp/openclaw-gateway.log"
# OPENCLAW_BIN="/usr/local/bin/openclaw"  # Auto-detected if on PATH
# OPENCLAW_ARGS=""              # Extra args (e.g. --profile myprofile)

# ── Health Check ─────────────────────────────────────────────────────
POLL_INTERVAL_SEC=10            # Seconds between health polls
HEALTH_TIMEOUT_SEC=5            # curl timeout for health check

# ── Timing ───────────────────────────────────────────────────────────
GRACE_PERIOD_SEC=20             # Wait after restart before checking health
PROBATION_DURATION_SEC=60      # Seconds stable before promoting known-good

# ── Retry + Backoff ──────────────────────────────────────────────────
MAX_RETRIES=3                   # Restart attempts before entering ALERT
BACKOFF_INITIAL_SEC=300         # 5 min — first alert repeat interval
BACKOFF_MAX_SEC=3600            # 1 hour — alert interval cap

# ── Restart Mode ─────────────────────────────────────────────────────
RESTART_MODE="native"           # native | docker
# DOCKER_CONTAINER=""           # Container name (required for docker mode)

# ── Alerts ───────────────────────────────────────────────────────────
ALERT_HOOK="none"               # imsg | webhook | command | none
# ALERT_IMSG_TO=""              # iMessage recipient
# ALERT_WEBHOOK_URL=""          # Webhook POST URL
# ALERT_COMMAND=""              # Custom command ($1 = message)

# ── Logging ──────────────────────────────────────────────────────────
LOG_FILE="./logs/watchclaw.log" # Absolute or relative to working dir
LOG_MAX_BYTES=1048576           # 1MB — auto-rotate (keeps .1 backup)

# ── Dry Run ──────────────────────────────────────────────────────────
DRY_RUN=0                       # 1 = log alerts but don't send them
```

## 🧪 Testing

Tests run against a separate "sheep" gateway on port 18851 with its own isolated config dir (`~/.openclaw-sheep`). Your real gateway is never touched.

```bash
# Setup
cp tests/test.conf.example tests/test.conf
# Edit if needed (defaults work for most setups)

# Run all 8 tests
bash tests/run-all.sh

# Run a single test
bash tests/test-04-u2-committed-bad-config.sh
```

| # | Test | What It Covers |
|---|------|----------------|
| 01 | Bootstrap | Known-good anchoring (4 scenarios: happy path, dirty tree, unhealthy, existing tag) |
| 02 | Transient crash | Kill gateway → watchclaw restarts → probation → healthy |
| 03 | U1: dirty config | Uncommitted bad config → `git stash` → recover |
| 04 | U2: committed bad config | Committed bad config → tag broken → `git revert` → recover |
| 05 | U3: known-good fails | Non-config failure → retry loop → alert |
| 06 | H1: probation death | Gateway dies during probation → retry |
| 07 | H3: config update | Valid config change while healthy → probation → new known-good promoted |
| 08 | Alert recovery | ALERT state → gateway comes back → auto-recover to HEALTHY |

## 🐳 Docker Mode

Watchclaw can monitor a gateway running inside a Docker container. Instead of calling `openclaw gateway start`, it uses `docker restart` for recovery.

```bash
# watchclaw-docker.conf
GATEWAY_PORT=18795
GATEWAY_CONFIG_DIR="$HOME/workspace/my-openclaw-docker"  # bind-mounted config (git repo)
RESTART_MODE="docker"
DOCKER_CONTAINER="my-openclaw-container"
```

**Requirements:**
- The container must expose the gateway port to the host (e.g., `127.0.0.1:18795:18795`)
- Set `gateway.bind` to `"lan"` in your OpenClaw config so the gateway listens on `0.0.0.0` inside the container (default `loopback` blocks port forwarding)
- `GATEWAY_CONFIG_DIR` should point to the bind-mounted config directory (must be a git repo)

**How it works:** Health checks hit `http://127.0.0.1:$GATEWAY_PORT/` from the host. On failure, git revert/stash logic runs on `GATEWAY_CONFIG_DIR` as usual, then `docker restart $DOCKER_CONTAINER` replaces the normal process restart.

## 🏗️ Design Decisions

**`git revert` not `git reset` (U2):** Creates forward commits that undo bad changes, preserving full history. Broken commits are tagged `broken-<hash>` for forensics.

**`git stash` (U1):** Non-destructive. Uncommitted changes are recoverable via `git stash pop`.

**Probation before promoting:** A single healthy response isn't proof of stability. Configs must survive `PROBATION_DURATION_SEC` seconds before earning `known-good` status.

**No file watchers:** Pure polling via health checks. Simple, portable, no inotify/kqueue dependencies.

**Alert hooks in config, not plugin scripts:** No hook directories to manage. One config variable picks your alerting method. Easy to extend — add a `case` branch.

## 📁 Project Structure

```
watchclaw/
├── watchclaw              # CLI entrypoint (start/stop/restart/status/logs/config)
├── watchclaw.sh           # Core FSM engine
├── watchclaw.conf.example # Config template
├── assets/
│   └── logo.jpg           # Project logo
├── tests/
│   ├── helpers.sh         # Shared test utilities
│   ├── run-all.sh         # Sequential test runner
│   ├── test.conf.example  # Test config (fast timers, alerts muted)
│   └── test-01..08.sh     # 8 test cases covering all FSM paths
├── logs/                  # Runtime logs (gitignored)
├── LICENSE                # MIT
└── README.md
```

## 🤝 Contributing

Issues and PRs welcome. If you build a new alert hook, please include a test case.

## 📜 License

[MIT](LICENSE) — Bruski & Jarvis Wang, 2026
